import pandas as pd
import numpy as np
from crypto_bot.indicators import compute_indicators

def test_indicators_columns():
    n=300
    df=pd.DataFrame({"open":np.arange(n)+1,"high":np.arange(n)+2,"low":np.arange(n),"close":np.arange(n)+1,"volume":np.ones(n)}, index=pd.date_range("2024-01-01", periods=n, freq="h", tz="UTC"))
    out=compute_indicators(df)
    for c in ["macd","macd_signal","macd_hist","rsi","ema_50","ema_200"]: assert c in out.columns
    assert out["rsi"].between(0,100).all()
    assert out.isna().sum().sum() == 0
