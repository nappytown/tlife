import os
import pytest

@pytest.fixture(autouse=True)
def env_defaults(tmp_path, monkeypatch):
    monkeypatch.setenv("PAPER_MODE", "True")
    monkeypatch.setenv("ACCOUNT_BALANCE", "1000")
    monkeypatch.setenv("MAX_DAILY_LOSS", "0.05")
    monkeypatch.setenv("MAX_TRADES_PER_DAY", "5")
    monkeypatch.setenv("LEDGER_PATH", str(tmp_path / "ledger.json"))
