"""
01_PREPARE_PANEL.PY
Step 1 — Data Preparation for Cross-Sectional Analysis (Birru 2018 JFE)
======================================================================
Cleans the raw panel and fundamentals, producing two analysis-ready files:

  data/analysis_daily.csv      — cleaned daily stock returns (filtered)
  data/stock_characteristics.csv — monthly stock characteristics for portfolio sorts

Usage:
    python scripts/01_prepare_panel.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ── Config ───────────────────────────────────────────────────────────────
DROP_RICS = [
    "MYRX_p.JK^G25",   # preferred share (common = MYRX.JK^G25)
    "RMKOn.JK",         # duplicate listing class (common = RMKO.JK)
    "CNTX_p.JK",        # orphan preferred share
    "SQBI_p.JK^C18",    # orphan preferred share
]
DATE_START = "2012-01-01"
DATE_END   = "2024-12-31"

# =====================================================================
# 1. LOAD RAW DATA
# =====================================================================
print("Loading data...")
panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"])
fund  = pd.read_csv(DATA / "idx_fundamentals.csv", parse_dates=["Date", "IPO_Date"])
print(f"  Panel: {len(panel):,} rows, {panel['Instrument'].nunique()} stocks")
print(f"  Fundamentals: {len(fund):,} rows, {fund['Instrument'].nunique()} stocks")

# =====================================================================
# 2. DROP DUPLICATE / PREFERRED RICS
# =====================================================================
n_before = panel["Instrument"].nunique() # count unique stocks before dropping
panel = panel[~panel["Instrument"].isin(DROP_RICS)].copy()
fund  = fund[~fund["Instrument"].isin(DROP_RICS)].copy()
n_after = panel["Instrument"].nunique()
print(f"\nDropped {n_before - n_after} duplicate/preferred RICs → {n_after} stocks")

# =====================================================================
# 3. FILTER TO ANALYSIS PERIOD
# =====================================================================
panel = panel[(panel["Date"] >= DATE_START) & (panel["Date"] <= DATE_END)].copy()
print(f"Filtered to {DATE_START[:7]}–{DATE_END[:7]}: {len(panel):,} rows")

# =====================================================================
# 4. ADD PERIOD INDICATOR
# =====================================================================
panel["Period"] = np.where(panel["Date"] < "2017-01-01", "Pre", "Post")
pre_n  = (panel["Period"] == "Pre").sum()
post_n = (panel["Period"] == "Post").sum()
print(f"  Pre  (2012-2016): {pre_n:,} rows")
print(f"  Post (2017-2024): {post_n:,} rows")

# =====================================================================
# 5. WINSORIZE STOCK RETURNS (1st/99th percentile)
# =====================================================================
if "Stock_Return" in panel.columns:
    p01 = panel["Stock_Return"].quantile(0.01)
    p99 = panel["Stock_Return"].quantile(0.99)
    n_clipped = ((panel["Stock_Return"] < p01) | (panel["Stock_Return"] > p99)).sum()
    panel["Stock_Return"] = panel["Stock_Return"].clip(lower=p01, upper=p99)
    print(f"\nWinsorized Stock_Return at [{p01:.4f}, {p99:.4f}]: {n_clipped:,} obs clipped")

# =====================================================================
# 6. SAVE CLEANED DAILY PANEL
# =====================================================================
panel.to_csv(DATA / "analysis_daily.csv", index=False)
print(f"\nSaved analysis_daily.csv: {len(panel):,} rows, {panel['Instrument'].nunique()} stocks")

# =====================================================================
# 7. BUILD MONTHLY STOCK CHARACTERISTICS
# =====================================================================
print("\n--- Building monthly characteristics ---")

# Fundamentals: convert to year-month, keep latest obs per stock-month
fund["YearMonth"] = fund["Date"].dt.to_period("M").astype(str)
fund = fund.sort_values("Date").groupby(["Instrument", "YearMonth"]).last().reset_index()

# Filter fundamentals to analysis period
fund = fund[(fund["YearMonth"] >= "2012-01") & (fund["YearMonth"] <= "2024-12")]

# Start with fundamental-based characteristics (directly available)
chars = fund[["Instrument", "YearMonth", "Market_Cap", "Market_Cap_Bil",
              "ROA", "BVPS", "Div_Payer", "Months_Since_Listing",
              "Shares_Outstanding", "Sector"]].copy()

# Log market cap (for size sorts — more normally distributed)
# chars["Log_MCap"] = np.log(chars["Market_Cap"].clip(lower=1))

# ── Price-based characteristics from daily panel ─────────────────────
# Group daily data by stock-month
panel["YearMonth_p"] = panel["Date"].dt.to_period("M").astype(str)

monthly_price = panel.groupby(["Instrument", "YearMonth_p"]).agg(
    Mean_Price=("Price", "mean"),
    End_Price=("Price", "last"),
    Monthly_Volume=("Volume", "sum"),
    Trading_Days=("Price", "count"),
    Std_Return=("Stock_Return", "std"),
    Max_Return=("Stock_Return", "max"),
    Min_Return=("Stock_Return", "min"),
).reset_index().rename(columns={"YearMonth_p": "YearMonth"})

# Max absolute daily return in month (Birru's "Max" characteristic)
monthly_price["Max_Abs_Return"] = monthly_price[["Max_Return", "Min_Return"]].abs().max(axis=1)

chars = chars.merge(monthly_price, on=["Instrument", "YearMonth"], how="outer")

# Book-to-Market ratio: BVPS / Price
chars["BM_Ratio"] = chars["BVPS"] / chars["End_Price"].clip(lower=1)

# Turnover: monthly volume / shares outstanding
chars["Turnover"] = chars["Monthly_Volume"] / chars["Shares_Outstanding"].clip(lower=1)

# Drop rows with no identifying info
chars = chars.dropna(subset=["Instrument", "YearMonth"])

# ── Lag characteristics by 1 month (avoid look-ahead bias) ──────────
# For portfolio formation in month t, use characteristics from month t-1
chars["Sort_YearMonth"] = (
    pd.to_datetime(chars["YearMonth"]) + pd.DateOffset(months=1)
).dt.to_period("M").astype(str)

# Sort_YearMonth = the month in which this characteristic will be used for sorting
# If characteristic is measured in 2015-06, it's used for sorting in 2015-07

chars = chars[(chars["Sort_YearMonth"] >= "2012-01") &
              (chars["Sort_YearMonth"] <= "2024-12")]

# =====================================================================
# 8. SAVE CHARACTERISTICS
# =====================================================================
chars.to_csv(DATA / "stock_characteristics.csv", index=False)
print(f"Saved stock_characteristics.csv: {len(chars):,} rows, {chars['Instrument'].nunique()} stocks")
