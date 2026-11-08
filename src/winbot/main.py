import argparse
from .config import StrategyConfig, RiskConfig
from .data import load_csv
from .strategy import HybridStrategy
from .risk import RiskManager
from .execution import PaperExecutor
from .engine import TradingEngine


def main():
    parser = argparse.ArgumentParser(description="WIN BOT — paper trading")
    parser.add_argument("--csv", required=True, help="CSV de candles OHLCV")
    args = parser.parse_args()

    candles = load_csv(args.csv)
    engine = TradingEngine(
        HybridStrategy(StrategyConfig()),
        RiskManager(RiskConfig()),
        PaperExecutor(),
    )
    state = engine.run(candles)
    print("\\n=== RESUMO DA SIMULAÇÃO ===")
    print(f"Operações encerradas: {state.trades}")
    print(f"Resultado: {state.realized_points:.0f} pontos")
    print(f"Bloqueado por risco: {state.halted}")


if __name__ == "__main__":
    main()
