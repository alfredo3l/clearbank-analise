"""
RO1 (Opcional) — Versão alternativa com pandas.

Objetivo:
- Ler o mesmo transacoes.csv com pandas
- Agrupar por mês e calcular as mesmas métricas do relatório nativo
- (Opcional) Comparar com relatorio.json, se existir
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


LIMITE_SUSPEITO = 10000.00
ARQUIVO_CSV = "transacoes.csv"
ARQUIVO_JSON = "relatorio.json"


def carregar_validar_com_pandas(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, dtype=str)

    # id: inteiro
    df["id_num"] = pd.to_numeric(df["id"], errors="coerce")

    # cliente_id: não vazio
    df["cliente_id"] = df["cliente_id"].fillna("").astype(str).str.strip()

    # tipo: credito/debito
    df["tipo"] = df["tipo"].fillna("").astype(str).str.strip().str.lower()

    # valor: float > 0
    df["valor_num"] = pd.to_numeric(df["valor"].astype(str).str.replace(",", ".", regex=False), errors="coerce")

    # data: AAAA-MM-DD
    df["data_dt"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")

    validas = (
        df["id_num"].notna()
        & (df["id_num"] % 1 == 0)
        & (df["cliente_id"] != "")
        & (df["tipo"].isin(["credito", "debito"]))
        & df["valor_num"].notna()
        & (df["valor_num"] > 0)
        & df["data_dt"].notna()
    )

    df = df.loc[validas].copy()
    df["id_num"] = df["id_num"].astype(int)
    df["mes"] = df["data_dt"].dt.strftime("%Y-%m")
    df["suspeita"] = df["valor_num"] > LIMITE_SUSPEITO
    return df


def gerar_resumo_mensal(df: pd.DataFrame) -> dict:
    agrupado = df.groupby("mes")
    resumo = {}

    for mes, grupo in agrupado:
        valores = grupo["valor_num"]
        total_credito = grupo.loc[grupo["tipo"] == "credito", "valor_num"].sum()
        total_debito = grupo.loc[grupo["tipo"] == "debito", "valor_num"].sum()

        resumo[mes] = {
            "quantidade": int(len(grupo)),
            "total_credito": round(float(total_credito), 2),
            "total_debito": round(float(total_debito), 2),
            "saldo": round(float(total_credito - total_debito), 2),
            "valor_medio": round(float(valores.mean()), 2),
            "maior_valor": round(float(valores.max()), 2),
            "menor_valor": round(float(valores.min()), 2),
        }

    return dict(sorted(resumo.items()))


def comparar_com_relatorio_nativo(resumo_pandas: dict, caminho_json: str) -> None:
    caminho = Path(caminho_json)
    if not caminho.exists():
        print(f"Arquivo '{caminho_json}' não encontrado; pulando comparação.")
        return

    dados = json.loads(caminho.read_text(encoding="utf-8"))
    resumo_nativo = dados.get("resumo_mensal", {})

    if resumo_pandas == resumo_nativo:
        print("OK: resumo mensal (pandas) é igual ao relatório nativo.")
    else:
        print("Diferença encontrada entre pandas e nativo.")
        print("Pandas:", resumo_pandas)
        print("Nativo:", resumo_nativo)


def main() -> None:
    df_validas = carregar_validar_com_pandas(ARQUIVO_CSV)
    resumo = gerar_resumo_mensal(df_validas)

    print("Resumo mensal (pandas):")
    for mes, info in resumo.items():
        print(mes, info)

    comparar_com_relatorio_nativo(resumo, ARQUIVO_JSON)


if __name__ == "__main__":
    main()

