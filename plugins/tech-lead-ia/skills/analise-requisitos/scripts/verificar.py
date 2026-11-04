#!/usr/bin/env python3
"""Checagens de estrutura dos arquivos do refinamento de requisitos.

Uso:
    python3 verificar.py negocio "<pasta>"
    python3 verificar.py sistema "<pasta>"
    python3 verificar.py final   "<pasta>"
    python3 verificar.py tudo    "<pasta>"

<pasta> é a pasta da solicitação, por exemplo ".agents/analises/#253954"
(entre aspas: no shell, "#" no início de uma palavra começa um comentário).

Cada problema sai numa linha começando com ERRO ou AVISO:
- ERRO: corrija antes de seguir para a próxima etapa;
- AVISO: confira; pode estar certo.

Código de saída: 0 sem erros, 1 com erros, 2 quando falta um arquivo
esperado ou o uso está errado.

As checagens são de estrutura (seções, IDs, tabelas, referências cruzadas).
O julgamento do conteúdo continua com quem faz o refinamento.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ARQ_NEGOCIO = "analise-negocios.md"
ARQ_SISTEMA = "analise-sistemas.md"

SECOES_NEGOCIO = [
    "Contexto",
    "O que precisa ser feito",
    "Fora do escopo",
    "Impactos no sistema",
    "Perguntas para o analista de negócio",
    "Pontos levantados",
]

SECOES_SISTEMA = [
    "Objetivo",
    "Escopo",
    "Comportamento atual",
    "Atores e permissões",
    "Requisitos funcionais",
    "Requisitos não funcionais",
    "Dúvidas e decisões",
    "Divergências aceitas da análise de negócio",
    "Premissas",
    "Cobertura da análise de negócio",
    "Rastreabilidade dos requisitos de sistema",
    "Pendências",
]

SITUACOES = [
    "Perguntar ao analista",
    "Respondido pelo usuário",
    "Respondido pelo analista",
    "Resolvido pelo código",
    "Descartado",
]

CAMPOS_PONTO = ["Tipo", "Onde", "O que foi encontrado", "Por que importa", "Situação", "Resposta"]

RE_CERCA = re.compile(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", re.S | re.M)
RE_CODIGO_INLINE = re.compile(r"`[^`\n]*`")
RE_CAMPO = re.compile(r"^\s*[-*]\s*\*\*([^*:]+):\*\*\s*(.*)$")
RE_ID_FINAL = re.compile(r"\b(?:RF|RNF|D|P|N|V)-\d+\b|\bReq\.\s*\d+")
RE_ARQUIVOS = re.compile(r"analise-negocios|analise-sistemas|requisitos-sistema|validacao\.md", re.I)
RE_FRASES_REF = re.compile(
    r"an[aá]lise de neg[oó]cios?|an[aá]lise de sistemas?|requisitos? de sistemas?|analista de neg[oó]cios?",
    re.I,
)
RE_PLACEHOLDER_ID = re.compile(r"\b[A-Z]{1,3}-xx\b")
RE_ANGULAR = re.compile(r"<([^<>\n]+)>")
VAZIOS = {"", "-", "—", "–", "?"}


class Relatorio:
    def __init__(self) -> None:
        self.itens: list[tuple[str, str, str]] = []
        self.faltando = False

    def erro(self, arquivo: str, msg: str) -> None:
        self.itens.append(("ERRO", arquivo, msg))

    def aviso(self, arquivo: str, msg: str) -> None:
        self.itens.append(("AVISO", arquivo, msg))

    def falta(self, arquivo: str) -> None:
        self.faltando = True
        self.erro(arquivo, "arquivo não encontrado.")

    @property
    def tem_erro(self) -> bool:
        return any(nivel == "ERRO" for nivel, _, _ in self.itens)

    def imprimir(self) -> None:
        for nivel, arquivo, msg in self.itens:
            print(f"{nivel}: {arquivo}: {msg}")
        erros = sum(1 for nivel, _, _ in self.itens if nivel == "ERRO")
        avisos = len(self.itens) - erros
        if not self.itens:
            print("OK: nenhum problema de estrutura encontrado.")
        print(f"Resumo: {erros} erro(s), {avisos} aviso(s).")


# ---------------------------------------------------------------- utilidades


def ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8-sig")


def sem_cercas(texto: str) -> str:
    """Apaga os blocos de código cercados, mantendo a numeração das linhas."""
    return RE_CERCA.sub(lambda m: "\n" * m.group(0).count("\n"), texto)


def sem_codigo_inline(texto: str) -> str:
    return RE_CODIGO_INLINE.sub(lambda m: " " * len(m.group(0)), texto)


def secoes(texto: str) -> dict[str, str]:
    """Seções de nível 2, na ordem: {título: conteúdo até o próximo '## '}."""
    resultado: dict[str, str] = {}
    atual: str | None = None
    linhas: list[str] = []
    for linha in texto.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", linha)
        if m:
            if atual is not None:
                resultado[atual] = "\n".join(linhas)
            atual, linhas = m.group(1).strip(), []
        elif atual is not None:
            linhas.append(linha)
    if atual is not None:
        resultado[atual] = "\n".join(linhas)
    return resultado


def secao(sec: dict[str, str], titulo: str) -> str | None:
    for chave, conteudo in sec.items():
        if chave.lower() == titulo.lower():
            return conteudo
    return None


def blocos(texto: str, padrao_id: str) -> tuple[dict[str, str], list[str]]:
    """Blocos '### <ID> ...' até o próximo '##' ou '###'. Devolve (blocos, duplicados)."""
    resultado: dict[str, str] = {}
    duplicados: list[str] = []
    atual: str | None = None
    corpo: list[str] = []
    for linha in texto.splitlines():
        if re.match(r"^#{2,3}\s", linha):
            if atual is not None:
                resultado[atual] = "\n".join(corpo)
            atual, corpo = None, []
            m = re.match(rf"^###\s+({padrao_id})\b", linha)
            if m:
                atual = m.group(1)
                if atual in resultado:
                    duplicados.append(atual)
            continue
        if atual is not None:
            corpo.append(linha)
    if atual is not None:
        resultado[atual] = "\n".join(corpo)
    return resultado, duplicados


def dividir_celulas(linha: str) -> list[str]:
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def linhas_tabela(conteudo: str | None) -> list[list[str]]:
    """Linhas de dados das tabelas do trecho, sem cabeçalho nem separador."""
    linhas: list[list[str]] = []
    for linha in (conteudo or "").splitlines():
        if not linha.strip().startswith("|"):
            continue
        celulas = dividir_celulas(linha)
        if celulas and all(re.fullmatch(r":?-{3,}:?", c) for c in celulas):
            if linhas:
                linhas.pop()  # a linha anterior era o cabeçalho
            continue
        linhas.append(celulas)
    return linhas


def campos(corpo: str) -> dict[str, str]:
    """Campos '- **Nome:** valor' de um bloco (linhas seguintes continuam o valor)."""
    resultado: dict[str, str] = {}
    atual: str | None = None
    for linha in corpo.splitlines():
        m = RE_CAMPO.match(linha)
        if m:
            atual = m.group(1).strip()
            resultado[atual] = m.group(2).strip()
        elif atual and linha.strip():
            resultado[atual] = (resultado[atual] + " " + linha.strip()).strip()
    return resultado


def vazio(valor: str) -> bool:
    return valor.strip() in VAZIOS


def tem_texto(conteudo: str | None) -> bool:
    return bool(conteudo and re.search(r"\w", conteudo))


def ordem(identificador: str) -> tuple[str, int]:
    prefixo, _, numero = identificador.partition("-")
    return (prefixo, int(numero) if numero.isdigit() else 0)


def checar_secoes(nome: str, sec: dict[str, str], esperadas: list[str], rel: Relatorio) -> None:
    for titulo in esperadas:
        if secao(sec, titulo) is None:
            rel.erro(nome, f'falta a seção "## {titulo}".')


def checar_modelo(nome: str, bruto: str, rel: Relatorio) -> None:
    """Texto do modelo que ficou sem preencher: <instrução>, N-xx, <card>, dd/mm."""
    texto = sem_codigo_inline(sem_cercas(bruto))
    for n, linha in enumerate(texto.splitlines(), 1):
        for m in RE_ANGULAR.finditer(linha):
            conteudo = m.group(1).strip()
            if conteudo.startswith(("/", "!", "http")) or "=" in conteudo:
                continue  # tag HTML, comentário ou link automático
            if " " in conteudo or "xx" in conteudo or conteudo == "card" or "dd/mm" in conteudo:
                rel.erro(nome, f'linha {n}: "{m.group(0)}" parece texto do modelo que não foi preenchido.')
        for m in RE_PLACEHOLDER_ID.finditer(linha):
            rel.erro(nome, f'linha {n}: "{m.group(0)}" parece ID do modelo que não foi preenchido.')


# ------------------------------------------------------------------ etapa 1


def verificar_negocio(pasta: Path, rel: Relatorio) -> dict[str, str] | None:
    """Confere analise-negocios.md e devolve {N-xx: situação}."""
    nome = ARQ_NEGOCIO
    arquivo = pasta / nome
    if not arquivo.is_file():
        rel.falta(nome)
        return None
    bruto = ler(arquivo)
    texto = sem_cercas(bruto)
    sec = secoes(texto)
    checar_secoes(nome, sec, SECOES_NEGOCIO, rel)

    if secao(sec, "O que precisa ser feito") is not None and not tem_texto(secao(sec, "O que precisa ser feito")):
        rel.erro(nome, 'a seção "O que precisa ser feito" está vazia.')

    pontos, duplicados = blocos(texto, r"N-\d+")
    for pid in duplicados:
        rel.erro(nome, f'{pid} tem mais de um bloco "### {pid}".')

    na_tabela = {
        linha[0]
        for linha in linhas_tabela(secao(sec, "Pontos levantados"))
        if linha and re.fullmatch(r"N-\d+", linha[0])
    }
    for pid in sorted(set(pontos) - na_tabela, key=ordem):
        rel.erro(nome, f"{pid} tem bloco de detalhe, mas não está na tabela de Pontos levantados.")
    for pid in sorted(na_tabela - set(pontos), key=ordem):
        rel.erro(nome, f'{pid} está na tabela de Pontos levantados, mas não tem o bloco "### {pid} — ...".')

    situacoes_validas = {s.lower(): s for s in SITUACOES}
    situacoes: dict[str, str] = {}
    for pid, corpo in sorted(pontos.items(), key=lambda item: ordem(item[0])):
        valores = campos(corpo)
        for campo in CAMPOS_PONTO:
            if campo not in valores:
                rel.erro(nome, f'{pid}: falta o campo "**{campo}:**".')
        if "Situação" not in valores:
            continue
        situacao = valores["Situação"].strip().rstrip(".").lower()
        if situacao not in situacoes_validas:
            rel.erro(
                nome,
                f'{pid}: situação "{valores["Situação"]}" fora das previstas ({", ".join(SITUACOES)}).',
            )
            continue
        situacoes[pid] = situacoes_validas[situacao]
        if situacao != "perguntar ao analista" and vazio(valores.get("Resposta", "")):
            rel.erro(nome, f'{pid}: a situação é "{situacoes_validas[situacao]}", mas a Resposta está vazia.')

    perguntas = secao(sec, "Perguntas para o analista de negócio") or ""
    nas_perguntas = set(re.findall(r"\bN-\d+\b", perguntas))
    para_analista = {pid for pid, s in situacoes.items() if s == "Perguntar ao analista"}
    for pid in sorted(para_analista - nas_perguntas, key=ordem):
        rel.erro(
            nome,
            f'{pid} está para perguntar ao analista, mas não aparece em "Perguntas para o analista de negócio".',
        )
    for pid in sorted(nas_perguntas - para_analista, key=ordem):
        rel.aviso(nome, f'{pid} aparece nas perguntas ao analista, mas a situação dele não é "Perguntar ao analista".')
    if not para_analista and not re.search(r"\bnenhuma\b", perguntas, re.I):
        rel.aviso(nome, 'nenhum ponto vai para o analista; escreva "Nenhuma." em "Perguntas para o analista de negócio".')

    if not pontos:
        rel.aviso(nome, "nenhum ponto N-xx levantado; confira se a análise realmente não tem lacunas nem divergências.")

    checar_modelo(nome, bruto, rel)
    return situacoes


# ------------------------------------------------------------------ etapa 2


def verificar_sistema(pasta: Path, rel: Relatorio, situacoes: dict[str, str] | None) -> None:
    nome = ARQ_SISTEMA
    arquivo = pasta / nome
    if not arquivo.is_file():
        rel.falta(nome)
        return
    bruto = ler(arquivo)
    texto = sem_cercas(bruto)
    sec = secoes(texto)
    checar_secoes(nome, sec, SECOES_SISTEMA, rel)

    # Requisitos
    rfs, dup_rf = blocos(texto, r"RF-\d+")
    rnfs, dup_rnf = blocos(texto, r"RNF-\d+")
    for rid in dup_rf + dup_rnf:
        rel.erro(nome, f'{rid} tem mais de um bloco "### {rid}".')
    if not rfs and not rnfs:
        rel.erro(nome, 'nenhum requisito encontrado ("### RF-01 — ..." ou "### RNF-01 — ...").')
    for rid, corpo in sorted(rfs.items(), key=lambda item: ordem(item[0])):
        if not re.search(r"crit[ée]rios de aceite", corpo, re.I):
            rel.erro(nome, f"{rid}: faltam os critérios de aceite.")
        elif not re.search(r"\bdad[oa]s?\b.*\bent[ãa]o\b", corpo, re.I | re.S):
            rel.aviso(nome, f'{rid}: critérios de aceite fora do formato "Dado…, quando…, então…".')
        if not re.search(r"\borigem\s*:", corpo, re.I):
            rel.erro(nome, f"{rid}: falta a origem.")
    for rid, corpo in sorted(rnfs.items(), key=lambda item: ordem(item[0])):
        if not re.search(r"verifica[çc][ãa]o\s*:", corpo, re.I):
            rel.erro(nome, f"{rid}: falta a verificação.")
        if not re.search(r"\borigem\s*:", corpo, re.I):
            rel.erro(nome, f"{rid}: falta a origem.")

    definidos = set(rfs) | set(rnfs)
    for rid in sorted(set(re.findall(r"\bRN?F-\d+\b", texto)) - definidos, key=ordem):
        rel.erro(nome, f'{rid} é citado, mas não existe o bloco "### {rid} — ...".')

    # Dúvidas e decisões
    tabela_decisoes = secao(sec, "Dúvidas e decisões") or ""
    decisoes: dict[str, list[str]] = {}
    for linha in linhas_tabela(tabela_decisoes):
        if not linha or not re.fullmatch(r"D-\d+", linha[0]):
            continue
        did = linha[0]
        if did in decisoes:
            rel.erro(nome, f"{did} aparece duas vezes na tabela de Dúvidas e decisões.")
        decisoes[did] = linha
        if len(linha) < 6:
            rel.erro(
                nome,
                f"{did}: a linha deveria ter 6 colunas (# | Dúvida | Decisão | Decidido por | Origem | Requisitos).",
            )
            continue
        if vazio(linha[2]) or re.search(r"pendente|a definir|\?\s*$", linha[2], re.I):
            rel.erro(nome, f"{did}: decisão vazia ou pendente; pergunte ao usuário ou mova o ponto para Pendências.")
        if vazio(linha[3]):
            rel.erro(nome, f"{did}: falta quem decidiu.")
        if vazio(linha[5]):
            rel.aviso(nome, f"{did}: não diz quais requisitos a decisão afeta.")
    if not decisoes:
        rel.aviso(nome, "nenhuma decisão D-xx registrada; confira se nenhuma dúvida foi levantada nas duas etapas.")

    citadas = set(re.findall(r"\bD-\d+\b", texto))
    for did in sorted(citadas - set(decisoes), key=ordem):
        rel.erro(nome, f"{did} é citada, mas não está na tabela de Dúvidas e decisões.")
    fora_da_tabela = texto.replace(tabela_decisoes, "") if tabela_decisoes else texto
    for did in sorted(set(decisoes) - set(re.findall(r"\bD-\d+\b", fora_da_tabela)), key=ordem):
        rel.aviso(nome, f"{did} não é citada em nenhum requisito, escopo ou cobertura.")

    # Divergências aceitas
    divergencias = secao(sec, "Divergências aceitas da análise de negócio")
    if divergencias is not None:
        linhas_div = [l for l in linhas_tabela(divergencias) if l and re.fullmatch(r"D-\d+", l[0])]
        if not linhas_div and not re.search(r"\bnenhuma\b", divergencias, re.I):
            rel.erro(nome, 'a seção "Divergências aceitas da análise de negócio" deve ter a tabela ou dizer "Nenhuma".')
        for linha in linhas_div:
            if linha[0] not in decisoes:
                rel.erro(nome, f"{linha[0]} está nas divergências aceitas, mas não na tabela de Dúvidas e decisões.")
            if len(linha) < 5 or any(vazio(c) for c in linha[1:5]):
                rel.erro(
                    nome,
                    f"{linha[0]}: divergência aceita sem todas as colunas (o que a análise diz, o que vale, motivo, quem decidiu).",
                )

    # Cobertura e rastreabilidade
    cobertura = secao(sec, "Cobertura da análise de negócio")
    if cobertura is not None:
        linhas_cob = linhas_tabela(cobertura)
        if not linhas_cob:
            rel.erro(nome, "a Cobertura da análise de negócio está vazia: cada requisito da análise precisa de destino.")
        for linha in linhas_cob:
            if len(linha) < 2 or vazio(linha[-1]):
                rel.erro(nome, f'Cobertura: o requisito "{linha[0]}" está sem "Atendido por".')
    rastreabilidade = secao(sec, "Rastreabilidade dos requisitos de sistema")
    if rastreabilidade is not None:
        linhas_ras = linhas_tabela(rastreabilidade)
        if not linhas_ras:
            rel.erro(nome, "a Rastreabilidade dos requisitos de sistema está vazia: cada trecho P-xx precisa de destino.")
        for linha in linhas_ras:
            if len(linha) < 2 or vazio(linha[-1]):
                rel.erro(nome, f'Rastreabilidade: "{linha[0]}" está sem "Atendido por".')

    # Pendências
    pendencias = secao(sec, "Pendências")
    if pendencias is not None:
        itens = [l for l in pendencias.splitlines() if re.match(r"^\s*(?:[-*]|\d+\.)\s+\S", l)]
        if itens:
            rel.aviso(nome, f"há {len(itens)} pendência(s) em aberto; confirme com o usuário que podem ficar abertas.")
        elif not re.search(r"\bnenhuma\b", pendencias, re.I):
            rel.erro(nome, 'a seção "Pendências" deve listar as pendências ou dizer "Nenhuma."')

    # Pontos da etapa 1
    if situacoes is None:
        rel.aviso(nome, f"sem {ARQ_NEGOCIO}: os pontos N-xx da etapa 1 não foram cruzados.")
    else:
        citados_n = set(re.findall(r"\bN-\d+\b", texto))
        for pid, situacao in sorted(situacoes.items(), key=lambda item: ordem(item[0])):
            if situacao != "Descartado" and pid not in citados_n:
                rel.erro(
                    nome,
                    f'{pid} ({situacao}) não aparece aqui: registre-o em "Dúvidas e decisões" (origem {pid}), em Premissas ou em Pendências.',
                )

    checar_modelo(nome, bruto, rel)


# --------------------------------------------------------- arquivo do dev


def achar_final(pasta: Path) -> Path | None:
    card = pasta.name.lstrip("#")
    esperado = pasta / f"#{card}-analise-final.md"
    if esperado.is_file():
        return esperado
    outros = sorted(pasta.glob("*-analise-final.md"))
    return outros[0] if outros else None


def verificar_final(pasta: Path, rel: Relatorio) -> None:
    card = pasta.name.lstrip("#")
    nome_esperado = f"#{card}-analise-final.md"
    arquivo = achar_final(pasta)
    if arquivo is None:
        rel.falta(nome_esperado)
        return
    nome = arquivo.name
    if nome != nome_esperado:
        rel.aviso(nome, f"o nome esperado é {nome_esperado}.")
    bruto = ler(arquivo)
    texto = sem_cercas(bruto)
    sec = secoes(texto)
    titulos = list(sec)

    if not titulos or titulos[0].lower() != "contexto":
        rel.erro(nome, 'a primeira seção deve ser "## Contexto", para o dev entender a entrega antes dos detalhes.')
    elif not tem_texto(sec[titulos[0]]):
        rel.erro(nome, 'a seção "Contexto" está vazia.')
    if "fora do escopo" not in (t.lower() for t in titulos):
        rel.aviso(nome, 'sem a seção "## Fora do escopo"; confira se não há nada que o dev deva deixar de fazer.')

    for n, linha in enumerate(texto.splitlines(), 1):
        for m in RE_ID_FINAL.finditer(linha):
            rel.erro(
                nome,
                f'linha {n}: "{m.group(0)}" aponta para outro documento; troque pelo conteúdo, porque o dev só recebe este arquivo.',
            )
        for m in RE_ARQUIVOS.finditer(linha):
            rel.erro(nome, f'linha {n}: cita "{m.group(0)}", que o dev não recebe.')
        for m in RE_FRASES_REF.finditer(linha):
            rel.aviso(nome, f'linha {n}: "{m.group(0)}"; confira se o trecho depende de um documento que o dev não tem.')

    cercas = [bruto.count("\n", 0, m.start()) + 1 for m in RE_CERCA.finditer(bruto)]
    if cercas:
        linhas = ", ".join(str(n) for n in cercas)
        rel.aviso(nome, f"{len(cercas)} bloco(s) de código (linha {linhas}); só cabem exemplos curtos.")

    checar_modelo(nome, bruto, rel)


# --------------------------------------------------------------------- main


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) != 3 or argv[1] not in {"negocio", "sistema", "final", "tudo"}:
        print(__doc__.strip())
        return 2
    pasta = Path(argv[2])
    if not pasta.is_dir():
        print(f"ERRO: pasta não encontrada: {pasta}")
        return 2

    modo = argv[1]
    rel = Relatorio()
    situacoes: dict[str, str] | None = None
    if modo in ("negocio", "tudo"):
        situacoes = verificar_negocio(pasta, rel)
    elif modo == "sistema" and (pasta / ARQ_NEGOCIO).is_file():
        situacoes = verificar_negocio(pasta, Relatorio())  # só para cruzar os N-xx
    if modo in ("sistema", "tudo"):
        verificar_sistema(pasta, rel, situacoes)
    if modo in ("final", "tudo"):
        verificar_final(pasta, rel)

    rel.imprimir()
    if rel.faltando:
        return 2
    return 1 if rel.tem_erro else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
