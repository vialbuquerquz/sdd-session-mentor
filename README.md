# sdd-session-mentor

Skill para [Claude Code](https://docs.claude.com/en/docs/claude-code) (CLI, VS Code ou JetBrains)
que transforma as interações de um projeto conduzido com **Spec-Driven Development (SDD)** em
**aulas ilustradas em PDF, um arquivo por tema**, em `docs/sessoes-sdd/<tema>.pdf`.

Pensada para quem está aprendendo a desenvolver com IA (e para quem ensina), ela age como um
professor sênior. Copia o prompt literal, explica o que foi pedido e entregue, avalia o prompt
com uma rubrica, sugere uma versão melhor e ilustra os conceitos com figuras. Um filtro de
relevância decide o que vira aula: só prompts fundamentais ganham aula completa; os
complementares enriquecem uma aula existente, e todos ficam listados numa linha do tempo.

## Funciona com qualquer linguagem ou stack

A skill observa a **conversa** com o Claude, não o código. O projeto pode ser em Java, C#,
JavaScript, Go, Python ou qualquer outra linguagem.

O Python só é usado pelas **ferramentas da própria skill** (o hook que coleta a interação e os
scripts que desenham as figuras e montam o PDF). Ele roda num ambiente isolado
(`.claude/sdd-mentor/venv/`) e nunca entra nas dependências do seu projeto. Os scripts de figura
quem escreve é o Claude: você não precisa saber Python.

## Pré-requisitos

- Claude Code instalado.
- **Python 3.9 ou superior** disponível no terminal (`python3`; no Windows, `python` ou `py`).
- Internet na primeira execução, para instalar no venv da skill reportlab, matplotlib e Pillow
  (`scripts/requirements.txt`).
- Opcional: uma spec do projeto (`spec.md`, `requirements.md`, `tasks.md`, Spec Kit, Kiro ou
  similar). Sem spec a skill funciona, mas aponta a falta de rastreabilidade nas análises.

## Instalação (na raiz do seu projeto)

1. Copie a pasta `.claude/` deste repositório para a raiz do seu projeto (mescle se já existir).
2. Se você já tinha um `.claude/settings.json`, junte o bloco `hooks.Stop` de
   `.claude/skills/sdd-session-mentor/assets/settings.example.json` ao seu arquivo em vez de
   sobrescrevê-lo.
3. Crie o ambiente Python da skill (o Claude também cria sozinho na primeira vez):
   ```bash
   python3 -m venv .claude/sdd-mentor/venv
   .claude/sdd-mentor/venv/bin/pip install -r .claude/skills/sdd-session-mentor/scripts/requirements.txt
   ```
   No Windows: `python -m venv .claude\sdd-mentor\venv` e
   `.claude\sdd-mentor\venv\Scripts\pip install -r .claude\skills\sdd-session-mentor\scripts\requirements.txt`.
   Troque também `python3` por `python` (ou `py`) no comando do hook em `.claude/settings.json`.
4. Abra o Claude Code no projeto, faça um pedido e confira `docs/sessoes-sdd/`.

Desligar: crie `.claude/sdd-mentor.off`. Religar: apague esse arquivo.
Registro manual: `/registrar-interacao`.

Onde cada arquivo gerado fica, o que versionar e as variáveis opcionais estão em
[`.claude/skills/sdd-session-mentor/README.md`](.claude/skills/sdd-session-mentor/README.md).

## Limitações conhecidas

- **Idioma:** os registros, templates e referências estão em português do Brasil. Para outro
  idioma, traduza os arquivos de `references/` e `assets/` e as instruções do `SKILL.md`.
- **Mermaid:** diagramas mermaid não são renderizados no PDF; a skill desenha as figuras com
  matplotlib.
- **Classificação:** as notas do filtro de relevância e da rubrica são julgamentos do Claude.
  Ajuste as faixas em `references/filtro-relevancia.md` se elas não servirem ao seu contexto.
- **Sem capturas de tela:** a skill não abre navegador nem tira screenshots; telas são
  representadas por diagramas ou pelas imagens que já existem no projeto.

## Estrutura do repositório

```text
.claude/
├── settings.json                       # hook Stop (exemplo pronto para copiar)
├── commands/registrar-interacao.md     # comando /registrar-interacao
└── skills/sdd-session-mentor/
    ├── SKILL.md                        # instruções da skill (ponto de entrada)
    ├── README.md                       # onde os arquivos gerados ficam e como usar
    ├── references/                     # fases SDD, rubrica, filtro de relevância, guia de ilustrações
    ├── assets/                         # templates (tema, aula, aprofundamento) e configurações
    └── scripts/                        # stop_hook.py, gerar_pdf.py, figuras_base.py, requirements.txt
```

## Contribuindo

- Abra uma *issue* descrevendo o problema ou a ideia, com um exemplo de prompt quando fizer
  sentido.
- Mantenha os scripts simples e com poucas dependências. O `stop_hook.py` deve continuar usando
  só a biblioteca padrão do Python, porque roda a cada resposta do Claude.
- Não há testes automatizados ainda. Antes de um *pull request*, rode o hook com um transcript
  de exemplo e gere um PDF de teste com `scripts/gerar_pdf.py`.
- Registre as mudanças no [`CHANGELOG.md`](CHANGELOG.md).

## Licença

[MIT](LICENSE).
