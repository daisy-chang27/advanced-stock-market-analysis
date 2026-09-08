"""
Quantitative Strategy Backtesting Module.
Implements trend-following and momentum rules (e.g., Simple Moving Average Crossover)
with strict elimination of look-ahead bias via signal shifting.
"""

from typing import Dict
import numpy as np
import pandas as pd


def run_sma_crossover_strategy(
    prices: pd.Series,
    window: int = 50,
    trading_days_per_year: int = 252
) -> Dict[str, Union[float, pd.Series]]:
    """
    Backtest a Simple Moving Average (SMA) Trend-Following Strategy against Buy-and-Hold.

    Trading Rule:
        - If Price > SMA(window): Long asset (Signal = 1)
        - Else: Stay in Cash (Signal = 0)
        - Signal is shifted by +1 day (t-1 signal applies to t return) to prevent look-ahead bias.

    Parameters:
        prices (pd.Series): Historical closing prices of a single asset.
        window (int): Moving average lookback period in days (default: 50).
        trading_days_per_year (int): Trading sessions per year (252).

    Returns:
        Dict: Performance statistics and equity curve comparison.
    """
    daily_returns = prices.pct_change().dropna()
    sma = prices.rolling(window=window).mean()

    # Generate raw binary trading signal (1 = Long, 0 = Cash)
    raw_signal = (prices > sma).astype(int)

    # Shift signal by 1 period to strictly eliminate look-ahead bias
    trading_signal = raw_signal.shift(1).dropna()

    # Align returns with active trading signals
    aligned_returns = daily_returns.loc[trading_signal.index]
    strategy_returns = trading_signal * aligned_returns

    # Cumulative growth trajectories
    bnh_equity = (1 + aligned_returns).cumprod()
    strat_equity = (1 + strategy_returns).cumprod()

    # Maximum Drawdowns
    bnh_dd = (bnh_equity - bnh_equity.cummax()) / bnh_equity.cummax()
    strat_dd = (strat_equity - strat_equity.cummax()) / strat_equity.cummax()

    return {
        "bnh_total_return": float(bnh_equity.iloc[-1] - 1),
        "strategy_total_return": float(strat_equity.iloc[-1] - 1),
        "bnh_annualized_volatility": float(aligned_returns.std() * np.sqrt(trading_days_per_year)),
        "strategy_annualized_volatility": float(strategy_returns.std() * np.sqrt(trading_days_per_year)),
        "bnh_max_drawdown": float(bnh_dd.min()),
        "strategy_max_drawdown": float(strat_dd.min()),
        "strategy_equity_curve": strat_equity,
        "bnh_equity_curve": bnh_equity,
    }
