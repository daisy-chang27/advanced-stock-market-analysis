"""
Quantitative Risk and Return Metrics Module.
Calculates annualized returns, rolling volatility, Sharpe ratio, maximum drawdowns,
and covariance / correlation matrices.
"""

from typing import Dict, Union
import numpy as np
import pandas as pd


def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Compute daily percentage returns from asset prices."""
    return prices.pct_change().dropna()


def calculate_cumulative_wealth(
    returns: Union[pd.DataFrame, pd.Series],
    initial_capital: float = 10000.0
) -> Union[pd.DataFrame, pd.Series]:
    """Calculate cumulative wealth curve given an initial capital allocation."""
    return initial_capital * (1 + returns).cumprod()


def calculate_annualized_metrics(
    returns: pd.DataFrame,
    risk_free_rate: float = 0.04,
    trading_days_per_year: int = 252
) -> pd.DataFrame:
    """
    Compute Annualized Return, Annualized Volatility, and Annualized Sharpe Ratio.

    Parameters:
        returns (pd.DataFrame): Daily return series.
        risk_free_rate (float): Annual risk-free rate (default: 4%).
        trading_days_per_year (int): Standard trading sessions per year (252).

    Returns:
        pd.DataFrame: Summary table with quantitative metrics.
    """
    daily_rf = (1 + risk_free_rate) ** (1 / trading_days_per_year) - 1

    ann_return = returns.mean() * trading_days_per_year
    ann_volatility = returns.std() * np.sqrt(trading_days_per_year)
    excess_return = returns.sub(daily_rf, axis=0)
    sharpe_ratio = (excess_return.mean() / returns.std()) * np.sqrt(trading_days_per_year)

    metrics = pd.DataFrame({
        "Annualized Return": ann_return,
        "Annualized Volatility": ann_volatility,
        "Sharpe Ratio": sharpe_ratio
    })
    return metrics


def calculate_drawdowns(prices: Union[pd.DataFrame, pd.Series]) -> pd.DataFrame:
    """
    Compute percentage drawdowns and peak-to-trough series.

    Returns:
        pd.DataFrame: Underwater drawdown series (prices - running_max) / running_max
    """
    running_max = prices.cummax()
    drawdowns = (prices - running_max) / running_max
    return drawdowns


def calculate_rolling_volatility(
    returns: pd.DataFrame,
    window: int = 20,
    trading_days_per_year: int = 252
) -> pd.DataFrame:
    """Compute annualized rolling standard deviation."""
    return returns.rolling(window=window).std() * np.sqrt(trading_days_per_year)
