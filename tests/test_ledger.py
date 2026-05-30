import crypto_bot.ledger as ledger

def test_open_close_trade(tmp_path, monkeypatch):
    monkeypatch.setattr(ledger, "LEDGER_PATH", str(tmp_path/"ledger.json"))
    trade={"trade_id":"1","symbol":"BTC/USDT","status":"OPEN","entry_price":100,"position_size":1,"entry_time":"2024-01-01T00:00:00Z"}
    ledger.open_trade(trade)
    assert len(ledger.get_open_trades("BTC/USDT"))==1
    t=ledger.close_trade("1",110,"TARGET")
    assert t["status"]=="CLOSED"
