from types import SimpleNamespace
from crypto_bot.risk import calculate_risk

def test_calculate_risk():
    sig=SimpleNamespace(price=100)
    r=calculate_risk(sig, 1000)
    assert round(r.stop_loss_price,2)==98
    assert round(r.take_profit_price,2)==104
    assert r.rr_ratio==2.0
