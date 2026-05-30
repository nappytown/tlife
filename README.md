# Crypto Trading Bot v2 (Paper Only)

## Setup
1. Create virtualenv and install dependencies from `requirements.txt`.
2. Copy `.env.example` to `.env` and review all values.
3. Keep `PAPER_MODE=True` for phases 0-6.

## .env explanation
Contains exchange settings, risk settings, safety limits, and Telegram credentials.

## Paper mode warning
This bot is a paper-trading research tool and should not be connected to real funds.

## Kill switch usage
To stop immediately, create a file named `STOP_BOT` at repo root (copy from `STOP_BOT.example`).

## Ledger
`data/ledger.json` stores OPEN/CLOSED trade lifecycle records.

## Backtest output
Backtest JSON files are written to `data/backtest_results/` and include `data_verdict`.

## Tests
Run `pytest`.
