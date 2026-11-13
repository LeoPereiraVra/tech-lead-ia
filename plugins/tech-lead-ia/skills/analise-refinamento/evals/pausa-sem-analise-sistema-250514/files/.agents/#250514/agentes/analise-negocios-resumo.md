# #250514 — Central de Notificações: submenus, grupos e notificações enviadas — resumo da análise de negócios

> Base: .agents/#250514/analise-negocios.md, com as decisões D1 a D8 de `decisoes.md`. Gerado em 11/11/2026.

## Contexto

Nos seis módulos administradores do SCI Report (24H, Atendimento, CND, Alvará, Tarefas e Central de Certificados), a "Central de notificações" abre hoje uma lista de grupos, e só o 24H tem consulta de e-mails enviados. A solicitação divide a Central em três submenus, leva a criação e a edição de grupos para um modal, cria a consulta de notificações enviadas em cada módulo (e-mail em todos; WhatsApp no 24H e no Atendimento, para escritórios Gerencial) e cria um log interno dos envios de WhatsApp. As regras de configuração das notificações não mudam.

## Requisitos funcionais

### RF-01 — Dividir a Central de notificações em três submenus
- Geral, Grupos de notificação e Notificações enviadas, nessa ordem, nos seis módulos.
- Ao sair dos dados gerais, volta para Geral; ao sair da configuração de um grupo, volta para Grupos de empresas.
- Origem: Req. 1

### RF-02 — Separar as permissões dos submenus
- Três permissões independentes por módulo; "Central de notificações" só agrupa.
- Valores iniciais: Geral e Grupos com o valor atual da Central; Notificações enviadas bloqueado nos cinco módulos diferentes do 24H; no 24H, com o valor de "Consultas / E-mails enviados".
- No 24H, enquanto o menu antigo existir, as duas permissões ficam espelhadas.
- Origem: Req. 1; D1, D6

### RF-03 — Listar e excluir grupos na tela Grupos de empresas
- Grid sem os grupos ocultos, com nome, quantidade de empresas e ações Configurações e Excluir.
- Excluir pede confirmação e apaga o grupo, o vínculo com as empresas e a configuração; as empresas voltam à configuração geral; a exclusão vai para o log do escritório.
- Origem: Req. 2

### RF-04 — Criar e editar grupo em modal
- Nome obrigatório (até 255 caracteres, repetição permitida) e seleção das empresas que não estão em outro grupo.
- Selecionar todos respeita o filtro aplicado.
- Toda gravação vai para o log do escritório, inclusive quando só o nome muda.
- Origem: Req. 3; D8

### RF-05 — Consultar as notificações enviadas do módulo
- Só os envios do módulo de acesso; abas E-mail e WhatsApp no 24H e no Atendimento de escritórios Gerencial, e só e-mail nos demais casos.
- Ao menos um filtro é obrigatório; uma data só considera aquele dia; ordem do mais recente para o mais antigo.
- O usuário adicional vê os envios de todas as empresas; só o campo Empresa fica restrito às empresas liberadas a ele.
- Origem: Req. 4; D5

### RF-06 — Consultar os e-mails enviados
- E-mails enviados com sucesso, inclusive os antigos. No 24H, continuam aparecendo também os e-mails que a consulta atual já mostra (senha, backup, cadastro).
- E-mail sem empresa aparece com "Nenhuma empresa vinculada a este e-mail" e não é encontrado pelo filtro Empresa.
- Exportação PDF e CSV com todos os resultados filtrados e a coluna Empresa igual à do grid.
- Origem: Req. 5; D3, D4, D7

### RF-07 — Consultar os envios de WhatsApp
- Uma linha por número de destino, com empresa, data e hora do envio pela SCI, integração, template (quando houver) e número.
- Só envios com sucesso; envios antigos aparecem quando o módulo de origem é identificável.
- Exportação PDF e CSV como no RF-06.
- Origem: Req. 6; D7

### RF-08 — Registrar o log interno de WhatsApp
- Registra os envios (sucesso ou erro com motivo, mensagem e variáveis), a troca de número e a conexão e desconexão.
- Consulta pela SCI na tela Logs do painel, só para administradores.
- Origem: Req. 7; D2

### RF-09 — Transformar o menu antigo do 24H em atalho
- "Consultas / E-mails enviados" mostra o alerta de descontinuação a cada acesso e leva a Notificações enviadas, aba E-mail.
- O menu sai numa versão futura, sem prazo definido.
- Origem: Req. 8; D6

### RF-10 — Adaptar as telas novas ao celular
- Filtros um abaixo do outro, datas lado a lado e botões abaixo dos filtros.
- Origem: RNF 1

## Diferenças em relação à análise de negócios

- O log interno não registra alterações de templates nem de datas de vínculo, que não acontecem no sistema (D2).
- O menu antigo do 24H não sai em 45 dias nem automaticamente; sai numa versão futura, sem data (D6).
