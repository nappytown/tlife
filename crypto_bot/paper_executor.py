import uuid
from datetime import timezone
from datetime import datetime
from crypto_bot.config import config
from crypto_bot.ledger import open_trade, close_trade


def paper_enter(signal, risk_params):
    trade = {
        "trade_id": str(uuid.uuid4()),
        "symbol": signal.symbol,
        "action": signal.action,
        "status": "OPEN",
        "entry_price": signal.price,
        "exit_price": None,
        "stop_loss": risk_params.stop_loss_price,
        "take_profit": risk_params.take_profit_price,
        "position_size": risk_params.position_size,
        "entry_time": signal.timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "exit_time": None,
        "exit_reason": None,
        "entry_reason": signal.reason,
        "estimated_fee": signal.price * risk_params.position_size * config["fee_rate"],
        "estimated_slippage": signal.price * risk_params.position_size * config["slippage_pct"],
        "realized_pnl": None,
        "paper": True,
        "rsi": signal.rsi,
    }
    open_trade(trade)
    return trade


def paper_exit(trade_id, exit_price, exit_reason):
    return close_trade(trade_id, exit_price, exit_reason)


def check_exit_conditions(open_trade, current_price):
    if current_price <= open_trade["stop_loss"]:
        return "STOP"
    if current_price >= open_trade["take_profit"]:
        return "TARGET"
    return None
