# #<card> — <título da solicitação>

> Fontes: análise de negócio (<caminho ou link>), pontos da etapa de negócio (analise-negocios.md), requisitos de sistema (<caminho, ou "informados na conversa", com cópia em requisitos-sistema.md>) e código (<repositório> <branch>@<commit curto>). Levantamento em <dd/mm/aaaa>.

## Objetivo

<Um parágrafo: o que existe hoje, o que esta solicitação cria ou muda e o resultado para quem usa o sistema.>

## Escopo

**Incluído**
- <entrega> (<RF-xx>)

**Fora do escopo**
- <item> — <motivo>; <quem decidiu> (<D-xx>)

## Comportamento atual

<Os fatos do código que o dev precisa conhecer para não quebrar nada: telas, regras, permissões, dados. Frases curtas, agrupadas por assunto, em linguagem de quem usa o sistema. Cite o caminho só quando ajudar a localizar.>

## Atores e permissões

| Perfil | O que pode fazer |
|---|---|
| <perfil> | <o que vê e faz nesta solicitação> |

## Requisitos funcionais

### RF-01 — <verbo no infinitivo + resultado>

<O que o sistema passa a fazer, em uma ou duas frases.>

- Regras:
  - <regra>
- Dados: <de onde vêm, formatos, limites; omita a linha se não se aplica>
- Exceções: <erro, vazio, sem permissão, limite; omita a linha se não se aplica>
- Critérios de aceite:
  - Dado <situação com dado concreto>, quando <ação>, então <resultado verificável>.
- Origem: <P-xx, Req. n da análise de negócio, N-xx> (<D-xx>)

## Requisitos não funcionais

### RNF-01 — <Categoria>: <resultado>

<O requisito, mensurável.>

- Verificação: <como conferir>
- Origem: <P-xx, Req. n, ou "Implícito (confirmado pelo usuário)"> (<D-xx>)

## Dúvidas e decisões

Toda dúvida levantada nas etapas de negócio e de sistema, e a resposta dada.

| # | Dúvida | Decisão | Decidido por | Origem | Requisitos |
|---|---|---|---|---|---|
| D-01 | <dúvida em uma frase> | <o que fica valendo> | <usuário, analista de negócio, requisito de sistema ou código> | <N-xx ou "etapa de sistema"> | <RF-xx, RNF-xx ou "Fora do escopo"> |

## Divergências aceitas da análise de negócio

Pontos em que os requisitos não seguem a análise de negócio, por decisão registrada. Divergir é aceitável; divergir sem explicação, não.

| # | A análise de negócio diz | Fica valendo | Motivo | Decidido por |
|---|---|---|---|---|
| D-xx | <Req. n: o que diz> | <o que vale> | <por quê> | <quem> |

<Sem divergências, troque a tabela por "Nenhuma: os requisitos seguem a análise de negócio.">

## Premissas

- <o que foi adotado sem confirmação explícita, e por quê (ex.: segue o comportamento atual)>

## Cobertura da análise de negócio

| Req. | Assunto | Atendido por |
|---|---|---|
| 1 | <assunto> | <RF-xx; "Fora do escopo (D-xx)"; ou "Divergência aceita (D-xx)"> |

## Rastreabilidade dos requisitos de sistema

| # | Trecho | Atendido por |
|---|---|---|
| P-01 | "<trecho literal dos requisitos de sistema>" | <RF-xx, RNF-xx ou "Fora do escopo (D-xx)"> |

## Pendências

Nenhuma.

<Se algo ficou em aberto por decisão do usuário, troque "Nenhuma." pela lista: "- <o que falta decidir> — <quem decide>; enquanto isso: <premissa adotada>".>
