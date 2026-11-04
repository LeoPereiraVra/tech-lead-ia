# Como perguntar

As etapas do refinamento só avançam com as respostas do usuário. Uma pergunta mal montada gera outra pergunta depois; uma bem montada fecha o assunto de uma vez. Este guia vale para todas as perguntas das três etapas.

## Ferramenta

- **Claude Code:** `AskUserQuestion`. **Codex:** `request_user_input`, quando disponível.
- **Sem ferramenta de perguntas:** escreva as perguntas numeradas, com as opções em letras (a, b, c), e pare até o usuário responder.
- Limites do `AskUserQuestion`: até 4 perguntas por chamada, de 2 a 4 opções por pergunta e cabeçalho (`header`) de até 12 caracteres. A opção "Outro", com texto livre, aparece sozinha: não a inclua.

## Montar cada pergunta

1. **Ela se explica sozinha.** A caixa de perguntas pode esconder o que você escreveu no chat. No texto da pergunta, diga em uma ou duas frases o que foi encontrado e onde (Req. 3, tela de contratos, perfil colaborador) e depois pergunte. Use o ID do ponto no cabeçalho (`N-03`, `D-07`, `V-02`).
2. **Opções concretas.** Cada opção é um resultado que dá para escrever como requisito ("Mostrar 'Nenhum contrato ativo.' e voltar ao login"), nunca "Opção A" ou "Depende". A descrição da opção diz a consequência: o que muda e o que fica igual.
3. **Recomendação primeiro.** Quando você tem base (código, padrão do sistema, a própria análise), a opção recomendada vem primeiro, com "(Recomendado)" no fim do rótulo, e a descrição diz por quê.
4. **Fechar o assunto.** Antes de enviar, confira se qualquer resposta escolhida deixa o requisito sem dúvida. Se a escolha abriria outra dúvida ("mostrar mensagem", mas qual texto?), embuta a continuação nas opções ou faça a pergunta dependente logo em seguida.
5. **Múltipla escolha quando as respostas se somam.** Use `multiSelect` quando várias opções podem valer juntas (quais perfis veem, quais telas mudam, quais filtros entram). Quando as opções se excluem, use escolha única.
6. **Comparar textos ou telas:** use o campo `preview` das opções para mostrar alternativas lado a lado (texto de mensagem, estrutura de tela em ASCII).
7. **Não pergunte o que o código responde.** Procure antes (`analise-codigo.md`). Pergunta serve para decisão, não para fato.

Exemplo de pergunta bem montada:

> **Cabeçalho:** N-04
> **Pergunta:** A análise remove o "Sair" do menu lateral (Req. 5), mas hoje ele é a única forma de sair nas telas sem cabeçalho, como as modais em tela cheia do app. O que fazer?
> **Opções:**
> - *Manter "Sair" só no app (Recomendado)*: no app não há menu do usuário, então o menu lateral continua sendo a saída.
> - *Perguntar ao analista*: vira pergunta no arquivo da etapa 1.
> - *Remover em todo lugar*: o app fica sem forma de sair até outra solicitação.

## Ordem e ritmo

- Ordene por impacto: primeiro o que muda o escopo ou as outras respostas.
- Perguntas independentes: até quatro por chamada. Dependentes: uma por vez, esperando a resposta, porque a primeira muda a segunda.
- Com mais de oito perguntas, mostre antes no chat a lista completa (ID, assunto, recomendação) para o usuário ter a visão do todo, e depois pergunte em lotes. Se ele disser "o resto pode seguir a recomendação" ou "manda tudo para o analista", aplique aos restantes e registre que foi assim.
- Resposta em "Outro": use o texto como resposta. Se ele não fecha o assunto, faça uma pergunta de continuação.

## Registrar

- Grave cada resposta no arquivo da etapa assim que ela chega, não no fim: a conversa pode ser compactada, e o arquivo é a memória do refinamento.
- Registre a resposta como decisão escrita (o que fica valendo), não como "opção 2".
- Diga quem decidiu: "usuário" (ou o papel que ele usar: dev, analista de sistemas), "analista de negócio" (resposta trazida do analista), "requisito de sistema" (já estava escrito nos requisitos) ou "código" (segue o comportamento atual, com a evidência).

## Perguntas para o analista de negócio (etapa 1)

Essas perguntas são lidas fora desta conversa, por quem não tem o código à mão. Escreva em linguagem de negócio:
- o contexto em termos de quem usa o sistema (tela, perfil, ação), sem caminho de arquivo;
- o que a análise diz e, quando for divergência, o que o sistema faz hoje;
- a pergunta e, quando as alternativas são claras, sugestões de resposta, para o analista responder escolhendo.
