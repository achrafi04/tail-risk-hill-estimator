"""
Hill estimator for the tail index of a distribution.

Given a series of losses (positive numbers = how much you lost that day),
this estimates alpha: how "fat" the tail is. Lower alpha = fatter tail =
more extreme events than a normal distribution would predict.
"""

import numpy as np


def hill_estimator(losses, kmax):
    """
    Compute the Hill estimator of alpha for k = 1, 2, ..., kmax.

    Parameters
    ----------
    losses : array-like
        Raw losses (should be positive numbers -- e.g. -returns on down days,
        or just all losses if you're only looking at negative returns).
    kmax : int
        Maximum number of top losses to consider.

    Returns
    -------
    k_values : np.ndarray
        Array [1, 2, ..., kmax]
    alpha_values : np.ndarray
        Estimated alpha for each corresponding k.
    """
    losses = np.asarray(losses)
    losses = losses[losses > 0]  # keep only actual losses, sanity check

    # sort descending: biggest loss first
    x = np.sort(losses)[::-1]

    if kmax >= len(x):
        raise ValueError(
            f"kmax ({kmax}) must be smaller than the number of losses ({len(x)})"
        )

    log_x = np.log(x[: kmax + 1])  # need kmax+1 points: x_1 ... x_kmax, x_{kmax+1}
    k_values = np.arange(1, kmax + 1)

    # Hill estimator formula:
    # alpha_hat(k) = [ (1/k) * sum_{i=1}^{k} ln(x_i / x_{k+1}) ]^-1
    #
    # cumsum(log_x)[:kmax] gives, for each k, sum_{i=1}^{k} ln(x_i)
    # log_x[1:kmax+1] gives ln(x_{k+1}) for each k
    cumulative_log = np.cumsum(log_x[:kmax])
    log_threshold = log_x[1 : kmax + 1]

    mean_log_excess = cumulative_log / k_values - log_threshold
    alpha_values = 1.0 / mean_log_excess

    return k_values, alpha_values


if __name__ == "__main__":
    # quick sanity check with fake data: a Pareto distribution with known alpha
    np.random.seed(42)
    true_alpha = 4.0
    fake_losses = (np.random.pareto(true_alpha, size=5000) + 1)  # Pareto(alpha)

    k_vals, alphas = hill_estimator(fake_losses, kmax=500)

    print(f"True alpha used to generate data: {true_alpha}")
    print(f"Estimated alpha around k=100: {alphas[99]:.2f}")
    print(f"Estimated alpha around k=300: {alphas[299]:.2f}")