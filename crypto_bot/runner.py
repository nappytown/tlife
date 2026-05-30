import asyncio
from loguru import logger
from crypto_bot.config import config
from crypto_bot.safety import is_bot_stopped, assert_paper_mode, check_daily_limits
from crypto_bot.exchange import fetch_ohlcv
from crypto_bot.indicators import compute_indicators
from crypto_bot.signals import generate_signal
from crypto_bot.risk import calculate_risk, is_trade_allowed
from crypto_bot.ledger import get_open_trades
from crypto_bot.paper_executor import paper_enter, paper_exit, check_exit_conditions
from crypto_bot.alerts import send_entry_alert, send_exit_alert, send_safety_alert


def run_cycle():
    if is_bot_stopped():
        asyncio.run(send_safety_alert("Manual STOP_BOT triggered"))
        logger.warning("Bot halted by STOP_BOT")
        return
    assert_paper_mode()
    if not check_daily_limits(config["ledger_path"]):
        asyncio.run(send_safety_alert("Max daily loss reached"))
        logger.warning("Bot halted by daily limits")
        return

    df = fetch_ohlcv(config["symbol"], config["timeframe"], 500)
    dfi = compute_indicators(df)
    current_price = float(dfi.iloc[-1]["close"])

    open_trades = get_open_trades(config["symbol"])
    for trade in open_trades:
        reason = check_exit_conditions(trade, current_price)
        if reason:
            closed = paper_exit(trade["trade_id"], current_price, reason)
            asyncio.run(send_exit_alert(closed))

    signal = generate_signal(dfi, config["symbol"])
    if signal.action == "NEUTRAL":
        logger.info("NEUTRAL signal; skipping new entry")
        return

    if len(get_open_trades(config["symbol"])) >= config["max_open_trades"]:
        return
    if not is_trade_allowed(config["symbol"], config["ledger_path"]):
        return

    risk_params = calculate_risk(signal, config["account_balance"])
    trade = paper_enter(signal, risk_params)
    asyncio.run(send_entry_alert(trade))
    logger.info(f"TradeResult: entered {trade['trade_id']}")
