from crypto_bot.signals import generate_signal, _last_signal
import pandas as pd

def test_buy_and_duplicate():
    _last_signal.clear()
    idx=pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC")
    df=pd.DataFrame({"macd":[0,2],"macd_signal":[1,1],"rsi":[40,40],"ema_50":[1,1],"ema_200":[1,1],"macd_hist":[0.1,0.2],"close":[100,101]}, index=idx)
    s1=generate_signal(df,"BTC/USDT"); assert s1.action=="BUY"
    s2=generate_signal(df,"BTC/USDT"); assert s2.action=="NEUTRAL"

def test_sell():
    _last_signal.clear()
    idx=pd.date_range("2024-01-01", periods=2, freq="h", tz="UTC")
    df=pd.DataFrame({"macd":[2,0],"macd_signal":[1,1],"rsi":[60,60],"ema_50":[2,2],"ema_200":[2,2],"macd_hist":[-0.1,-0.2],"close":[100,99]}, index=idx)
    s=generate_signal(df,"ETH/USDT"); assert s.action=="SELL"
