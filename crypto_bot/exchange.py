import ccxt
import pandas as pd
from crypto_bot.config import config


def get_exchange():
    cls = getattr(ccxt, config["exchange_name"])
    return cls({"apiKey": config.get("binance_api_key"), "secret": config.get("binance_secret")})


def fetch_ohlcv(symbol, timeframe, limit=500):
    exchange = get_exchange()
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("timestamp")
    return df
