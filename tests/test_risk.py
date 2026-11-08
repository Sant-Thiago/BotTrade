from datetime import datetime
from winbot.config import RiskConfig
from winbot.models import Signal, Side
from winbot.risk import RiskManager


def test_daily_loss_blocks_new_trades():
    risk = RiskManager(RiskConfig(max_daily_loss_points=100, max_trades_per_day=5))
    risk.register_trade(-100)
    signal = Signal(Side.BUY, 1000, 900, 1200, 0.8, "test")
    assert risk.approve(signal) is False
    assert risk.state.halted is True
