import json
import os
from datetime import datetime, timezone
from pathlib import Path


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes", "on"}


def is_bot_stopped() -> bool:
    stop_path = Path(os.getenv("STOP_BOT_PATH", "./STOP_BOT"))
    return stop_path.exists()


def check_daily_limits(ledger_path: str) -> bool:
    max_daily_loss = float(os.getenv("MAX_DAILY_LOSS", "0.05"))
    max_trades_per_day = int(os.getenv("MAX_TRADES_PER_DAY", "5"))
    today = datetime.now(timezone.utc).date()

    if not Path(ledger_path).exists():
        return True
    with open(ledger_path, "r", encoding="utf-8") as f:
        trades = json.load(f) or []

    today_trades = []
    realized_losses = 0.0
    for t in trades:
        entry_time = t.get("entry_time") or t.get("exit_time")
        if not entry_time:
            continue
        dt = datetime.fromisoformat(entry_time.replace("Z", "+00:00"))
        if dt.date() != today:
            continue
        today_trades.append(t)
        pnl = t.get("realized_pnl")
        if pnl is not None and pnl < 0:
            realized_losses += abs(float(pnl))

    account_balance = float(os.getenv("ACCOUNT_BALANCE", "1000"))
    loss_pct = realized_losses / account_balance if account_balance else 0
    if loss_pct > max_daily_loss:
        return False
    if len(today_trades) >= max_trades_per_day:
        return False
    return True


def assert_paper_mode() -> None:
    if not _env_bool("PAPER_MODE", True):
        raise RuntimeError("Live trading not enabled in this phase")
