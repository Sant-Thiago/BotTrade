from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyConfig:
    fast_ema: int = 9
    slow_ema: int = 21
    breakout_lookback: int = 5
    volume_lookback: int = 20
    min_relative_volume: float = 1.20
    min_score: float = 0.75
    stop_points: float = 150.0
    reward_risk: float = 2.5


@dataclass(frozen=True)
class RiskConfig:
    max_daily_loss_points: float = 300.0
    max_trades_per_day: int = 3
    max_contracts: int = 5
