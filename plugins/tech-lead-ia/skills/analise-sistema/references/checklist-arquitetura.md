# Checklist de arquitetura e tradeoffs

Use para olhar a proposta com os olhos de quem vai manter o sistema. Cada linha é uma pergunta, e não uma obrigação: só vira ponto ou requisito o que a solicitação toca. Uma análise final que lista todas as categorias "por garantia" fica longa e esconde o que importa.

## Como pesar um tradeoff

Para cada decisão estrutural, responda em poucas linhas:
- **Escolha:** o que a proposta faz.
- **Alternativa:** a outra forma razoável de fazer.
- **Ganho e custo:** o que cada uma resolve e o que cobra (complexidade, desempenho, acoplamento, prazo, risco de regressão).
- **Quando revisitar:** o sinal de que a escolha deixou de servir (volume, número de módulos, outra integração).

Se a proposta do analista é a mais simples que atende, diga isso e siga. Se tem um risco que ele talvez não tenha visto, vira pergunta, com as alternativas.

## Estrutura e reaproveitamento

- Existe funcionalidade parecida no projeto? A proposta segue o mesmo padrão (camadas, componentes, nomes)? Se foge, há motivo?
- A regra fica num lugar só ou vai ser repetida por módulo, por tela ou por sistema? Repetição vira divergência no primeiro ajuste.
- Componentes compartilhados (grid, modal, alerta, exportação, upload) são reaproveitados ou duplicados?
- A responsabilidade está na camada certa (controller fino, regra em biblioteca ou serviço, acesso a dados no modelo)?
- Quando vários módulos ganham a mesma tela, é uma implementação parametrizada pelo módulo ou várias cópias?

## Dados

- Tabelas, colunas e índices novos: o nome e o tipo seguem o padrão do banco? Os filtros novos têm índice?
- Dados já gravados: precisam de carga inicial, conversão ou valor padrão? O que acontece com registros antigos que não têm o dado novo?
- Scripts de banco: o projeto versiona migrações ou usa script manual? Em qual banco ou esquema? Em que ordem rodam em relação ao deploy?
- Dá para reverter? O que acontece se o script rodar e o deploy voltar?
- Outros sistemas leem ou gravam as mesmas tabelas? Continuam funcionando com a mudança?

## Segurança

- Isolamento por cliente: toda consulta e toda gravação filtram pelo escritório ou empresa da sessão, inclusive JSON, exportações e ações por ID vindo da requisição?
- Permissão: a tela, os endpoints de dados, as ações e as exportações conferem a mesma permissão, inclusive em acesso pela URL direta?
- SQL: valores da requisição só entram por binding? A ordenação e os filtros por coluna usam uma lista permitida?
- Segredos e dados pessoais: logs, exportações e mensagens de erro não expõem token, chave, senha nem mais dado pessoal (telefone, e-mail, CPF) do que o necessário?
- Entrada do usuário: limite de tamanho, tipo e formato validados no servidor, e não só na tela.

## Desempenho e escalabilidade

- Volume: quantos registros a consulta lê hoje e em um ano? Tabelas de log crescem sem limite.
- Paginação e filtros no servidor? A consulta sem filtro é barrada ou limitada?
- Exportação de "todos os resultados": cabe em memória? Precisa de limite, processamento em fila ou geração em partes?
- Consultas dentro de laço (N+1), chamadas externas síncronas na requisição do usuário, tempo limite de integrações.
- Sessão e cache: o que fica guardado na sessão (menus, permissões) só muda no próximo login? Isso é aceitável na liberação?

## Compatibilidade e impacto

- Quem mais usa a tela, o endpoint, o componente ou a tabela que vai mudar? Outros módulos, o app, outros portais, integrações.
- Links e caminhos fixos no código que apontam para o que muda (redirecionamentos, views, menus no banco).
- Permissões e menus existentes: o que acontece com quem já tem acesso hoje no dia da liberação?
- Funcionalidade que depende de outra solicitação ainda não entregue.

## Manutenção

- Um dev novo entende onde está cada parte da regra? Nomes dizem o que fazem?
- A solução cria um caso especial que vai precisar ser lembrado (um `if` por módulo, um id fixo no código)?
- Há como testar a regra sem subir o sistema inteiro? Existem testes no projeto que precisam ser atualizados?
- Código morto ou duplicado que a mudança deixa para trás, e que deveria sair junto.

## Observabilidade e operação

- Falhas relevantes ficam registradas com contexto suficiente para investigar, sem dado sensível?
- A falha de um componente auxiliar (log, notificação, integração) não derruba a operação principal?
- Dependências de outra equipe (infraestrutura, coleta de logs, outra API): o que precisa estar pronto, em qual ambiente, antes do quê?
- Ordem de deploy entre sistemas, scripts manuais e configurações por ambiente (HML e produção).

## Usabilidade técnica

- Telas novas funcionam no celular e em telas pequenas sem rolagem horizontal da página?
- Estados de carregamento, vazio e erro estão tratados nas chamadas assíncronas?
