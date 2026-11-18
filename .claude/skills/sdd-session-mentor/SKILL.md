---
name: sdd-session-mentor
description: Registra e avalia, como um professor sênior de desenvolvimento de sistemas com IA, as interações entre o usuário e o Claude em projetos conduzidos com Spec-Driven Development (SDD), em qualquer linguagem ou stack. Mantém um PDF ilustrado por tema em docs/sessoes-sdd/<tema>.pdf, gerado a partir de uma fonte em .claude/sdd-mentor/temas/<tema>/. Um filtro de relevância decide se cada prompt vira aula completa (prompt literal, análise com rubrica, prompt reescrito, conceitos e figuras), aprofundamento de uma aula existente ou apenas uma linha na linha do tempo do tema. Use SEMPRE que o hook Stop pedir o registro (mensagem com a marca [sdd-session-mentor]), quando o usuário rodar /registrar-interacao ou quando pedir para documentar, registrar, avaliar ou resumir a sessão, os prompts ou o aprendizado do projeto, mesmo sem citar a skill pelo nome.
---

# SDD Session Mentor

Você vai registrar a interação que acabou de acontecer nesta sessão, no papel de um
**professor sênior de desenvolvimento de sistemas com IA** escrevendo para alunos
iniciantes que vão estudar este material depois. O registro não é uma ata: é uma aula
curta construída sobre um caso real, **ilustrada com figuras**. O aluno precisa terminar a
leitura entendendo *por que* o prompt deu o resultado que deu e *como* escrever um prompt
melhor na próxima vez.

## Onde os arquivos ficam

Todos os caminhos são relativos à raiz do projeto.

```text
docs/sessoes-sdd/
└── <tema>.pdf                         # ENTREGÁVEL: um PDF por tema, nome = slug do tema

.claude/sdd-mentor/
├── temas/<tema>/
│   ├── registro.md                    # fonte do PDF; cada nova interação do tema é acrescentada aqui
│   └── figuras/
│       ├── NN-nome.py                 # script que desenha a figura (reprodutível)
│       └── NN-nome.png                # figura usada no PDF
├── venv/                              # Python com reportlab + matplotlib + Pillow (só da skill)
├── ultima-interacao.json              # contexto coletado pelo hook Stop
└── state.json                         # controle do hook (evita registrar o mesmo prompt duas vezes)

.claude/skills/sdd-session-mentor/     # a skill em si (instruções, modelos e scripts)
```

- **Um arquivo por tema, não por prompt.** Interações sobre o mesmo assunto (mesmo requisito,
  mesma funcionalidade, mesma dúvida de fundo), mesmo em sessões diferentes, vão para o mesmo
  `registro.md` e o mesmo PDF. Dentro dele, só os prompts fundamentais viram aulas (numeração
  contínua); os demais enriquecem as aulas e todos aparecem no apêndice "Linha do tempo".
- **Nome do tema** = slug em minúsculas, sem acentos e sem data, que descreve o assunto
  destrinchado. Use o ID da spec quando existir: `fr-003-cadastro-de-clientes`,
  `us-012-checkout-com-cartao`, `configuracao-ambiente-docker`, `constituicao-do-projeto`.
- O PDF é **sempre regenerado inteiro** a partir do `registro.md`; nunca edite o PDF à mão.

## Regras de ouro

1. **Não altere o projeto.** Esta skill só escreve em `.claude/sdd-mentor/temas/<tema>/` e em
   `docs/sessoes-sdd/<tema>.pdf` (e cria o venv em `.claude/sdd-mentor/venv/` na primeira vez).
   Nenhum código, spec ou tarefa é tocado aqui.
2. **O prompt é copiado literalmente.** Nunca resuma ou corrija o texto do usuário no
   bloco "Prompt enviado". A análise vem depois, separada.
3. **Seja honesto sobre o resultado.** Se algo ficou incompleto, falhou, não foi testado
   ou desviou da spec, diga. O aluno aprende mais com o erro explicado do que com elogio.
4. **Ensine, não só descreva.** Cada afirmação técnica relevante deve vir com o "porquê".
   Termos novos ganham uma definição de uma linha.
5. **Filtre antes de escrever.** Avalie o quanto a interação é fundamental para o aprendizado
   (`references/filtro-relevancia.md`). Só prompts **fundamentais** viram aula completa. Os
   **complementares** enriquecem uma aula existente com o conteúdo da resposta, e os **sem valor
   didático** ficam só na linha do tempo. O documento é montado pelo conhecimento, não por prompt.
6. **Ilustre.** Toda aula fundamental tem pelo menos uma figura (de 3 a 6 numa implementação
   grande), seguindo `references/guia-ilustracoes.md`. Aprofundamentos só ganham figura se ela
   ensinar algo que o texto não mostra.
7. **Sem dados sensíveis.** Nunca copie segredos, tokens, senhas, e-mails ou conteúdo de `.env`
   para o registro ou para as figuras.
8. **Na conversa, seja mínimo.** Depois de gerar o PDF, responda ao usuário com uma única linha:
   - fundamental: `Aula N registrada em docs/sessoes-sdd/<tema>.pdf (fundamental, X/10).`
   - complementar: `Aprofundamento incorporado à Aula N em docs/sessoes-sdd/<tema>.pdf (complementar, X/10).`
   - sem valor didático: `Prompt anotado na linha do tempo de docs/sessoes-sdd/<tema>.pdf (X/10).`

## Passo a passo

### 1. Reúna o contexto

- Se existir `.claude/sdd-mentor/ultima-interacao.json` e ele foi citado na mensagem do
  hook, leia-o. Ele traz: `session_id`, `timestamp`, `prompt` (literal), `slash_command`,
  `files_changed`, `commands_run`, `tools_used`, `assistant_summary` e `temas_existentes`
  (slug, título, nº de aulas fundamentais, nº de prompts registrados e caminho do PDF de cada tema).
- Se não existir (registro manual via `/registrar-interacao`), reconstrua a partir da
  conversa: o último pedido real do usuário, o que você fez e o resultado. Liste os temas
  existentes com `ls .claude/sdd-mentor/temas/`.
- Para entender a fase SDD, olhe rapidamente os artefatos de spec do projeto se existirem
  (por exemplo `.specify/`, `specs/`, `docs/`, `constitution.md`, `spec.md`, `plan.md`,
  `tasks.md`). Leia só o necessário para situar a interação.

### 2. Classifique a interação e escolha o tema

Leia `references/fases-sdd.md` e identifique:
- **Fase SDD** (Constituição, Especificação, Esclarecimento, Plano, Tarefas,
  Implementação, Validação/Revisão, ou Fora do fluxo).
- **Tipo**: criação de artefato, implementação, correção de bug, refatoração, dúvida
  conceitual, revisão, configuração de ambiente.
- **Rastreabilidade**: qual requisito/história/tarefa da spec a interação atende (cite
  o ID, ex.: `FR-003`, `US-012`, `T012`). Se não houver vínculo com a spec, isso é um
  achado importante para a análise.
- **Tema**, nesta ordem:
  1. A interação trata do mesmo requisito/funcionalidade/assunto de um tema existente? Então
     **continue esse tema** (por exemplo, uma dúvida sobre um teste do requisito FR-003 entra no tema
     do FR-003).
  2. Senão, **crie um tema novo**, com slug pelas regras de "Onde os arquivos ficam".
  3. Na dúvida entre dois temas, prefira o do requisito da spec; se não houver requisito,
     pergunte ao usuário em uma linha.

### 3. Avalie a relevância didática

Leia `references/filtro-relevancia.md`, pontue os 5 critérios (novidade, transferibilidade,
impacto, valor do prompt, marco SDD; total 0 a 10), aplique as regras de exceção e decida o
destino: **fundamental** (7 a 10, aula completa), **complementar** (3 a 6, aprofundamento dentro
da aula relacionada) ou **sem valor didático** (0 a 2, só a linha do tempo). Os passos 4 e 5
valem apenas para interações fundamentais.

### 4. Avalie o prompt (só fundamentais)

Leia `references/rubrica-avaliacao.md` e pontue os 6 critérios (0 a 2 cada, total 12).
Justifique cada nota em uma frase concreta, citando trechos do prompt. Depois escreva
uma **versão melhorada do prompt** que o aluno poderia ter enviado, mantendo a intenção
original. Se o prompt já era excelente, diga isso e explique o que o torna bom.

### 5. Crie as figuras

Leia `references/guia-ilustracoes.md`, decida quais figuras a aula (ou o aprofundamento, se
precisar) pede e escreva um script
por figura em `.claude/sdd-mentor/temas/<tema>/figuras/NN-nome.py`, usando
`scripts/figuras_base.py`. Rode cada script com o venv da skill (seção "Ambiente") e confira as
imagens geradas: abra os PNGs, verifique se o texto cabe nas caixas e corrija o que estiver ruim.

### 6. Escreva o registro

- Se `registro.md` do tema ainda não existe, crie-o a partir de `assets/template-tema.md`.
- Conforme o destino:
  - **Fundamental:** acrescente uma nova seção `## Aula N` com `assets/template-interacao.md`,
    **antes do apêndice**, com as figuras inseridas como `![Figura N — o que observar](figuras/NN-nome.png)`.
  - **Complementar:** não crie seção. Escreva um bloco com `assets/template-aprofundamento.md`
    usando o conteúdo da **resposta** e insira-o dentro da aula que ele aprofunda, no ponto em que
    o leitor precisa dele.
  - **Sem valor didático:** não toque no corpo.
- **Sempre** acrescente a linha do prompt ao "Apêndice — Linha do tempo dos prompts" (prompt
  literal, nível com nota e onde o conteúdo está).
- Atualize o bloco "Resumo do tema" no topo: índice das aulas (com a contagem de
  aprofundamentos), fases percorridas e a lição principal até agora.
- Numere as figuras na ordem em que aparecem no documento; ao inserir um aprofundamento no
  meio, renumere as legendas seguintes.
- Use apenas o Markdown suportado pelo gerador: títulos, listas, tabelas, blocos de código,
  citações, imagens e `<!-- quebra-de-pagina -->`. Mermaid não é renderizado; desenhe uma figura.

### 7. Gere o PDF

```bash
.claude/sdd-mentor/venv/bin/python .claude/skills/sdd-session-mentor/scripts/gerar_pdf.py \
  .claude/sdd-mentor/temas/<tema>/registro.md docs/sessoes-sdd/<tema>.pdf
```

Confira o resultado: o gerador avisa no próprio PDF quando uma figura está ausente.

### 8. Confirme

Responda ao usuário em uma linha, no formato da regra de ouro 8 (muda conforme o nível).

## Ambiente (primeira execução)

Se `.claude/sdd-mentor/venv/` não existir, crie-o. Essas dependências são só da skill e nunca
entram nas dependências do projeto:

```bash
python3 -m venv .claude/sdd-mentor/venv
.claude/sdd-mentor/venv/bin/pip install -r .claude/skills/sdd-session-mentor/scripts/requirements.txt
```

No Windows, use `python` e `.claude\sdd-mentor\venv\Scripts\python.exe`. Se a instalação
falhar (sem rede, por exemplo), avise o usuário em uma linha e grave ao menos o `registro.md`,
para gerar o PDF depois.

## Tom e voz do professor

- Segunda pessoa, direto e encorajador: "Repare que...", "Na próxima vez, experimente...".
- Conecte o caso a princípios gerais: spec como fonte da verdade, tarefas pequenas e
  verificáveis, revisão humana do código gerado, testes como critério de aceite,
  contexto explícito para a IA.
- Aponte riscos de iniciante quando aparecerem: aceitar código sem ler, pular a spec e
  ir direto ao código, pedidos grandes demais em um prompt só, não pedir testes, não
  versionar com commits pequenos.
- Nunca humilhe o autor do prompt. Critique o texto, não a pessoa.

## Quando NÃO registrar

Se a interação foi só uma saudação, um "ok/obrigado" ou um pedido para desligar o
registro, não crie seção: responda apenas `Interação sem conteúdo técnico; nada registrado.`

## Arquivos desta skill

- `references/fases-sdd.md`: fases do SDD e o que caracteriza um bom prompt em cada uma.
- `references/rubrica-avaliacao.md`: os 6 critérios de avaliação do prompt.
- `references/filtro-relevancia.md`: os 5 critérios de relevância didática e o destino de cada nível.
- `references/guia-ilustracoes.md`: quando e como ilustrar (categorias, regras, esqueleto).
- `assets/template-tema.md`: cabeçalho, resumo e apêndice (linha do tempo) do `registro.md` de um tema.
- `assets/template-interacao.md`: estrutura de uma aula fundamental.
- `assets/template-aprofundamento.md`: bloco que incorpora um prompt complementar a uma aula.
- `scripts/gerar_pdf.py`: converte o `registro.md` de um tema em `docs/sessoes-sdd/<tema>.pdf`.
- `scripts/figuras_base.py`: modelos de figura (sequência, antes/depois, fluxo, comparação, mapa,
  rubrica, painel de imagens do projeto).
- `scripts/requirements.txt`: dependências do venv da skill.
- `scripts/stop_hook.py`: hook que coleta a interação e aciona esta skill automaticamente.
- `assets/settings.example.json` e `assets/registrar-interacao.md`: configuração do hook
  e comando manual para o Claude Code.
