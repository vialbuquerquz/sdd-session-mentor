# Filtro de relevância didática

Nem todo prompt merece uma aula. Um pedido que só detalha um trecho de uma resposta anterior
não deve ganhar rubrica, prompt reescrito e lista de conceitos como se fosse uma entrega nova.
Esse tipo de pedido **enriquece** a aula que já existe. Antes de escrever qualquer coisa,
avalie o quanto a interação é fundamental para o aprendizado e escolha o destino dela.

## 1. Pontue os 5 critérios (0 a 2 cada, total 0 a 10)

| Critério | 0 | 1 | 2 |
| --- | --- | --- | --- |
| **Novidade** | Repete ou só detalha o que o tema já registra | Acrescenta um detalhe novo a um assunto já registrado | Traz conceito, decisão ou artefato que o tema ainda não tem |
| **Transferibilidade** | Só vale para este caso/ambiente | Vale para projetos parecidos | Lição geral de engenharia ou de trabalho com IA |
| **Impacto** | Nada mudou no projeto | Ajuste pequeno (correção pontual, configuração) | Mudou código, spec ou uma decisão relevante |
| **Valor do prompt** | Prompt comum, sem nada a ensinar | Tem um ponto de melhoria útil | Exemplar: muito bom (vira modelo) ou com um erro clássico |
| **Marco SDD** | Não marca etapa | Apoia a fase atual (dúvida, verificação) | Abre ou fecha uma fase (spec, plano, tarefas, implementação, validação) |

## 2. Escolha o destino

| Nível | Nota | Destino no documento do tema |
| --- | --- | --- |
| **Fundamental** | 7 a 10 | **Aula completa**: nova seção `## Aula N` com `assets/template-interacao.md` (rubrica, prompt reescrito, conceitos, figuras) |
| **Complementar** | 3 a 6 | **Sem seção nova.** O conteúdo útil da resposta vira um bloco "Aprofundamento" (`assets/template-aprofundamento.md`), inserido **dentro da seção que ele aprofunda** (normalmente a da aula fundamental relacionada) |
| **Sem valor didático** | 0 a 2 | **Nada no corpo.** Só uma linha no apêndice "Linha do tempo dos prompts" |

**Regras de exceção:**
- A **primeira interação de um tema novo** é sempre fundamental: ela abre a aula.
- Um **erro que revela um antipadrão** (de `references/fases-sdd.md`) sobe um nível.
- Saudações, "ok/obrigado" e pedidos para desligar o registro **não são registrados**, nem no apêndice.

## 3. Como incorporar um aprofundamento

- **Use a resposta, não o prompt:** extraia o conteúdo explicado (o porquê, os passos, os
  sintomas), reescreva-o como texto de aula e coloque-o onde o leitor precisa dele.
- **Escolha o ponto de inserção:** junto ao conceito, ao passo ou aos "Pontos de atenção" que ele
  detalha. Se aprofundar um conceito da seção 5, insira logo abaixo dele.
- **Não repita** o que a aula já diz; acrescente só o que é novo.
- **Figura** só se ela ensinar algo que o texto não mostra (ex.: um roteiro em passos).
- **Dica de prompt:** se o prompt complementar tiver um ponto de melhoria útil, registre uma
  linha "Dica de prompt" dentro do bloco, sem rubrica.

## 4. Linha do tempo dos prompts (apêndice obrigatório)

Todo prompt registrado (de qualquer nível, exceto os não registrados) entra no apêndice do
tema, em ordem cronológica:

| # | Data | Sessão | Prompt (literal) | Nível (nota) | Onde está |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-03-02 | `a1b2c3d4` | "Implemente o requisito FR-003 (cadastro de clientes)..." | Fundamental (8) | Aula 1 |
| 2 | 2026-03-02 | `a1b2c3d4` | "não entendi o passo 3 do teste" | Complementar (4) | Aula 1 › Pontos de atenção |
| 3 | 2026-03-03 | `e5f6a7b8` | "roda o lint de novo" | Sem valor didático (1) | — |

Prompts longos podem ser abreviados no apêndice com "..." **somente** quando o texto
literal completo já aparece na aula correspondente; prompts complementares e sem valor
didático aparecem completos. Use a coluna "Nível" também para justificar decisões: alguém
que discorde da classificação deve conseguir ver a nota.
