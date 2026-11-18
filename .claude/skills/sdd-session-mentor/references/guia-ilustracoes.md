# Guia de ilustrações dos registros

Cada registro é uma aula, e uma boa figura ensina mais rápido do que três parágrafos. Toda
**aula fundamental** DEVE ter pelo menos **uma figura**, e o número deve ser proporcional a ela:
uma aula curta pede 1; uma implementação grande pede de 3 a 6. Um **aprofundamento**
(prompt complementar, ver `filtro-relevancia.md`) só ganha figura se ela ensinar algo que o
texto não mostra, por exemplo um roteiro em passos.
Uma figura sem propósito é ruído, então antes de criar uma, responda: **"o que o aluno deve
enxergar aqui que o texto sozinho não mostra bem?"**

## As três categorias

| Categoria | Para quê | Exemplos | Função em `figuras_base.py` |
| --- | --- | --- | --- |
| **1. Elementos do projeto** | Mostrar o que existe de fato no projeto apresentado | Árvore de pastas antes/depois, logos, ícones e imagens de `assets/`, fluxo entre módulos reais, chamadas HTTP reais | `antes_depois`, `painel_imagens`, `sequencia`, `fluxo` |
| **2. Ensinar um conceito** | Tornar visível uma ideia abstrata | Sequência de um protocolo (login, refresh), certo × errado, condição de corrida, camadas de arquitetura | `sequencia`, `comparacao`, `fluxo` |
| **3. Condensar informação** | Transformar texto ou tabela em leitura de relance | Rubrica do prompt em barras, mapa "código de erro → comportamento", linha do tempo das fases SDD | `barras_rubrica`, `mapa`, `fluxo` |

Combinação recomendada por tipo de interação:

| Tipo de interação | Figuras sugeridas |
| --- | --- |
| Implementação | Antes/depois dos arquivos (1), fluxo ou sequência do comportamento implementado (1 ou 2), um conceito-chave (2), rubrica (3) |
| Correção de bug | Comparação comportamento errado × correto (2), sequência que mostra onde falhava (1 ou 2) |
| Criação de spec / plano / tarefas | Fluxo das fases SDD destacando a fase atual (3), mapa requisito → tarefas (3) |
| Dúvida conceitual | Uma figura do conceito (2); se a dúvida for sobre o projeto, mostre o elemento real (1) |
| Configuração de ambiente | Fluxo dos passos (3) ou diagrama de componentes (1) |

## Regras

1. **Arquivos:** cada figura é um script `NN-nome-curto.py` em
   `.claude/sdd-mentor/temas/<tema>/figuras/`, que grava `NN-nome-curto.png` ao lado. Guarde o
   script: ele permite corrigir a figura depois. A numeração `NN` é contínua dentro do tema.
2. **Legenda numerada que ensina:** `![Figura N — o que observar](figuras/NN-nome.png)`. A
   legenda diz o que o aluno deve notar, não só o nome da figura.
3. **Referência no texto:** cite a figura no parágrafo que ela apoia ("veja a Figura 3").
4. **Fiel ao projeto:** nomes de arquivos, rotas, códigos e cores devem ser os reais. Para
   imagens do projeto, use os arquivos originais com `painel_imagens`. Para a paleta da marca,
   sobrescreva `CORES` no script.
5. **Legível:** no máximo cerca de 12 caixas por figura; texto com no mínimo 8 pt; cor nunca como
   único portador de informação (use também rótulos como "✓", "✗", "Evite"/"Prefira").
6. **Sem dados sensíveis:** nada de segredos, tokens, senhas, e-mails reais ou conteúdo de `.env`.
7. **Diagramas mermaid não são renderizados no PDF:** desenhe a figura com `figuras_base.py`.
8. **Sem capturas de tela inventadas:** se não for possível capturar a tela real, use um diagrama
   e diga isso na legenda.

## Esqueleto de um script de figura

```python
import sys
sys.path.insert(0, ".claude/skills/sdd-session-mentor/scripts")
from figuras_base import *

mapa(
    [("401 INVALID_CREDENTIALS", "Alerta + limpa a senha"),
     ("429 ACCOUNT_LOCKED", "Contagem regressiva")],
    arquivo=aqui("04-mapa-erros.png"),
    titulo_esq="Resposta da API", titulo_dir="Comportamento na tela",
)
```

Rode na raiz do projeto: `.claude/sdd-mentor/venv/bin/python .claude/sdd-mentor/temas/<tema>/figuras/04-mapa-erros.py`.
Para figuras fora dos modelos prontos, use `nova_figura`, `caixa` e `seta`.
