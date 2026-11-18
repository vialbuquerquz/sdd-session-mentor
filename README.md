# sdd-session-mentor

Skill para [Claude Code](https://docs.claude.com/en/docs/claude-code) (CLI, VS Code ou JetBrains)
que transforma o seu trabalho com IA em **material de estudo**. A cada pedido que você faz ao
Claude num projeto conduzido com **Spec-Driven Development (SDD)**, ela avalia se aquilo ensina
algo e, se ensinar, escreve uma aula curta sobre o caso real: o que foi pedido, o que foi
entregue, o que o prompt fez bem ou mal e como escrevê-lo melhor. Tudo fica num **PDF
ilustrado, um por tema**, em `docs/sessoes-sdd/<tema>.pdf`.

É útil para quem está aprendendo a desenvolver com IA, para quem ensina e para equipes que
querem registrar decisões e boas práticas de prompt ao longo de um projeto.

## Funcionalidades

### 1. Registro automático ao fim de cada resposta
Um hook do Claude Code roda quando o Claude termina de responder. Ele coleta o prompt literal,
os arquivos alterados, os comandos executados e um resumo da resposta, e pede ao Claude que
registre a interação. Não precisa lembrar de documentar nada. Se preferir controlar quando
registrar, use o comando `/registrar-interacao` ou desligue o automático.

### 2. Filtro de relevância didática
Nem todo prompt merece uma aula. Antes de escrever, a skill dá ao prompt uma nota de 0 a 10
em cinco critérios (novidade, transferibilidade, impacto, valor do prompt e marco SDD) e escolhe
o destino:

| Nível | Exemplo de prompt | O que acontece no documento |
| --- | --- | --- |
| **Fundamental** (7–10) | "Implemente o requisito FR-003 seguindo a spec" | Vira uma **aula completa** |
| **Complementar** (3–6) | "Não entendi o passo 3 do teste" | A explicação é **incorporada à aula relacionada**, como um bloco "Aprofundamento" |
| **Sem valor didático** (0–2) | "Roda o lint de novo" | Só uma linha na **linha do tempo** do tema |

Assim o documento cresce em conhecimento, não em volume.

### 3. Aulas completas para os prompts fundamentais
Cada aula segue a mesma estrutura, escrita como um professor sênior falaria com um iniciante:

- **Prompt literal:** o texto exato que foi enviado, sem correções.
- **O que foi pedido:** a intenção explicada, e se o pedido fazia sentido naquela fase do SDD.
- **O que foi feito e o resultado:** ações, arquivos alterados e um resultado **honesto**, dizendo
  o que ficou pendente, o que não foi testado e onde houve desvios da spec.
- **Avaliação do prompt:** uma rubrica de 6 critérios (clareza, ancoragem na spec, escopo,
  critério de aceite, restrições, aderência à fase) com nota e justificativa.
- **Prompt reescrito:** uma versão melhor do mesmo pedido, mantendo a intenção.
- **Conceitos para estudar**, **pontos de atenção** e uma **pergunta para refletir**.

### 4. Um PDF por tema, não um arquivo por prompt
Interações sobre o mesmo assunto, mesmo em dias ou sessões diferentes, vão para o mesmo
documento. O tema é identificado de preferência pelo requisito da spec (ex.:
`fr-003-cadastro-de-clientes.pdf`), e o nome do arquivo descreve o assunto, sem data.

### 5. Figuras que ensinam
Toda aula traz ilustrações geradas para o caso, em três categorias:

- **Elementos do projeto:** árvore de arquivos antes/depois, logos e imagens do próprio
  projeto, fluxo entre módulos.
- **Conceitos:** diagramas de sequência (ex.: um login com renovação de token), comparação
  "evite × prefira".
- **Informação condensada:** mapa "entrada → comportamento", gráfico com as notas da rubrica.

Cada figura vem com uma legenda numerada que diz o que observar, e o script que a desenhou fica
guardado, para ser corrigido depois.

### 6. Rastreabilidade com a spec e com o histórico
- Cada aula aponta a **fase SDD** (especificação, plano, tarefas, implementação, validação...) e
  os **IDs da spec** atendidos. A falta de vínculo com a spec aparece como um achado.
- O apêndice **"Linha do tempo dos prompts"** lista todos os prompts do tema, com data, nota do
  filtro e onde o conteúdo foi parar. Quem discordar de uma classificação vê a justificativa.

## Como funciona

```text
você envia um prompt ──► o Claude responde ──► hook Stop coleta a interação
        │
        ▼
filtro de relevância (0–10) ──► fundamental?   ──► nova aula + figuras
                              ├─► complementar? ──► aprofundamento na aula relacionada
                              └─► sem valor?    ──► linha na linha do tempo
        │
        ▼
.claude/sdd-mentor/temas/<tema>/registro.md  ──►  docs/sessoes-sdd/<tema>.pdf
     (fonte editável + figuras)                      (regenerado inteiro)
```

Ao terminar, o Claude confirma em uma linha, por exemplo:
`Aula 2 registrada em docs/sessoes-sdd/fr-003-cadastro-de-clientes.pdf (fundamental, 8/10).`

## Funciona com qualquer linguagem ou stack

A skill observa a **conversa** com o Claude, não o código. O projeto pode ser em Java, C#,
JavaScript, Go, Python ou qualquer outra linguagem.

O Python só é usado pelas **ferramentas da própria skill** (o hook, o desenho das figuras e a
montagem do PDF). Ele roda num ambiente isolado (`.claude/sdd-mentor/venv/`) e nunca entra nas
dependências do seu projeto. Os scripts de figura quem escreve é o Claude: você não precisa
saber Python.

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

## Uso no dia a dia

| Quero... | Como |
| --- | --- |
| Registrar automaticamente | Nada a fazer: o hook dispara ao fim de cada resposta |
| Registrar manualmente | `/registrar-interacao` (aceita observações: `/registrar-interacao foque no tratamento de erros`) |
| Pausar o registro | Crie o arquivo `.claude/sdd-mentor.off` (apague para religar) |
| Corrigir um registro | Edite `.claude/sdd-mentor/temas/<tema>/registro.md` e regenere o PDF (comando no README da skill) |
| Mudar a cor do PDF | Variável de ambiente `SDD_MENTOR_COR` (ex.: `#EC4E26`) |

Onde cada arquivo gerado fica, o que versionar e todas as variáveis opcionais estão em
[`.claude/skills/sdd-session-mentor/README.md`](.claude/skills/sdd-session-mentor/README.md).

## Limitações conhecidas

- **Específico do Claude Code:** o hook, o comando `/registrar-interacao` e o carregamento
  automático da skill dependem do Claude Code. Em outros assistentes, os templates, as
  referências e os scripts funcionam, mas o registro é manual: peça para a IA ler o `SKILL.md` e
  registrar a última interação.
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


## Licença

[MIT](LICENSE).
