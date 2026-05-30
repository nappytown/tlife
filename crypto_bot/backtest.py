import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import numpy as np
from loguru import logger
from crypto_bot.indicators import compute_indicators
from crypto_bot.signals import generate_signal, _last_signal


@dataclass
class BacktestResult:
    symbol: str; timeframe: str; candles_tested: int; total_trades: int; winning_trades: int; losing_trades: int
    win_rate: float; avg_win_pct: float; avg_loss_pct: float; profit_factor: float; max_drawdown_pct: float
    max_losing_streak: int; total_fees_paid: float; total_slippage: float; net_return_pct: float; sharpe_ratio: float; data_verdict: str


def run_backtest(df, symbol, config):
    _last_signal.clear()
    dfi = compute_indicators(df)
    balance = 10000.0
    equity = [balance]
    trades=[]; fees=0.0; slip=0.0; losing_streak=0; max_ls=0
    for i in range(2, len(dfi)):
        window = dfi.iloc[: i + 1]
        sig = generate_signal(window, symbol)
        if sig.action not in {"BUY", "SELL"}: continue
        entry=sig.price; stop=entry*0.98; target=entry*1.04
        next_close=float(dfi.iloc[i]["close"])
        if next_close <= stop: exit_p=stop
        elif next_close >= target: exit_p=target
        else: continue
        ret=(exit_p-entry)/entry
        fee = (entry+exit_p)*config["fee_rate"]
        sl = (entry+exit_p)*config["slippage_pct"]
        net = ret - fee/entry - sl/entry
        fees += fee; slip += sl
        trades.append(net)
        balance *= (1+net)
        equity.append(balance)
        if net<0: losing_streak+=1; max_ls=max(max_ls,losing_streak)
        else: losing_streak=0
    total=len(trades); wins=[t for t in trades if t>0]; losses=[t for t in trades if t<=0]
    dd = max((max(equity[:i+1])-v)/max(equity[:i+1]) for i,v in enumerate(equity)) if equity else 0
    profit_factor = (sum(wins)/abs(sum(losses))) if losses and sum(losses)!=0 else float('inf') if wins else 0
    sharpe = (np.mean(trades)/np.std(trades))*np.sqrt(252) if len(trades)>1 and np.std(trades)!=0 else 0
    verdict = "SUFFICIENT" if total >= config["min_backtest_trades"] else "INSUFFICIENT_DATA"
    if verdict=="INSUFFICIENT_DATA": logger.warning(f"Only {total} trades found. Increase BACKTEST_CANDLES or widen signal conditions before trusting this result.")
    res=BacktestResult(symbol, config.get("timeframe","1h"), len(df), total, len(wins), len(losses), (len(wins)/total*100 if total else 0), (np.mean(wins)*100 if wins else 0), (np.mean(losses)*100 if losses else 0), profit_factor, dd*100, max_ls, fees, slip, ((balance-10000)/10000*100), sharpe, verdict)
    Path("data/backtest_results").mkdir(parents=True, exist_ok=True)
    p=Path("data/backtest_results")/f"{symbol.replace('/','_')}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
    p.write_text(json.dumps(asdict(res), indent=2), encoding='utf-8')
    return res

def print_report(result):
    print(asdict(result))
