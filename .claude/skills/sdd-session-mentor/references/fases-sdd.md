# Fases do Spec-Driven Development (SDD)

No SDD a especificação é a fonte da verdade. O código é uma consequência dela, e toda
mudança relevante começa (ou termina) atualizando a spec. Ferramentas como o GitHub
Spec Kit (`/speckit.constitution`, `/speckit.specify`, `/speckit.clarify`,
`/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) e o Kiro (requirements →
design → tasks) seguem essa mesma sequência. Use os nomes abaixo no registro.

| Fase | Pergunta central | Artefato típico | Sinais no prompt | O que um bom prompt traz |
| --- | --- | --- | --- | --- |
| Constituição | Quais princípios nunca podem ser violados? | `constitution.md` | "princípios", "padrões do projeto", stack, qualidade | Regras verificáveis (ex.: "todo endpoint tem teste de contrato") |
| Especificação | O quê e por quê, sem o como | `spec.md`, histórias, requisitos `FR-xxx` | "quero que o sistema...", "usuário pode..." | Problema, usuários, histórias, critérios de aceite, fora de escopo |
| Esclarecimento | O que está ambíguo na spec? | Seção de perguntas/decisões | "o que falta definir", `/clarify` | Pedido para listar ambiguidades antes de decidir |
| Plano | Como vamos construir? | `plan.md`, modelo de dados, contratos | stack, arquitetura, banco, API | Restrições técnicas, alternativas, vínculo com a constituição |
| Tarefas | Em que passos pequenos? | `tasks.md` com IDs `T001...` | "quebre em tarefas", ordem, dependências | Tarefas pequenas, testáveis, com dependências e paralelismo |
| Implementação | Escrever o código de uma tarefa | código + testes | "implemente T012", "crie o endpoint" | ID da tarefa, arquivos-alvo, critério de pronto, pedir testes |
| Validação/Revisão | Atende à spec? | relatório, testes, PR | "revise", "teste", "está de acordo?" | Comparar resultado com critérios de aceite da spec |
| Fora do fluxo | Ajuda pontual | variável | dúvida conceitual, erro de ambiente | Contexto do erro, o que já foi tentado |

## Antipadrões comuns de iniciantes (aponte quando aparecerem)

- **Vibe coding dentro do SDD**: pedir código sem citar spec, plano ou tarefa.
- **Spec com "como" demais**: escolher framework na fase de especificação.
- **Tarefa gigante**: "implemente o módulo inteiro" num prompt só, sem critério de pronto.
- **Spec desatualizada**: mudar comportamento no código e não atualizar a spec.
- **Aceite cego**: aceitar o resultado sem rodar testes ou ler o diff.
- **Pular o esclarecimento**: deixar a IA decidir sozinha o que a spec não define.
