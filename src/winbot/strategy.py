import pandas as pd
from .config import StrategyConfig
from .models import Candle, Signal, Side


class HybridStrategy:
    # \"\"\"Baseline explicável: tendência + rompimento + volume + candle direcional.\"\"\"

    def __init__(self, config: StrategyConfig):
        self.config = config

    def evaluate(self, candles: list[Candle]) -> Signal | None:
        required = max(
            self.config.slow_ema,
            self.config.volume_lookback,
            self.config.breakout_lookback,
        ) + 2
        if len(candles) < required:
            return None

        df = pd.DataFrame([{
            "open": c.open, "high": c.high, "low": c.low,
            "close": c.close, "volume": c.volume
        } for c in candles])

        close = df["close"]
        fast = close.ewm(span=self.config.fast_ema, adjust=False).mean().iloc[-1]
        slow = close.ewm(span=self.config.slow_ema, adjust=False).mean().iloc[-1]

        last = df.iloc[-1]
        previous = df.iloc[-(self.config.breakout_lookback + 1):-1]
        prior_volumes = df["volume"].iloc[-(self.config.volume_lookback + 1):-1]
        avg_volume = float(prior_volumes.mean())
        if avg_volume <= 0:
            return None

        relative_volume = float(last["volume"] / avg_volume)
        upper = float(previous["high"].max())
        lower = float(previous["low"].min())

        bullish = last["close"] > last["open"]
        bearish = last["close"] < last["open"]

        # Pontuação simples e transparente; não é probabilidade calibrada.
        if fast > slow and last["close"] > upper and bullish:
            score = 0.5 + min(relative_volume / 4, 0.5)
            if relative_volume >= self.config.min_relative_volume and score >= self.config.min_score:
                entry = float(last["close"])
                stop = entry - self.config.stop_points
                target = entry + self.config.stop_points * self.config.reward_risk
                return Signal(Side.BUY, entry, stop, target, score,
                              f"EMA alta + rompimento + volume relativo {relative_volume:.2f}x")

        if fast < slow and last["close"] < lower and bearish:
            score = 0.5 + min(relative_volume / 4, 0.5)
            if relative_volume >= self.config.min_relative_volume and score >= self.config.min_score:
                entry = float(last["close"])
                stop = entry + self.config.stop_points
                target = entry - self.config.stop_points * self.config.reward_risk
                return Signal(Side.SELL, entry, stop, target, score,
                              f"EMA baixa + rompimento + volume relativo {relative_volume:.2f}x")

        return None
