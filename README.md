# Tail Risk Estimation with the Hill Estimator

Estimating the tail index of real equity returns using the Hill estimator,
and showing where Gaussian Value-at-Risk breaks down.

## Idea

Pull ~20 years of daily returns for several equity indices, fit a power law
to the left tail of the loss distribution using the Hill estimator, and
compare the resulting tail exponents. Then backtest a Gaussian 99% VaR
against real historical breaches to show that extreme losses are more
frequent -- and more clustered -- than a normal distribution would predict.

## Structure

- src/data_loader.py -- download prices, compute log-returns
- src/hill_estimator.py -- Hill estimator implementation
- src/var_backtest.py -- Gaussian VaR vs. empirical breaches
- src/viz.py -- plots (Hill plot, return distributions)
- notebooks/01_analysis.ipynb -- main analysis and results

## Setup

\\\
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
\\\

## Status

Work in progress
