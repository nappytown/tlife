import json
import os
from datetime import datetime, timezone


LEDGER_PATH = os.getenv("LEDGER_PATH", "data/ledger.json")


def load_ledger():
    try:
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except FileNotFoundError:
        return []


def _save(data):
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def open_trade(trade):
    d = load_ledger()
    d.append(trade)
    _save(d)


def close_trade(trade_id, exit_price, exit_reason):
    d = load_ledger()
    for t in d:
        if t["trade_id"] == trade_id and t["status"] == "OPEN":
            t["status"] = "CLOSED"
            t["exit_price"] = exit_price
            t["exit_reason"] = exit_reason
            t["exit_time"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            t["realized_pnl"] = (exit_price - t["entry_price"]) * t["position_size"]
            _save(d)
            return t
    raise ValueError("Trade not found")


def get_open_trades(symbol):
    return [t for t in load_ledger() if t["symbol"] == symbol and t["status"] == "OPEN"]


def get_today_trades():
    today = datetime.now(timezone.utc).date()
    out = []
    for t in load_ledger():
        dt = datetime.fromisoformat(t["entry_time"].replace("Z", "+00:00"))
        if dt.date() == today:
            out.append(t)
    return out
