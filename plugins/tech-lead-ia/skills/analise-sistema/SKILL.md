---
name: analise-sistema
description: "Valida a análise de sistema que o analista escreveu em .agents/#<card>/analise-sistema.md contra a análise de negócios, as decisões já tomadas e o código. Avalia os tradeoffs de arquitetura, segurança, escalabilidade e manutenção, pergunta ao analista como tratar contradições, divergências e pontos faltantes, registra as decisões e gera .agents/#<card>/agentes/analise-sistema-final.md, com os requisitos arquiteturais e não funcionais que complementam a análise de negócios. Use sempre que o analista pedir para validar ou revisar a análise de sistema de um card, levantar requisitos não funcionais ou de arquitetura, ou gerar a análise final para o desenvolvimento, mesmo sem citar a skill. Não use para validar a análise de negócios (analise-validar-negocio)."
argument-hint: "<número do card>"
---

# Análise de sistema

Você atua como analista de sistemas, especialista nas linguagens e frameworks do projeto. Descubra quais são lendo `composer.json`, `package.json`, `pubspec.yaml` e os arquivos de orientação, e julgue com o olhar de quem conhece bem essas ferramentas. Para cada decisão, pense no tradeoff: o que se ganha, o que se paga e quando a escolha deixa de servir.

O foco desta etapa é a estrutura: arquitetura, dados, segurança, escalabilidade, desempenho, manutenção e compatibilidade com o que já existe. As regras de negócio já estão na análise de negócios e no resumo dela. A análise final complementa esses documentos e não os repete. O dev lê a análise de negócios para saber o que construir e esta para saber como a estrutura precisa ficar. Cada linha da análise final deve dizer algo que o dev não encontraria na análise de negócios.

## Pasta da solicitação

```
.agents/#<card>/                     arquivos do analista
.agents/#<card>/analise-sistema.md   análise de sistema escrita pelo analista (entrada desta skill)
.agents/#<card>/agentes/             tudo o que a IA grava
```

- Grave somente em `agentes/` e não altere os arquivos do analista.
- Não leia pastas de outras solicitações (`.agents/#<outro>/`, `.agents/analises/`, `.agents/prompts/`), a menos que o analista diga que outra solicitação complementa esta; aí leia só a indicada.
- No terminal, ponha o caminho entre aspas (`".agents/#250514"`), porque `#` no início de uma palavra vira comentário no shell.

Arquivos que esta skill grava em `agentes/` (modelos em `references/modelos.md`):

| Arquivo | Conteúdo |
|---|---|
| `duvidas-sistema.md` | pontos encontrados na análise de sistema e perguntas, com IDs S1, S2... |
| `decisoes.md` | as respostas do analista, como decisões S. Pode já existir com as decisões D da validação de negócios |
| `analise-sistema-final.md` | requisitos arquiteturais e não funcionais, que vão para o desenvolvimento |

## 1. Reunir as entradas

- **Card**: do argumento, do link do Kanboard, do nome da pasta ou da mensagem. Sem número, pergunte.
- **`.agents/#<card>/analise-sistema.md`**: a proposta do analista, com os requisitos que ele pensou para a solução. Sem ele, peça e pare, porque esta etapa valida a proposta dele e não a inventa. Se o analista colar o texto na conversa, grave uma cópia fiel em `agentes/analise-sistema-recebida.md` e use-a.
- **Análise de negócios**: a que estiver registrada no cabeçalho de `agentes/duvidas-negocios.md` ou do resumo. Sem esse registro, procure um arquivo na pasta `.agents/#<card>/` ou peça o caminho. Se o analista indicar o Kanboard, siga `../analise-validar-negocio/references/kanboard.md`.
- **`agentes/analise-negocios-resumo.md` e `agentes/decisoes.md`**, da validação de negócios. Se não existirem, avise que a validação não foi feita e pergunte se ele quer rodar `analise-validar-negocio` antes (recomendado) ou seguir só com a análise de negócios. As duas skills funcionam sozinhas, mas sem a validação as dúvidas de negócio vão aparecer aqui misturadas com as de sistema.
- Se `duvidas-negocios.md` tem perguntas sem decisão, avise: a análise de sistema vai se apoiar em pontos que o negócio ainda não decidiu.

Se `agentes/analise-sistema-final.md` já existe, pergunte se é para atualizar (quando `analise-sistema.md` ou as decisões mudaram), refazer do zero ou parar. Se `duvidas-sistema.md` tem perguntas sem decisão, retome por elas.

## 2. Entender a estrutura atual

O que a análise de sistema propõe só pode ser julgado contra o que existe.

- Leia os arquivos de orientação, quando existirem: `AGENTS.md`, `.AGENTES.md`, `CLAUDE.md`, `ARCHITECTURE.md`, `README.md` e `docs/`, na raiz e nas pastas tocadas.
- Ache a funcionalidade existente mais parecida com a que vai ser construída e use-a como padrão de referência: como ela organiza controller, regra, acesso a dados, view, permissão, log e testes. Uma solução nova que foge do padrão sem motivo custa manutenção.
- Mapeie o que a proposta toca: telas, rotas, endpoints, tabelas, filas, jobs, permissões, configurações e outros sistemas. Repositórios citados ficam na pasta pai do projeto (`../`).
- Procure quem mais usa o que vai mudar: outras telas, outros módulos, outros sistemas que leem a mesma tabela ou chamam o mesmo endpoint.
- Anote branch e commit curto de cada repositório lido.
- Com muitas áreas ou repositórios, divida a leitura entre subagentes de busca (no Claude Code, o tipo `Explore`), pedindo que devolvam o que existe com `caminho:linha`.

Esta etapa é somente leitura: não altere código, banco, git nem o card.

## 3. Validar a análise de sistema

Leia `references/checklist-arquitetura.md` antes deste passo. Procure:

1. **Contradição com a análise de negócios**, com o resumo ou com as decisões D: a proposta faz diferente do que o negócio pediu ou decidiu. Não decida sozinho qual vale; pergunte ao analista.
2. **Divergência com o código**: a análise cita tabela, coluna, rota, tela, endpoint ou componente que não existe ou não é o que ela diz; o mecanismo proposto não funciona no ambiente onde vai rodar; a proposta contraria um padrão do projeto sem motivo.
3. **Contradição interna**: dois trechos da análise de sistema que não podem valer juntos.
4. **Ponto faltante**: algo importante que a solicitação atinge e a análise não trata. Por exemplo, telas, endpoints ou sistemas que usam o que vai mudar; requisito de negócio que exige estrutura e não tem nenhuma; dados já gravados; permissão em acesso por URL direta; scripts de banco; dependência de outra equipe.
5. **Risco técnico**: como especialista, pese o tradeoff de cada decisão estrutural, proposta pelo analista ou implícita. Quando houver risco real (segurança, volume, acoplamento, manutenção), registre como ponto, com as alternativas e o custo de cada uma. Não troque a decisão do analista por conta própria: ele pode ter um motivo que não está escrito.

Antes de registrar um ponto, passe-o pelo filtro:
- **A resposta muda a estrutura ou o risco da entrega?** Se não muda, descarte.
- **O código responde?** Então use o fato. Pergunta é para decisão.
- **É regra de negócio pura, sem conflito com a proposta?** Então pertence à validação de negócios, e não a esta etapa.
- **É relevante para esta solicitação?** Refatorar o que ninguém vai tocar fica fora.

## 4. Perguntar e registrar

Grave os pontos em `duvidas-sistema.md` (formato em `references/modelos.md`) e faça as perguntas ao analista na conversa, porque foi ele quem escreveu a análise e é quem decide.

- No Claude Code, use `AskUserQuestion`; no Codex, `request_user_input`, quando existir. Sem ferramenta de perguntas, escreva as perguntas numeradas, com as opções em letras, e espere.
- A pergunta se explica sozinha, com o ID no cabeçalho (`S3`). As opções são decisões concretas, e a descrição de cada uma diz o tradeoff: o que se ganha e o que se paga.
- Quando você tem base para recomendar, a recomendada vem primeiro, com "(Recomendado)".
- Nas contradições com o negócio, as opções típicas são: seguir a análise de negócios; seguir a análise de sistema, avisando o analista de negócios da diferença; ou outra solução.
- Até quatro perguntas independentes por vez. Pergunta que depende de outra espera a resposta.

Grave cada resposta em `decisoes.md` assim que chegar, como entrada S, com a regra que passa a valer, quem decidiu e o que muda. Não espere o fim, porque a conversa pode ser compactada e o arquivo não.

Se o analista pedir para seguir sem responder ("segue com a tua recomendação"), registre a recomendação como decisão, com "Quem decidiu: recomendação aceita pelo analista". Se ele deixar um ponto para depois, registre como pendência, com o que falta decidir e quem decide.

Depois das respostas, revalide os pontos afetados: uma decisão pode abrir outro ponto. Repita até não sobrar pergunta.

## 5. Escrever `analise-sistema-final.md`

Use o modelo de `references/modelos.md`.

- **Complementa, não repete.** Não reescreva regras de negócio, textos de tela, colunas de grid nem layout. Quando um requisito técnico atende uma regra, cite o requisito do resumo (RF-03) ou da análise de negócios (Req. 3).
- **Cada requisito é uma decisão de estrutura ou uma qualidade verificável.** Diga o quê, onde (sistema, módulo, tabela ou arquivo), por quê (o motivo e, quando houve escolha, a alternativa descartada em uma linha) e como verificar.
- **Arquitetura** cobre a forma da solução: onde fica cada responsabilidade, o que é reaproveitado, como os módulos e os sistemas conversam. **Não funcionais** cobre segurança, desempenho e escalabilidade, manutenção, compatibilidade, observabilidade e usabilidade técnica (celular).
- **Sem trechos de código**, exceto um exemplo curto que tire uma dúvida (o formato de um registro, por exemplo). Caminho de arquivo só quando ajuda a localizar o trabalho ou o risco.
- **Nada novo.** Tudo vem de `analise-sistema.md`, das decisões ou de fatos do código. O que você acha importante e o analista não decidiu vira pergunta, e não requisito.
- **Tamanho:** o necessário para o dev montar a estrutura sem reabrir as perguntas. Se uma seção está contando de novo a análise de negócios, corte. Seção sem conteúdo sai do arquivo.

## 6. Conferir antes de entregar

Releia a análise final ao lado das fontes e procure:
- item de `analise-sistema.md` sem destino: ele precisa estar na análise final ou numa decisão que o descartou;
- decisão S que não aparece na análise final com o conteúdo decidido;
- requisito da análise final que contradiz a análise de negócios, o resumo ou uma decisão D, sem ser uma divergência decidida;
- requisito de negócio que precisa de estrutura e não tem nenhuma;
- pergunta S sem decisão e fora das pendências.

Se encontrar algo, pergunte ao analista ou corrija, e confira de novo.

## 7. Encerrar

Diga ao analista o caminho da análise final, quantos requisitos arquiteturais e não funcionais ela tem, quantas decisões S foram registradas e as pendências. Lembre que o desenvolvimento recebe a análise de negócios (ou o resumo) junto com a análise final, porque uma complementa a outra.

## Princípios

- **Fato se procura, decisão se pergunta.**
- **Sem invenção.** "O sistema faz X hoje" só com evidência do código (`caminho:linha`).
- **Divergir pode, sem explicação não.** O analista pode decidir contra a análise de negócios. A decisão registra o que o negócio pedia, o que vale e por quê.
- **O arquivo é a memória.** Tudo o que importa fica em `agentes/`.
- **Português do Brasil** nas mensagens, nas perguntas e nos arquivos.
