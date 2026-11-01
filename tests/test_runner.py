from types import SimpleNamespace
from crypto_bot import runner


def test_runner_order(monkeypatch):
    calls=[]
    monkeypatch.setattr(runner, "is_bot_stopped", lambda: calls.append("stop") or False)
    monkeypatch.setattr(runner, "assert_paper_mode", lambda: calls.append("paper"))
    monkeypatch.setattr(runner, "check_daily_limits", lambda p: calls.append("limits") or True)
    monkeypatch.setattr(runner, "fetch_ohlcv", lambda s,t,l: calls.append("fetch") or __import__('pandas').DataFrame({"close":[1,2]}, index=__import__('pandas').date_range("2024", periods=2, tz="UTC")))
    monkeypatch.setattr(runner, "compute_indicators", lambda df: calls.append("ind") or df.assign(macd=[0,0],macd_signal=[0,0],rsi=[50,50],ema_50=[1,1],ema_200=[1,1],macd_hist=[0,0]))
    monkeypatch.setattr(runner, "get_open_trades", lambda s: calls.append("open") or [{"trade_id":"1","stop_loss":1.5,"take_profit":2.5,"symbol":s,"status":"OPEN"}])
    monkeypatch.setattr(runner, "check_exit_conditions", lambda t,p: calls.append("exit_check") or None)
    monkeypatch.setattr(runner, "generate_signal", lambda df,s: calls.append("sig") or SimpleNamespace(action="NEUTRAL"))
    runner.run_cycle()
    assert calls[:4]==["stop","paper","limits","fetch"]
    assert "exit_check" in calls and calls.index("exit_check") < calls.index("sig")
