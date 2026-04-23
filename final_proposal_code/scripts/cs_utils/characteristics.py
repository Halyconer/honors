"""
Characteristic computation: Idiosyncratic Volatility and Max Return.
"""

import pandas as pd
import numpy as np


def compute_ivol(daily_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute idiosyncratic volatility via rolling 60-day CAPM residuals.

    Returns DataFrame with columns [Instrument, Sort_YearMonth, Ivol].
    Sort_YearMonth is lagged +1 month (measured in t-1, used for sorting in t).
    """
    print("\nComputing idiosyncratic volatility (CAPM residuals, 60-day rolling)...")
    daily_sorted = daily_df.sort_values(["Instrument", "Date"])

    ivol_records = []
    for instrument, grp in daily_sorted.groupby("Instrument"):
        grp = grp.dropna(subset=["Stock_Return", "Market_Excess"]).copy()
        if len(grp) < 60:
            continue

        ret = grp["Stock_Return"].values
        mkt = grp["Market_Excess"].values
        dates = grp["Date"].values
        ym = grp["YearMonth"].values

        for i in range(60, len(grp)):
            window_ret = ret[i - 60:i]
            window_mkt = mkt[i - 60:i]

            X = np.column_stack([np.ones(60), window_mkt])
            try:
                beta = np.linalg.lstsq(X, window_ret, rcond=None)[0]
                residuals = window_ret - X @ beta
                ivol_records.append({
                    "Instrument": instrument,
                    "Date": dates[i],
                    "YearMonth": ym[i],
                    "Ivol": residuals.std(),
                })
            except np.linalg.LinAlgError:
                continue

    ivol_daily = pd.DataFrame(ivol_records)

    # Aggregate to monthly: use end-of-month Ivol for sorting
    ivol_monthly = (
        ivol_daily.sort_values("Date")
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
