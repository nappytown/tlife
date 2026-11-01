import signal
import sys
import time
import schedule
from loguru import logger
from crypto_bot.runner import run_cycle
from crypto_bot.config import config


def _sigint_handler(sig, frame):
    _ = (sig, frame)
    logger.info("Bot shutting down")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, _sigint_handler)
    schedule.every(config["run_interval_minutes"]).minutes.do(run_cycle)
    run_cycle()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
