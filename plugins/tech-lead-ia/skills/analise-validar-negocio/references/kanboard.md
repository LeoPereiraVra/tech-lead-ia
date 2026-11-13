# Ler a análise de negócios no Kanboard

Use só quando a análise não está num arquivo da pasta `.agents/#<card>/` nem num caminho informado pelo analista. O Kanboard é só fonte: não escreva nada nele (comentário, anexo, tag, movimentação).

## Ferramentas (MCP `kanboard-sci`)

| Ferramenta | Argumentos | Para quê |
|---|---|---|
| `mcp__kanboard-sci__consultar_cartao_completo` | `{"task_id": <card>, "modo": "completo"}` | descrição, requisitos com o campo "Análise de negócios", comentários e lista de anexos |
| `mcp__kanboard-sci__baixar_anexo` | `{"task_id": <card>, "file_id": <id do anexo>, "confirmar": true}` | baixa o documento da análise e as imagens; devolve o `caminho` do arquivo |

- O número do card é o `task_id`: no link `https://kanboard.sci.com.br/t/250514`, é `250514`.
- Use sempre `"modo": "completo"`. O modo `fluxo` não traz a descrição nem o texto dos requisitos.
- `baixar_anexo` exige `"confirmar": true`, mas só grava o arquivo na pasta `downloads/` do próprio MCP; o card não muda.

## Onde está a análise no card

1. **Documento anexo**: o anexo cujo nome termina em `analise_negocio_V<n>` (em geral `<card>_analise_negocio_V<n>.md`). Vale o maior `<n>`. Cards antigos podem ter `.docx` ou `.pdf`; leia com a skill do formato.
2. **Requisitos do card** (`requisitos_funcionais`): títulos `R01 - <assunto>`, com as regras no campo "Análise de negócios" (`business_analysis`). Podem ter sido editados depois do documento.
3. **Descrição e comentários**: o pedido original e, depois da primeira rodada, possíveis respostas do analista de negócios.

Sem documento anexo, a análise é o que estiver nos requisitos do card e na descrição; diga isso ao analista. Sem documento e sem requisito com "Análise de negócios" preenchida, a análise ainda não foi publicada: avise e pergunte se ele vai passar a análise por arquivo.

## Registrar o que foi lido

Grave uma cópia fiel do documento (ou dos requisitos do card, se não houver documento) em `agentes/analise-negocios-recebida.md`, com esta linha no topo:

> Lida do card [#<card>](https://kanboard.sci.com.br/t/<card>), documento <nome do anexo> (anexo <id>), em <data>.

Nas rodadas seguintes, releia o card e compare com essa linha. Se houver documento novo, requisito alterado ou comentário novo, diga ao analista o que mudou e grave a versão nova antes de revalidar.

## Quando a leitura falha

| O que acontece | O que fazer |
|---|---|
| As ferramentas `mcp__kanboard-sci__*` não existem na sessão | O MCP não está configurado. Peça ao analista para salvar a análise na pasta `.agents/#<card>/`. |
| `AUTENTICAÇÃO WEB NECESSÁRIA: abra o link…` | Mostre o link e peça para abrir no navegador e responder **ok**. Nunca peça a senha no chat. |
| `O cartão não pertence a um quadro autorizado.` | O MCP só lê os quadros Inovação, Manutenção e Refinamento. Peça a análise por arquivo. |
| `Cartão não encontrado ou indisponível.` | Confira o número com o analista. |
| Credenciais ausentes ou inválidas, ou erro de rede | Explique o erro e peça a análise por arquivo, ou para tentar de novo depois de corrigir. |
