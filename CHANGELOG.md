# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/); versões seguem
[SemVer](https://semver.org/lang/pt-BR/).

## [1.0.0] — 2026-11-18

### Adicionado
- Um PDF ilustrado por tema em `docs/sessoes-sdd/<tema>.pdf`, regenerado a partir de
  `.claude/sdd-mentor/temas/<tema>/registro.md` (`scripts/gerar_pdf.py`).
- Filtro de relevância didática: cada prompt vira aula completa, aprofundamento de uma aula
  existente ou só uma linha na linha do tempo (`references/filtro-relevancia.md`).
- Figuras obrigatórias nas aulas, com modelos prontos (`scripts/figuras_base.py`) e guia de uso
  (`references/guia-ilustracoes.md`).
- Apêndice "Linha do tempo dos prompts" em cada tema.
- Hook Stop que coleta a interação, lista os temas existentes e evita registros duplicados.

### Alterado
- Registros deixam de ser um arquivo Markdown por sessão e passam a ser um PDF por tema.
- Seções fundamentais passam a se chamar "Aula N". O hook ainda reconhece o formato antigo
  "Interação N".
