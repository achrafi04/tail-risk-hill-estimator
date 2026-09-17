# Tail Risk Estimation with the Hill Estimator

Estimating the tail index of real equity returns using the Hill estimator,
and showing where Gaussian Value-at-Risk breaks down.

## Idea

Equity returns are widely modeled as normally distributed, but extreme
losses (crashes) happen far more often -- and in tighter clusters -- than
a Gaussian model predicts. This project:

1. Estimates the tail index (alpha) of real equity index losses using the
   Hill estimator, across four major markets.
2. Backtests a Gaussian 99% Value-at-Risk model against real historical
   data to measure how badly it underestimates risk.
3. Shows that VaR breaches are temporally clustered around crisis periods,
   not uniformly distributed as a Gaussian model would imply.

## Results

### Tail index (Hill estimator, k=200)

| Index         | Alpha |
|---------------|-------|
| S&P 500       | 2.49  |
| CAC 40        | 2.61  |
| Nikkei 225    | 2.72  |
| EuroStoxx 50  | 2.57  |

All four major indices converge to alpha ~2.5-2.7 in the Hill plot plateau,
well below the alpha ~3-5 range often cited for equities -- suggesting
heavier tails than a naive Gaussian model would assume. Data: 2004-2026
(22 years), covering the 2008 financial crisis and the 2020 COVID crash.

![Hill plot comparison](results/figures/hill_plot_comparison.png)

### Gaussian VaR backtest (S&P 500, 99% confidence, 250-day rolling window)

| Metric              | Value |
|---------------------|-------|
| Expected breach rate| 1.00% |
| Observed breach rate| 2.73% |
| Number of breaches  | 149   |
| Observed / expected | 2.73x |

A Gaussian VaR model breaches its own 99% confidence threshold **2.73x more
often** than it should -- meaning a risk manager relying on this model is
caught off guard far more frequently than they believe.

### Breach clustering

| Metric                    | Value    |
|----------------------------|---------|
| Mean gap between breaches | 52 days  |
| Median gap between breaches | 14 days |
| Min gap                   | 1 day    |
| Max gap                   | 680 days |

The large gap between mean and median gap length is the signature of
clustering: breaches pile up during crisis windows (2008-09, 2011-12,
2020, 2022) and are nearly absent during calm periods -- violating the
independence assumption baked into the Gaussian VaR model.

![Breach timeline](results/figures/var_breaches_timeline.png)

## Structure

- `src/data_loader.py` -- download prices, compute log-returns and losses
- `src/hill_estimator.py` -- Hill estimator implementation
- `src/var_backtest.py` -- Gaussian VaR backtest + breach detection
- `notebooks/01_analysis.ipynb` -- full analysis, plots, and interpretation

## Setup

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


## Method notes

- The Hill estimator's choice of `k` (number of top losses used) matters:
  too small and the estimate is noisy, too large and non-extreme losses
  contaminate it. `k=200` was chosen by inspecting the Hill plot plateau
  across all four indices.
- Log-returns are used throughout (standard in quantitative finance --
  additive across time, well-behaved for small daily moves).
- VaR is computed with a 250-trading-day rolling window (~1 year), so the
  first year of data has no VaR estimate.

## Status

Core analysis complete. Possible extensions: formal statistical clustering
test (e.g. Ljung-Box on breach indicators), comparison against a
Student-t or EVT-based VaR model instead of Gaussian.
