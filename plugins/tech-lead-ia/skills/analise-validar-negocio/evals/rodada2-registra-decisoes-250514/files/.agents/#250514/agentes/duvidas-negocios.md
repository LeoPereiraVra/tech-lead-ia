# #250514 — Dúvidas da análise de negócios

> Análise: .agents/#250514/analise-negocios.md, lida em 10/11/2026. Código: sci-web main@a4a06163f, area-do-cliente master, sci-fila-email, cnd-painel-admin, api-atendimento. Figma: não verificado (sem acesso ao MCP do Figma na sessão).

## Rodada 1 — 10/11/2026

### Dúvidas análise de negócios

D1:
Tipo: Ambiguidade
Na análise: "Geral e Grupos de notificação herdam a liberação atual de 'Central de notificações' no módulo" (Req. 1)
Porque: o texto não deixa claro se são uma permissão ou duas, nem se "herdar" quer dizer copiar o valor uma vez ou depender do pai para sempre. O caso de teste "Consultas / E-mails enviados liberado e Central de notificações bloqueado → só Notificações enviadas acessível" só funciona se o pai for só um agrupador, porque hoje o submenu só aparece com o pai liberado. (app/lib/Base/MenuAdmin.php:46-66; area-do-cliente/modulo/usuarioAdicional/permissoes/scireport/form.php:709-753)

D2:
Tipo: Divergência com o código
Na análise: "O log guarda as mensagens enviadas, as variáveis utilizadas na mensagem, as alterações realizadas nos templates, as alterações dos números vinculados e as alterações das datas de vínculo." (Req. 7)
Porque: o sistema não tem tela nem rotina que altere templates ou "datas de vínculo"; os templates só existem cadastrados à mão na integração. Além disso, a tela Logs do painel só recebe registros de requisições da api-atendimento, e os envios de WhatsApp saem do sci-fila-email, que não grava nesse log. (cnd-painel-admin/config/athena.php:77-79; api-atendimento/app/Http/Middleware/FirehoseRequestLogger.php:18-62)

D3:
Tipo: Ponto em aberto
Na análise: "Lista os e-mails efetivamente enviados pelas notificações do módulo de acesso [...] E-mails de outros módulos aparecem só no módulo de origem." (Req. 5)
Porque: a fila de e-mail também guarda e-mails de senha, backup e cadastro, que não são de nenhum dos seis módulos. Com a regra "só do módulo de acesso", eles sumiriam da única consulta que existe hoje, a do 24H. (app/controller/admin/Relatorio/Consulta/Email.php:64-73)

D4:
Tipo: Ponto em aberto
Na análise: "Quando o e-mail não tem empresa, a coluna Empresa mostra 'Nenhuma empresa vinculada a este e-mail'." (Req. 5)
Porque: vários envios de uma empresa só são gravados sem a empresa (aviso de visualização, 2ª via, solicitação de CND, e-mails de Tarefas). Nesses módulos, boa parte dos e-mails vai aparecer sem empresa e não será encontrada pelo filtro Empresa. (app/lib/Relatorio/Publicado.php:504; app/lib/Tarefa/Tarefa.php:1668-1680)

D5:
Tipo: Ponto em aberto
Na análise: "Campo Empresa: começa vazio." (Req. 4)
Porque: a análise não fala do usuário adicional com acesso a só algumas empresas. Hoje, na consulta do 24H, o campo Empresa lista só as empresas liberadas a ele, mas o grid traz os e-mails de todas as empresas do escritório. (app/controller/admin/Relatorio/Pesquisa.php:30-72; app/controller/admin/Relatorio/Consulta/Email.php:71)

D6:
Tipo: Divergência com o código
Na análise: "Ao fim dos 45 dias, o menu e a permissão 'Consultas / E-mails enviados' saem automaticamente; se isso não for viável, saem na primeira versão liberada após o prazo." (Req. 8)
Porque: não existe menu com data de expiração nem processo que remova menu; os menus ficam só no banco e na sessão até o próximo login. A saída automática exige um mecanismo novo, e a alternativa depende de alguém lembrar da data. (app/lib/Base/MenuAdmin.php; app/controller/admin/Base.php:205-212)

D7:
Tipo: Ambiguidade
Na análise: "Botão 'Ações' [...] com as mesmas colunas do grid. Exatamente como funciona atualmente." (Req. 5)
Porque: hoje a exportação não é igual ao grid. No e-mail sem empresa, o grid mostra "Nenhuma empresa vinculada a este e-mail", e o PDF/CSV mostra " - ". "Mesmas colunas do grid" e "como funciona atualmente" dão resultados diferentes na coluna Empresa. (app/lib/Relatorio/CsvEmail.php:36-43; app/lib/Relatorio/RelatorioEmail.php:118-125)

D8:
Tipo: Ponto em aberto
Na análise: "Salvar grava o grupo, mesmo sem empresas, e registra a inclusão ou a alteração no log do escritório." (Req. 3)
Porque: hoje a alteração do grupo só vai para o log quando as empresas mudam; trocar só o nome não gera registro. Não está claro se "a alteração" inclui a troca só do nome. (app/lib/SciReport/CentralNotificacao.php:895)

Dúvidas:
D1: Geral e Grupos de notificação são uma permissão ou duas? E, depois da liberação, (a) cada uma é independente e "Central de notificações" só agrupa, ou (b) bloquear a Central bloqueia as duas?
D2: Já que templates e datas de vínculo não são alterados no sistema, o log interno registra só os envios (sucesso e erro), a troca de número e a conexão/desconexão? E ele deve aparecer na tela Logs do painel, como a api-atendimento?
D3: Os e-mails de senha, backup e cadastro, que hoje aparecem na consulta do 24H, continuam aparecendo no 24H ou deixam de aparecer?
D4: Os e-mails gravados sem empresa seguem como hoje (sem empresa e fora do filtro Empresa) ou os envios passam a gravar a empresa nesta solicitação?
D5: O usuário adicional com acesso a só algumas empresas vê os envios de todas as empresas do escritório, como hoje, ou só os das empresas liberadas a ele?
D6: Sem mecanismo de expiração, o menu antigo sai (a) com um mecanismo novo de data, (b) manualmente na primeira versão após o prazo, ou (c) numa versão futura, sem prazo definido?
D7: Na coluna Empresa do PDF e do CSV, o e-mail sem empresa sai com "Nenhuma empresa vinculada a este e-mail", igual ao grid, ou com " - ", como hoje?
D8: Trocar só o nome do grupo também deve gerar registro no log do escritório?
