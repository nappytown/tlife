from dataclasses import dataclass
from datetime import datetime

_last_signal: dict[str, str] = {}


@dataclass
class Signal:
    symbol: str
    timestamp: datetime
    action: str
    reason: str
    rsi: float
    macd_hist: float
    price: float


def generate_signal(df, symbol) -> Signal:
    last = df.iloc[-1]
    prev = df.iloc[-2]

    buy_votes = 0
    sell_votes = 0
    reasons = []

    if prev["macd"] <= prev["macd_signal"] and last["macd"] > last["macd_signal"] and last["rsi"] < 50:
        buy_votes += 1
        reasons.append("MACD crossover + RSI < 50")
    if prev["macd"] >= prev["macd_signal"] and last["macd"] < last["macd_signal"] and last["rsi"] > 50:
        sell_votes += 1
        reasons.append("MACD crossdown + RSI > 50")
    if prev["ema_50"] <= prev["ema_200"] and last["ema_50"] > last["ema_200"]:
        buy_votes += 1
        reasons.append("EMA50 crossed above EMA200")
    if prev["ema_50"] >= prev["ema_200"] and last["ema_50"] < last["ema_200"]:
        sell_votes += 1
        reasons.append("EMA50 crossed below EMA200")

    action = "NEUTRAL"
    if buy_votes > sell_votes:
        action = "BUY"
    elif sell_votes > buy_votes:
        action = "SELL"

    if _last_signal.get(symbol) == action and action in {"BUY", "SELL"}:
        action = "NEUTRAL"
        reason = "Duplicate signal suppressed"
    else:
        reason = " | ".join(reasons) if reasons else "No consensus"
        if action in {"BUY", "SELL"}:
            _last_signal[symbol] = action

    return Signal(symbol=symbol, timestamp=last.name.to_pydatetime(), action=action, reason=reason, rsi=float(last["rsi"]), macd_hist=float(last["macd_hist"]), price=float(last["close"]))
