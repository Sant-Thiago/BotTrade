from dataclasses import dataclass
from .config import RiskConfig
from .models import Signal


@dataclass
class DailyRiskState:
    realized_points: float = 0.0
    trades: int = 0
    halted: bool = False


class RiskManager:
    def __init__(self, config: RiskConfig):
        self.config = config
        self.state = DailyRiskState()

    def approve(self, signal: Signal) -> bool:
        if self.state.halted:
            return False
        if self.state.trades >= self.config.max_trades_per_day:
            return False
        if self.state.realized_points <= -abs(self.config.max_daily_loss_points):
            self.state.halted = True
            return False
        if signal.stop == signal.entry or signal.target == signal.entry:
            return False
        return True

    def register_trade(self, pnl_points: float) -> None:
        self.state.trades += 1
        self.state.realized_points += pnl_points
        if self.state.realized_points <= -abs(self.config.max_daily_loss_points):
            self.state.halted = True
