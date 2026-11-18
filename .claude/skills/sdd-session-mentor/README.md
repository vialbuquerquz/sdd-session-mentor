# sdd-session-mentor

Skill para Claude Code (CLI, VS Code ou JetBrains) que transforma as interações de um projeto SDD em
**aulas ilustradas em PDF, uma por tema**.

## Onde os arquivos gerados ficam

| O quê | Onde | Versionar? |
| --- | --- | --- |
| PDF de cada tema (entregável para estudo) | `docs/sessoes-sdd/<tema>.pdf` | Sim |
| Fonte do PDF: texto em Markdown | `.claude/sdd-mentor/temas/<tema>/registro.md` | Opcional (é o que permite continuar o tema) |
| Figuras: script + imagem | `.claude/sdd-mentor/temas/<tema>/figuras/NN-nome.py` e `.png` | Opcional |
| Ambiente Python da skill | `.claude/sdd-mentor/venv/` | Não |
| Estado do hook | `.claude/sdd-mentor/state.json` e `ultima-interacao.json` | Não |

- **Um arquivo por tema, não por prompt.** O tema é o assunto destrinchado (de preferência o
  requisito da spec, ex.: `fr-003-cadastro-de-clientes`). Novas interações sobre o mesmo assunto,
  mesmo em outra sessão, são acrescentadas ao mesmo PDF.
- **O nome do PDF é o slug do tema**, sem data.
- **Filtro de relevância didática** (`references/filtro-relevancia.md`): cada prompt recebe uma
  nota de 0 a 10. **Fundamental** (7–10) vira aula completa; **complementar** (3–6, ex.: "explique
  melhor o passo X") tem a resposta incorporada como aprofundamento à aula relacionada; **sem
  valor didático** (0–2) só entra no apêndice. Todo prompt aparece no apêndice "Linha do tempo
  dos prompts", com a nota e o local onde está.
- **Toda aula fundamental traz figuras** (elementos do projeto, conceitos, resumos visuais),
  conforme `references/guia-ilustracoes.md`.

Sugestão de `.gitignore`:

```gitignore
.claude/sdd-mentor/venv/
.claude/sdd-mentor/state.json
.claude/sdd-mentor/ultima-interacao.json
```

## Instalação rápida (na raiz do seu projeto)

1. Copie a pasta `.claude/` deste pacote para a raiz do projeto (mescle se já existir).
2. Se você já tinha um `.claude/settings.json`, junte o bloco `hooks.Stop` de
   `assets/settings.example.json` ao seu arquivo em vez de sobrescrever.
3. Crie o ambiente Python da skill (o Claude também cria sozinho na primeira vez):
   ```bash
   python3 -m venv .claude/sdd-mentor/venv
   .claude/sdd-mentor/venv/bin/pip install -r .claude/skills/sdd-session-mentor/scripts/requirements.txt
   ```
4. No Windows, troque `python3` por `python` (ou `py`) no comando do hook e use
   `.claude\sdd-mentor\venv\Scripts\python.exe`.
5. Abra o Claude Code no projeto, faça um pedido e confira `docs/sessoes-sdd/`.

## Uso

- **Automático:** o hook Stop pede o registro ao fim de cada resposta.
- **Manual:** `/registrar-interacao`.
- **Regenerar um PDF** depois de editar o `registro.md` à mão:
  ```bash
  .claude/sdd-mentor/venv/bin/python .claude/skills/sdd-session-mentor/scripts/gerar_pdf.py \
    .claude/sdd-mentor/temas/<tema>/registro.md docs/sessoes-sdd/<tema>.pdf
  ```
- **Desligar:** crie `.claude/sdd-mentor.off`. **Religar:** apague esse arquivo.
- **Variáveis opcionais:**
  - `SDD_MENTOR_DOCS_DIR` (pasta dos PDFs) e `SDD_MENTOR_TEMAS_DIR` (pasta das fontes);
  - `SDD_MENTOR_COR` (cor de destaque do PDF, ex.: `#EC4E26`);
  - `SDD_MENTOR_OFF=1` (desliga o registro).
