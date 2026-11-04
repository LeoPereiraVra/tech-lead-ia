---
name: analise-sistema
description: 'Etapa 2 do refinamento de requisitos. Recebe os requisitos de sistema de uma solicitação (arquivo ou texto do analista) e os confronta com a análise de negócio, com os pontos da etapa 1 e com o código. Pergunta ao usuário como tratar cada lacuna ou divergência e gera dois arquivos. O analise-sistemas.md traz requisitos funcionais e não funcionais, dúvidas e decisões, divergências aceitas e rastreabilidade. O #<card>-analise-final.md é o resumo autossuficiente que vai para o dev. Use quando o usuário passar os requisitos de sistema de um card, pedir para detalhar, levantar ou refinar requisitos depois da análise de negócio, ou pedir o documento para o dev desenvolver.'
argument-hint: '<número do card> <caminho ou texto dos requisitos de sistema>'
---

# Etapa 2 — Análise de sistemas

Os requisitos de sistema dizem como a solicitação vai ser atendida no sistema. Esta etapa os confronta com a análise de negócio, com as dúvidas da etapa 1 e com o código, e resolve com o usuário tudo o que não fecha. No fim, produz dois arquivos: `analise-sistemas.md`, o registro detalhado de requisitos e decisões, e `#<card>-analise-final.md`, o resumo que vai para o dev e que se entende sozinho.

Os recursos comuns ficam na skill irmã, em `<skills>/analise-requisitos/`, onde `<skills>` é a pasta que contém esta skill. Antes de começar, leia por inteiro:
- `references/perguntas.md`
- `references/analise-codigo.md`

## 1. Reunir as entradas

- **Pasta e card**: como na skill `analise-requisitos`.
- **`analise-negocios.md`**, da etapa 1. Se não existir, avise que a etapa 1 não foi feita e pergunte se roda a etapa 1 antes (recomendado) ou se segue só com a análise de negócio. Seguindo sem ela, os pontos `N-xx` não existem e as checagens deles não se aplicam.
- **Análise de negócio original**: o caminho está no cabeçalho de `analise-negocios.md`.
- **Requisitos de sistema**, em arquivo ou texto. Sem eles, peça e espere: esta etapa não começa sem os requisitos do analista de sistemas. Se chegarem como texto, grave uma cópia fiel em `requisitos-sistema.md`, na pasta.
- **Respostas do analista de negócio** às perguntas da etapa 1: podem vir dentro dos requisitos de sistema, numa versão nova da análise, num arquivo à parte ou na conversa. Pergunte se há respostas que ainda não estão em nenhum desses lugares.

Se `analise-sistemas.md` já existe, pergunte: **Atualizar**, **Refazer do zero** ou **Parar**.

## 2. Ler e numerar os requisitos de sistema

Leia tudo até o fim. Separe os requisitos de sistema em trechos com uma demanda cada (`P-01`, `P-02`…), guardando o texto literal. Esses trechos formam a rastreabilidade e garantem que nada do que foi pedido se perca.

## 3. Procurar lacunas e divergências

Faça a mesma busca da etapa 1 (`analise-codigo.md`), agora em quatro frentes:

1. **Requisitos de sistema × análise de negócio**: requisito de negócio sem trecho de sistema que o atenda e fora do "Fora do escopo"; trecho que contradiz a análise; trecho que pede algo que a análise não pede.
2. **Requisitos de sistema × código**: o que é citado existe e serve (tela, endpoint, componente, biblioteca, tabela)? O endpoint devolve os dados necessários? A tela indicada é a do perfil certo? A consulta nova continua isolada por cliente/empresa?
3. **Pontos da etapa 1**: para cada `N-xx` que não foi descartado, veja se já tem resposta (do analista, dos requisitos de sistema ou da triagem). Os que não têm continuam abertos.
4. **Os próprios requisitos de sistema**: contradições, termos vagos ("conforme o Figma" sem link ou sem dizer qual quadro), estados sem definição.

Feche com uma varredura de requisitos implícitos, só nas dimensões que a solicitação toca: isolamento por cliente/empresa e permissões, validação e limites de entrada, falhas (API fora, erro ao salvar, tempo esgotado), dados que já existem, desempenho, compatibilidade com telas que usam o mesmo componente ou endpoint, celular e app, mensagens. Cada dimensão presente vira requisito (em geral um RNF) ou dúvida. Não invente requisito só para preencher a lista.

## 4. Perguntar e só seguir com a resposta

Toda divergência ou lacuna que o código não resolve vai para o usuário, pela caixa de perguntas, seguindo `perguntas.md`. Não escreva requisito sobre um ponto em aberto supondo a resposta.

As opções típicas, quando cabem, são **Seguir a análise de negócio**, **Seguir o requisito de sistema** e **Manter como o sistema faz hoje**, cada uma com a consequência na descrição. Sempre que der, prefira opções que já tragam o resultado concreto (o texto da mensagem, o perfil, o limite).

Para cada `N-xx` ainda sem resposta, pergunte se o analista respondeu. As opções são:
- **Respondeu**: o usuário escreve a resposta em "Outro";
- **Decidir agora**: você oferece as alternativas numa pergunta seguinte;
- **Deixar em aberto**: o ponto vai para Pendências, com a premissa adotada enquanto isso.

Se aparecer na conversa algo que nem a análise de negócio nem os requisitos de sistema pedem, pergunte se entra nesta solicitação (vira divergência aceita) ou fica fora do escopo.

Cada resposta vira uma decisão `D-xx`, gravada assim que chega.

## 5. Registrar a divergência aceita

O usuário pode responder contra a análise de negócio. Isso é aceitável, e o arquivo deixa explícito. Na tabela "Divergências aceitas da análise de negócio" entram o que a análise diz, o que fica valendo, o motivo e quem decidiu. Sem esse registro, a etapa 3 e o dev tratariam a diferença como erro.

## 6. Escrever `analise-sistemas.md`

Use o modelo `assets/analise-sistemas.md` desta skill. Orientações por seção:
- **Objetivo**: um parágrafo com o que existe hoje, o que muda e o resultado para o usuário.
- **Escopo**: o que está incluído e o que fica fora, cada exclusão com motivo e decisão.
- **Comportamento atual**: os fatos do código que o dev precisa conhecer para não quebrar nada, agrupados por assunto e em linguagem de quem usa o sistema.
- **Atores e permissões**: cada perfil e o que ele vê e faz.
- **Requisitos funcionais (RF)**: título com verbo e resultado; regras, dados e exceções; critérios de aceite no formato "Dado…, quando…, então…", com valores concretos (texto exato, número, perfil); origem (`P-xx`, `Req. n`, `N-xx`, `D-xx`). Cada RF é um comportamento que pode ser entregue e conferido sozinho.
- **Requisitos não funcionais (RNF)**: "Categoria: resultado", mensurável, com verificação e origem. O RNF implícito confirmado pelo usuário tem origem "Implícito (confirmado pelo usuário)".
- **Dúvidas e decisões**: é o mapa de dúvidas e respostas das duas etapas. Toda pergunta feita e toda resposta dada entram, com quem decidiu, a origem (`N-xx` ou "etapa de sistema") e os requisitos afetados.
- **Divergências aceitas da análise de negócio**: ver o passo 5.
- **Premissas**: o que foi adotado sem confirmação explícita, com o motivo.
- **Cobertura da análise de negócio**: cada requisito da análise de negócio e o que o atende (RF, RNF, fora do escopo ou divergência aceita).
- **Rastreabilidade dos requisitos de sistema**: cada `P-xx` e o que o atende.
- **Pendências**: "Nenhuma." ou o que ficou em aberto por decisão do usuário, com quem decide.

## 7. Conferência final antes do arquivo do dev

Rode e corrija os ERROs:

```bash
python3 "<skills>/analise-requisitos/scripts/verificar.py" sistema ".agents/analises/#<card>"
```

Depois, releia a análise de negócio original lado a lado com `analise-sistemas.md` e procure:
- requisito ou caso de teste da análise sem destino na cobertura;
- caso de teste da análise que nenhum critério de aceite garante e que não é divergência aceita;
- `N-xx` sem resposta e fora das pendências;
- decisões que se contradizem;
- pendências que impedem o dev de começar.

Se encontrar algo, pergunte ao usuário como seguir, atualize o arquivo e repita a conferência.

## 8. Escrever `#<card>-analise-final.md`

Este é o único arquivo que vai para o dev. Ele não leu nada do que veio antes e não vai receber os outros arquivos. Use o modelo `assets/analise-final.md` desta skill e grave em `.agents/analises/#<card>/#<card>-analise-final.md`.

- **Contexto** vem primeiro: quem usa, o problema de hoje, o que muda, onde (sistema, módulo, tela, perfis) e o que continua igual. Quem lê só essa seção entende a entrega.
- Depois vem uma seção por área, tela ou funcionalidade, com o que fazer: regras, casos, mensagens com o texto exato, permissões, estados (vazio, erro). Só o que foi decidido.
- **Restrições**: as decisões técnicas dos requisitos de sistema (biblioteca, endpoint, isolamento por cliente/empresa, desempenho, compatibilidade).
- **Em aberto**: só quando o usuário aceitou deixar algo para depois; diz o que falta decidir e o que fazer enquanto isso.
- **Fora do escopo**: o que o dev não deve fazer, mesmo que pareça natural.
- Sem IDs (`RF-`, `D-`, `P-`, `N-`, `Req.`) e sem citar os outros arquivos nem "a análise": o arquivo vale por si.
- Sem trechos de código, exceto exemplos curtos que tirem uma dúvida (um formato de dado, um exemplo de resposta). Caminhos de tela, rota ou endpoint podem aparecer quando ajudam a localizar onde trabalhar.
- Cores e medidas, só quando são regra (ex.: vencido em vermelho) e não há protótipo. Havendo protótipo, cite o link.
- Nada novo: tudo o que está aqui está em `analise-sistemas.md`.

Rode `verificar.py final` na pasta e corrija.

## 9. Encerrar

Diga ao usuário os caminhos dos dois arquivos, quantos RF e RNF foram escritos, quantas decisões e divergências aceitas há, e as pendências. Se esta skill foi chamada pela `analise-requisitos`, volte para ela, que roda a validação em seguida. Se foi chamada sozinha, sugira rodar `/analise-validar`.
