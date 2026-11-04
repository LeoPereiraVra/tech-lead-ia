---
name: analise-negocio
description: 'Etapa 1 do refinamento de requisitos. Lê a análise de negócio de uma solicitação (arquivo, texto ou card do Kanboard) e procura lacunas e divergências dentro dela e em relação ao código do projeto (ex.: pede para remover o botão Sair, mas não existe outra forma de sair). Depois tria com o usuário quais pontos viram perguntas para o analista de negócio e grava .agents/analises/#<card>/analise-negocios.md com o resumo do que precisa ser feito. Use quando o usuário indicar uma análise de negócio e pedir para analisá-la, revisá-la, achar furos, levantar dúvidas ou preparar perguntas para o analista, mesmo sem dizer "etapa 1". Não use para escrever a análise de negócio (isso é do sci-analise-negocio).'
argument-hint: '<número do card> <caminho da análise de negócio>'
---

# Etapa 1 — Análise de negócio

Quem escreve a análise de negócio conhece o problema, mas nem sempre conhece o sistema. Esta etapa cruza os dois: acha o que falta ou não fecha na análise e no encontro dela com o código, decide com o usuário o que vale perguntar ao analista de negócio e registra o que precisa ser feito. O arquivo gerado é lido pelo analista de negócio, que responde às perguntas, e pelo analista de sistemas, que escreve os requisitos de sistema a partir dele.

Os recursos comuns ficam na skill irmã, em `<skills>/analise-requisitos/`, onde `<skills>` é a pasta que contém esta skill. Antes de começar, leia por inteiro:
- `references/perguntas.md`
- `references/analise-codigo.md`

## 1. Localizar a análise e a pasta

A análise de negócio pode chegar como:
- **caminho de arquivo**: `.md` se lê direto; `.docx` e `.pdf`, com a skill do formato, quando houver;
- **texto colado** na conversa;
- **número ou link do card no Kanboard**: com a skill `sci-analise-negocio-ler-solicitacao` disponível, use-a para baixar o card e os anexos em `.sci/<card>/` e procure a análise de negócio entre eles. Sem ela, peça o arquivo.

Sem nenhuma indicação, pergunte onde está a análise. Descubra o número do card como descrito na skill `analise-requisitos` (argumento, nome do arquivo, título, link) e use a pasta `.agents/analises/#<card>/`.

Se `analise-negocios.md` já existe, pergunte antes de mexer: **Atualizar** (mantém as respostas já dadas e reavalia o resto), **Refazer do zero** (sobrescreve) ou **Parar**. Ao atualizar porque o analista respondeu às perguntas (ou mandou uma versão nova da análise), registre a resposta dele no ponto, com a situação *Respondido pelo analista*.

## 2. Ler a análise inteira

Leia até o fim: contexto, requisitos, exceções, casos de teste, fora do escopo, pendências e referências. Abra as imagens citadas. Links de Figma, protótipo ou artefato servem para conferir regras e textos que a análise menciona; não descreva o layout deles.

Monte para si a lista de requisitos com a numeração da própria análise (Req. 1, Req. 2…). Se a análise não numera, numere na ordem em que aparecem e diga isso no arquivo.

## 3. Procurar lacunas e divergências na própria análise

Confronte as partes da análise entre si:
- **requisito × caso de teste**: o caso espera algo que o requisito não diz, ou o contrário;
- **requisito × requisito**: regras que se contradizem, o mesmo termo com sentidos diferentes;
- **texto × imagem ou protótipo**: a imagem mostra regra ou conteúdo que o texto não cobre ou contradiz (estética não conta);
- **comportamento sem definição**: perfil não citado, estado vazio, erro, limite, sem permissão, o que acontece com dados que já existem, mensagem sem texto;
- **fora do escopo × escopo**: algo excluído de que um item incluído depende;
- **pendências e [LACUNA]** que a própria análise registrou: entram como pontos, porque continuam sem resposta.

## 4. Procurar lacunas e divergências com o sistema

Siga `analise-codigo.md`. Para cada requisito, ache onde ele cai no código e o que existe hoje. O que interessa é o encontro da análise com o sistema: remoção sem substituto, referência a algo que não existe, regra atual que a análise ignora, perfil que usa a tela e não foi citado, outro lugar atingido, dado que não existe.

Guarde também os **impactos no sistema** que não são dúvida, mas que o analista de sistemas precisa saber. Por exemplo: trinta telas calculam a altura do conteúdo contando com o rodapé que vai sair.

## 5. Tentar resolver antes de perguntar

Para cada ponto, veja se a própria análise ou o código já respondem:
- **respondem**: o ponto fica como *Resolvido pelo código*, com a evidência e a conclusão (ex.: "o usuário adicional segue as permissões da empresa, como hoje");
- **é detalhe de implementação** (como fazer, não o que fazer): não é pergunta para o analista de negócio; vai para "Impactos no sistema" se o analista de sistemas precisar saber;
- **não respondem**: o ponto vai para a triagem com o usuário.

Numere os pontos como `N-01`, `N-02`…, do mais para o menos impactante.

## 6. Triar com o usuário

Primeiro, mostre no chat a lista completa numa tabela curta (ID, tipo, assunto, recomendação), incluindo os resolvidos pelo código, para o usuário ver o todo.

Depois, pergunte pela caixa de perguntas cada ponto ainda aberto, até quatro por vez, seguindo `perguntas.md`. A pergunta diz o que foi encontrado e por que importa. As opções típicas são:
- **Perguntar ao analista**: é decisão de negócio; vira pergunta no arquivo. Situação: *Perguntar ao analista*;
- **Seguir o sistema atual**: só quando há comportamento atual que resolve; a descrição diz qual é. Situação: *Respondido pelo usuário*, com a resposta "segue o sistema atual: <comportamento>";
- **Descartar**: não é relevante para esta solicitação. Situação: *Descartado*, com o motivo na resposta.

O usuário também pode responder ele mesmo em "Outro"; aí o ponto fica *Respondido pelo usuário*. Ponha a opção recomendada primeiro. Para os pontos resolvidos pelo código, faça uma pergunta só, no fim: o usuário concorda com as conclusões, ou quer que alguma vire pergunta?

Grave cada resposta no ponto assim que ela chega.

## 7. Escrever as perguntas para o analista de negócio

Para cada ponto marcado como *Perguntar ao analista*, escreva uma pergunta que o analista responda sem precisar voltar com outra: o contexto em termos de tela, perfil e ação (sem caminhos de arquivo), o que a análise diz e o que o sistema faz hoje quando for divergência, a pergunta e, quando as alternativas são claras, sugestões de resposta.

## 8. Escrever o que precisa ser feito

Esta seção diz o que muda, não como fica na tela:
- organize por área, tela ou funcionalidade;
- diga o que é criado, o que muda, o que sai e o resultado esperado para o usuário;
- deixe de fora cores, medidas, fontes e espaçamentos; havendo Figma ou protótipo, cite o link;
- aplique as respostas da triagem ("Respondido pelo usuário", "Seguir o sistema atual");
- marque com "(aguarda N-xx)" o item que depende de pergunta ainda sem resposta;
- cite o requisito de origem, como em "(Req. 3)".

## 9. Gravar e conferir

Preencha o modelo `assets/analise-negocios.md` desta skill e grave em `.agents/analises/#<card>/analise-negocios.md`. Depois rode:

```bash
python3 "<skills>/analise-requisitos/scripts/verificar.py" negocio ".agents/analises/#<card>"
```

Corrija os ERROs e confira os AVISOs.

## 10. Encerrar

Diga ao usuário, em poucas linhas:
- o caminho do arquivo;
- quantos pontos foram levantados e como ficaram (perguntar ao analista, respondidos, resolvidos pelo código, descartados);
- que a seção "Perguntas para o analista de negócio" está pronta para enviar;
- o próximo passo: com os requisitos de sistema e as respostas do analista, chamar `/analise-sistema` ou `/analise-requisitos <card>`.

Se esta skill foi chamada pela `analise-requisitos`, volte para ela.
