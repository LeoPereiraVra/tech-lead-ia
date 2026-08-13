# Tech Lead IA

Ferramentas para auxiliar o techlead no dia a dia.

Este repositório é um [marketplace de plugins do Claude Code](https://code.claude.com/docs/en/plugin-marketplaces) contendo o plugin `tech-lead-ia`, que reúne skills voltadas para o dia a dia de um tech lead.

## Instalação

```
/plugin marketplace add LeoPereiraVra/tech-lead-ia
/plugin install tech-lead-ia@tech-lead-ia
```

## Skills disponíveis

- **refinar-requisitos** — refina requisitos funcionais e técnicos antes da implementação, investigando a arquitetura e o código do projeto e conduzindo uma entrevista de decisões, uma pergunta por vez, até obter entendimento mútuo. Gera um documento `*-refinado.md` pronto para orientar a implementação.

## Estrutura do repositório

```
.claude-plugin/
  marketplace.json          # catálogo do marketplace
plugins/
  tech-lead-ia/
    .claude-plugin/
      plugin.json            # manifesto do plugin
    skills/
      refinar-requisitos/
        SKILL.md
```

## Desenvolvimento

Para testar localmente antes de publicar:

```
/plugin marketplace add ./tech-lead-ia
/plugin install tech-lead-ia@tech-lead-ia
```

Após alterações, atualize a versão em `plugins/tech-lead-ia/.claude-plugin/plugin.json` e rode `/plugin marketplace update` para recarregar.
