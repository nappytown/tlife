import ta


def compute_indicators(df):
    out = df.copy()
    macd_obj = ta.trend.MACD(out["close"], window_fast=12, window_slow=26, window_sign=9)
    out["macd"] = macd_obj.macd()
    out["macd_signal"] = macd_obj.macd_signal()
    out["macd_hist"] = macd_obj.macd_diff()
    out["rsi"] = ta.momentum.RSIIndicator(out["close"], window=14).rsi()
    out["ema_50"] = ta.trend.EMAIndicator(out["close"], window=50).ema_indicator()
    out["ema_200"] = ta.trend.EMAIndicator(out["close"], window=200).ema_indicator()
    return out.dropna()
