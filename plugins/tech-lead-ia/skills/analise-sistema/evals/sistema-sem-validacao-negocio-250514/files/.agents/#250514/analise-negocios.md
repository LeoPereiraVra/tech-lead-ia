**Requisito 1 — Reestruturar o menu e os acessos da Central de Notificações**
-

- Nos seis módulos administradores (SCI Report 24H, SCI Report Atendimento, CND, Alvará, Tarefas e Central de Certificados), a opção "Central de notificações" deixa de abrir uma tela e passa a exibir os submenus, nesta ordem:
  - Geral: abre a tela de dados gerais da Central, sem mudança de regra;
  - Grupos de notificação: abre a tela Grupos de empresas (Requisito 2);
  - Notificações enviadas: abre a tela Notificações enviadas (Requisito 4).
- Ao sair da tela de dados gerais, o usuário volta para Geral; ao sair da configuração de um grupo, volta para Grupos de empresas.
- Acesso do usuário adicional (o usuário principal acessa tudo):
  - Geral e Grupos de notificação herdam a liberação atual de "Central de notificações" no módulo;
  - Notificações enviadas nos cinco módulos diferentes do SCI Report 24H nasce desabilitado, mesmo com a Central liberada;
  - Notificações enviadas no SCI Report 24H nasce com a liberação de "Consultas / E-mails enviados" e não depende da liberação da Central. Durante a transição (Requisito 8), as duas permissões ficam espelhadas: liberar ou bloquear uma faz o mesmo com a outra. Quando o menu antigo é removido, fica só "Notificações enviadas", com o valor que tinha.
- Nenhuma regra de negócio da Central de Notificações muda.

**Requisito 2 — Montar a tela Grupos de empresas**
-

- Título "Central de notificações", subtítulo "Grupos de empresas" e o texto: *"Crie configuração de notificações específicas para grupos de empresas que não se aplicam na configuração geral. Para editar um grupo existente, clique no grupo que deseja alterar."*
- Botão "Novo grupo", que abre o modal de criação (Requisito 3).
- Grid dos grupos já criados, sem os grupos ocultos, com as colunas:
  - Nome do grupo;
  - Empresas: quantidade de empresas vinculadas, como "1 empresa" ou "5 empresas", e "-" quando o grupo não tem empresas;
  - Ações: ícone Configurações, que abre a tela "Central de notificações para empresas do grupo [nome do grupo]" já existente, sem mudança; e ícone Excluir.
- Clique na linha do grupo, fora dos ícones: abre o modal de edição (Requisito 3).
- Excluir abre o alerta *"Deseja excluir o grupo?"* / *"O grupo, a seleção de empresas e a configuração das notificações serão excluídos. Esta ação não pode ser desfeita."*, com os botões Confirmar e Cancelar:
  - Confirmar exclui o grupo, o vínculo com as empresas e a configuração das notificações do grupo; as empresas voltam a seguir a configuração geral e a exclusão fica no log do escritório;
  - Cancelar fecha o alerta sem excluir.
- Observação: para o negócio, a exclusão também poderia apagar os e-mails cadastrados por categoria e por departamento do grupo; a análise de sistemas precisa confirmar se há motivo técnico para mantê-los como é feito atualmente.


**Requisito 3 — Criar e editar grupo em modal**
-

- O botão Novo grupo abre o modal "Criando grupo de notificação"; o clique na linha de um grupo abre o modal "Alterando grupo de notificação", com o nome atual preenchido e as empresas do grupo já marcadas.
- Aviso abaixo do título: *"São listadas apenas as empresas que não pertencem a outro grupo."*
- Campo "Nome do grupo*": obrigatório, com até 255 caracteres; nomes iguais aos de outros grupos são aceitos. Salvar sem o nome segue a validação de campo obrigatório que já existe hoje.
- Grid de empresas, com uma coluna de seleção e a coluna Empresa no formato "código - nome", com filtro na coluna. Lista as empresas que não pertencem a outro grupo e, na edição, também as do próprio grupo, que podem ser desmarcadas.
- Checkbox do cabeçalho: marca ou desmarca todas as empresas da consulta; com filtro aplicado, só as filtradas.
- Abaixo do grid, o contador "[quantidade] Selecionadas" e, quando há ao menos uma empresa selecionada, a opção "Limpar seleção", que desmarca todas.
- Salvar grava o grupo, mesmo sem empresas, e registra a inclusão ou a alteração no log do escritório. A empresa desmarcada volta a seguir a configuração geral.
- Cancelar, ou fechar o modal, descarta as alterações.


**Requisito 4 — Montar a tela Notificações enviadas**
-

- A tela mostra só as notificações do módulo pelo qual foi acessada. O módulo é um filtro fixo e não aparece como campo.
- Abas, conforme o módulo e o escritório:
  - SCI Report 24H e SCI Report Atendimento, em escritório com a versão Gerencial: abas E-mail (Requisito 5) e WhatsApp (Requisito 6). A tela sempre abre na aba E-mail;
  - CND, Alvará, Tarefas e Central de Certificados, e escritório sem a versão Gerencial: só a consulta de e-mail (Requisito 5), sem o indicativo de abas.
- Layout de cada consulta:
  - fieldset informativo no topo, na largura da tela;
  - primeira linha com Empresa, Data inicial envio e Data final envio;
  - segunda linha com os dois filtros da consulta (Requisito 5 ou 6) e os botões Consultar e Limpar.
- Campo Empresa: começa vazio.
- Antes da consulta, o SVG padrão com *"Nada para exibir aqui!"* / *"Informe os dados para visualizar mais informações."*
- Consultar, com ao menos um campo preenchido, exibe o grid com paginação, em ordem decrescente de data e hora de envio. Não há período obrigatório. Quando só uma das datas é informada, a consulta considera apenas aquele dia.
- Exceção — nenhum campo preenchido: *Crítica* — impedir a consulta: *"Preencha pelo menos um dos campos."* / *"Quanto mais filtros informados, mais rápido será o retorno dos resultados da consulta."*, com o botão Confirmar.
- Limpar: apaga os filtros informados.

**Requisito 5 — Consultar os e-mails enviados**
-

- Lista os e-mails efetivamente enviados pelas notificações do módulo de acesso, incluindo os já registrados antes da liberação. E-mails de outros módulos aparecem só no módulo de origem.
- Filtros da segunda linha: Assunto e Destinatário(s).
- Grid com as colunas Empresa, Data e hora envio, Assunto e Destinatário(s). Quando o e-mail não tem empresa, a coluna Empresa mostra *"Nenhuma empresa vinculada a este e-mail"*.
- Fieldset informativo: *"Confira as notificações enviadas por E-mail"* / *"Consulte aqui as mensagens enviadas por e-mail. Caso alguma mensagem não seja localizada, verifique possíveis bloqueios na caixa de entrada ou na pasta de spam."* / *"Se um endereço de e-mail não aparecer na consulta, confira as configurações na Central de Notificações e os e-mails definidos nos parâmetros de notificações."*
- Botão "Ações": com opções 'Relatório PDF' e 'Relatório CSV', para exportar os dados no formato selecionado, com todos os resultados filtrados, e não só a página exibida, e com as mesmas colunas do grid. Exatamente como funciona atualmente.


**Requisito 6 — Consultar os envios de WhatsApp**
-

- Lista os envios de WhatsApp com sucesso das notificações do módulo de acesso (SCI Report 24H ou SCI Report Atendimento), de qualquer integração de WhatsApp, atual ou futura.
- Inclui os envios registrados antes da liberação, desde que o módulo de origem possa ser identificado; o envio antigo sem origem identificada não aparece.
- Filtros da segunda linha: Assunto / Template e WhatsApp.
- Grid com uma linha por número de destino, para todos os destinatários da notificação (empresa, usuários adicionais, usuários adicionais da matriz e responsável pelo atendimento), com as colunas:
  - Empresa: empresa notificada;
  - Data e hora envio: momento em que a SCI enviou a mensagem para a integração, e não a data informada pela Meta;
  - Integração: nome da integração usada no envio;
  - Assunto/Template: nome do template, quando puder ser identificado; vazio quando não puder;
  - WhatsApp: número de destino.
- Fieldset informativo: *"Confira as notificações enviadas por WhatsApp"* / *"Consulte aqui as mensagens enviadas pelo WhatsApp. Caso alguma mensagem não seja localizada, verifique o status e as configurações da integração na Central de Notificações."* / *"Se um contato não aparecer na consulta, confira se o número está configurado corretamente nos parâmetros de notificação."*
- Botão "Ações": com opções 'Relatório PDF' e 'Relatório CSV', para exportar os dados no formato selecionado, com todos os resultados filtrados, e não só a página exibida, e com as mesmas colunas do grid. Exatamente como funciona atualmente.

- Observação: a análise de sistemas avalia se é possível identificar o módulo de origem dos envios antigos pelo texto da mensagem.

**Requisito 7 — Registrar o log interno de WhatsApp no painel de robotizações**
-

- Cada envio de WhatsApp, de qualquer integração, gera um registro no log interno, com o tipo sucesso ou erro e, no erro, o motivo.
- O log guarda as mensagens enviadas, as variáveis utilizadas na mensagem, as alterações realizadas nos templates, as alterações dos números vinculados e as alterações das datas de vínculo.
- A consulta é feita pela SCI na tela Logs do painel de robotizações, com os acessos que ela já tem (administradores do painel) e os filtros que já existem: aplicação, tipo, escritório, situação e período.
- Observação: os dados do log dependem do que a análise de sistemas conseguir receber da api-wasci, mantida por outra equipe.

**Requisito 8 — Fazer a transição do menu "Consultas / E-mails enviados" do SCI Report 24H**
-

- Por 45 dias, contados da liberação da versão em produção para os clientes gerais, o menu "Consultas / E-mails enviados" continua no SCI Report 24H, mas só como acesso: a consulta antiga não abre mais.
- A cada acesso, o menu exibe o alerta *"Esta consulta será descontinuada."* / *"A consulta de e-mails enviados será desativada através desta opção, em breve. Acesse as notificações enviadas, através do novo caminho: Central de Notificações > Notificações enviadas > E-mail."*, com o botão Confirmar. Confirmar leva para a tela Notificações enviadas, na aba E-mail (Requisito 4).
- Ao fim dos 45 dias, o menu e a permissão "Consultas / E-mails enviados" saem automaticamente; se isso não for viável, saem na primeira versão liberada após o prazo.
- Observação: a análise de sistemas avalia a viabilidade da saída automática.

Critérios de aceite e casos de teste
-

| | Req. | Cenário | Resultado esperado |
|---|---|---|---|
| ☐ | 1 | Usuário principal abre "Central de notificações" em qualquer um dos seis módulos administradores e entra em Geral e em Grupos de notificação | Submenus Geral, Grupos de notificação e Notificações enviadas, nessa ordem; Geral abre os dados gerais; Grupos de notificação abre Grupos de empresas |
| ☐ | 1 | Usuário adicional com "Central de notificações" liberado, em módulo diferente do SCI Report 24H, logo após a liberação | Geral e Grupos de notificação acessíveis; Notificações enviadas desabilitado |
| ☐ | 1 | No SCI Report 24H, usuário adicional com "Consultas / E-mails enviados" liberado e "Central de notificações" bloqueado | Só Notificações enviadas acessível |
| ☐ | 1 | No SCI Report 24H, usuário adicional sem "Consultas / E-mails enviados" liberado | Notificações enviadas desabilitado |
| ☐ | 1 | Durante os 45 dias, o administrador bloqueia "Notificações enviadas" de um usuário adicional e depois libera "Consultas / E-mails enviados" | Após o bloqueio, as duas permissões bloqueadas; após a liberação, as duas liberadas |
| ☐ | 1 | Usuário sai da tela de dados gerais e, depois, da configuração de um grupo | Volta para Geral e, depois, para Grupos de empresas |
| ☐ | 2 | Escritório com grupos de uma empresa, de várias empresas e sem empresas | Coluna Empresas com "1 empresa", com a quantidade seguida de "empresas" e com "-"; ícones Configurações e Excluir em cada linha; grupos ocultos ausentes |
| ☐ | 2 | Usuário clica em Configurações de um grupo | Abre a tela de configuração do grupo com o nome do grupo |
| ☐ | 2 | Usuário clica na linha de um grupo, fora dos ícones | Abre o modal de edição do grupo |
| ☐ | 2 | Usuário clica em Excluir e depois em Cancelar | Alerta de exclusão com Confirmar e Cancelar; o grupo continua no grid |
| ☐ | 2 | Usuário exclui um grupo com empresas e confirma | Grupo sai do grid; as empresas passam a seguir a configuração geral; exclusão no log do escritório |
| ☐ | 3 | Usuário clica em Novo grupo, informa o nome, marca empresas e salva | Modal "Criando grupo de notificação" com o aviso; grid só com empresas sem grupo; contador com a quantidade marcada e "Limpar seleção"; grupo novo no grid com a quantidade de empresas; inclusão no log |
| ☐ | 3 | Usuário edita um grupo com empresas, desmarca uma e salva | Modal "Alterando grupo de notificação" com o nome atual e as empresas do grupo marcadas; a empresa desmarcada passa a seguir a configuração geral; alteração no log |
| ☐ | 3 | Empresa já vinculada a outro grupo | Não aparece no grid do modal |
| ☐ | 3 | Usuário aplica filtro na coluna Empresa e marca o checkbox do cabeçalho | Só as empresas filtradas ficam marcadas |
| ☐ | 3 | Nenhuma empresa selecionada, e o usuário salva | Contador "0 Selecionadas", sem "Limpar seleção"; grupo gravado sem empresas, com "-" na coluna Empresas |
| ☐ | 3 | Usuário salva com o nome do grupo vazio | Grupo não gravado; validação de campo obrigatório |
| ☐ | 3 | Usuário informa um nome com 255 caracteres e depois um nome igual ao de outro grupo | Os dois nomes são aceitos e os grupos gravados |
| ☐ | 3 | Usuário altera o nome e as empresas e clica em Cancelar ou fecha o modal | Nenhuma alteração gravada |
| ☐ | 4 | No SCI Report 24H ou no Atendimento, escritório com a versão Gerencial, usuário abre Notificações enviadas | Abas E-mail e WhatsApp, com a aba E-mail selecionada; fieldset no topo; Empresa vazio; SVG "Nada para exibir aqui!" |
| ☐ | 4 | Usuário abre Notificações enviadas no CND, no Alvará, no Tarefas ou na Central de Certificados, e no SCI Report 24H em escritório sem a versão Gerencial | Só a consulta de e-mail, sem indicativo de abas |
| ☐ | 4 | Usuário clica em Consultar sem preencher nenhum campo | Consulta não realizada; alerta *"Preencha pelo menos um dos campos."* / *"Quanto mais filtros informados, mais rápido será o retorno dos resultados da consulta."* com Confirmar |
| ☐ | 4 | Usuário informa só a Data inicial envio e consulta | Grid só com envios do dia informado, em ordem decrescente de data e hora |
| ☐ | 4 | Consulta com mais resultados que uma página; o usuário gera Relatório PDF e Relatório CSV e depois clica em Limpar | Os dois relatórios com todos os resultados filtrados e as colunas do grid; filtros vazios após Limpar |
| ☐ | 5 | Módulo com e-mails enviados antes e depois da liberação, consulta por período que cobre os dois | Grid com Empresa, Data e hora envio, Assunto e Destinatário(s), com os e-mails dos dois períodos, só do módulo de acesso |
| ☐ | 5 | E-mail enviado sem empresa vinculada | Coluna Empresa com a mensagem de e-mail sem empresa vinculada |
| ☐ | 5 | No período existem e-mails de outro módulo e e-mails com falha de envio | Nenhum deles aparece; o e-mail do outro módulo aparece na consulta do módulo de origem |
| ☐ | 5 | Usuário filtra por Assunto e por Destinatário(s) | Grid só com os e-mails correspondentes |
| ☐ | 6 | Notificação enviada com sucesso para a empresa e para dois usuários adicionais, consultada no módulo de origem | Uma linha por número; Empresa com a empresa notificada; Data e hora envio do envio pela SCI; Integração com o nome da integração usada; WhatsApp com cada número |
| ☐ | 6 | Um envio com template identificável e outro sem template identificável | Assunto/Template com o nome do template no primeiro; vazio no segundo |
| ☐ | 6 | Envio com falha e envio do Atendimento consultado no SCI Report 24H | Nenhum dos dois aparece |
| ☐ | 6 | Envios anteriores à liberação, um com módulo de origem identificado e outro sem | Só o envio com origem identificada aparece, e no seu módulo |
| ☐ | 6 | Usuário filtra por um número de WhatsApp | Grid só com os envios para esse número |
| ☐ | 7 | Um envio de WhatsApp com sucesso e outro com erro | Tela Logs do painel com os dois registros, o de erro com o motivo; filtráveis por aplicação, tipo, escritório, situação e período |
| ☐ | 7 | Alteração em um template, em um número vinculado e em uma data de vínculo | As três alterações registradas no log interno |
| ☐ | 7 | Usuário do painel de robotizações sem perfil de administrador | Não acessa a tela Logs |
| ☐ | 8 | Dentro dos 45 dias, usuário com acesso clica em "Consultas / E-mails enviados" e confirma | Alerta de descontinuação; após Confirmar, tela Notificações enviadas na aba E-mail; a consulta antiga não abre |
| ☐ | 8 | Usuário acessa o menu antigo pela segunda vez | Alerta exibido de novo |
| ☐ | 8 | No 45º dia e depois do fim do prazo | No 45º dia, menu antigo presente; depois do prazo, menu e permissão "Consultas / E-mails enviados" ausentes |




**RNF 1 — Adaptar a tela Notificações enviadas a telas menores**
-

- Em telas menores, como a de celular, os elementos visuais precisam se ajustar harmoniosamente, como por exemplo na telas de consulta onde os filtros ficam um abaixo do outro, com Data inicial envio e Data final envio lado a lado, e os botões Consultar e Limpar abaixo dos filtros, como no protótipo.

Critérios de aceite dos requisitos não funcionais
-

| | RNF | Cenário | Resultado esperado |
|---|---|---|---|
| ☐ | 1 | Usuário abre telas e modais da criadas nesta análise em tela de celular | Os elementos visuais se organizam de forma harmoniosa e sem prejudicar sua usabilidade |
| ☐ | 1 | Usuário abre Notificações enviadas em tela de celular | Filtros um abaixo do outro, datas lado a lado e Consultar e Limpar abaixo dos filtros |