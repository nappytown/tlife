import pandas as pd
from crypto_bot.exchange import fetch_ohlcv

def test_fetch_ohlcv(monkeypatch):
    class Ex:
        def fetch_ohlcv(self, symbol, timeframe, limit):
            return [[1700000000000+i*3600000,1,2,0.5,1.5,10] for i in range(limit)]
    monkeypatch.setattr("crypto_bot.exchange.get_exchange", lambda: Ex())
    df = fetch_ohlcv("BTC/USDT", "1h", 500)
    assert len(df) == 500
    assert list(df.columns) == ["open","high","low","close","volume"]
    assert isinstance(df.index, pd.DatetimeIndex)
