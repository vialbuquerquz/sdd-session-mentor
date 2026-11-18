#!/usr/bin/env python3
"""
Gera o PDF de um tema a partir do seu registro em Markdown (skill sdd-session-mentor).

Uso (na raiz do projeto, com o venv da skill):
    .claude/sdd-mentor/venv/bin/python .claude/skills/sdd-session-mentor/scripts/gerar_pdf.py \\
        .claude/sdd-mentor/temas/<tema>/registro.md docs/sessoes-sdd/<tema>.pdf

Markdown suportado (subconjunto simples, o mesmo dos templates da skill):
  - títulos #, ##, ###, ####          - listas "- " / "* " / "1. " (com recuo)
  - tabelas com "|"                    - blocos de código ``` (mermaid NÃO é renderizado)
  - citações "> "                      - linha horizontal "---"
  - imagem sozinha na linha: ![Legenda](figuras/01-nome.png)
  - inline: **negrito**, *itálico*, `código`, [texto](url)
  - <!-- quebra-de-pagina --> força nova página; outros comentários HTML são ignorados.

Caminhos de imagem são relativos à pasta do registro.md.
Dependências: reportlab, matplotlib (fornece a fonte DejaVu, com acentos e símbolos), Pillow.
"""

import os
import re
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, Image, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table,
    TableStyle,
)

# ------------------------------------------------------------------ fontes e cores
_TTF = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
pdfmetrics.registerFont(TTFont("Txt", str(_TTF / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("Txt-B", str(_TTF / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Txt-I", str(_TTF / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("Txt-BI", str(_TTF / "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("Mono", str(_TTF / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("Txt", normal="Txt", bold="Txt-B", italic="Txt-I", boldItalic="Txt-BI")

DESTAQUE = colors.HexColor(os.environ.get("SDD_MENTOR_COR", "#2B5C8A"))
TEXTO = colors.HexColor("#1F1F1F")
SUAVE = colors.HexColor("#555555")
BORDA = colors.HexColor("#9A9A9A")
FUNDO_CAB = colors.HexColor("#E6ECF2")
FUNDO_COD = colors.HexColor("#F4F4F4")

LARGURA = A4[0] - 4 * cm
ALTURA_MAX_IMG = A4[1] * 0.62

_base = ParagraphStyle("base", fontName="Txt", fontSize=9.6, leading=14, textColor=TEXTO, spaceAfter=6)
EST = {
    "h1": ParagraphStyle("h1", parent=_base, fontName="Txt-B", fontSize=18, leading=23, spaceAfter=6),
    "h2": ParagraphStyle("h2", parent=_base, fontName="Txt-B", fontSize=14, leading=18, spaceBefore=12,
                         spaceAfter=6, textColor=DESTAQUE),
    "h3": ParagraphStyle("h3", parent=_base, fontName="Txt-B", fontSize=11.5, leading=15, spaceBefore=10,
                         spaceAfter=4),
    "h4": ParagraphStyle("h4", parent=_base, fontName="Txt-B", fontSize=10, leading=14, spaceBefore=6, spaceAfter=3),
    "p": _base,
    "li": ParagraphStyle("li", parent=_base, spaceAfter=3),
    "cit": ParagraphStyle("cit", parent=_base, fontName="Txt-I", textColor=SUAVE, leftIndent=14),
    "leg": ParagraphStyle("leg", parent=_base, fontName="Txt-I", fontSize=8.3, leading=11, textColor=SUAVE,
                          alignment=TA_CENTER, spaceAfter=10),
    "cel": ParagraphStyle("cel", parent=_base, fontSize=8.4, leading=11, spaceAfter=0),
    "celc": ParagraphStyle("celc", parent=_base, fontName="Txt-B", fontSize=8.4, leading=11, spaceAfter=0),
    "cod": ParagraphStyle("cod", fontName="Mono", fontSize=7.8, leading=10.6, textColor=TEXTO),
}


# ------------------------------------------------------------------ inline
def inline(texto):
    """Converte o Markdown inline em marcação do reportlab, escapando o resto."""
    partes = re.split(r"(`[^`]+`)", texto)
    saida = []
    for parte in partes:
        if parte.startswith("`") and parte.endswith("`") and len(parte) > 1:
            saida.append(f"<font face='Mono'>{escape(parte[1:-1])}</font>")
            continue
        s = escape(parte)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r"<link href='\2'><u>\1</u></link>", s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
        s = re.sub(r"(?<![\w])_(?!\s)(.+?)(?<!\s)_(?![\w])", r"<i>\1</i>", s)
        saida.append(s)
    return "".join(saida)


def par(texto, estilo="p", **kw):
    return Paragraph(inline(texto), EST[estilo], **kw)


# ------------------------------------------------------------------ blocos
def bloco_codigo(linhas):
    quebradas = []
    for linha in linhas:
        quebradas.extend(textwrap.wrap(linha, 98, drop_whitespace=False, replace_whitespace=False) or [""])
    t = Table([[Preformatted("\n".join(quebradas), EST["cod"])]], colWidths=[LARGURA])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), FUNDO_COD), ("BOX", (0, 0), (-1, -1), 0.5, BORDA),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def _celulas(linha):
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", linha)]


def tabela(linhas):
    cab = _celulas(linhas[0])
    corpo = [_celulas(l) for l in linhas[2:]] if len(linhas) > 1 and re.match(r"^\s*\|?\s*:?-", linhas[1]) \
        else [_celulas(l) for l in linhas[1:]]
    n = len(cab)
    dados = [[par(c, "celc") for c in cab]]
    for linha in corpo:
        linha = (linha + [""] * n)[:n]
        dados.append([par(c, "cel") for c in linha])
    # Cada coluna tem largura mínima para a sua maior palavra (evita "Sessã/o", "11/ 12") e o
    # espaço restante é dividido conforme o volume de texto da coluna.
    linhas_texto = [[re.sub(r"[*`]", "", c) for c in (r + [""] * n)[:n]] for r in [cab] + corpo]
    largura_char = 8.4 * 0.62
    minimos, volumes = [], []
    for j in range(n):
        celulas = [r[j] for r in linhas_texto]
        palavra = max((len(p) for c in celulas for p in c.split()), default=1)
        minimos.append(min(palavra * largura_char + 10, LARGURA * 0.45))
        volumes.append(min(max(len(c) for c in celulas), 70) + 1)
    sobra = LARGURA - sum(minimos)
    if sobra > 0:
        larguras = [m + sobra * v / sum(volumes) for m, v in zip(minimos, volumes)]
    else:
        larguras = [LARGURA * m / sum(minimos) for m in minimos]
    t = Table(dados, colWidths=larguras, repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, BORDA), ("BACKGROUND", (0, 0), (-1, 0), FUNDO_CAB),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def imagem(caminho, legenda, base):
    arq = (base / caminho).resolve()
    if not arq.exists():
        return par(f"**[figura ausente: {caminho}]** {legenda}", "leg")
    img = Image(str(arq))
    larg, alt = LARGURA, LARGURA * img.imageHeight / img.imageWidth
    if alt > ALTURA_MAX_IMG:
        larg, alt = larg * ALTURA_MAX_IMG / alt, ALTURA_MAX_IMG
    img.drawWidth, img.drawHeight = larg, alt
    return KeepTogether([img, Spacer(1, 3), par(legenda, "leg")])


# ------------------------------------------------------------------ parser
RE_LISTA = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(.*)$")
RE_IMG = re.compile(r"^!\[(.*)\]\(([^)]+)\)\s*$")


def converter(md, base):
    linhas = md.splitlines()
    el, titulo = [], None
    i, paragrafo = 0, []

    def fechar_paragrafo():
        if paragrafo:
            el.append(par(" ".join(s.strip() for s in paragrafo)))
            paragrafo.clear()

    while i < len(linhas):
        linha = linhas[i]
        tira = linha.strip()

        if tira.startswith("<!--"):
            fechar_paragrafo()
            bloco = tira
            while "-->" not in bloco and i + 1 < len(linhas):
                i += 1
                bloco += linhas[i]
            if "quebra-de-pagina" in bloco:
                el.append(PageBreak())
            i += 1
            continue

        if tira.startswith("```"):
            fechar_paragrafo()
            codigo = []
            i += 1
            while i < len(linhas) and not linhas[i].strip().startswith("```"):
                codigo.append(linhas[i].rstrip("\n"))
                i += 1
            el.append(bloco_codigo(codigo))
            el.append(Spacer(1, 6))
            i += 1
            continue

        if not tira:
            fechar_paragrafo()
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", tira)
        if m:
            fechar_paragrafo()
            nivel = len(m.group(1))
            if nivel == 1 and titulo is None:
                titulo = re.sub(r"[*`]", "", m.group(2))
            el.append(par(m.group(2), f"h{nivel}"))
            i += 1
            continue

        if re.match(r"^(-{3,}|\*{3,})$", tira):
            fechar_paragrafo()
            el.append(HRFlowable(width="100%", thickness=0.6, color=BORDA, spaceBefore=6, spaceAfter=8))
            i += 1
            continue

        m = RE_IMG.match(tira)
        if m:
            fechar_paragrafo()
            el.append(imagem(m.group(2), m.group(1), base))
            i += 1
            continue

        if tira.startswith("|"):
            fechar_paragrafo()
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith("|"):
                bloco.append(linhas[i])
                i += 1
            el.append(tabela(bloco))
            el.append(Spacer(1, 6))
            continue

        if tira.startswith(">"):
            fechar_paragrafo()
            bloco = []
            while i < len(linhas) and linhas[i].strip().startswith(">"):
                bloco.append(linhas[i].strip()[1:].strip())
                i += 1
            # Cada linha "> " da citação vira uma linha própria.
            el.append(Paragraph("<br/>".join(inline(b) for b in bloco), EST["cit"]))
            continue

        m = RE_LISTA.match(linha)
        if m:
            fechar_paragrafo()
            while i < len(linhas):
                m = RE_LISTA.match(linhas[i])
                if not m:
                    # continuação recuada de um item
                    if linhas[i].startswith("  ") and linhas[i].strip() and el:
                        ultimo = el.pop()
                        texto = ultimo.text + " " + inline(linhas[i].strip())
                        el.append(Paragraph(texto, ultimo.style, bulletText=ultimo.bulletText))
                        i += 1
                        continue
                    break
                nivel = len(m.group(1).expandtabs(2)) // 2
                marcador = "•" if m.group(2) in "-*" else m.group(2)
                estilo = ParagraphStyle(f"li{nivel}", parent=EST["li"], leftIndent=14 + nivel * 14,
                                        bulletIndent=3 + nivel * 14)
                el.append(Paragraph(inline(m.group(3)), estilo, bulletText=marcador))
                i += 1
            el.append(Spacer(1, 3))
            continue

        paragrafo.append(linha)
        i += 1

    fechar_paragrafo()
    # A quebra de página do fim do template não deve gerar uma página em branco.
    while el and isinstance(el[-1], (PageBreak, Spacer)):
        el.pop()
    return el, titulo or base.name


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    origem, destino = Path(sys.argv[1]), Path(sys.argv[2])
    elementos, titulo = converter(origem.read_text(encoding="utf-8"), origem.parent)
    destino.parent.mkdir(parents=True, exist_ok=True)

    def moldura(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(DESTAQUE)
        canvas.rect(0, A4[1] - 0.3 * cm, A4[0], 0.3 * cm, stroke=0, fill=1)
        canvas.setFont("Txt", 7.5)
        canvas.setFillColor(SUAVE)
        rodape = titulo if len(titulo) <= 95 else titulo[:92] + "..."
        canvas.drawString(2 * cm, 1.1 * cm, rodape)
        canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"página {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(destino), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.7 * cm,
                            bottomMargin=1.9 * cm, title=titulo, author="sdd-session-mentor")
    doc.build(elementos, onFirstPage=moldura, onLaterPages=moldura)
    print(f"PDF gerado: {destino}")


if __name__ == "__main__":
    main()
