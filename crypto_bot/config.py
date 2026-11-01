import os
from dotenv import load_dotenv
from crypto_bot.safety import assert_paper_mode

load_dotenv()

config = {
    "exchange_name": os.getenv("EXCHANGE_NAME", "binance"),
    "symbol": os.getenv("SYMBOL", "BTC/USDT"),
    "timeframe": os.getenv("TIMEFRAME", "1h"),
    "run_interval_minutes": int(os.getenv("RUN_INTERVAL_MINUTES", "60")),
    "account_balance": float(os.getenv("ACCOUNT_BALANCE", "1000")),
    "risk_per_trade": float(os.getenv("RISK_PER_TRADE", "0.02")),
    "paper_mode": os.getenv("PAPER_MODE", "True").lower() == "true",
    "max_daily_loss": float(os.getenv("MAX_DAILY_LOSS", "0.05")),
    "max_trades_per_day": int(os.getenv("MAX_TRADES_PER_DAY", "5")),
    "max_open_trades": int(os.getenv("MAX_OPEN_TRADES", "1")),
    "stop_bot_path": os.getenv("STOP_BOT_PATH", "./STOP_BOT"),
    "fee_rate": float(os.getenv("FEE_RATE", "0.001")),
    "slippage_pct": float(os.getenv("SLIPPAGE_PCT", "0.0005")),
    "backtest_candles": int(os.getenv("BACKTEST_CANDLES", "5000")),
    "min_backtest_trades": int(os.getenv("MIN_BACKTEST_TRADES", "50")),
    "telegram_token": os.getenv("TELEGRAM_TOKEN", ""),
    "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "binance_api_key": os.getenv("BINANCE_API_KEY", ""),
    "binance_secret": os.getenv("BINANCE_SECRET", ""),
    "ledger_path": os.getenv("LEDGER_PATH", "data/ledger.json"),
}

assert_paper_mode()
