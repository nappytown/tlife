from dataclasses import dataclass
from crypto_bot.config import config
from crypto_bot.ledger import get_open_trades


@dataclass
class RiskParams:
    position_size: float
    stop_loss_price: float
    take_profit_price: float
    risk_amount: float
    reward_amount: float
    rr_ratio: float


def calculate_risk(signal, account_balance: float) -> RiskParams:
    stop_distance = signal.price * 0.02
    stop_loss_price = signal.price - stop_distance
    take_profit_price = signal.price + (stop_distance * 2)
    position_size = (account_balance * config["risk_per_trade"]) / stop_distance
    risk_amount = position_size * stop_distance
    reward_amount = position_size * stop_distance * 2
    return RiskParams(position_size, stop_loss_price, take_profit_price, risk_amount, reward_amount, 2.0)


def is_trade_allowed(symbol: str, ledger_path: str) -> bool:
    _ = ledger_path
    return len(get_open_trades(symbol)) == 0
