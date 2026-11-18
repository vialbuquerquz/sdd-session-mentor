## Aula {{N}} — {{TITULO_CURTO}}

**Quando:** {{DATA_HORA ou "AAAA-MM-DD (horário não registrado)"}} · **Sessão:** `{{8 primeiros caracteres do session_id}}` · **Fase SDD:** {{FASE}} · **Tipo:** {{TIPO}} · **Rastreabilidade:** {{IDS_DA_SPEC ou "sem vínculo com a spec"}}

### 1. Prompt enviado

```text
{{PROMPT_LITERAL}}
```

### 2. O que foi solicitado

{{Explique em 1 a 3 parágrafos curtos, como para um iniciante: qual era a intenção,
em que ponto do projeto isso acontece, e por que esse pedido faz (ou não) sentido nesta
fase do SDD.}}

### 3. O que o Claude fez e o resultado

{{Resumo do raciocínio e das ações, em ordem. Cite as figuras no texto ("veja a Figura N").}}

![Figura {{N}} — {{o que o aluno deve observar}}](figuras/{{NN-nome}}.png)

| Arquivo / artefato | O que mudou |
| --- | --- |
| `{{caminho}}` | {{descrição}} |

**Resultado:** {{O que ficou pronto, o que ficou pendente, se houve testes e se passaram.
Seja honesto sobre falhas ou desvios da spec.}}

### 4. Análise do professor

**Avaliação do prompt**

| Critério | Nota | Justificativa |
| --- | --- | --- |
| Clareza do objetivo | x/2 | ... |
| Contexto e ancoragem na spec | x/2 | ... |
| Escopo adequado | x/2 | ... |
| Critério de aceite / verificação | x/2 | ... |
| Restrições técnicas | x/2 | ... |
| Aderência à fase SDD | x/2 | ... |
| **Total** | **x/12** | **{{NÍVEL}}** |

![Figura {{N}} — Notas por critério: {{onde o prompt perdeu pontos}}](figuras/{{NN-rubrica}}.png)

**O que funcionou:** {{1 a 3 pontos, com o porquê.}}

**O que poderia ser melhor:** {{1 a 3 pontos, com o porquê e o impacto no resultado.}}

**Prompt reescrito (versão sugerida):**

```text
{{PROMPT_MELHORADO}}
```

### 5. Conceitos para estudar

{{Uma linha por termo. Quando um conceito for central, ilustre-o (categoria 2 do guia).}}

- **{{Termo}}**: {{definição de uma linha e por que importa aqui.}}

### 6. Pontos de atenção

{{Riscos técnicos, coisas que o aluno deve verificar manualmente (ler o diff, rodar
testes, atualizar a spec), dívidas criadas. Omita a seção se não houver nada relevante.}}

### 7. Para refletir

> {{Uma pergunta que faça o aluno pensar sobre a decisão tomada ou o próximo passo.}}

<!-- quebra-de-pagina -->
