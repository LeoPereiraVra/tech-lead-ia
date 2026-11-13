# Modelos dos arquivos

Todos ficam em `.agents/#<card>/agentes/`. Datas no formato dd/mm/aaaa.

## duvidas-sistema.md

Mesmo formato das dúvidas de negócios: primeiro os pontos, cada um com o trecho e o motivo, e no fim a lista de perguntas. Os IDs usam S e continuam entre as rodadas.

```md
# #<card> — Dúvidas da análise de sistema

> Análise de sistema: .agents/#<card>/analise-sistema.md, lida em <data>. Análise de negócios: <arquivo ou card e versão>[; resumo e decisões D1 a D<n>]. Código: <repositório> <branch>@<commit>[, ...].

## Rodada 1 — <data>

### Dúvidas análise de sistema

S1:
Tipo: Contradição com a análise de negócios
Na análise de sistema: "A exportação CSV será gerada em fila e enviada por e-mail ao usuário"
Porque: o Req. 5 da análise de negócios pede que o arquivo seja baixado na hora, ao clicar em Relatório CSV.

S2:
Tipo: Risco técnico
Na análise de sistema: "A consulta lê direto da tabela de log, com todos os filtros opcionais"
Porque: a tabela de log cresce sem limite e não tem índice por data. Uma consulta sem período lê a tabela inteira a cada clique. Exigir período limita a leitura, mas muda a regra de negócio; criar índice resolve a leitura por data, mas não a consulta sem filtro nenhum. (app/model/Log.php:18)

S3:
...

Dúvidas:
S1: A exportação CSV é baixada na hora, como pede a análise de negócios, ou gerada em fila e enviada por e-mail, como propõe a análise de sistema?
S2: Para a consulta de log: (a) criar índice por data e limitar o período a 90 dias, levando a regra ao analista de negócios, (b) só criar o índice, aceitando consultas lentas sem filtro, ou (c) outra solução?
S3: ...
```

- `Tipo`: Contradição com a análise de negócios, Divergência com o código, Contradição interna, Ponto faltante ou Risco técnico.
- Na divergência com o código, a evidência vai no fim do "Porque", entre parênteses (`caminho:linha`).

## Entradas S em decisoes.md

Acrescente ao fim de `decisoes.md`. Se o arquivo não existe, crie com o cabeçalho abaixo.

```md
# #<card> — Decisões

> Cada resposta do analista, registrada como decisão. D = validação da análise de negócios; S = análise de sistema.

## S1 — Forma da exportação CSV
- Pergunta: download na hora (negócios) ou arquivo gerado em fila e enviado por e-mail (sistema)?
- Decisão: o CSV é gerado em fila e enviado por e-mail, porque a consulta pode passar de 500 mil linhas e estoura o tempo da requisição. A tela mostra o aviso de que o arquivo chegará por e-mail.
- Quem decidiu: analista de sistemas, em 12/11/2026
- Diverge da análise de negócios: sim. O Req. 5 pedia o download na hora. Avisar o analista de negócios.
- Afeta: RA-02; Req. 5
```

## analise-sistema-final.md

```md
# #<card> — <título curto da solicitação> — análise de sistema

> Complementa a análise de negócios (<arquivo ou card e versão>)[ e o resumo `agentes/analise-negocios-resumo.md`]. Base: `analise-sistema.md` do analista e as decisões S1 a S<n>. Código: <repositório> <branch>@<commit>[, ...]. Gerado em <data>.

## Visão da solução

<De 3 a 6 linhas: como a solução se encaixa na estrutura atual. Quais sistemas e camadas participam, o que é novo, o que é reaproveitado e o padrão existente que serve de referência.>

## Requisitos arquiteturais

### RA-01 — <decisão de estrutura, com verbo. Ex.: Centralizar o cálculo do vencimento numa biblioteca usada pela tela e pela API>
- O quê: <a decisão>
- Onde: <sistemas, módulos, tabelas ou arquivos>
- Por quê: <motivo; quando houve escolha, a alternativa descartada e o custo dela>
- Atende: RF-04, RF-05

## Requisitos não funcionais

### RNF-01 — Segurança: <resultado verificável. Ex.: Toda consulta e exportação de contratos filtra pelo escritório da sessão>
- Regra: <o que precisa valer, com limites concretos quando houver>
- Como verificar: <o teste ou a conferência que prova>
- Atende: RF-04

## Dados e scripts

- <tabela, coluna, índice ou script manual; banco ou esquema; carga inicial; o que acontece com os dados antigos; ordem em relação ao deploy>

## Impactos em outras partes

- <tela, sistema ou rotina que usa o que muda, e o que precisa continuar funcionando>

## Riscos e dependências

- <dependência de outra equipe ou de outra solicitação, ordem de deploy, risco aceito pelo analista>

## Fora do escopo técnico

- <o que o dev não deve fazer, mesmo que pareça natural, com o motivo>

## Pendências

Nenhuma.
```

- Os IDs RA e RNF são locais deste arquivo. "Atende" cita os requisitos do resumo (RF-n) ou, sem resumo, os da análise de negócios (Req. n).
- Seções sem conteúdo saem do arquivo, exceto "Pendências".
- Categorias de RNF mais comuns: Segurança, Desempenho, Escalabilidade, Manutenção, Compatibilidade, Observabilidade, Usabilidade.
