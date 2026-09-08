"""
Advanced Stock Market Analysis & Quantitative Portfolio Optimization.
Modular library for financial data ingestion, risk metrics calculation, and strategy backtesting.
"""

from .data_loader import fetch_stock_data, clean_financial_data
from .metrics import (
    calculate_daily_returns,
    calculate_cumulative_wealth,
    calculate_annualized_metrics,
    calculate_rolling_volatility,
    calculate_drawdowns,
)
from .backtest import run_sma_crossover_strategy

__all__ = [
    "fetch_stock_data",
    "clean_financial_data",
    "calculate_daily_returns",
    "calculate_cumulative_wealth",
    "calculate_annualized_metrics",
    "calculate_rolling_volatility",
    "calculate_drawdowns",
    "run_sma_crossover_strategy",
]
