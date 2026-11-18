---
description: Registra a última interação desta sessão no PDF ilustrado do tema correspondente
---

Use a skill `sdd-session-mentor` para registrar a última interação técnica desta sessão.
Escolha o tema (continue um existente em `.claude/sdd-mentor/temas/` se for o mesmo assunto,
ou crie um novo), acrescente a interação ao `registro.md` do tema com figuras ilustrativas e
regenere `docs/sessoes-sdd/<tema>.pdf`. Se existir `.claude/sdd-mentor/ultima-interacao.json`
referente a esta sessão, use-o; caso contrário, reconstrua a interação a partir da conversa.

Observações adicionais do usuário (opcional): $ARGUMENTS
