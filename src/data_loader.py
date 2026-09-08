"""
Data Acquisition and Pipeline Module for Financial Time Series.
Retrieves and validates multi-asset OHLCV data using the Yahoo Finance API.
"""

from typing import List, Tuple
import pandas as pd
import yfinance as yf


def fetch_stock_data(
    tickers: List[str],
    start_date: str = "2020-01-01",
    end_date: str = "2026-01-01"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Download historical market data for multiple tickers.

    Parameters:
        tickers (List[str]): List of stock ticker symbols.
        start_date (str): Start date string (YYYY-MM-DD).
        end_date (str): End date string (YYYY-MM-DD).

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - Full multi-index OHLCV DataFrame
            - Closing prices DataFrame for the selected tickers
    """
    print(f"Fetching market data for {len(tickers)} assets: {', '.join(tickers)}...")
    raw_data = yf.download(tickers, start=start_date, end=end_date, progress=False)

    if raw_data.empty:
        raise ValueError("No data returned from Yahoo Finance API.")

    prices = raw_data["Close"][tickers].copy()
    prices.index = pd.to_datetime(prices.index)

    return raw_data, prices


def clean_financial_data(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Verify and clean historical price DataFrame (forward fill and drop leading nulls).

    Parameters:
        prices (pd.DataFrame): Asset price series.

    Returns:
        pd.DataFrame: Cleaned price series.
    """
    cleaned = prices.ffill().dropna()
    missing_count = cleaned.isna().sum().sum()
    if missing_count > 0:
        print(f"Warning: {missing_count} missing values remain after cleaning.")
    return cleaned
