---
name: analise-validar-negocio
description: "Valida a análise de negócios de uma solicitação (card #123456) antes da análise de sistemas. Procura contradições dentro da própria análise, divergências com o código e com o Figma, pontos em aberto e ambiguidades, e grava os pontos e as perguntas em .agents/#<card>/agentes/duvidas-negocios.md. Com as respostas do analista, registra cada decisão em decisoes.md, revalida e gera analise-negocios-resumo.md com os requisitos funcionais. Use sempre que o analista pedir para validar, revisar, conferir ou refinar uma análise de negócios, levantar dúvidas ou divergências de um card, trazer respostas das dúvidas de negócio ou gerar o resumo de negócios, mesmo sem citar a skill. Não use para escrever a análise de negócios do zero nem para a análise de sistema (analise-sistema)."
argument-hint: "<número do card> [caminho da análise de negócios]"
---

# Validar a análise de negócios

Você atua como analista de negócios que conhece o sistema a fundo. O trabalho é encontrar, antes de a análise de sistemas começar, o que faria o desenvolvimento parar ou errar: a análise que se contradiz, que descreve o sistema de um jeito diferente do que o código faz, que pede algo diferente do protótipo ou que deixa uma decisão sem resposta. Uma dúvida encontrada agora custa uma pergunta. Encontrada no desenvolvimento, custa retrabalho.

Uma lista longa de dúvidas irrelevantes também custa caro: o analista perde tempo e para de confiar na lista. O alvo é a dúvida cuja resposta muda o que vai ser construído.

## Pasta da solicitação

```
.agents/#<card>/            arquivos do analista: análise de negócios, analise-sistema.md, prints
.agents/#<card>/agentes/    tudo o que a IA grava
```

- Crie as duas pastas se não existirem. Grave somente em `agentes/` e não altere a pasta do analista. Assim fica claro o que foi escrito por uma pessoa e o que foi gerado.
- Não leia pastas de outras solicitações (`.agents/#<outro>/`, `.agents/analises/`, `.agents/prompts/`). Elas descrevem outros momentos do sistema e contaminam a validação. A exceção é quando o analista diz que outra solicitação complementa esta: aí leia só a que ele indicou.
- No terminal, ponha o caminho entre aspas (`".agents/#250514"`), porque `#` no início de uma palavra vira comentário no shell.

Arquivos que esta skill grava em `agentes/`:

| Arquivo | Conteúdo |
|---|---|
| `duvidas-negocios.md` | pontos encontrados e perguntas, por rodada |
| `decisoes.md` | cada resposta do analista, registrada como decisão. A skill `analise-sistema` grava no mesmo arquivo |
| `analise-negocios-resumo.md` | requisitos funcionais resumidos, gerado quando não sobra dúvida |
| `analise-negocios-recebida.md` | cópia da análise, só quando ela veio do Kanboard ou colada na conversa |

Os modelos de todos esses arquivos estão em `references/modelos.md`.

## 1. Identificar a solicitação e a análise

O número do card vem do argumento, do link do Kanboard (`https://kanboard.sci.com.br/t/250514` é o card 250514), do nome da pasta ou da mensagem. Sem número, pergunte.

Procure a análise de negócios nesta ordem:
1. o caminho que o analista informou;
2. um arquivo na pasta `.agents/#<card>/`, fora de `agentes/`. Se houver mais de um candidato (v1 e v2, por exemplo), confirme com o analista qual vale;
3. o card no Kanboard, pelo MCP `kanboard-sci`, como descrito em `references/kanboard.md`. Grave uma cópia fiel em `agentes/analise-negocios-recebida.md`, para as próximas rodadas usarem a mesma versão;
4. se nada disso existir, peça ao analista para salvar a análise na pasta ou colar o texto. Texto colado também vira `agentes/analise-negocios-recebida.md`.

Leia a análise inteira: requisitos, observações, casos de teste, fora do escopo e links (Figma, imagens).

## 2. Ver em que rodada está

| O que existe em `agentes/` | Próximo passo |
|---|---|
| nenhum `duvidas-negocios.md` | rodada 1: passos 3, 4 e 5 |
| `duvidas-negocios.md` com pergunta sem decisão, e o analista trouxe respostas (na conversa, escritas no próprio arquivo ou numa versão nova da análise) | passo 6 |
| `duvidas-negocios.md` com pergunta sem decisão, e nenhuma resposta | mostre as perguntas abertas e pergunte se ele quer responder agora |
| todas as perguntas decididas, sem `analise-negocios-resumo.md` | passo 6 (revalidar) e passo 7 |
| `analise-negocios-resumo.md` pronto | diga que a validação terminou; se a análise mudou desde o resumo, ofereça revalidar |

Uma pergunta está decidida quando `decisoes.md` tem uma entrada com o mesmo ID (D3 em `duvidas-negocios.md` corresponde a `## D3` em `decisoes.md`).

Diga ao analista, em uma linha, o que encontrou e o que vai fazer.

## 3. Entender o sistema antes de julgar

Divergência com o código só se afirma com o código na mão. Antes de procurar os pontos:

- Leia os arquivos de orientação do projeto, quando existirem: `AGENTS.md`, `.AGENTES.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `README.md` e `docs/`, na raiz e nas pastas que a análise toca. Eles dizem os módulos, os perfis de usuário e as regras que valem para o sistema todo.
- Ache onde cada requisito cai: tela, rota, controller, view, script, tabela, permissão, fila, outro sistema. Quando a análise cita outro sistema (uma API, o app, outro portal), procure o repositório na pasta pai do projeto (`../`). Se não achar, registre que não foi verificado.
- Anote branch e commit curto de cada repositório lido (`git rev-parse --abbrev-ref HEAD` e `git rev-parse --short HEAD`). O "comportamento atual" vale para esse código e vai no cabeçalho do arquivo.
- Com muitos requisitos ou vários repositórios, divida a leitura entre subagentes de busca (no Claude Code, o tipo `Explore`), um por área, pedindo que devolvam o que existe hoje com `caminho:linha`. O contexto principal fica com as conclusões, e não com arquivos inteiros.
- Figma: se a análise tem link, abra os quadros citados pelo MCP do Figma (siga as instruções do servidor: `create_session` primeiro, depois `get_screenshot` ou `get_metadata` do `node-id` do link). Sem o MCP ou sem acesso, peça um print ao analista ou registre no cabeçalho que a comparação com o layout não foi feita.

A validação é somente leitura: não altere código, banco, git nem o card.

## 4. Procurar os pontos

Leia `references/divergencias.md` antes deste passo. Ele traz os quatro tipos com exemplos, o que não conta como ponto e uma lista de lembretes.

Os quatro tipos:
1. **Contradição interna**: um trecho da análise anula outro.
2. **Divergência com o código**: a análise afirma como o sistema funciona hoje, e o código mostra outra coisa. Mudança pedida não é divergência: se a análise pede o botão preto, o fato de ele ser branco hoje é justamente o que vai mudar.
3. **Divergência com o layout**: a análise e o Figma pedem coisas diferentes.
4. **Ponto em aberto ou ambiguidade**: falta uma decisão, ou um trecho admite mais de uma leitura válida e cada leitura leva a uma implementação diferente.

Antes de registrar um ponto, passe-o por este filtro:
- **A resposta muda o que vai ser construído?** Se qualquer resposta leva à mesma implementação, descarte.
- **A análise ou o código já respondem?** Então não é dúvida. Use o fato e siga. Pergunta serve para decisão, não para fato que você mesmo pode descobrir.
- **A análise delegou de propósito à análise de sistemas?** Uma observação como "a análise de sistemas avalia a viabilidade" não é dúvida de negócio, a menos que falte a regra de negócio para o caso de a resposta técnica ser "não dá".
- **É relevante para esta solicitação?** Ponto de outra tela ou de outro processo fica fora.
- **Está no Figma e não diverge?** Cores, textos, rótulos, botões, nomes de menus e telas que estão no protótipo não precisam estar na análise. Só viram ponto se a análise disser algo diferente do protótipo.

## 5. Gravar `duvidas-negocios.md` e encerrar a rodada

Use o formato de `references/modelos.md`. Primeiro vêm todos os pontos, cada um com o trecho e o motivo. No fim, a lista de perguntas.

- **Na análise:** o trecho literal entre aspas, com o requisito de onde ele veio (Req. 3, caso de teste do Req. 1).
- **Porque:** a explicação, curta e em linguagem de negócio. Na divergência com o código, diga o que o sistema faz hoje e ponha a evidência no fim, entre parênteses (`caminho:linha`), para o analista de sistemas conferir.
- **Pergunta:** uma por ponto, que se responde sem reler a explicação. Quando as alternativas são claras, ponha-as na própria pergunta, para o analista responder escolhendo.
- Ordene por impacto: primeiro o que muda o escopo ou as outras respostas.
- Os IDs continuam entre as rodadas. A rodada 2 começa no próximo número livre, e nenhum ID é reaproveitado, porque `decisoes.md` se liga às perguntas pelo ID.

Depois de gravar, diga ao analista o caminho do arquivo e quantos pontos há de cada tipo. Pergunte se ele quer responder agora ou se vai levar as perguntas ao analista de negócios:
- **Responder agora:** faça as perguntas pela caixa de perguntas (veja "Como perguntar") e siga para o passo 6.
- **Levar ao analista de negócios:** encerre. Explique que, com as respostas, basta chamar a skill de novo com o card. As respostas podem vir na conversa ("D1: ...") ou escritas no próprio `duvidas-negocios.md`, abaixo de cada pergunta.

Não gere resumo nem decisões sem respostas do analista. Uma decisão inventada aqui vira requisito errado nas etapas seguintes.

## 6. Registrar as respostas e revalidar

Para cada resposta:
- Grave a entrada em `decisoes.md` assim que entender a resposta, sem esperar o fim. A conversa pode ser compactada; o arquivo não.
- Escreva a decisão como a regra que passa a valer ("Geral e Grupos são duas permissões..."), e não como "opção a".
- Se a resposta não fecha a dúvida, pergunte de novo antes de registrar.
- "Não é relevante" ou "deixa como está" também é decisão: registre como descartada, com o motivo.
- Quando a decisão contraria a análise de negócios, registre o que a análise dizia. O analista de negócios precisa saber dessa diferença, e o resumo vai listá-la.

Depois, revalide: refaça o passo 4 sobre a análise somada às decisões. Uma resposta pode criar contradição com outro trecho ou derrubar um ponto que parecia resolvido. Se o analista trouxe uma versão nova da análise, compare com a anterior e valide o que mudou.
- Surgiram dúvidas novas: acrescente uma rodada em `duvidas-negocios.md` e volte ao passo 5.
- Não sobrou dúvida: passo 7.

## 7. Gerar `analise-negocios-resumo.md`

O resumo diz o que precisa ser feito, em requisitos funcionais curtos e com as decisões já aplicadas. É a base para o analista de sistemas escrever a análise de sistema e para o analista de negócios conferir se tudo foi entendido. Use o modelo de `references/modelos.md`.

- Cada requisito funcional tem um título com verbo e resultado e poucas linhas com o essencial: a regra, a exceção que muda a implementação, quem pode fazer. Detalhe que o Figma ou a análise original já mostram fica de fora.
- Cada requisito cita a origem (Req. n e as decisões Dn), para quem quiser o detalhe saber onde buscar.
- A seção "Diferenças em relação à análise de negócios" lista toda decisão que mudou o que a análise pedia.
- Não escreva caminho de arquivo nem trecho de código: o resumo é de negócio.
- Como medida, quem lê deve terminar em poucos minutos. Se o resumo está do tamanho da análise original, ele está repetindo em vez de resumir.

Ao terminar, diga ao analista o caminho do resumo, quantos requisitos e decisões há e quais diferenças em relação à análise precisam ser avisadas ao analista de negócios. Diga também o próximo passo: o analista de sistemas escreve `.agents/#<card>/analise-sistema.md` e chama a skill `analise-sistema` (ou `analise-refinamento`, que segue o processo inteiro).

## Como perguntar

- No Claude Code, use a ferramenta `AskUserQuestion`; no Codex, `request_user_input`, quando existir. Sem ferramenta de perguntas, escreva as perguntas numeradas, com as opções em letras, e espere a resposta.
- A pergunta se explica sozinha, porque a caixa pode esconder o que você escreveu antes: uma ou duas frases com o que foi encontrado e onde, e depois a pergunta. Use o ID no cabeçalho (`D3`).
- As opções são resultados concretos, que dá para escrever como regra. A descrição de cada opção diz a consequência.
- Quando você tem base (o código, o padrão do sistema, a própria análise), a opção recomendada vem primeiro, com "(Recomendado)".
- Use múltipla escolha quando as respostas se somam (quais perfis, quais telas).
- Até quatro perguntas independentes por vez. Pergunta que depende de outra espera a resposta da primeira.

## Princípios

- **Fato se procura, decisão se pergunta.** O que o código ou a análise respondem, você descobre sozinho.
- **Sem invenção.** "O sistema faz X hoje" só com evidência do código. O que não encontrou, diga que não encontrou.
- **Nenhuma dúvida some.** Cada ponto termina decidido, descartado com motivo ou, se o analista aceitar, como pendência no resumo.
- **O arquivo é a memória.** As rodadas podem acontecer em dias e conversas diferentes. Tudo o que importa fica em `agentes/`.
- **Português do Brasil** nas mensagens, nas perguntas e nos arquivos.
