# Modelos dos arquivos

Todos ficam em `.agents/#<card>/agentes/`. Datas no formato dd/mm/aaaa.

## duvidas-negocios.md

Formato pedido pelo analista: primeiro todos os pontos, cada um com o trecho e o motivo, e no fim a lista de perguntas. Cada rodada nova entra abaixo da anterior, com os IDs continuando.

```md
# #<card> — Dúvidas da análise de negócios

> Análise: <caminho do arquivo, ou card e versão do documento>, lida em <data>. Código: <repositório> <branch>@<commit>[, <outro repositório> ...]. Figma: <verificado | não verificado, e o motivo>.

## Rodada 1 — <data>

### Dúvidas análise de negócios

D1:
Tipo: Ambiguidade
Na análise: "Geral e Grupos de notificação herdam a liberação atual de 'Central de notificações'" (Req. 1)
Porque: o texto não deixa claro se são uma permissão ou duas, nem se "herdar" quer dizer copiar o valor uma vez ou depender do pai para sempre. O caso de teste "Notificações enviadas liberado e Central bloqueada" só funciona se o pai for só um agrupador.

D2:
Tipo: Divergência com o código
Na análise: "O botão deve continuar sendo exibido apenas para usuários do tipo (1 - Admin), assim como é feito hoje" (Req. 4)
Porque: hoje o botão Salvar aparece só para o usuário do tipo 5, e não para o Admin. (app/view/relatorio/form.blade.php:42)

D3:
...

Dúvidas:
D1: Geral e Grupos de notificação são uma permissão ou duas? E, depois da liberação, (a) cada uma é independente e o pai só agrupa, ou (b) bloquear a Central bloqueia as duas?
D2: O botão Salvar deve aparecer para o Admin (tipo 1), como diz a análise, ou continuar só para o tipo 5, como é hoje?
D3: ...
```

- `Tipo`: Contradição interna, Divergência com o código, Divergência com o layout, Ponto em aberto ou Ambiguidade.
- Na rodada 2, acrescente `## Rodada 2 — <data>` com a mesma estrutura, começando no próximo ID livre (se a rodada 1 terminou em D7, a rodada 2 começa em D8).
- Se o analista escrever as respostas no próprio arquivo, elas ficam abaixo de cada pergunta. Ao registrar em `decisoes.md`, não apague o que ele escreveu.

## decisoes.md

Um registro para consulta posterior: cada resposta do analista vira uma entrada, na ordem em que chega. As decisões da análise de negócios usam o ID da dúvida (D1, D2...). As da análise de sistema, gravadas pela skill `analise-sistema`, usam S1, S2...

```md
# #<card> — Decisões

> Cada resposta do analista, registrada como decisão. D = validação da análise de negócios; S = análise de sistema.

## D1 — Permissões de Geral e Grupos
- Pergunta: Geral e Grupos são uma permissão ou duas? Dependem do pai?
- Decisão: Geral e Grupos de notificação são duas permissões. Na liberação, cada uma recebe o valor atual de "Central de notificações"; depois disso, são independentes, e o pai só agrupa.
- Quem decidiu: analista de sistemas, em 12/11/2026
- Diverge da análise: não
- Afeta: Req. 1 e o caso de teste "Notificações enviadas liberado e Central bloqueada"

## D2 — Botão Salvar
- Pergunta: ...
- Decisão: descartada. O botão continua só para o tipo 5, como hoje; a análise descreveu errado e o analista confirmou que nada muda.
- Quem decidiu: analista de negócios, resposta trazida pelo analista de sistemas em 13/11/2026
- Diverge da análise: sim. A análise dizia que hoje o botão aparece para o Admin.
- Afeta: Req. 4
```

- **Quem decidiu**: analista de sistemas, analista de negócios (resposta trazida por alguém), ou "código", quando a resposta foi "segue como o sistema faz hoje" e há evidência.
- **Diverge da análise**: "sim" sempre que a decisão muda o que a análise pedia ou descrevia. É o que alimenta a seção de diferenças do resumo.

## analise-negocios-resumo.md

```md
# #<card> — <título curto da solicitação> — resumo da análise de negócios

> Base: <análise lida>, com as decisões D1 a D<n> de `decisoes.md`. Gerado em <data>.

## Contexto

<De 3 a 5 linhas: quem usa, o que existe hoje, o que muda e o que continua igual.>

## Requisitos funcionais

### RF-01 — <verbo e resultado, ex.: Separar a Central de notificações em três submenus>
- <regra essencial>
- <exceção ou caso que muda a implementação>
- Origem: Req. 1; D1

### RF-02 — ...

## Diferenças em relação à análise de negócios

- <o que a análise pedia ou descrevia> → <o que vale> (D4)

## Fora do escopo

- <o que não será feito, com o motivo>

## Pendências

Nenhuma.
```

- "Diferenças", "Fora do escopo" e "Pendências" podem ser omitidas quando não há nada a dizer. Pendência só existe se o analista aceitou deixar algo em aberto; nesse caso, diga o que falta decidir e quem decide.
- Sem caminhos de arquivo, trechos de código ou detalhes de layout que o Figma já mostra.
