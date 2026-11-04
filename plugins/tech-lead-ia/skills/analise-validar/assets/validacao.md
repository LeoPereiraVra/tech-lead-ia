# #<card> — Validação do refinamento

> Validado em <dd/mm/aaaa>, com a análise de negócio (<caminho>), analise-negocios.md, analise-sistemas.md e #<card>-analise-final.md. Comparação feita por <subagente independente, ou o próprio agente relendo os arquivos>.

## Resultado

<APROVADO | APROVADO COM RESSALVAS | REPROVADO> — <uma frase com o motivo>

## Verificações

| Verificação | Resultado | Observação |
|---|---|---|
| Requisitos e casos de teste da análise de negócio têm destino no arquivo final | <ok ou falha> | <detalhe> |
| Decisões tomadas aparecem no arquivo final com o conteúdo decidido | <ok ou falha> | <detalhe> |
| Toda diferença em relação à análise de negócio é divergência aceita, com motivo | <ok ou falha> | <detalhe> |
| Perguntas das etapas de negócio e de sistema têm resposta | <ok ou falha> | <detalhe> |
| Pendências em aberto | <nenhuma ou quantas> | <detalhe> |
| Nada no arquivo final sem origem nas fontes | <ok ou falha> | <detalhe> |
| Arquivo final sem contradições internas | <ok ou falha> | <detalhe> |
| Arquivo final se entende sozinho (sem IDs nem referência a outros arquivos) | <ok ou falha> | <detalhe> |
| Checagem de estrutura (verificar.py tudo) | <ok ou falha> | <detalhe> |

## Achados

### V-01 — <assunto>

- **Tipo:** <Divergência sem explicação | Pergunta sem resposta | Ponto em aberto | Decisão não refletida | Sem origem | Contradição | Autossuficiência>
- **Onde:** <arquivo, seção e trecho>
- **Decisão do usuário:** <o que foi decidido>
- **Correção:** <o que foi alterado e em quais arquivos>

<Sem achados, troque os blocos por "Nenhum.">

## Pendências aceitas em aberto

<"Nenhuma." ou a lista, com quem decide e o risco para o desenvolvimento.>
