"""
Backtest a Gaussian Value-at-Risk (VaR) model against real historical
losses, to show how often the "normal distribution" assumption gets
violated in practice.
"""

import numpy as np
import pandas as pd


def gaussian_var(returns, confidence=0.99, window=250):
    """
    Compute a rolling Gaussian VaR estimate.

    At each point in time, look at the trailing `window` days of returns,
    compute their mean and standard deviation, and use the normal
    distribution to estimate the loss threshold that should only be
    breached (1 - confidence) of the time.

    Parameters
    ----------
    returns : pd.Series
        Daily log-returns.
    confidence : float
        VaR confidence level, e.g. 0.99 for 99% VaR.
    window : int
        Rolling window size in trading days (250 ~ 1 year).

    Returns
    -------
    pd.Series
        The VaR threshold (as a positive loss magnitude) for each day,
        aligned with `returns.index`. First `window` days will be NaN
        (not enough history yet).
    """
    from scipy.stats import norm

    z = norm.ppf(1 - confidence)  # e.g. for 99%, z ~ -2.33

    rolling_mean = returns.rolling(window).mean()
    rolling_std = returns.rolling(window).std()

    # VaR threshold: how far below the mean is the (1-confidence) quantile
    # expressed as a positive loss number
    var_threshold = -(rolling_mean + z * rolling_std)

    return var_threshold


def count_breaches(returns, var_threshold):
    """
    Count how many days the actual loss exceeded the VaR threshold.

    A "breach" happens when the realized loss (-return) is bigger than
    what the model said should only happen (1 - confidence) of the time.

    Returns
    -------
    breach_dates : pd.DatetimeIndex
        Dates where a breach occurred.
    breach_rate : float
        Fraction of valid days that were breaches.
    """
    losses = -returns
    valid = var_threshold.notna()

    is_breach = (losses > var_threshold) & valid
    breach_dates = returns.index[is_breach]
    breach_rate = is_breach.sum() / valid.sum()

    return breach_dates, breach_rate


if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from data_loader import download_prices, compute_log_returns

    prices = download_prices("^GSPC", start="2004-01-01")
    returns = compute_log_returns(prices)

    confidence = 0.99
    var_threshold = gaussian_var(returns, confidence=confidence, window=250)
    breach_dates, breach_rate = count_breaches(returns, var_threshold)

    expected_rate = 1 - confidence

    print(f"Confidence level: {confidence*100:.0f}%")
    print(f"Expected breach rate: {expected_rate*100:.2f}%")
    print(f"Observed breach rate: {breach_rate*100:.2f}%")
    print(f"Number of breaches: {len(breach_dates)}")
    print(f"Ratio observed/expected: {breach_rate/expected_rate:.2f}x")