"""
Monthly aggregation and regression tests for day-of-week analysis.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm


def nw_lag(T):
    """Newey-West lag = floor(0.75 * T^(1/3))."""
    return max(1, int(0.75 * T ** (1 / 3)))


def aggregate_monthly_legs(legs_daily, date_info):
    """
    SUM daily returns within each (month, day-of-week) for each leg.

    Parameters
    ----------
    legs_daily : DataFrame indexed by Date with Spec_Return, Safe_Return, LS_Return
    date_info : DataFrame indexed by Date with DayName, YM, Daily_Rf

    Returns DataFrame with columns:
        YM, DayName, LS_Monthly, Spec_Monthly, Safe_Monthly, Rf_Monthly, N_Days
    """
    df = legs_daily.join(date_info[["DayName", "YM", "Daily_Rf", "Market_Excess"]])
    df = df.dropna(subset=["DayName"])

    monthly = df.groupby(["YM", "DayName"]).agg(
        LS_Monthly=("LS_Return", "sum"),
        Spec_Monthly=("Spec_Return", "sum"),
        Safe_Monthly=("Safe_Return", "sum"),
        Rf_Monthly=("Daily_Rf", "sum"),
        MktRF_Monthly=("Market_Excess", "sum"),
        N_Days=("LS_Return", "count"),
    ).reset_index()

    return monthly


def run_mean_test(excess_returns):
    """
    Excess return test: is mean(excess_returns) ≠ 0?

    Regresses on a constant only with Newey-West HAC standard errors.
    The coefficient = mean, t-stat tests H0: mean = 0.

    Parameters
    ----------
    excess_returns : Series of monthly excess returns

    Returns (result_obj, n_obs) or (None, n_obs) if < 12 observations.
    """
    Y = excess_returns.dropna()
    if len(Y) < 12:
        return None, len(Y)

    X = pd.DataFrame({"const": np.ones(len(Y))}, index=Y.index)
    lag = nw_lag(len(Y))
    result = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})
    return result, len(Y)


def run_capm(excess_returns, monthly_mktrf):
    """
    CAPM: excess_return = alpha + beta * MktRF + epsilon
    Newey-West HAC standard errors.

    Parameters
    ----------
    excess_returns : Series indexed by YM
    monthly_mktrf : Series indexed by YM

    Returns (result_obj, n_obs) or (None, n_obs) if < 12 observations.
    """
    df = pd.DataFrame({"Y": excess_returns, "MktRF": monthly_mktrf}).dropna()
    if len(df) < 12:
        return None, len(df)

    Y = df["Y"]
    X = sm.add_constant(df["MktRF"])
    lag = nw_lag(len(df))
    result = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})
    return result, len(df)


# ── Period helpers ────────────────────────────────────────────────────

def make_post_dummy(ym_index, break_ym):
    """
    Build a 0/1 Series: 0 for months before break_ym, 1 from break_ym onward.

    Parameters
    ----------
    ym_index : Index of YM period strings (e.g. "2017-01")
    break_ym : str, first month of Post period (e.g. "2017-01")

    Returns Series of 0/1 ints aligned to ym_index.
    """
    return (ym_index >= break_ym).astype(int)


def filter_period(series, break_ym, period):
    """
    Keep only Pre or Post observations from a YM-indexed Series.

    Parameters
    ----------
    series : Series indexed by YM strings
    break_ym : str, first month of Post period
    period : "Pre" or "Post"
    """
    if period == "Pre":
        return series[series.index < break_ym]
    else:
        return series[series.index >= break_ym]


# ── Split-sample regressions ─────────────────────────────────────────

def run_mean_test_period(excess_returns, break_ym, period):
    """Run mean test on Pre or Post subsample only."""
    sub = filter_period(excess_returns, break_ym, period)
    return run_mean_test(sub)


def run_capm_period(excess_returns, monthly_mktrf, break_ym, period):
    """Run CAPM alpha test on Pre or Post subsample only."""
    sub_y = filter_period(excess_returns, break_ym, period)
    sub_mkt = filter_period(monthly_mktrf, break_ym, period)
    return run_capm(sub_y, sub_mkt)


# ── Dummy-variable regressions (pooled sample) ───────────────────────

def run_mean_test_dummy(excess_returns, break_ym):
    """
    Pooled mean test with Post dummy:
        excess_return = alpha + delta * Post + epsilon

    The intercept (alpha) = Pre-period mean excess return.
    delta = change in mean from Pre to Post.
    Tests H0: delta = 0 (no change across periods).

    Returns (result_obj, n_obs) or (None, n_obs).
    """
    Y = excess_returns.dropna()
    if len(Y) < 12:
        return None, len(Y)

    post = make_post_dummy(Y.index, break_ym)
    X = pd.DataFrame({"const": np.ones(len(Y)), "Post": post}, index=Y.index)
    lag = nw_lag(len(Y))
    result = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})
    return result, len(Y)


def run_capm_dummy(excess_returns, monthly_mktrf, break_ym):
    """
    Full-Interaction Pooled CAPM (Chow-style):
        excess_return = alpha + delta*Post + beta*MktRF + theta*(MktRF*Post) + eps

    This tests for shifts in BOTH the alpha (anomaly) and beta (risk).
    """
    df = pd.DataFrame({"Y": excess_returns, "MktRF": monthly_mktrf}).dropna()
    if len(df) < 12:
        return None, len(df)

    post = make_post_dummy(df.index, break_ym)
    Y = df["Y"]
    X = pd.DataFrame({
        "const": np.ones(len(df)),
        "Post": post,
        "MktRF": df["MktRF"],
        "MktRF_Post": df["MktRF"] * post
    }, index=df.index)
    
    lag = nw_lag(len(df))
    result = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})
    
    # Structural Break F-Test (Chow Test equivalent)
    # H0: delta = 0 and theta = 0 (No change in alpha or beta)
    try:
        f_test = result.f_test("Post = 0, MktRF_Post = 0")
        result.chow_f = f_test.fvalue
        result.chow_p = f_test.pvalue
    except:
        result.chow_f, result.chow_p = np.nan, np.nan

    return result, len(df)
