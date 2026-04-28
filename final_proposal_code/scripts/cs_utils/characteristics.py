"""
Characteristic computation: Idiosyncratic Volatility and Max Return.
"""

import pandas as pd
import numpy as np


def compute_ivol(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute idiosyncratic volatility via rolling 60-day CAPM residuals.
    Optimized for performance using pandas rolling.apply.

    Returns DataFrame with columns [Instrument, Sort_YearMonth, Ivol].
    """
    print("\nComputing idiosyncratic volatility (CAPM residuals, 60-day rolling)...")
    df = daily_df.dropna(subset=["Stock_Return", "Market_Excess"]).copy()
    df = df.sort_values(["Instrument", "Date"])

    def solve_ivol(window):
        # window is a 2D array if we use a helper, but rolling.apply passes 1D.
        # We'll use a trick: rolling on an index and then looking up data.
        pass

    # A more robust vectorized way for rolling regressions:
    # Let y = beta*x + e.  beta = cov(x,y)/var(x).  e = y - beta*x.
    # We need rolling cov and rolling var.
    
    # 1. Rolling window stats per instrument
    g = df.groupby("Instrument")
    
    # We use a more robust alignment by keeping the original index
    mkt_var = g["Market_Excess"].rolling(window=60, min_periods=60).var().reset_index(level=0, drop=True)
    
    # For covariance, we need to be careful with the index
    # rolling().cov() returns a series with MultiIndex (Instrument, original_index)
    cov_series = g.apply(lambda x: x["Stock_Return"].rolling(60).cov(x["Market_Excess"]), include_groups=False).reset_index(level=0, drop=True)
    
    # Ensure they are aligned with df by using the same index
    mkt_var = mkt_var.reindex(df.index)
    cov_series = cov_series.reindex(df.index)

    # beta = cov(r, m) / var(m)
    beta = cov_series / mkt_var
    
    # We need rolling means and variances for the IVOL formula
    roll_mean_ret = g["Stock_Return"].rolling(window=60).mean().reset_index(level=0, drop=True).reindex(df.index)
    roll_mean_mkt = g["Market_Excess"].rolling(window=60).mean().reset_index(level=0, drop=True).reindex(df.index)
    roll_var_ret  = g["Stock_Return"].rolling(window=60).var().reset_index(level=0, drop=True).reindex(df.index)
    
    # Standard deviation of residuals in the 60-day window
    # Var(e) = Var(r) + beta^2 * Var(m) - 2 * beta * Cov(r, m)
    ivol_var = roll_var_ret + (beta**2 * mkt_var) - (2 * beta * cov_series)
    df["Ivol"] = np.sqrt(ivol_var.clip(lower=0))

    # Aggregate to monthly: use end-of-month Ivol for sorting
    ivol_monthly = (
        df.dropna(subset=["Ivol"])
        .sort_values("Date")
        .groupby(["Instrument", "YearMonth"])
        .last()[["Ivol"]]
        .reset_index()
    )

    # Lag by 1 month for sorting
    ivol_monthly["Sort_YearMonth"] = (
        pd.to_datetime(ivol_monthly["YearMonth"]) + pd.DateOffset(months=1)
    ).dt.to_period("M").astype(str)

    return ivol_monthly[["Instrument", "Sort_YearMonth", "Ivol"]]


def compute_max_return(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute max daily return in prior month (Birru's Max characteristic).

    Returns DataFrame with columns [Instrument, Sort_YearMonth, Max_Return].
    Sort_YearMonth is lagged +1 month.
    """
    daily_sorted = daily_df.sort_values(["Instrument", "Date"])

    max_monthly = (
        daily_sorted.groupby(["Instrument", "YearMonth"])
        .agg(Max_Return=("Stock_Return", "max"), N_Days=("Stock_Return", "count"))
        .reset_index()
    )
    max_monthly = max_monthly[max_monthly["N_Days"] >= 15].copy()
    max_monthly["Sort_YearMonth"] = (
        pd.to_datetime(max_monthly["YearMonth"]) + pd.DateOffset(months=1)
    ).dt.to_period("M").astype(str)

    return max_monthly[["Instrument", "Sort_YearMonth", "Max_Return"]]
