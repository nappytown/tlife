import pytest
from crypto_bot.alerts import format_entry_message, format_exit_message, send_safety_alert


def test_formats():
    t={"symbol":"BTC/USDT","entry_price":43250.0,"stop_loss":42385.0,"take_profit":44980.0,"entry_reason":"MACD crossover + RSI < 50","entry_time":"2024-01-15T14:30:00Z","rsi":28.4,
       "exit_price":44980.0,"exit_reason":"TARGET","realized_pnl":39.84,"position_size":0.023,"exit_time":"2024-01-16T09:15:00Z"}
    assert "PAPER BUY" in format_entry_message(t)
    assert "PAPER EXIT" in format_exit_message(t)

@pytest.mark.asyncio
async def test_safety_alert_no_crash():
    await send_safety_alert("Max daily loss reached")
