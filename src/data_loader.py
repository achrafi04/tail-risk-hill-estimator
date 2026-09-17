"""
Download historical price data and compute daily log-returns and losses.
"""

import numpy as np
import pandas as pd
import yfinance as yf


def download_prices(ticker, start="2004-01-01", end=None):
    """
    Download daily closing prices for a given ticker.

    Parameters
    ----------
    ticker : str
        Yahoo Finance ticker, e.g. "^GSPC" for S&P 500, "^FCHI" for CAC 40.
    start : str
        Start date, "YYYY-MM-DD".
    end : str or None
        End date. None means "up to today".

    Returns
    -------
    pd.Series
        Daily closing prices, indexed by date.
    """
    data = yf.download(ticker, start=start, end=end, progress=False)

    if data.empty:
        raise ValueError(f"No data returned for ticker '{ticker}'. Check the symbol.")

    prices = data["Close"]

    # yfinance sometimes returns a DataFrame with a single column
    # instead of a Series -- squeeze it down if needed
    if isinstance(prices, pd.DataFrame):
        prices = prices.iloc[:, 0]

    return prices


def compute_log_returns(prices):
    """
    Compute daily log-returns from a price series.

    log-return_t = ln(price_t / price_{t-1})

    This is the standard way to measure daily % change in finance --
    it's approximately the same as % change for small moves, but has
    nicer mathematical properties (returns over multiple days just add up).
    """
    log_returns = np.log(prices / prices.shift(1))
    return log_returns.dropna()


def compute_losses(log_returns):
    """
    Extract the "losses" from a return series: how much you lost on
    down days, expressed as a positive number.

    A day with return -0.03 (lost 3%) becomes a loss of 0.03.
    Up days are dropped entirely -- we only care about the left tail.
    """
    losses = -log_returns[log_returns < 0]
    return losses


if __name__ == "__main__":
    # quick manual test: download S&P 500 and print basic stats
    ticker = "^GSPC"
    prices = download_prices(ticker, start="2004-01-01")
    returns = compute_log_returns(prices)
    losses = compute_losses(returns)

    print(f"Ticker: {ticker}")
    print(f"Price data points: {len(prices)}")
    print(f"Return data points: {len(returns)}")
    print(f"Number of down days (losses): {len(losses)}")
    print(f"Biggest single-day loss: {losses.max():.4f} ({losses.max()*100:.2f}%)")
    print(f"Date range: {prices.index.min().date()} to {prices.index.max().date()}")