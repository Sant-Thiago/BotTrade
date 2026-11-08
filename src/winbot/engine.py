from .strategy import HybridStrategy
from .risk import RiskManager
from .execution import PaperExecutor


class TradingEngine:
    def __init__(self, strategy: HybridStrategy, risk: RiskManager, executor: PaperExecutor):
        self.strategy = strategy
        self.risk = risk
        self.executor = executor

    def run(self, candles):
        history = []
        for candle in candles:
            history.append(candle)

            # Gerencia posição aberta usando máxima/mínima do candle.
            pos = self.executor.position
            if pos:
                if pos.side.value == "BUY":
                    if candle.low <= pos.stop:
                        pnl = self.executor.close("STOP", pos.stop)
                        self.risk.register_trade(pnl)
                    elif candle.high >= pos.target:
                        pnl = self.executor.close("ALVO", pos.target)
                        self.risk.register_trade(pnl)
                else:
                    if candle.high >= pos.stop:
                        pnl = self.executor.close("STOP", pos.stop)
                        self.risk.register_trade(pnl)
                    elif candle.low <= pos.target:
                        pnl = self.executor.close("ALVO", pos.target)
                        self.risk.register_trade(pnl)
                continue

            if self.risk.state.halted:
                break

            signal = self.strategy.evaluate(history)
            if signal and self.risk.approve(signal):
                self.executor.submit(signal, candle.timestamp)

        return self.risk.state
