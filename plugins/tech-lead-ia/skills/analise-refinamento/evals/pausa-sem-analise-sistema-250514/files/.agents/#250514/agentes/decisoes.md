# #250514 — Decisões

> Cada resposta do analista, registrada como decisão. D = validação da análise de negócios; S = análise de sistema.

## D1 — Permissões de Geral, Grupos e Notificações enviadas
- Pergunta: Geral e Grupos são uma permissão ou duas? Dependem do pai?
- Decisão: são três permissões separadas (Geral, Grupos de notificação e Notificações enviadas), cada uma liberada sozinha. Na liberação, Geral e Grupos recebem o valor atual de "Central de notificações"; depois disso, são independentes, e o pai só agrupa.
- Quem decidiu: analista de sistemas, em 11/11/2026
- Diverge da análise: não
- Afeta: Req. 1 e os casos de teste do Req. 1

## D2 — Conteúdo do log interno de WhatsApp
- Pergunta: o log registra só envios, troca de número e conexão/desconexão? Aparece na tela Logs do painel?
- Decisão: o log registra o envio de mensagens (sucesso ou erro com o motivo, a mensagem e as variáveis), a troca do número e a conexão e desconexão, gravado da mesma forma que a api-atendimento grava hoje, e aparece na tela Logs do painel. Alterações de templates e de datas de vínculo ficam de fora, porque não acontecem no sistema.
- Quem decidiu: analista de negócios, resposta trazida pelo analista de sistemas em 11/11/2026
- Diverge da análise: sim. O Req. 7 pedia também as alterações de templates e de datas de vínculo.
- Afeta: Req. 7 e seus casos de teste

## D3 — E-mails de senha, backup e cadastro
- Pergunta: continuam aparecendo no 24H?
- Decisão: o que a consulta atual do 24H mostra hoje continua aparecendo no 24H, além dos e-mails do próprio 24H. Os e-mails dos outros cinco módulos aparecem só no módulo de origem.
- Quem decidiu: analista de negócios, em 11/11/2026
- Diverge da análise: não
- Afeta: Req. 5

## D4 — E-mails gravados sem empresa
- Pergunta: seguem como hoje ou os envios passam a gravar a empresa?
- Decisão: segue o sistema atual. Os e-mails sem empresa aparecem com a mensagem da análise e não são encontrados pelo filtro Empresa. Os envios não passam a gravar a empresa nesta solicitação.
- Quem decidiu: analista de sistemas, em 11/11/2026
- Diverge da análise: não
- Afeta: Req. 5

## D5 — Usuário adicional restrito a algumas empresas
- Pergunta: vê os envios de todas as empresas ou só das liberadas?
- Decisão: segue o sistema atual. O usuário adicional vê os envios de todas as empresas do escritório; só o campo Empresa fica restrito às empresas liberadas a ele. Vale para e-mail e WhatsApp.
- Quem decidiu: analista de sistemas, em 11/11/2026
- Diverge da análise: não
- Afeta: Req. 4, 5 e 6

## D6 — Saída do menu antigo do 24H
- Pergunta: mecanismo de data, remoção manual após o prazo ou versão futura sem prazo?
- Decisão: o menu antigo continua como atalho, com o alerta de descontinuação, sem prazo de 45 dias e sem saída automática. O menu e a permissão saem numa versão futura, sem data definida. Enquanto o menu existir, as permissões ficam espelhadas.
- Quem decidiu: analista de negócios, em 11/11/2026
- Diverge da análise: sim. O Req. 8 removia o menu em 45 dias; o caso de teste "No 45º dia e depois do fim do prazo" deixa de valer.
- Afeta: Req. 8 e seus casos de teste

## D7 — Coluna Empresa na exportação
- Pergunta: igual ao grid ou " - ", como hoje?
- Decisão: a coluna Empresa do PDF e do CSV sai igual à do grid, inclusive com "Nenhuma empresa vinculada a este e-mail". O resto da exportação segue como hoje.
- Quem decidiu: analista de negócios, em 11/11/2026
- Diverge da análise: não
- Afeta: Req. 5 e Req. 6

## D8 — Log quando só o nome do grupo muda
- Pergunta: trocar só o nome gera registro no log?
- Decisão: toda alteração salva vai para o log do escritório, inclusive quando só o nome muda.
- Quem decidiu: analista de sistemas, em 11/11/2026
- Diverge da análise: não
- Afeta: Req. 3
