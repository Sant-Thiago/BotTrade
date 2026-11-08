from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass(frozen=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class Signal:
    side: Side
    entry: float
    stop: float
    target: float
    score: float
    reason: str


@dataclass
class Position:
    side: Side
    entry: float
    stop: float
    target: float
    opened_at: datetime
    quantity: int = 1
