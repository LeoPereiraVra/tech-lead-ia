# Análise do código: lacunas e divergências

A análise de negócio descreve o que se quer; o código mostra o que existe. As lacunas mais caras aparecem quando os dois se encontram: "remover o botão Sair", quando ele é a única forma de sair do sistema. Este guia diz onde olhar e o que procurar.

## Antes de procurar

1. **Leia a orientação do projeto:** `AGENTS.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `README.md` e `docs/`, quando existirem. Eles dizem os módulos, os perfis de usuário, as regras críticas (no sci-web, por exemplo, toda consulta filtra pelo escritório/empresa da sessão) e onde ficam telas, rotas e APIs.
2. **Ache os projetos citados.** A solicitação pode tocar outro repositório (uma API, o app, outro portal). Procure pelo nome citado na pasta pai do projeto atual, onde ficam os repositórios irmãos. Se não achar, pergunte o caminho ao usuário. Leia também o `AGENTS.md`/`CLAUDE.md` de cada projeto envolvido.
3. **Anote a referência:** branch e commit curto (`git rev-parse --abbrev-ref HEAD` e `git rev-parse --short HEAD`) de cada repositório. O "comportamento atual" descrito vale para esse código.

## Mapear requisito → código

Para cada requisito, ache onde ele cai: tela (view), rota, controller, script JS, endpoint de API, tabela, permissão, configuração. Quando a varredura for larga (vários requisitos ou vários projetos) e houver subagentes (no Claude Code, o tipo `Explore`), divida por área e rode em paralelo, pedindo que cada um devolva o que existe hoje com `caminho:linha`. Assim o contexto principal fica com as conclusões, não com os arquivos inteiros.

## O que procurar

| Tipo | Pergunta-guia | Exemplo |
|---|---|---|
| Remoção sem substituto | O que sai é a única forma de fazer algo? | remover "Sair" do menu sem outro botão de sair; remover o rodapé que exibe o aviso de cookies |
| Referência inexistente | A tela, o campo, o botão ou o endpoint citado existe com esse nome e nesse lugar? | "lista do cliente" aponta para uma tela do administrador |
| Regra atual ignorada | O código tem regra (permissão, licença, módulo contratado, ambiente, status) que a análise não cita ou contradiz? | ação que hoje só aparece para guia de imposto |
| Perfil não coberto | Quais perfis usam a tela hoje? A análise cobre todos? | a análise fala da empresa, mas o colaborador também acessa |
| Impacto em outro lugar | Quem mais usa o componente, a tela ou o endpoint que vai mudar? | endpoint usado pela lista do escritório e pela da empresa |
| Dado inexistente | O dado que a análise mostra existe no banco ou na API? Dá para calcular? | "último contrato acessado" não é gravado |
| Estados e limites | Vazio, erro, carregando, paginação, limite, sessão expirada, sem permissão | lista sem itens; API fora do ar |
| Dados que já existem | O que acontece com registros gravados, preferências salvas, links antigos? | filtros salvos no navegador no formato antigo |
| Variações de acesso | App, celular, modal/iframe, telas sem cabeçalho, acesso pela URL direta | tela aberta dentro do app, sem menu |
| Isolamento | A consulta nova continua filtrada pelo cliente/empresa da sessão? | totalizador que somaria outras empresas |

A tabela serve para lembrar, não para gerar pontos. Só vira ponto o que tem relação com a solicitação.

## Evidência

- Todo "o sistema faz X hoje" vem com `caminho:linha`. Sem evidência, escreva "não encontrei no código" e trate como dúvida, nunca como fato.
- Em `analise-negocios.md` e `analise-sistemas.md`, a evidência fica no ponto levantado. No arquivo final do dev, entram só os caminhos que ajudam a localizar onde trabalhar.

## Limites

- **Somente leitura:** não altere código, não rode migrações nem comandos que mudem estado, não faça commit. Grave só na pasta da solicitação.
- **Comportamento, não implementação:** o objetivo é entender o que o sistema faz e o que a mudança atinge. Como implementar fica com quem desenvolve; registre só o que for restrição ou risco.
