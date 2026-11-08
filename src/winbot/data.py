from pathlib import Path
import pandas as pd
from .models import Candle


def load_csv(path: str | Path) -> list[Candle]:
    df = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no CSV: {sorted(missing)}")

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="raise")
    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="raise")

    if (df["high"] < df["low"]).any():
        raise ValueError("CSV inválido: há candle com máxima menor que mínima.")
    return [
        Candle(row.timestamp.to_pydatetime(), float(row.open), float(row.high),
               float(row.low), float(row.close), float(row.volume))
        for row in df.itertuples(index=False)
    ]
