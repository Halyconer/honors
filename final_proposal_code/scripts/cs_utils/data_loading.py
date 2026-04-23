"""
Data loading and characteristic preparation.
"""

import pandas as pd
import numpy as np
from pathlib import Path

from .characteristics import compute_ivol, compute_max_return


def load_data(data_dir):
    """Load daily panel and stock characteristics, compute derived columns."""
    print("Loading data...")
    daily = pd.read_csv(data_dir / "analysis_daily.csv", parse_dates=["Date"])
    chars = pd.read_csv(data_dir / "stock_characteristics.csv")

    print(f"  Daily panel: {len(daily):,} rows, {daily['Instrument'].nunique()} stocks")
    print(f"  Characteristics: {len(chars):,} rows")

    # Log market cap (not pre-computed in prepare_data.py)
    chars["Log_MCap"] = np.log(chars["Market_Cap"].clip(lower=1))

    # Idiosyncratic volatility
    ivol_monthly = compute_ivol(daily)
    chars = chars.merge(ivol_monthly, on=["Instrument", "Sort_YearMonth"], how="left")
    print(f"  Ivol coverage: {chars['Ivol'].notna().mean():.1%}")

    # Max daily return
    max_monthly = compute_max_return(daily)
    if "Max_Abs_Return" in chars.columns:
        chars = chars.drop(columns=["Max_Abs_Return"])
    if "Max_Return" in chars.columns:
        chars = chars.drop(columns=["Max_Return"])
    chars = chars.merge(max_monthly, on=["Instrument", "Sort_YearMonth"], how="left")
    print(f"  Max_Return coverage: {chars['Max_Return'].notna().mean():.1%}")

    return daily, chars


def build_date_info(daily):
    """Build date-level info (day name, risk-free rate, market excess)."""
    date_info = daily.groupby("Date").agg(
        DayName=("DayName", "first"),
        Daily_Rf=("Daily_Rf", "first"),
        Market_Excess=("Market_Excess", "first"),
    ).copy()
    date_info["YM"] = date_info.index.to_period("M").astype(str)
    return date_info
