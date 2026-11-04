---
name: analise-requisitos
description: 'Conduz o refinamento de requisitos de uma solicitação (card) de ponta a ponta, da análise de negócio até o arquivo final que vai para o dev. A etapa 1 levanta lacunas e divergências da análise e prepara as perguntas ao analista; depois há uma pausa para os requisitos de sistema; a etapa 2 gera a análise de sistemas, com RF/RNF e decisões, e o arquivo final; a etapa 3 valida. Retoma de onde parou pelos arquivos em .agents/analises/#<card>/. Use sempre que o usuário pedir para refinar uma solicitação ou card, fazer o refinamento de requisitos, rodar todas as etapas ou continuar um refinamento, mesmo sem citar as etapas pelo nome. Não use para escrever a análise de negócio (sci-analise-negocio) nem para implementar (tlc-spec-driven).'
argument-hint: '<número do card> [caminho da análise de negócio ou dos requisitos de sistema]'
---

# Refinamento de requisitos

Transforma a análise de negócio de uma solicitação num arquivo que o dev consegue desenvolver sem voltar com dúvidas. O caminho tem três etapas, cada uma com a sua skill, e uma pausa no meio, porque a etapa 2 depende dos requisitos que o analista de sistemas escreve depois de ler a etapa 1.

```
Análise de negócio
  │
  ├─ Etapa 1 · analise-negocio ─→ analise-negocios.md
  │     lacunas e divergências; perguntas para o analista de negócio
  │
  ⏸  o analista de sistemas lê a etapa 1 e escreve os requisitos de sistema
  │
  ├─ Etapa 2 · analise-sistema ─→ analise-sistemas.md + #<card>-analise-final.md
  │     RF/RNF, decisões, divergências aceitas, rastreabilidade; resumo para o dev
  │
  └─ Etapa 3 · analise-validar ─→ validacao.md
        arquivo final × análise inicial; nada em aberto sem o usuário saber
```

Cada etapa também pode ser chamada sozinha. Esta skill descobre qual etapa vem agora e encadeia as demais.

## Pasta da solicitação

Tudo fica em `.agents/analises/#<card>/`, na raiz do projeto aberto (crie a pasta quando não existir). Nos comandos de terminal, ponha o caminho entre aspas, porque um `#` no início de uma palavra vira comentário no shell.

| Arquivo | Gravado por | Para quem |
|---|---|---|
| `analise-negocios.md` | etapa 1 | analista de negócio (perguntas) e analista de sistemas |
| `requisitos-sistema.md` | etapa 2, só quando os requisitos chegam como texto | registro da entrada |
| `analise-sistemas.md` | etapa 2 | registro detalhado; base da etapa 3 |
| `#<card>-analise-final.md` | etapa 2, ajustado na etapa 3 | dev: é o único arquivo enviado a ele |
| `validacao.md` | etapa 3 | registro da validação |

## Recursos comuns

Ficam nesta skill e valem para as quatro. As skills de etapa os acessam em `<skills>/analise-requisitos/`, onde `<skills>` é a pasta que contém as skills (por exemplo, `.agents/skills` ou `.claude/skills`).

- `references/perguntas.md`: como montar e fazer as perguntas (caixa de perguntas, opções, múltipla escolha, registro das respostas).
- `references/analise-codigo.md`: onde e como procurar lacunas e divergências no código.
- `scripts/verificar.py`: checagens de estrutura dos arquivos, com os modos `negocio`, `sistema`, `final` e `tudo`. Rode com `python3` (no Windows, `py -3` ou `python`). ERRO pede correção antes de seguir; AVISO pede conferência.

## Como conduzir

### 1. Identificar a solicitação

Pegue o número do card no argumento, no nome do arquivo indicado (`#253954-...`), no título da análise (`# 253954 — ...`) ou no link do Kanboard. Se não achar em nenhum deles, pergunte. Guarde também o que o usuário já trouxe: caminho da análise de negócio, requisitos de sistema, respostas do analista.

### 2. Ver em que ponto está

| O que existe na pasta | Próximo passo |
|---|---|
| nada, ou falta `analise-negocios.md` | etapa 1 |
| `analise-negocios.md`, sem `analise-sistemas.md` | pausa: pedir os requisitos de sistema; com eles, etapa 2 |
| `analise-sistemas.md`, sem o arquivo final | etapa 2, retomando pela conferência final e pelo arquivo final |
| arquivo final, sem `validacao.md` | etapa 3 |
| `validacao.md` | informar o resultado e perguntar se quer refazer alguma etapa |

Diga ao usuário, em uma linha, o que encontrou e qual etapa vai rodar. Se ele pediu para começar de novo e já existem arquivos, pergunte antes de sobrescrever.

### 3. Rodar a etapa

Chame a skill da etapa (no Claude Code, pela ferramenta Skill; em outros agentes, leia o `SKILL.md` dela por inteiro e siga). Passe o card, a pasta e as entradas que você já tem, para ela não perguntar de novo.

### 4. Pausar depois da etapa 1

Depois da etapa 1, pare. As perguntas para o analista de negócio estão no arquivo, prontas para enviar, e a etapa 2 precisa dos requisitos de sistema, que ainda não existem. Encerre dizendo:
- onde está `analise-negocios.md` e quantas perguntas foram para o analista;
- que a seção "Perguntas para o analista de negócio" pode ser copiada e enviada;
- que, com os requisitos de sistema (arquivo ou texto) e as respostas do analista, basta chamar `/analise-requisitos <card>` de novo.

Se o usuário já trouxe os requisitos de sistema nesta conversa, pergunte se pode seguir direto para a etapa 2.

### 5. Validar logo depois da etapa 2

Ao terminar a etapa 2, rode a etapa 3 sem pausa. A validação fecha o refinamento, e o arquivo final só deve ir para o dev depois dela.

### 6. Encerrar

Ao final da etapa 3, diga o resultado da validação, o caminho do `#<card>-analise-final.md` (o arquivo que vai para o dev) e as pendências que o usuário aceitou deixar abertas, se houver.

## Princípios das três etapas

- **Fato se procura, decisão se pergunta.** O que o código, a análise ou os requisitos respondem, você mesmo descobre. Ao usuário vão só as decisões. Uma pergunta que o código responderia gasta a atenção dele e a confiança no processo.
- **Nenhuma dúvida some.** Cada lacuna termina perguntada, respondida, assumida como premissa ou descartada pelo usuário, e o arquivo diz qual das quatro. Dúvida esquecida volta como retrabalho no desenvolvimento.
- **Divergir pode; divergir sem explicação, não.** O usuário pode decidir diferente da análise de negócio. O arquivo registra o que a análise dizia, o que vale e por quê.
- **Sem invenção.** "O sistema faz X hoje" só com evidência do código. O que você não achou, diga que não achou.
- **Só leitura no código.** As skills não alteram código, banco nem git. Gravam apenas na pasta da solicitação.
- **O arquivo é a memória.** Grave as respostas no arquivo da etapa à medida que chegam. A conversa pode ser compactada; o arquivo, não.
- **Português do Brasil** nas mensagens, nas perguntas e nos arquivos.
