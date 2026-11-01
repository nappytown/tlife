import asyncio
from loguru import logger
from telegram import Bot
from crypto_bot.config import config


def format_entry_message(trade) -> str:
    return (f"🟢 PAPER BUY — {trade['symbol']}\n"
            f"💰 Entry: ${trade['entry_price']:,.2f}\n"
            f"🛑 Stop Loss: ${trade['stop_loss']:,.2f}\n"
            f"🎯 Take Profit: ${trade['take_profit']:,.2f}\n"
            f"📊 RSI: {trade.get('rsi', 0):.1f} | MACD cross ✅\n"
            f"📝 BUY — {trade['entry_reason']}\n"
            f"🕐 {trade['entry_time'].replace('T',' ')[:16]} UTC\n"
            f"⚠️ PAPER MODE — no real funds")


def format_exit_message(trade) -> str:
    pnl = trade["realized_pnl"] or 0
    pct = (pnl / (trade["entry_price"] * trade["position_size"])) * 100 if trade["entry_price"] else 0
    return (f"🔴 PAPER EXIT — {trade['symbol']}\n"
            f"📤 Exit: ${trade['exit_price']:,.2f} ({trade['exit_reason']} HIT)\n"
            f"📥 Entry was: ${trade['entry_price']:,.2f}\n"
            f"💵 PnL: {pnl:+.2f} ({pct:+.2f}%)\n"
            f"🕐 {trade['exit_time'].replace('T',' ')[:16]} UTC\n"
            f"⚠️ PAPER MODE")


async def _send(msg: str):
    if not config["telegram_token"] or not config["telegram_chat_id"]:
        return
    try:
        bot = Bot(token=config["telegram_token"])
        await bot.send_message(chat_id=config["telegram_chat_id"], text=msg)
    except Exception as e:
        logger.error(f"Telegram send failed: {e}")


async def send_entry_alert(trade):
    await _send(format_entry_message(trade))


async def send_exit_alert(trade):
    await _send(format_exit_message(trade))


async def send_safety_alert(reason: str):
    await _send(f"🚨 BOT HALTED — {reason}\n🛑 Manual review required before restart")
