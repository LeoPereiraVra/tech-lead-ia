- O sistema deve alterar a tela `/admin/relatorio/consulta/email/index` de acordo com o [figma](https://www.figma.com/design/OkeEs5DIgDTaS1UTvXG1BS/SCI-WEB---Entregas?node-id=17795-1515&p=f&t=1Gp6vEp9pq7smg82-0)
- A tela deve filtrar os logs de acordo com o modulo acessado
  - Cada modulo tem um banco de log:
    - fila_email.alvara_log -> alvará
    - fila_email.atendimento_log -> Atendimento
    - fila_email.cnd_log -> CND
    - fila_email.folha_log -> SCI Report - Serviços 24h
    - fila_email.imposto_log -> SCI Report - Serviços 24h
    - fila_email.relatorio_log -> SCI Report - Serviços 24h
    - fila_email.sbs_log -> SBS
    - fila_email.tarefa_log -> Tarefas
  - A aba de whatsapp
    - fila_mensagem.atendimento_log -> Atendimento 
    - fila_mensagem.relatorio_log -> SCI Report - Serviços 24h
- A aba de whatsapp, só deve aparecer os módulos 'SCI Report Serviços 24h' e 'Atendimento'
- A aba de whats app só deve aparecer pra quem tem modulo gerencial
- Caso não tenha o modulo gerencial a tela deve exibir as mensagens sem abas como no [figma](https://www.figma.com/design/OkeEs5DIgDTaS1UTvXG1BS/SCI-WEB---Entregas?node-id=20229-2759&t=1Gp6vEp9pq7smg82-4)

- Alterar menus, adicionando o sub-menus
  - Central de notificação
      |
      |--- Geral
      |--- Grupo de notificação
      |--- Notificações enviadas

- O menu "Geral" deve abrir a tela `/admin/relatorio/central/notificacao/configuracao/form`
- O menu "Grupo de notificações" abre `/admin/relatorio/central/notificacao/index`
- O menu "Notificações enviadas" abre a tela de `/admin/relatorio/consulta/email/index`
- A tela de "Central de notificações" deve ter o nome do grupo e uma nova aba de "Empresas" caso não seja o grupo geral
- Para a aba de "Empresas" listar as empresas em uma grid com datatable, ao marcar selecionar todos, deve ser gravado o filtro e deve gravar todas as empresas filtradas que não estejam em outro grupo
- As empresas em outro grupo devem ficar desabilitadas e não podem ser marcadas
- Ao selecionar o checkobox do cabeçalho da grid, todas as empresa elegiveis devem ser selecionadas
- A estrutura das abas de "Central de notificações" permanece como é hoje
- As telas devem seguir o padrão atual com datatable e totalizadores
- Manter responsividade no mobile

### Log interno
- Criar logs dos envio feitos pelo whatsapp salvando no firehouse, como é feito no api-atendimento `app/Http/Middleware/FirehoseRequestLogger.php`
- Adicionar a opção de consultar o log no painel
- Criar solicitação com os dev-ops pra monitorar os logs e salvar no firehouse