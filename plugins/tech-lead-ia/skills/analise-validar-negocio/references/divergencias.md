# Tipos de ponto: o que é e o que não é

Leia antes de procurar os pontos. Os exemplos são reais e mostram o raciocínio esperado: o que se compara, por que vira ponto e como registrar.

## 1. Contradição interna

Um trecho da análise anula ou torna impossível outro trecho. Acontece muito quando a análise altera algo e, mais adiante, cria uma regra sobre o que foi alterado e não existe mais.

**Exemplo 1**

```md
- A tela de relatórios só pode ser acessada pelo usuário do tipo 1 - Admin
...
- Quando o funcionário acessar a tela de relatórios, deve ser exibido um alerta
```

Se só o Admin acessa a tela, o funcionário nunca chega a ela, e o alerta não tem quando aparecer. É contradição.

**Exemplo 2**

```md
- Na tela de endereço, alterar o campo "Número" de numérico para texto.
...
- O campo de número do endereço não pode ser maior que 9999
```

Se o campo vira texto, "maior que 9999" deixa de ter sentido. Antes de registrar, confira na tela se existe outro campo de número ao qual a segunda regra possa se referir. Se não existir, é contradição.

Casos de teste contam como parte da análise. Um caso de teste que só funciona numa das leituras de um requisito, ou que contradiz o texto, é ponto.

## 2. Divergência com o código

A análise afirma como o sistema funciona hoje ("assim como é feito hoje", "como funciona atualmente", "a tela atual", "continua") e o código mostra outra coisa.

**Exemplo**

```php
@if($usuario->tipo == 5)
<button class="bt" style="#FFFF">Salvar</button>
@endif
```

```md
- O botão de salvar deve ter a cor preta #000000
- O botão deve continuar sendo exibido apenas para usuários do tipo (1 - Admin), assim como é feito hoje
```

- O código exibe o botão só para o tipo 5, e a análise diz que hoje ele aparece só para o tipo 1. É divergência: a análise descreve errado o comportamento atual, e a pergunta é qual tipo vale.
- A cor preta não é divergência. A análise pede a mudança, e o código ainda ter outra cor é exatamente o que vai mudar.

A regra: **mudança pedida não é divergência; descrição errada do que existe é.** Também entra aqui a análise que cita algo que não existe no sistema (uma tela, um campo, um dado que não é gravado, uma alteração que nenhuma tela permite fazer). Nesse caso, a análise pede uma coisa que depende de outra que não existe.

Toda divergência com o código traz a evidência (`caminho:linha`). Sem evidência, não afirme: escreva o que procurou e não encontrou.

## 3. Divergência com o layout

Quando há link para o Figma, compare o que a análise pede com o que o protótipo mostra.

**Exemplo**

```md
- Criar duas novas abas com os nomes "Empresa" e "Relatório"
```

No Figma só existe a aba Empresa. É divergência com o protótipo, e a pergunta é qual dos dois vale.

O que está no Figma não precisa estar na análise: cores, textos, rótulos, botões, nomes de menus e de telas. A ausência desses detalhes na análise não é ponto. Só é ponto quando a análise diz algo **diferente** do protótipo.

Textos de exemplo no protótipo ("Placeholder", "Label", um campo preenchido para ilustrar) não são divergência.

## 4. Ponto em aberto e ambiguidade

**Ponto em aberto:** a análise trata um assunto, mas falta a decisão que a implementação precisa, e nenhum outro trecho da análise responde.

**Ambiguidade:** um trecho admite mais de uma leitura válida, e cada leitura leva a uma implementação diferente. Não é ambiguidade quando só uma das leituras faz sentido com o resto da análise ou com o código.

Para cada ambiguidade, registre o trecho, as leituras possíveis, o que muda em cada uma e a pergunta.

**Exemplo 1: duas referências no mesmo requisito que, no código, não batem**

```md
- Botão "Ações" com as opções "Relatório PDF" e "Relatório CSV", exportando todos os resultados filtrados, com as mesmas colunas do grid. Exatamente como funciona atualmente.
```

```php
// Grid da tela
{{ $email->empresa ?? 'Nenhuma empresa vinculada a este e-mail' }}

// Exportação PDF/CSV atual
$linha['empresa'] = $email->empresa ?? ' - ';
```

Lido sozinho, o texto parece coerente: "mesmas colunas do grid" e "exatamente como funciona atualmente" parecem dizer a mesma coisa. O código mostra que hoje a exportação não é igual ao grid. No e-mail sem empresa, o grid mostra "Nenhuma empresa vinculada a este e-mail", e o PDF/CSV mostra " - ".
- Leitura A (igual ao grid): a exportação passa a mostrar "Nenhuma empresa vinculada a este e-mail".
- Leitura B (como funciona hoje): a exportação continua mostrando " - ".

Registre como ambiguidade e pergunte qual das duas vale, deixando claro que a dúvida é só na coluna Empresa e que o resto da exportação segue como hoje.

**Exemplo 2: palavra que admite dois sentidos, exposta por um caso de teste**

```md
- O menu "Central de notificações" deixa de abrir uma tela e passa a ter os submenus Geral, Grupos de notificação e Notificações enviadas.
- Geral e Grupos de notificação herdam a liberação atual de "Central de notificações".
...
| Caso de teste | Usuário com "Notificações enviadas" liberado e "Central de notificações" bloqueado | Só Notificações enviadas acessível |
```

"Herdam" pode significar:
- Leitura A: na liberação, Geral e Grupos copiam o valor atual da Central e, depois disso, cada permissão é independente. O menu pai só agrupa.
- Leitura B: Geral e Grupos sempre dependem da permissão do menu pai. Bloqueou a Central, bloqueia tudo.

A análise também não diz se Geral e Grupos são uma permissão só ou duas. O caso de teste só funciona na leitura A, porque na leitura B a Central bloqueada esconderia Notificações enviadas. Registre como ambiguidade e pergunte quantas permissões são e se o pai é só um agrupador.

**Exemplo 3: termo vago, sem critério para medir**

```md
- O botão da tela deve ser grande
```

"Grande" não tem medida nem referência. Pergunte o tamanho ou peça um botão existente que sirva de modelo. Se o Figma mostra o botão, não é ponto.

## O que não vira ponto

- Mudança pedida pela análise, mesmo que o código hoje faça diferente.
- Detalhe de layout que está no Figma e não diverge.
- Dúvida que o código responde (descubra e use o fato).
- Dúvida cuja resposta não muda a implementação.
- Assunto que a análise delegou de propósito à análise de sistemas ("a análise de sistemas avalia..."), desde que a regra de negócio para cada resultado possível esteja escrita.
- Melhoria que ninguém pediu. Se você enxerga uma oportunidade, ela não é dúvida da análise.
- Ponto de outra solicitação ou de outra tela, sem relação com esta.

## Lembretes de onde costumam estar os pontos

A lista serve para lembrar onde olhar. Só vira ponto o que tem relação com a solicitação e passa pelo filtro do passo 4.

| Onde olhar | Pergunta-guia |
|---|---|
| Remoção | O que sai é a única forma de fazer algo? (remover "Sair" sem outro jeito de sair) |
| Referência | A tela, o campo, o menu ou o dado citado existe com esse nome e nesse lugar? |
| Regra atual | O código tem regra (permissão, módulo contratado, tipo de usuário, status) que a análise ignora ou descreve diferente? |
| Perfis | Quem usa a tela hoje? A análise cobre todos os perfis (principal, adicional, restrito a algumas empresas)? |
| Dado | O dado que a análise mostra ou filtra é gravado hoje? Em todos os casos? |
| Dados existentes | O que acontece com o que já está gravado, com permissões já dadas, com links antigos? |
| Estados | Vazio, erro, sem permissão, sem resultado, limite |
| Acesso | App, celular, URL direta, tela aberta dentro de modal |
| Casos de teste | Cada caso de teste é possível com as regras escritas? |
