---
tags: [skill-creator]
max_turns: 120
timeout_seconds: 3600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

voltei com as respostas das dúvidas do card 250514 (o analista de negócios respondeu a D2, D3, D6 e D7, o resto eu decidi):

D1: são três permissões separadas, Geral, Grupos de notificação e Notificações enviadas. Na liberação Geral e Grupos copiam o valor atual da Central, depois cada uma é independente e a Central só agrupa
D2: isso, o log registra o envio (sucesso ou erro com motivo, mensagem e variáveis), a troca de número e a conexão/desconexão, gravado igual a api-atendimento grava hoje e aparecendo na tela Logs do painel. templates e data de vínculo ficam de fora
D3: o que aparece hoje na consulta do 24H continua aparecendo no 24H
D4: segue como hoje, não vamos gravar a empresa nos envios agora
D5: segue como hoje, vê de todas as empresas e só o campo Empresa fica restrito
D6: opção c, fica como atalho com o alerta e sai numa versão futura, sem prazo
D7: igual ao grid
D8: sim, qualquer alteração salva vai pro log

Input files: .agents/#250514/analise-negocios.md, .agents/#250514/agentes/duvidas-negocios.md
