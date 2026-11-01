from datetime import datetime, timezone
import json
import pytest
from crypto_bot.safety import is_bot_stopped, check_daily_limits, assert_paper_mode

def test_stop_bot_default_false(tmp_path, monkeypatch):
    monkeypatch.setenv("STOP_BOT_PATH", str(tmp_path / "STOP_BOT"))
    assert is_bot_stopped() is False

def test_stop_bot_true(tmp_path, monkeypatch):
    p = tmp_path / "STOP_BOT"; p.write_text("x")
    monkeypatch.setenv("STOP_BOT_PATH", str(p))
    assert is_bot_stopped() is True

def test_daily_limits(tmp_path, monkeypatch):
    lp = tmp_path / "l.json"
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    lp.write_text(json.dumps([{"entry_time": now, "realized_pnl": -100}], indent=2))
    monkeypatch.setenv("ACCOUNT_BALANCE", "1000")
    monkeypatch.setenv("MAX_DAILY_LOSS", "0.05")
    assert check_daily_limits(str(lp)) is False

def test_trade_count_limit(tmp_path, monkeypatch):
    lp=tmp_path / "l.json"; now=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    lp.write_text(json.dumps([{"entry_time": now, "realized_pnl": 1} for _ in range(5)]))
    monkeypatch.setenv("MAX_TRADES_PER_DAY", "5")
    assert check_daily_limits(str(lp)) is False

def test_assert_paper_mode(monkeypatch):
    monkeypatch.setenv("PAPER_MODE", "False")
    with pytest.raises(RuntimeError): assert_paper_mode()
