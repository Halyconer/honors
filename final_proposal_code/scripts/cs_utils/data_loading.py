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

    # Log market cap (not pre-computed in prepare_data.py).
    # clip(lower=1) guards against zero/negative values; in IDR units this
    # should never fire in practice (IDX market caps are ≥ millions of IDR).
    # An assertion below confirms no rows are actually clipped.
    assert (chars["Market_Cap"] > 0).all(), (
        f"Unexpected non-positive Market_Cap values: "
        f"{(chars['Market_Cap'] <= 0).sum()} rows"
    )
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


def build_date_info(daily, data_dir=None):
    """Build date-level info (day name, risk-free rate, market excess, FF3 factors)."""
    date_info = daily.groupby("Date").agg(
        DayName=("DayName", "first"),
        Daily_Rf=("Daily_Rf", "first"),
        Market_Excess=("Market_Excess", "first"),
    ).copy()
    date_info["YM"] = date_info.index.to_period("M").astype(str)

    # Merge FF3 factors when available (built by 01b_build_ff3_factors.py)
    if data_dir is not None:
        ff3_path = data_dir / "ff3_factors.csv"
        if ff3_path.exists():
            ff3 = pd.read_csv(ff3_path, parse_dates=["Date"]).set_index("Date")
            date_info = date_info.join(ff3[["SMB", "HML"]], how="left")
            n = date_info["SMB"].notna().sum()
            print(f"  FF3 factors loaded: {n:,} days with SMB/HML")
        else:
            date_info["SMB"] = np.nan
            date_info["HML"] = np.nan
            print("  FF3 factors not found — run 01b_build_ff3_factors.py first")
    else:
        date_info["SMB"] = np.nan
        date_info["HML"] = np.nan

    return date_info
