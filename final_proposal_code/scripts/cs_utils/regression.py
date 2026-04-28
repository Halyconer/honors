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
    Sum daily returns within each (month, day-of-week) for each leg.
    Matches Birru (2018) arithmetic aggregation.

    Parameters
    ----------
    legs_daily : DataFrame indexed by Date with Spec_Return, Safe_Return, LS_Return
    date_info : DataFrame indexed by Date with DayName, YM, Daily_Rf

    Returns DataFrame with columns:
        YM, DayName, LS_Monthly, Spec_Monthly, Safe_Monthly, Rf_Monthly, N_Days
    """
    factor_cols = ["DayName", "YM", "Daily_Rf", "Market_Excess"]
    for fac in ["SMB", "HML"]:
        if fac in date_info.columns:
            factor_cols.append(fac)

    df = legs_daily.join(date_info[factor_cols])
    df = df.dropna(subset=["DayName"])

    agg_kwargs = dict(
        LS_Monthly=("LS_Return", "sum"),
        Spec_Monthly=("Spec_Return", "sum"),
        Safe_Monthly=("Safe_Return", "sum"),
        Rf_Monthly=("Daily_Rf", "sum"),
        MktRF_Monthly=("Market_Excess", "sum"),
        N_Days=("LS_Return", "count"),
    )
    for fac in ["SMB", "HML"]:
        if fac in df.columns:
            agg_kwargs[f"{fac}_Monthly"] = (fac, "sum")

    monthly = df.groupby(["YM", "DayName"]).agg(**agg_kwargs).reset_index()
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


def run_ff3(excess_returns, monthly_mktrf, monthly_smb, monthly_hml):
    """
    FF3: excess_return = alpha + beta_mkt*MktRF + beta_smb*SMB + beta_hml*HML + eps
    Newey-West HAC standard errors.

    Factors are IDX-constructed following Foye & Valentinčič (2020).

    Parameters
    ----------
    excess_returns : Series indexed by YM
    monthly_mktrf  : Series indexed by YM (full-month JCI excess return)
    monthly_smb    : Series indexed by YM (monthly SMB from ff3_factors.csv)
    monthly_hml    : Series indexed by YM (monthly HML from ff3_factors.csv)

    Returns (result_obj, n_obs) or (None, n_obs) if < 12 observations.
    """
    df = pd.DataFrame({
        "Y": excess_returns, "MktRF": monthly_mktrf,
        "SMB": monthly_smb, "HML": monthly_hml,
    }).dropna()
    if len(df) < 12:
        return None, len(df)

    Y = df["Y"]
    X = sm.add_constant(df[["MktRF", "SMB", "HML"]])
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


def run_ff3_period(excess_returns, monthly_mktrf, monthly_smb, monthly_hml,
                   break_ym, period):
    """Run FF3 alpha test on Pre or Post subsample only."""
    sub_y   = filter_period(excess_returns, break_ym, period)
    sub_mkt = filter_period(monthly_mktrf,  break_ym, period)
    sub_smb = filter_period(monthly_smb,    break_ym, period)
    sub_hml = filter_period(monthly_hml,    break_ym, period)
    return run_ff3(sub_y, sub_mkt, sub_smb, sub_hml)


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
    Full-Interaction Pooled CAPM with HAC Wald test for structural break:
        excess_return = alpha + delta*Post + beta*MktRF + theta*(MktRF*Post) + eps

    The joint Wald F-test (H0: delta=0, theta=0) tests for a parameter shift
    in both alpha and beta at the pre-specified break date `break_ym`.

    NOTE ON METHODOLOGY: We use a Wald F-statistic on the interaction coefficients
    calculated with a HAC (Newey-West) covariance matrix. This is a robust
    alternative to the classical 1960s-era RSS-based tests that require 
    homoskedasticity. In daily-aggregated monthly returns, heteroskedasticity
    and autocorrelation are first-order concerns, making the HAC Wald approach 
    the correct econometric choice.

    INTERPRETATION CAVEAT: Rejecting H0 implies the parameters differ at the
    pre-specified date `break_ym`. It does NOT validate that this date is the
    "true" or "best" break point — that requires either a Wald F-sequence
    across candidate dates, a Quandt-Andrews supF (Andrews 1993), or a
    Bai-Perron endogenous breakpoint estimator.

    The break-test statistic and p-value are stored on the result object as:
        result.break_f         : Wald F-statistic
        result.break_p         : p-value
        result.break_test_type : "HAC Wald (joint: Post=0, MktRF*Post=0)"
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

    # Joint Wald F-test on interaction terms with HAC-robust covariance.
    # H0: delta = 0 AND theta = 0  (no change in alpha or beta across break)
    result.break_test_type = "HAC Wald (joint: Post=0, MktRF*Post=0)"
    try:
        f_test = result.f_test("Post = 0, MktRF_Post = 0")
        result.break_f = float(np.squeeze(f_test.fvalue))
        result.break_p = float(np.squeeze(f_test.pvalue))
    except (ValueError, np.linalg.LinAlgError) as e:
        result.break_f, result.break_p = np.nan, np.nan
        result.break_test_error = repr(e)

    return result, len(df)


def run_ff3_dummy(excess_returns, monthly_mktrf, monthly_smb, monthly_hml, break_ym):
    """
    Full-interaction pooled FF3 with HAC Wald test for structural break:
        excess = alpha + delta*Post
               + beta_mkt*MktRF + theta_mkt*(MktRF*Post)
               + beta_smb*SMB   + theta_smb*(SMB*Post)
               + beta_hml*HML   + theta_hml*(HML*Post) + eps

    Joint Wald F-test H0: delta=theta_mkt=theta_smb=theta_hml=0.
    Same HAC-robust interpretation as run_capm_dummy.

    Break statistic stored as result.break_f, result.break_p.
    """
    df = pd.DataFrame({
        "Y": excess_returns, "MktRF": monthly_mktrf,
        "SMB": monthly_smb, "HML": monthly_hml,
    }).dropna()
    if len(df) < 12:
        return None, len(df)

    post = make_post_dummy(df.index, break_ym)
    Y = df["Y"]
    X = pd.DataFrame({
        "const":      np.ones(len(df)),
        "Post":       post,
        "MktRF":      df["MktRF"],
        "MktRF_Post": df["MktRF"] * post,
        "SMB":        df["SMB"],
        "SMB_Post":   df["SMB"]   * post,
        "HML":        df["HML"],
        "HML_Post":   df["HML"]   * post,
    }, index=df.index)

    lag = nw_lag(len(df))
    result = sm.OLS(Y, X).fit(cov_type="HAC", cov_kwds={"maxlags": lag})

    result.break_test_type = "HAC Wald (joint: Post=0, MktRF_Post=0, SMB_Post=0, HML_Post=0)"
    try:
        f_test = result.f_test(
            "Post = 0, MktRF_Post = 0, SMB_Post = 0, HML_Post = 0"
        )
        result.break_f = float(np.squeeze(f_test.fvalue))
        result.break_p = float(np.squeeze(f_test.pvalue))
    except (ValueError, np.linalg.LinAlgError) as e:
        result.break_f, result.break_p = np.nan, np.nan
        result.break_test_error = repr(e)

    return result, len(df)
