"""
Utilitários para as figuras ilustrativas dos registros (skill sdd-session-mentor).

Cada figura é um script curto em .claude/sdd-mentor/temas/<tema>/figuras/NN-nome.py que
importa este módulo e grava NN-nome.png ao lado. Exemplo:

    import sys; sys.path.insert(0, ".claude/skills/sdd-session-mentor/scripts")
    from figuras_base import *

    sequencia(
        participantes=["Navegador", "API"],
        mensagens=[("Navegador", "API", "POST /login", "ok"), ("API", "Navegador", "200 + token", "ok")],
        arquivo=aqui("01-login.png"),
    )

Rode com o venv da skill:  .claude/sdd-mentor/venv/bin/python <script>.py
Funções: caixa, seta, nova_figura, salvar, aqui, sequencia, antes_depois, fluxo, comparacao,
         mapa, barras_rubrica, painel_imagens.
O guia de quando usar cada uma está em references/guia-ilustracoes.md.
"""

import inspect
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

# Paleta neutra e acessível; troque CORES no script da figura para usar a marca do projeto.
CORES = {
    "texto": "#1F1F1F",
    "suave": "#555555",
    "borda": "#6B6B6B",
    "fundo": "#F7F7F7",
    "destaque": "#2B5C8A",
    "destaque_claro": "#DCE6F0",
    "ok": "#146C43",
    "ok_claro": "#E3F1EA",
    "erro": "#B02A37",
    "erro_claro": "#F8E1E3",
    "alerta": "#9A6700",
    "alerta_claro": "#FFF4D6",
}

plt.rcParams.update({
    "font.family": ["DejaVu Sans"],
    "font.size": 10,
    "text.color": CORES["texto"],
    "axes.edgecolor": CORES["borda"],
})

__all__ = ["CORES", "caixa", "seta", "nova_figura", "salvar", "aqui", "sequencia", "antes_depois", "fluxo",
           "comparacao", "mapa", "barras_rubrica", "painel_imagens", "plt"]


# ------------------------------------------------------------------ básicos
def aqui(nome):
    """Caminho ao lado do script que chamou (para gravar o PNG junto do .py)."""
    chamador = Path(inspect.stack()[1].filename).resolve().parent
    return chamador / nome


def nova_figura(largura=9, altura=5):
    fig, ax = plt.subplots(figsize=(largura, altura))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def salvar(fig, arquivo):
    arquivo = Path(arquivo)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(arquivo, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"figura gerada: {arquivo}")


def _quebrar(ax, texto, w, fonte):
    """Quebra linhas longas para caberem na largura w (em coordenadas do eixo)."""
    largura_pol = w * ax.get_position().width * ax.figure.get_figwidth()
    capacidade = max(8, int(largura_pol * 72 / (fonte * 0.62)))
    return "\n".join(textwrap.fill(l, capacidade) if len(l) > capacidade else l for l in texto.split("\n"))


def caixa(ax, x, y, w, h, texto, cor=None, borda=None, fonte=9, negrito=False, mono=False, cor_texto=None):
    """Caixa arredondada com texto centralizado; linhas longas são quebradas automaticamente."""
    texto = _quebrar(ax, texto, w, fonte)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.015",
                                facecolor=cor or CORES["fundo"], edgecolor=borda or CORES["borda"],
                                linewidth=1.2))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fonte,
            weight="bold" if negrito else "normal", color=cor_texto or CORES["texto"],
            family="DejaVu Sans Mono" if mono else "DejaVu Sans", linespacing=1.35)


def seta(ax, x1, y1, x2, y2, cor=None, tracejada=False, espessura=1.3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12,
                                 color=cor or CORES["borda"], linewidth=espessura,
                                 linestyle="--" if tracejada else "-"))


# ------------------------------------------------------------------ modelos prontos
def sequencia(participantes, mensagens, arquivo, titulo=None, nota=None):
    """
    Diagrama de sequência (quem fala com quem, em ordem).
    mensagens: lista de (de, para, texto, tipo) com tipo em {"normal", "ok", "erro"},
               ou ("--", None, "Título da fase", None) para uma faixa de fase.
    """
    n = len(mensagens)
    fig, ax = nova_figura(9.5, max(3.0, 0.5 * n + 1.6))
    xs = {p: (i + 0.5) / len(participantes) for i, p in enumerate(participantes)}
    topo = 0.92
    meia = min(0.15, 0.45 / len(participantes))
    for p, x in xs.items():
        caixa(ax, x - meia, topo, 2 * meia, 0.07, p, fonte=8.5, cor=CORES["destaque_claro"], borda=CORES["destaque"],
              negrito=True)
        ax.plot([x, x], [0.03, topo], color=CORES["borda"], lw=1, ls=(0, (4, 3)))
    passo = (topo - 0.08) / max(n, 1)
    y = topo - passo * 0.7
    for de, para, texto, tipo in mensagens:
        if de == "--":
            ax.add_patch(FancyBboxPatch((0.005, y - 0.012), 0.99, 0.03, boxstyle="round,pad=0.004",
                                        facecolor=CORES["destaque_claro"], edgecolor="none"))
            ax.text(0.012, y + 0.003, texto, fontsize=8.5, weight="bold", va="center")
        else:
            cor = {"ok": CORES["ok"], "erro": CORES["erro"]}.get(tipo, CORES["texto"])
            volta = xs[para] < xs[de]
            seta(ax, xs[de], y, xs[para], y, cor=cor, tracejada=volta)
            ax.text((xs[de] + xs[para]) / 2, y + 0.01, texto, ha="center", va="bottom", fontsize=8, color=cor,
                    bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
        y -= passo
    if titulo:
        ax.set_title(titulo, weight="bold")
    if nota:
        ax.text(0.5, 0.0, nota, ha="center", fontsize=8, style="italic", color=CORES["suave"])
    salvar(fig, arquivo)


def antes_depois(antes, depois, arquivo, titulo_antes="Antes", titulo_depois="Depois"):
    """Duas colunas: itens que saíram (riscados) e itens que entraram. depois aceita (rótulo, descrição)."""
    linhas = max(len(antes), len(depois))
    fig, ax = nova_figura(9, max(3.0, 0.55 * linhas + 1))
    ax.text(0.22, 0.98, titulo_antes, ha="center", weight="bold", fontsize=12, color=CORES["erro"])
    ax.text(0.74, 0.98, titulo_depois, ha="center", weight="bold", fontsize=12, color=CORES["ok"])
    h = 0.86 / linhas
    for i, item in enumerate(antes):
        y = 0.9 - (i + 1) * h
        caixa(ax, 0.02, y, 0.40, h * 0.8, item, cor=CORES["erro_claro"], borda=CORES["erro"], mono=True, fonte=8.5)
        ax.plot([0.05, 0.39], [y + h * 0.4, y + h * 0.4], color=CORES["erro"], lw=1)
    for i, item in enumerate(depois):
        y = 0.9 - (i + 1) * h
        rotulo, desc = item if isinstance(item, tuple) else (item, "")
        if desc:
            caixa(ax, 0.48, y, 0.18, h * 0.8, rotulo, cor=CORES["destaque_claro"], borda=CORES["destaque"],
                  mono=True, fonte=8.3, negrito=True)
            caixa(ax, 0.67, y, 0.31, h * 0.8, desc, cor=CORES["ok_claro"], borda=CORES["ok"], fonte=8)
        else:
            caixa(ax, 0.48, y, 0.50, h * 0.8, rotulo, cor=CORES["ok_claro"], borda=CORES["ok"], mono=True, fonte=8.5)
    seta(ax, 0.43, 0.47, 0.47, 0.47, cor=CORES["texto"], espessura=2)
    salvar(fig, arquivo)


def fluxo(etapas, arquivo, titulo=None, vertical=False):
    """Etapas encadeadas (passo a passo, pipeline, ciclo de vida). etapas: lista de textos."""
    n = len(etapas)
    if vertical:
        fig, ax = nova_figura(8, max(3, 0.9 * n))
        h = 0.9 / n
        for i, e in enumerate(etapas):
            y = 0.95 - (i + 1) * h
            caixa(ax, 0.1, y + h * 0.1, 0.8, h * 0.7, e, cor=CORES["destaque_claro"], borda=CORES["destaque"])
            if i < n - 1:
                seta(ax, 0.5, y + h * 0.1, 0.5, y - h * 0.2, cor=CORES["destaque"])
    else:
        fig, ax = nova_figura(max(6, 2.1 * n), 2.4)
        w = 0.96 / n
        for i, e in enumerate(etapas):
            x = 0.02 + i * w
            caixa(ax, x, 0.25, w * 0.78, 0.5, e, cor=CORES["destaque_claro"], borda=CORES["destaque"], fonte=8.5)
            if i < n - 1:
                seta(ax, x + w * 0.78, 0.5, x + w, 0.5, cor=CORES["destaque"])
    if titulo:
        ax.set_title(titulo, weight="bold")
    salvar(fig, arquivo)


def comparacao(titulo_esq, itens_esq, titulo_dir, itens_dir, arquivo, rotulo_esq="Evite", rotulo_dir="Prefira"):
    """Lado a lado: jeito errado × jeito certo (ou opção A × opção B)."""
    linhas = max(len(itens_esq), len(itens_dir))
    fig, ax = nova_figura(9.5, max(2.6, 0.6 * linhas + 1.2))
    for x0, tit, itens, cor, claro, rot in ((0.01, titulo_esq, itens_esq, CORES["erro"], CORES["erro_claro"], rotulo_esq),
                                             (0.51, titulo_dir, itens_dir, CORES["ok"], CORES["ok_claro"], rotulo_dir)):
        ax.text(x0 + 0.24, 0.97, f"{rot}: {tit}", ha="center", weight="bold", color=cor, fontsize=11)
        h = 0.85 / linhas
        for i, item in enumerate(itens):
            y = 0.9 - (i + 1) * h
            caixa(ax, x0, y, 0.48, h * 0.82, item, cor=claro, borda=cor, fonte=8.5)
    salvar(fig, arquivo)


def mapa(pares, arquivo, titulo_esq="Entrada", titulo_dir="Resultado", nota=None):
    """Mapa de decisão: cada entrada (código, situação) aponta para um comportamento."""
    n = len(pares)
    fig, ax = nova_figura(9.5, max(2.8, 0.85 * n + 0.8))
    ax.text(0.2, 0.97, titulo_esq, ha="center", weight="bold")
    ax.text(0.72, 0.97, titulo_dir, ha="center", weight="bold")
    h = 0.88 / n
    for i, (esq, dir_) in enumerate(pares):
        y = 0.92 - (i + 1) * h
        caixa(ax, 0.02, y, 0.36, h * 0.78, esq, cor=CORES["destaque_claro"], borda=CORES["destaque"], mono=True,
              negrito=True, fonte=8.3)
        caixa(ax, 0.46, y, 0.52, h * 0.78, dir_, fonte=8.3)
        seta(ax, 0.38, y + h * 0.39, 0.46, y + h * 0.39, cor=CORES["texto"])
    if nota:
        ax.text(0.5, 0.0, nota, ha="center", fontsize=8, style="italic", color=CORES["suave"])
    salvar(fig, arquivo)


def barras_rubrica(criterios, notas, arquivo, maximo=2):
    """Gráfico das notas da rubrica (0 a 2 por critério)."""
    total, possivel = sum(notas), maximo * len(notas)
    fig, ax = plt.subplots(figsize=(8, 0.5 * len(criterios) + 1.2))
    cores = [CORES["ok"] if n == maximo else CORES["alerta"] if n > 0 else CORES["erro"] for n in notas]
    ax.barh(criterios[::-1], notas[::-1], color=cores[::-1], edgecolor=CORES["texto"], height=0.6)
    for i, n in enumerate(notas[::-1]):
        ax.text(n + 0.04, i, f"{n}/{maximo}", va="center", fontsize=9, weight="bold")
    ax.set_xlim(0, maximo + 0.4)
    ax.set_xticks(range(maximo + 1))
    ax.set_xlabel("Nota (0 = ausente · 1 = parcial · 2 = bem feito)")
    ax.set_title(f"Avaliação do prompt: {total}/{possivel}", weight="bold")
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    salvar(fig, arquivo)


def painel_imagens(imagens, arquivo, colunas=None):
    """
    Painel com imagens reais do projeto (logos, telas, ícones), cada uma com legenda.
    imagens: lista de (caminho_da_imagem, legenda).
    """
    from PIL import Image as PILImage

    colunas = colunas or len(imagens)
    linhas = -(-len(imagens) // colunas)
    fig, eixos = plt.subplots(linhas, colunas, figsize=(3.2 * colunas, 3.2 * linhas), squeeze=False)
    for eixo in eixos.flat:
        eixo.axis("off")
    for eixo, (caminho, legenda) in zip(eixos.flat, imagens):
        img = PILImage.open(caminho).convert("RGBA")
        img.thumbnail((900, 900))
        eixo.imshow(img)
        eixo.set_title(legenda, fontsize=9)
    salvar(fig, arquivo)
