from dataclasses import dataclass
from .models import Signal, Position


@dataclass
class PaperExecutor:
    #\"\"\"Executor de simulação. Não possui integração com corretora.\"\"\"

    position: Position | None = None

    def submit(self, signal: Signal, timestamp) -> Position:
        if self.position is not None:
            raise RuntimeError("Já existe posição aberta; ordem recusada.")
        self.position = Position(
            side=signal.side,
            entry=signal.entry,
            stop=signal.stop,
            target=signal.target,
            opened_at=timestamp,
        )
        print(f"[PAPER] {signal.side.value} @ {signal.entry:.0f} | "
              f"stop={signal.stop:.0f} alvo={signal.target:.0f} | {signal.reason}")
        return self.position

    def close(self, reason: str, exit_price: float) -> float:
        if self.position is None:
            raise RuntimeError("Não existe posição aberta.")
        p = self.position
        pnl = (exit_price - p.entry) if p.side.value == "BUY" else (p.entry - exit_price)
        print(f"[PAPER] FECHAMENTO {reason} @ {exit_price:.0f} | P&L={pnl:.0f} pontos")
        self.position = None
        return pnl
