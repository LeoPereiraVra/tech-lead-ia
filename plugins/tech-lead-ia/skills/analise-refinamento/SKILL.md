---
name: analise-refinamento
description: "Conduz o refinamento completo de uma solicitação (card #123456), da validação da análise de negócios até a análise de sistema final, chamando as skills analise-validar-negocio e analise-sistema na ordem certa. Descobre pelos arquivos em .agents/#<card>/ em que ponto o refinamento está e continua de lá: se a validação de negócios já terminou, segue para a análise de sistema. Use quando o analista pedir para refinar um card, fazer, continuar ou retomar o refinamento, rodar o processo inteiro ou ver em que ponto um card está, mesmo sem citar as etapas."
argument-hint: "<número do card>"
---

# Refinamento de uma solicitação

Esta skill não analisa nada sozinha. Ela descobre em que ponto o refinamento está, chama a skill da etapa certa e para nos momentos em que o processo depende do analista. As duas etapas também podem ser chamadas diretamente; esta skill serve para o analista não precisar lembrar qual vem agora.

```
[Analista de negócios]  escreve a análise de negócios a partir da história do usuário
[Analista de sistemas]  passa a análise para a IA (arquivo em .agents/#<card>/)
[IA]                    analise-validar-negocio, rodada 1 → agentes/duvidas-negocios.md
   ⏸ pausa A            o analista responde as dúvidas (ele mesmo ou com o analista de negócios)
[IA]                    analise-validar-negocio, revalidação → agentes/decisoes.md e agentes/analise-negocios-resumo.md
   ⏸ pausa B            o analista de sistemas escreve .agents/#<card>/analise-sistema.md
[IA]                    analise-sistema → agentes/duvidas-sistema.md, decisoes.md e agentes/analise-sistema-final.md
```

## Dependências

As skills `analise-validar-negocio` e `analise-sistema` precisam estar instaladas ao lado desta (na mesma pasta de skills). Se uma delas faltar, diga qual e pare: sem elas, esta skill não tem o que orquestrar.

## 1. Identificar a solicitação

O número do card vem do argumento, do link do Kanboard (`https://kanboard.sci.com.br/t/250514` é o card 250514), do nome da pasta ou da mensagem. Sem número, pergunte. Guarde também o que o analista já trouxe na mensagem (caminho da análise, respostas das dúvidas, análise de sistema), para passar à etapa e ela não perguntar de novo.

A pasta é `.agents/#<card>/`, com os arquivos da IA em `.agents/#<card>/agentes/`. No terminal, ponha o caminho entre aspas, porque `#` no início de uma palavra vira comentário no shell.

## 2. Ver em que ponto está

Liste as duas pastas e confira as perguntas abertas. Uma pergunta (D ou S) está aberta quando aparece em `duvidas-*.md` e não tem entrada com o mesmo ID em `decisoes.md`.

| Situação | Próximo passo |
|---|---|
| Nenhuma análise de negócios na pasta, nem caminho informado | chame `analise-validar-negocio`; ela procura no Kanboard ou pede o arquivo |
| Sem `agentes/duvidas-negocios.md` | `analise-validar-negocio`, rodada 1. Depois, pausa A |
| Dúvidas D abertas, e o analista trouxe respostas | `analise-validar-negocio`, para registrar e revalidar |
| Dúvidas D abertas, sem respostas | mostre as perguntas abertas e pergunte se ele quer responder agora. Se não, pausa A |
| Nenhuma dúvida D aberta e sem `agentes/analise-negocios-resumo.md` | `analise-validar-negocio`, para revalidar e gerar o resumo |
| Resumo pronto e sem `.agents/#<card>/analise-sistema.md` | pausa B |
| `analise-sistema.md` presente e sem `agentes/analise-sistema-final.md`, ou com dúvidas S abertas | `analise-sistema` |
| `agentes/analise-sistema-final.md` pronto | diga que o refinamento terminou. Se `analise-sistema.md`, `decisoes.md` ou a análise de negócios forem mais recentes que a análise final, diga isso e pergunte se ele quer atualizar |

Diga ao analista, em uma linha, o que encontrou e o que vai fazer. Se ele pediu para recomeçar e já existem arquivos em `agentes/`, pergunte antes de sobrescrever.

## 3. Chamar a etapa

No Claude Code, chame a skill pela ferramenta Skill, passando o card e o que você já sabe. Em outros agentes (Codex), leia o `SKILL.md` da etapa por inteiro, na pasta de skills ao lado desta, e siga as instruções dela.

A etapa conduz o trabalho dela até o fim, inclusive as perguntas ao analista. Quando ela terminar, volte ao passo 2 e veja se dá para seguir sem pausa. Por exemplo, se o analista respondeu as dúvidas na hora e o resumo saiu, a próxima situação é a pausa B. Se ele já tinha escrito `analise-sistema.md`, siga direto para `analise-sistema`.

## 4. Pausas

As pausas existem porque a etapa seguinte depende de algo que só o analista pode fazer. Ao parar, diga exatamente o que falta e como continuar.

**Pausa A — respostas das dúvidas de negócio.** Diga:
- onde está `agentes/duvidas-negocios.md` e quantas perguntas estão abertas;
- que a lista "Dúvidas" no fim do arquivo pode ser enviada ao analista de negócios;
- que, com as respostas, basta chamar `/analise-refinamento <card>` de novo, trazendo-as na conversa ("D1: ...") ou escritas no próprio arquivo, abaixo de cada pergunta.

**Pausa B — análise de sistema do analista.** Diga:
- onde está `agentes/analise-negocios-resumo.md`, que é a base para a análise de sistema;
- que o analista de sistemas escreve `.agents/#<card>/analise-sistema.md` com os requisitos que pensou para a solução, complementando a análise de negócios: arquitetura, segurança, escalabilidade e manutenção, sem trechos de código, a não ser como exemplo;
- quais diferenças em relação à análise de negócios o resumo registrou, para avisar o analista de negócios;
- que, com o arquivo pronto, basta chamar `/analise-refinamento <card>` de novo.

## 5. Encerrar

Ao final da análise de sistema, diga:
- o caminho de `agentes/analise-sistema-final.md` e de `agentes/analise-negocios-resumo.md`;
- que o desenvolvimento recebe a análise de negócios (ou o resumo) junto com a análise de sistema final, porque uma complementa a outra;
- quantas decisões foram registradas em `agentes/decisoes.md` e quais divergem da análise de negócios;
- as pendências que o analista aceitou deixar abertas, se houver.

## Princípios

- **O arquivo é o estado.** O refinamento acontece em dias e conversas diferentes. O ponto em que ele está se descobre pelos arquivos, e não pela memória da conversa.
- **Não pule a pausa.** Sem as respostas do analista, a revalidação inventaria decisões; sem a análise de sistema dele, a etapa de sistema não tem o que validar.
- **Português do Brasil** nas mensagens e nos arquivos.
