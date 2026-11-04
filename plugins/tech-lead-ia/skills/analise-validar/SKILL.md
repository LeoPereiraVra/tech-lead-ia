---
name: analise-validar
description: 'Etapa 3 do refinamento de requisitos. Valida o #<card>-analise-final.md contra a análise de negócio inicial, a analise-negocios.md e a analise-sistemas.md. Procura requisitos que se perderam, decisões não refletidas, divergências sem explicação, perguntas sem resposta e pontos em aberto, resolve cada achado com o usuário, corrige os arquivos e grava validacao.md. Use quando o usuário pedir para validar, conferir ou revisar o refinamento ou o arquivo final antes de enviá-lo ao dev, mesmo sem dizer "etapa 3". Não use para validar código já implementado (isso é do tlc-spec-driven).'
argument-hint: '<número do card>'
---

# Etapa 3 — Validação

O arquivo final vai sozinho para o dev. Esta etapa confere se ele entrega o que foi analisado e decidido, e se o que ficou em aberto está em aberto porque o usuário quis, não por esquecimento.

Os recursos comuns ficam na skill irmã, em `<skills>/analise-requisitos/`, onde `<skills>` é a pasta que contém esta skill. Leia `references/perguntas.md` antes de perguntar.

## 1. Reunir os arquivos

Na pasta `.agents/analises/#<card>/`, pegue `analise-negocios.md`, `analise-sistemas.md`, `#<card>-analise-final.md` e `requisitos-sistema.md`, se existir. Pegue também a análise de negócio original, cujo caminho está no cabeçalho de `analise-negocios.md`, e os requisitos de sistema em arquivo, cujo caminho está no cabeçalho de `analise-sistemas.md`.

Sem o arquivo final, a etapa 2 não terminou: diga isso e ofereça rodá-la.

## 2. Checagem de estrutura

```bash
python3 "<skills>/analise-requisitos/scripts/verificar.py" tudo ".agents/analises/#<card>"
```

Cada ERRO vira achado. Confira os AVISOs e decida se viram achado.

## 3. Comparação independente

Quem escreveu os arquivos tende a ler neles o que quis dizer. Por isso, a comparação é feita com olhos novos:
- **Com subagentes** (no Claude Code, a ferramenta Agent): delegue a um subagente novo, sem o histórico desta conversa. Passe os caminhos dos arquivos e a lista abaixo, e peça que devolva cada achado com o trecho, o arquivo e a seção, sem editar nada.
- **Sem subagentes**: faça você mesmo, relendo cada arquivo até o fim, sem se apoiar na memória da conversa.

O que procurar:
1. **Cobertura**: cada requisito e caso de teste da análise de negócio aparece no arquivo final, ou está fora do escopo com motivo, ou é divergência aceita.
2. **Decisões refletidas**: cada decisão de "Dúvidas e decisões" aparece no arquivo final com o conteúdo decidido, não com o da análise original.
3. **Divergências explicadas**: toda diferença entre o arquivo final e a análise de negócio é uma divergência aceita, com motivo. Diferença sem registro é achado.
4. **Perguntas respondidas**: todo `N-xx` mandado ao analista tem resposta ou está nas pendências; toda pergunta da etapa 2 tem decisão.
5. **Pendências**: o que continua em aberto e se isso impede o desenvolvimento.
6. **Sem origem**: nada no arquivo final que não esteja em `analise-sistemas.md`.
7. **Contradições** dentro do arquivo final.
8. **Autossuficiência**: o arquivo final se entende sozinho, com contexto, sem IDs e sem citar outros arquivos.

## 4. Resolver com o usuário

Mostre os achados numa lista curta, com ID (`V-01`, `V-02`…), tipo, onde e o que falta. Cada achado que pede decisão vai para a caixa de perguntas (`perguntas.md`), com a correção recomendada primeiro. Se o achado for só falha de escrita (por exemplo, um ID esquecido no arquivo final), corrija sem perguntar e mencione a correção.

Aplique cada decisão nos dois arquivos: no arquivo final e em `analise-sistemas.md` (nova `D-xx`, divergência aceita ou pendência), para que continuem dizendo a mesma coisa. Depois, rode `verificar.py tudo` de novo.

Repita até não sobrar achado ou até o usuário aceitar deixar algo em aberto. Se depois de três rodadas ainda aparecerem achados novos, pare e mostre o que sobrou, em vez de continuar em círculo.

## 5. Gravar `validacao.md` e encerrar

Preencha o modelo `assets/validacao.md` desta skill e grave na pasta. O resultado é um destes:
- **APROVADO**: nenhum achado e nenhuma pendência;
- **APROVADO COM RESSALVAS**: há pendências que o usuário aceitou deixar abertas, listadas no arquivo final e em `validacao.md`;
- **REPROVADO**: o usuário decidiu parar com divergências ou dúvidas sem resolver.

Diga ao usuário o resultado, o caminho do `#<card>-analise-final.md` e, se houver, as ressalvas que acompanham o arquivo quando ele for para o dev.
