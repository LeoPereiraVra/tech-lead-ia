# #<card> — <título da solicitação>

> Análise de negócio: <caminho do arquivo, link do card ou "texto informado na conversa">. Código analisado: <repositório> <branch>@<commit curto>. Data: <dd/mm/aaaa>.

## Contexto

<Duas a quatro frases: o problema que a solicitação resolve e o resultado esperado para quem usa o sistema.>

## O que precisa ser feito

<Organize por área, tela ou funcionalidade. Diga o que é criado, o que muda e o que sai, e o resultado esperado. Sem cores, medidas, fontes ou espaçamentos. Havendo Figma ou protótipo, cite o link e não descreva o layout. Item que depende de pergunta ainda sem resposta leva "(aguarda N-xx)".>

### <Área, tela ou funcionalidade>

- <o que fazer e o resultado esperado> (Req. <n>)

## Fora do escopo

- <item> — <motivo dado pela análise>

## Impactos no sistema

<Para o analista de sistemas: telas, componentes, endpoints e regras atuais que a mudança atinge, com o caminho. Fatos, não solução. Sem impactos além das telas citadas, escreva "Nenhum além das telas citadas.">

- <o que é atingido e por quê> (`<caminho>`)

## Perguntas para o analista de negócio

<Só os pontos que o usuário mandou perguntar. Cada pergunta se explica sozinha, porque quem responde não tem o código à mão. Sem perguntas, escreva "Nenhuma.">

1. **N-xx — <assunto>.** <O que a análise diz e, se for divergência, o que o sistema faz hoje, em termos de tela e perfil.> <Pergunta?> Sugestões: <resposta possível>; <outra resposta possível>.

## Pontos levantados

| # | Tipo | Assunto | Situação |
|---|---|---|---|
| N-01 | <tipo> | <assunto> | <situação> |

### N-01 — <assunto>

- **Tipo:** <Lacuna na análise | Divergência na análise | Lacuna com o sistema | Divergência com o sistema>
- **Onde:** <Req. n, caso de teste, imagem; `caminho/arquivo:linha`>
- **O que foi encontrado:** <o fato, com a evidência>
- **Por que importa:** <o que fica indefinido ou quebra se ninguém decidir>
- **Situação:** <Perguntar ao analista | Respondido pelo usuário | Respondido pelo analista | Resolvido pelo código | Descartado>
- **Resposta:** <resposta do usuário ou do analista, conclusão tirada do código ou motivo do descarte; "—" enquanto aguarda o analista>
