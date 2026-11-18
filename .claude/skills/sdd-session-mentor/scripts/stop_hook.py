#!/usr/bin/env python3
"""
Hook "Stop" do Claude Code para a skill sdd-session-mentor.

Roda sempre que o Claude termina uma resposta. Ele:
  1. lê o transcript da sessão (JSONL) informado pelo Claude Code;
  2. extrai a última interação real (prompt literal, arquivos alterados, comandos);
  3. grava esse contexto em .claude/sdd-mentor/ultima-interacao.json;
  4. lista os temas já registrados em .claude/sdd-mentor/temas/ (um registro por tema);
  5. devolve {"decision": "block", "reason": ...} para que o Claude, antes de encerrar,
     use a skill, escolha o tema (existente ou novo) e gere docs/sessoes-sdd/<tema>.pdf.

Proteções:
  - stop_hook_active=True  -> não bloqueia de novo (evita loop infinito);
  - arquivo .claude/sdd-mentor.off ou SDD_MENTOR_OFF=1 -> registro desligado;
  - o mesmo prompt nunca é registrado duas vezes (state.json);
  - qualquer erro inesperado -> sai sem bloquear (nunca trava sua sessão).

Somente biblioteca padrão do Python 3.8+.
"""
import hashlib
import json
import os
import re
import sys
from datetime import datetime

MARKER = "[sdd-session-mentor]"
DOCS_DIR = os.environ.get("SDD_MENTOR_DOCS_DIR", "docs/sessoes-sdd")          # PDFs (um por tema)
TEMAS_DIR = os.environ.get("SDD_MENTOR_TEMAS_DIR", ".claude/sdd-mentor/temas")  # fontes: registro.md + figuras
MIN_PROMPT_CHARS = int(os.environ.get("SDD_MENTOR_MIN_CHARS", "15"))
EDIT_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
TRIVIAL = {"ok", "obrigado", "obrigada", "valeu", "thanks", "sim", "nao", "não", "blz", "beleza"}


def allow_stop():
    """Deixa o Claude encerrar normalmente."""
    sys.exit(0)


def text_from_content(content):
    """Extrai texto de um campo 'content' (string ou lista de blocos)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def is_tool_result(content):
    return isinstance(content, list) and any(
        isinstance(b, dict) and b.get("type") == "tool_result" for b in content
    )


def parse_slash_command(text):
    """Converte o formato interno de slash command em algo legível."""
    name = re.search(r"<command-name>(.*?)</command-name>", text, re.S)
    if not name:
        return None, text
    args = re.search(r"<command-args>(.*?)</command-args>", text, re.S)
    cmd = name.group(1).strip()
    arg_text = args.group(1).strip() if args else ""
    return cmd, f"{cmd} {arg_text}".strip()


def load_transcript(path):
    entries = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def find_last_prompt(entries):
    """Índice e texto do último prompt real do usuário."""
    for i in range(len(entries) - 1, -1, -1):
        e = entries[i]
        if e.get("type") != "user" or e.get("isMeta"):
            continue
        content = (e.get("message") or {}).get("content")
        if is_tool_result(content):
            continue
        text = text_from_content(content).strip()
        if not text or MARKER in text or text.startswith("Stop hook feedback"):
            continue
        if "<local-command-stdout>" in text or "<command-name>/sdd-mentor" in text:
            continue
        return i, e, text
    return None, None, None


def collect_after(entries, start):
    files, commands, tools, texts = [], [], [], []
    for e in entries[start + 1:]:
        if e.get("type") != "assistant":
            continue
        for block in (e.get("message") or {}).get("content") or []:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                texts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                name = block.get("name", "")
                inp = block.get("input") or {}
                tools.append(name)
                if name in EDIT_TOOLS:
                    p = inp.get("file_path") or inp.get("notebook_path")
                    norm = (p or "").replace("\\", "/")
                    if p and DOCS_DIR not in norm and TEMAS_DIR not in norm and p not in files:
                        files.append(p)
                elif name == "Bash" and inp.get("command"):
                    commands.append(inp["command"][:300])
    summary = "\n".join(t for t in texts if t.strip())
    if len(summary) > 4000:
        summary = summary[:4000] + "\n[...resumo truncado...]"
    tool_counts = {t: tools.count(t) for t in sorted(set(tools))}
    return files, commands[:20], tool_counts, summary


def listar_temas(project):
    """Temas já registrados: slug, título (1º "# "), nº de aulas, nº de prompts e caminho do PDF."""
    raiz = os.path.join(project, TEMAS_DIR)
    temas = []
    if not os.path.isdir(raiz):
        return temas
    for slug in sorted(os.listdir(raiz)):
        registro = os.path.join(raiz, slug, "registro.md")
        if not os.path.isfile(registro):
            continue
        titulo, aulas, prompts, no_apendice = slug, 0, 0, False
        try:
            with open(registro, "r", encoding="utf-8") as fh:
                for linha in fh:
                    if linha.startswith("# ") and titulo == slug:
                        titulo = linha[2:].strip()
                    elif linha.startswith(("## Aula ", "## Interação ")):  # "Interação" = formato antigo
                        aulas += 1
                    elif linha.startswith("## Apêndice"):
                        no_apendice = True
                    elif no_apendice and re.match(r"^\|\s*\d+\s*\|", linha):
                        prompts += 1  # linhas da "Linha do tempo dos prompts"
        except OSError:
            continue
        temas.append({
            "tema": slug,
            "titulo": titulo,
            "aulas_fundamentais": aulas,
            "prompts_registrados": prompts,
            "registro": f"{TEMAS_DIR}/{slug}/registro.md",
            "pdf": f"{DOCS_DIR}/{slug}.pdf",
        })
    return temas


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        allow_stop()

    if data.get("stop_hook_active"):
        allow_stop()

    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    if os.environ.get("SDD_MENTOR_OFF") == "1" or os.path.exists(
        os.path.join(project, ".claude", "sdd-mentor.off")
    ):
        allow_stop()

    transcript = data.get("transcript_path")
    if not transcript or not os.path.exists(transcript):
        allow_stop()

    entries = load_transcript(transcript)
    idx, entry, raw_prompt = find_last_prompt(entries)
    if idx is None:
        allow_stop()

    slash_cmd, prompt = parse_slash_command(raw_prompt)
    if len(prompt) < MIN_PROMPT_CHARS and prompt.lower().strip(" .!") in TRIVIAL:
        allow_stop()

    session_id = data.get("session_id") or "sessao"
    state_dir = os.path.join(project, ".claude", "sdd-mentor")
    os.makedirs(state_dir, exist_ok=True)
    state_path = os.path.join(state_dir, "state.json")
    try:
        with open(state_path, "r", encoding="utf-8") as fh:
            state = json.load(fh)
    except Exception:
        state = {}

    sess = state.get(session_id)
    prompt_key = entry.get("uuid") or hashlib.sha1(prompt.encode("utf-8")).hexdigest()
    if sess and prompt_key in sess.get("registered", []):
        allow_stop()  # já registrado

    now = datetime.now()
    if not sess:
        sess = {"started_at": now.isoformat(timespec="seconds"), "registered": []}

    files, commands, tool_counts, summary = collect_after(entries, idx)
    temas = listar_temas(project)

    context = {
        "session_id": session_id,
        "docs_dir": DOCS_DIR,
        "temas_dir": TEMAS_DIR,
        "temas_existentes": temas,
        "timestamp": entry.get("timestamp") or now.isoformat(timespec="seconds"),
        "prompt": prompt,
        "slash_command": slash_cmd,
        "files_changed": files,
        "commands_run": commands,
        "tools_used": tool_counts,
        "assistant_summary": summary,
    }
    ctx_path = os.path.join(state_dir, "ultima-interacao.json")
    with open(ctx_path, "w", encoding="utf-8") as fh:
        json.dump(context, fh, ensure_ascii=False, indent=2)

    sess["registered"].append(prompt_key)
    state[session_id] = sess
    with open(state_path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)

    lista = ", ".join(t["tema"] for t in temas) or "nenhum ainda"
    reason = (
        f"{MARKER} Antes de encerrar, use a skill sdd-session-mentor para registrar a última "
        f"interação. Contexto coletado em .claude/sdd-mentor/ultima-interacao.json. "
        f"Temas existentes: {lista}. Continue o tema do mesmo assunto ou crie um novo; avalie a "
        f"relevância didática (references/filtro-relevancia.md): fundamental vira aula com "
        f"figuras, complementar é incorporado como aprofundamento à aula relacionada e sem valor "
        f"didático só entra na linha do tempo de {TEMAS_DIR}/<tema>/registro.md; depois "
        f"regenere {DOCS_DIR}/<tema>.pdf. Não altere nenhum outro arquivo do projeto e, ao "
        f"final, responda apenas com uma linha confirmando o registro."
    )
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # nunca travar a sessão por erro do hook
