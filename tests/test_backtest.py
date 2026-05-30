import pandas as pd
import numpy as np
from crypto_bot.backtest import run_backtest

def test_backtest_insufficient_data(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path/"data/backtest_results").mkdir(parents=True, exist_ok=True)
    n=300
    close=np.sin(np.linspace(0,20,n))*10+100
    df=pd.DataFrame({"open":close,"high":close+1,"low":close-1,"close":close,"volume":np.ones(n)}, index=pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"))
    cfg={"fee_rate":0.001,"slippage_pct":0.0005,"min_backtest_trades":999,"timeframe":"1h"}
    r=run_backtest(df,"BTC/USDT",cfg)
    assert r.data_verdict=="INSUFFICIENT_DATA"
