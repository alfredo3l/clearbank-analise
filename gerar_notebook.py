"""Script auxiliar para gerar e executar o notebook do desafio."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0",
        },
    },
    "cells": [],
}


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": source.splitlines(keepends=True),
        "outputs": [],
        "execution_count": None,
    }


cells = [
    md(
        "# Desafio Final: Análise Financeira com Python\n\n"
        "**ClearBank** — Notebook para leitura, validação e análise de transações bancárias.\n\n"
        "## Instruções\n"
        "- O arquivo `transacoes.csv` deve estar na mesma pasta deste notebook.\n"
        "- Execute as células em ordem, da primeira à última.\n"
        "- A célula principal ao final gera `relatorio.json` e exibe o relatório no terminal.\n\n"
        "O CSV contém **18 registros válidos** em 4 meses, **5 registros inválidos** "
        "e **2 transações acima de R$ 10.000,00**."
    ),
    code(
        'import csv\n'
        'import json\n'
        'from datetime import datetime\n\n'
        'LIMITE_SUSPEITO = 10000.00\n'
        'ARQUIVO_CSV = "transacoes.csv"\n'
        'ARQUIVO_JSON = "relatorio.json"\n\n'
        'print("Constantes e imports carregados.")\n'
        'print(f"Limite para transações suspeitas: R$ {LIMITE_SUSPEITO:,.2f}")'
    ),
    md("## R1 — Leitura do CSV com módulo nativo"),
    code(
        'def ler_transacoes(caminho: str) -> list[dict]:\n'
        '    """Lê o arquivo CSV e retorna a lista de transações brutas."""\n'
        '    transacoes = []\n'
        '    try:\n'
        '        with open(caminho, encoding="utf-8", newline="") as arquivo:\n'
        '            leitor = csv.DictReader(arquivo)\n'
        '            for linha in leitor:\n'
        '                transacoes.append(dict(linha))\n'
        '    except FileNotFoundError:\n'
        '        print(f"Erro: arquivo \'{caminho}\' não encontrado.")\n'
        '        return []\n'
        '    return transacoes\n\n\n'
        'brutas = ler_transacoes(ARQUIVO_CSV)\n'
        'print(f"Linhas brutas lidas: {len(brutas)}")\n'
        'print("Primeira transação:", brutas[0] if brutas else "Nenhuma")'
    ),
    md("## R2 — Validação e limpeza dos dados"),
    code(
        'def validar_transacao(linha: dict) -> dict | None:\n'
        '    """Valida uma linha e retorna o registro limpo ou None se inválida."""\n'
        '    id_texto = (linha.get("id") or "").strip()\n'
        '    if not id_texto.isdigit():\n'
        '        return None\n'
        '\n'
        '    cliente_id = (linha.get("cliente_id") or "").strip()\n'
        '    if not cliente_id:\n'
        '        return None\n'
        '\n'
        '    tipo = (linha.get("tipo") or "").strip().lower()\n'
        '    if tipo not in ("credito", "debito"):\n'
        '        return None\n'
        '\n'
        '    try:\n'
        '        valor = float(str(linha.get("valor", "")).strip().replace(",", "."))\n'
        '        if valor <= 0:\n'
        '            return None\n'
        '    except ValueError:\n'
        '        return None\n'
        '\n'
        '    data_texto = (linha.get("data") or "").strip()\n'
        '    try:\n'
        '        data_obj = datetime.strptime(data_texto, "%Y-%m-%d")\n'
        '    except ValueError:\n'
        '        return None\n'
        '\n'
        '    return {\n'
        '        "id": int(id_texto),\n'
        '        "data": data_obj,\n'
        '        "data_texto": data_texto,\n'
        '        "mes": data_obj.strftime("%Y-%m"),\n'
        '        "cliente_id": cliente_id,\n'
        '        "tipo": tipo,\n'
        '        "valor": valor,\n'
        '        "descricao": (linha.get("descricao") or "").strip(),\n'
        '        "categoria": (linha.get("categoria") or "").strip(),\n'
        '        "suspeita": valor > LIMITE_SUSPEITO,\n'
        '    }\n\n\n'
        'def limpar_transacoes(brutas: list[dict]) -> tuple[list[dict], int, int]:\n'
        '    """Retorna transações válidas, total lidas e total inválidas."""\n'
        '    validas = []\n'
        '    invalidas = 0\n'
        '    for linha in brutas:\n'
        '        registro = validar_transacao(linha)\n'
        '        if registro is None:\n'
        '            invalidas += 1\n'
        '        else:\n'
        '            validas.append(registro)\n'
        '    return validas, len(brutas), invalidas\n\n\n'
        'validas, total_lidas, total_invalidas = limpar_transacoes(brutas)\n'
        'print(f"Total de linhas lidas: {total_lidas}")\n'
        'print(f"Linhas válidas: {len(validas)}")\n'
        'print(f"Linhas inválidas: {total_invalidas}")'
    ),
    md("## R4 — Manipulação de datas"),
    code(
        'def calcular_periodo(transacoes: list[dict]) -> dict:\n'
        '    """Calcula data mais antiga, mais recente e dias entre elas."""\n'
        '    if not transacoes:\n'
        '        return {"inicio": None, "fim": None, "dias": 0}\n'
        '\n'
        '    datas = [t["data"] for t in transacoes]\n'
        '    inicio = min(datas)\n'
        '    fim = max(datas)\n'
        '    dias = (fim - inicio).days\n'
        '    return {\n'
        '        "inicio": inicio.strftime("%Y-%m-%d"),\n'
        '        "fim": fim.strftime("%Y-%m-%d"),\n'
        '        "dias": dias,\n'
        '    }\n\n\n'
        'periodo = calcular_periodo(validas)\n'
        'print(f"Período: {periodo[\'inicio\']} → {periodo[\'fim\']}")\n'
        'print(f"Dias entre a transação mais antiga e a mais recente: {periodo[\'dias\']}")'
    ),
    md("## R5 — Agrupamento mensal e métricas"),
    code(
        'def gerar_relatorio(transacoes: list[dict], total_invalidas: int) -> dict:\n'
        '    """Agrupa os dados por mês e calcula métricas financeiras."""\n'
        '    resumo_mensal = {}\n'
        '    suspeitas = []\n'
        '\n'
        '    for t in transacoes:\n'
        '        mes = t["mes"]\n'
        '        if mes not in resumo_mensal:\n'
        '            resumo_mensal[mes] = {\n'
        '                "quantidade": 0,\n'
        '                "total_credito": 0.0,\n'
        '                "total_debito": 0.0,\n'
        '                "valores": [],\n'
        '            }\n'
        '\n'
        '        resumo_mensal[mes]["quantidade"] += 1\n'
        '        resumo_mensal[mes]["valores"].append(t["valor"])\n'
        '\n'
        '        if t["tipo"] == "credito":\n'
        '            resumo_mensal[mes]["total_credito"] += t["valor"]\n'
        '        else:\n'
        '            resumo_mensal[mes]["total_debito"] += t["valor"]\n'
        '\n'
        '        if t["suspeita"]:\n'
        '            suspeitas.append({\n'
        '                "id": t["id"],\n'
        '                "cliente_id": t["cliente_id"],\n'
        '                "data": t["data_texto"],\n'
        '                "valor": t["valor"],\n'
        '            })\n'
        '\n'
        '    for mes, dados in resumo_mensal.items():\n'
        '        valores = dados.pop("valores")\n'
        '        dados["saldo"] = round(dados["total_credito"] - dados["total_debito"], 2)\n'
        '        dados["valor_medio"] = round(sum(valores) / len(valores), 2)\n'
        '        dados["maior_valor"] = round(max(valores), 2)\n'
        '        dados["menor_valor"] = round(min(valores), 2)\n'
        '        dados["total_credito"] = round(dados["total_credito"], 2)\n'
        '        dados["total_debito"] = round(dados["total_debito"], 2)\n'
        '\n'
        '    periodo_info = calcular_periodo(transacoes)\n'
        '\n'
        '    return {\n'
        '        "gerado_em": datetime.now().strftime("%Y-%m-%d"),\n'
        '        "total_transacoes_validas": len(transacoes),\n'
        '        "total_transacoes_invalidas": total_invalidas,\n'
        '        "periodo": periodo_info,\n'
        '        "resumo_mensal": dict(sorted(resumo_mensal.items())),\n'
        '        "transacoes_suspeitas": suspeitas,\n'
        '    }\n\n\n'
        'relatorio = gerar_relatorio(validas, total_invalidas)\n'
        'print("Meses analisados:", list(relatorio["resumo_mensal"].keys()))\n'
        'print("Transações suspeitas:", len(relatorio["transacoes_suspeitas"]))'
    ),
    md("## R7 — Exportação do relatório em JSON"),
    code(
        'def salvar_json(dados: dict, caminho: str) -> None:\n'
        '    """Salva o relatório no arquivo JSON."""\n'
        '    with open(caminho, "w", encoding="utf-8") as arquivo:\n'
        '        json.dump(dados, arquivo, ensure_ascii=False, indent=2)\n'
        '    print(f"Relatório salvo em \'{caminho}\'.")\n\n\n'
        'salvar_json(relatorio, ARQUIVO_JSON)'
    ),
    md("## R8 — Exibição formatada no terminal"),
    code(
        'def formatar_moeda(valor: float) -> str:\n'
        '    """Formata valor no padrão monetário brasileiro."""\n'
        '    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")\n\n\n'
        'def exibir_relatorio(dados: dict) -> None:\n'
        '    """Formata e imprime os resultados no terminal."""\n'
        '    periodo = dados["periodo"]\n'
        '    print("=" * 30)\n'
        '    print(" RESUMO DA ANÁLISE")\n'
        '    print("=" * 30)\n'
        '    print(f"Período analisado: {periodo[\'inicio\']} → {periodo[\'fim\']}")\n'
        '    print(f"Dias no período: {periodo[\'dias\']}")\n'
        '    print(f"Transações válidas: {dados[\'total_transacoes_validas\']}")\n'
        '    print(f"Transações inválidas: {dados[\'total_transacoes_invalidas\']}")\n'
        '    print()\n'
        '    print("===== RELATÓRIO MENSAL =====")\n'
        '    print()\n'
        '\n'
        '    for mes, info in dados["resumo_mensal"].items():\n'
        '        print(f"Mês: {mes}")\n'
        '        print(f"  Transações: {info[\'quantidade\']}")\n'
        '        print(f"  Total crédito: {formatar_moeda(info[\'total_credito\'])}")\n'
        '        print(f"  Total débito:  {formatar_moeda(info[\'total_debito\'])}")\n'
        '        print(f"  Saldo:         {formatar_moeda(info[\'saldo\'])}")\n'
        '        print(f"  Média:         {formatar_moeda(info[\'valor_medio\'])}")\n'
        '        print(f"  Maior valor:   {formatar_moeda(info[\'maior_valor\'])}")\n'
        '        print(f"  Menor valor:   {formatar_moeda(info[\'menor_valor\'])}")\n'
        '        print()\n'
        '\n'
        '    print("===== TRANSAÇÕES SUSPEITAS =====")\n'
        '    if dados["transacoes_suspeitas"]:\n'
        '        for t in dados["transacoes_suspeitas"]:\n'
        '            print(\n'
        '                f"ID: {t[\'id\']} | Cliente: {t[\'cliente_id\']} | "\n'
        '                f"Data: {t[\'data\']} | Valor: {formatar_moeda(t[\'valor\'])}"\n'
        '            )\n'
        '    else:\n'
        '        print("Nenhuma transação suspeita encontrada.")\n\n\n'
        'exibir_relatorio(relatorio)'
    ),
    md("## Célula de Execução Principal"),
    code(
        'def executar_analise() -> dict:\n'
        '    """Executa o fluxo completo da análise financeira."""\n'
        '    brutas = ler_transacoes(ARQUIVO_CSV)\n'
        '    if not brutas:\n'
        '        return {}\n'
        '\n'
        '    validas, total_lidas, total_invalidas = limpar_transacoes(brutas)\n'
        '    print(f"Total de linhas lidas: {total_lidas}")\n'
        '    print(f"Linhas válidas: {len(validas)}")\n'
        '    print(f"Linhas inválidas: {total_invalidas}")\n'
        '    print()\n'
        '\n'
        '    relatorio_final = gerar_relatorio(validas, total_invalidas)\n'
        '    salvar_json(relatorio_final, ARQUIVO_JSON)\n'
        '    exibir_relatorio(relatorio_final)\n'
        '    return relatorio_final\n\n\n'
        'resultado_final = executar_analise()'
    ),
    md("## RO1 (Opcional) — Visualização com matplotlib"),
    code(
        'import matplotlib.pyplot as plt\n\n'
        'meses = list(relatorio["resumo_mensal"].keys())\n'
        'creditos = [relatorio["resumo_mensal"][m]["total_credito"] for m in meses]\n'
        'debitos = [relatorio["resumo_mensal"][m]["total_debito"] for m in meses]\n'
        'saldos = [relatorio["resumo_mensal"][m]["saldo"] for m in meses]\n\n'
        'fig, ax = plt.subplots(figsize=(10, 6))\n'
        'x = range(len(meses))\n'
        'largura = 0.35\n'
        'ax.bar([i - largura / 2 for i in x], creditos, largura, label="Crédito", color="#2ecc71")\n'
        'ax.bar([i + largura / 2 for i in x], debitos, largura, label="Débito", color="#e74c3c")\n'
        'ax.set_title("Crédito e Débito por Mês — ClearBank")\n'
        'ax.set_xlabel("Mês")\n'
        'ax.set_ylabel("Valor (R$)")\n'
        'ax.set_xticks(list(x))\n'
        'ax.set_xticklabels(meses)\n'
        'ax.legend()\n'
        'plt.tight_layout()\n'
        'plt.savefig("grafico.png", dpi=150)\n'
        'plt.show()\n'
        'print("Gráfico salvo em grafico.png")'
    ),
]

NOTEBOOK["cells"] = cells

notebook_path = BASE / "desafio-final.ipynb"
notebook_path.write_text(json.dumps(NOTEBOOK, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Notebook criado: {notebook_path}")

# Executar notebook para salvar saídas
try:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--inplace",
            str(notebook_path),
        ],
        cwd=BASE,
        check=True,
    )
    print("Notebook executado com sucesso.")
except subprocess.CalledProcessError as exc:
    print(f"Aviso: não foi possível executar o notebook automaticamente: {exc}")
    sys.exit(1)
