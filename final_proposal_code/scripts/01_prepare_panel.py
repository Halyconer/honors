"""
01_PREPARE_PANEL.PY
Step 1 — Data Preparation for Cross-Sectional Analysis (Birru 2018 JFE)
======================================================================
Produces:
  data/analysis_daily.csv        — cleaned daily stock returns
  data/stock_characteristics.csv — monthly characteristics for portfolio sorts

Updates:
  - Extended range: 2008-2024
  - Integrated Foreign Ownership data
  - Improved MAX and IVOL logic
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ── Paths ────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# ── Config ───────────────────────────────────────────────────────────────
DROP_RICS = [
    "MYRX_p.JK^G25", "RMKOn.JK", "CNTX_p.JK", "SQBI_p.JK^C18",
]
DATE_START = "2008-01-01"
DATE_END   = "2024-12-31"

# =====================================================================
# 1. LOAD DATA
# =====================================================================
print("Loading data...")
# Use low_memory=False to avoid DtypeWarnings on large panels
panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"], low_memory=False)
fund  = pd.read_csv(DATA / "idx_fundamentals.csv", parse_dates=["Date"], low_memory=False)
own   = pd.read_csv(DATA / "idx_institutional_ownership.csv", parse_dates=["Date"], low_memory=False)

print(f"  Prices: {len(panel):,} rows")
print(f"  Fundamentals: {len(fund):,} rows")
print(f"  Ownership: {len(own):,} rows")

# =====================================================================
# 2. CLEANING & FILTERING
# =====================================================================
# Drop preferreds/duplicates
panel = panel[~panel["Instrument"].isin(DROP_RICS)].copy()
fund  = fund[~fund["Instrument"].isin(DROP_RICS)].copy()
own   = own[~own["Instrument"].isin(DROP_RICS)].copy()

# Date filter
panel = panel[(panel["Date"] >= DATE_START) & (panel["Date"] <= DATE_END)].copy()
print(f"\nFiltered to {DATE_START}–{DATE_END}: {len(panel):,} daily rows")

# Winsorize Daily Returns (1%/99%) to handle IDX "limit" outliers
if "Stock_Return" in panel.columns:
    p01, p99 = panel["Stock_Return"].quantile([0.01, 0.99])
    panel["Stock_Return"] = panel["Stock_Return"].clip(lower=p01, upper=p99)
    print(f"Winsorized Stock_Return at [{p01:.4f}, {p99:.4f}]")

# =====================================================================
# 3. BUILD MONTHLY CHARACTERISTICS
# =====================================================================
print("\nBuilding monthly characteristics...")

# 3.1. Fundamental Characteristics
fund["YearMonth"] = fund["Date"].dt.to_period("M").astype(str)
fund_m = fund.sort_values("Date").groupby(["Instrument", "YearMonth"]).last().reset_index()

# Forward-fill fundamentals per instrument (max 12 months)
# This is crucial because reporting is infrequent (quarterly/annual)
# but we need monthly characteristics for sorting.
fund_m = fund_m.sort_values(["Instrument", "YearMonth"])
cols_to_ffill = ["Market_Cap_Bil", "ROA", "BVPS", "Div_Payer", "Market_Cap"]
fund_m[cols_to_ffill] = fund_m.groupby("Instrument")[cols_to_ffill].ffill(limit=12)

# 3.2. Ownership Characteristics (Foreign Pct)
own["YearMonth"] = own["Date"].dt.to_period("M").astype(str)
own_m = own.sort_values("Date").groupby(["Instrument", "YearMonth"]).last().reset_index()
own_m = own_m[["Instrument", "YearMonth", "Foreign_Pct", "Institutional_Pct"]]

# 3.3. Price-based Characteristics (IVOL, MAX, Size)
panel["YearMonth"] = panel["Date"].dt.to_period("M").astype(str)

# MAX characteristic (max daily return in month)
# IVOL proxy (std dev of daily returns in month)
price_m = panel.groupby(["Instrument", "YearMonth"]).agg(
    End_Price=("Price", "last"),
    Max_Return=("Stock_Return", "max"),
    IVOL_Proxy=("Stock_Return", "std"),
    Volume_Monthly=("Volume", "sum"),
    Trading_Days=("Date", "count")
).reset_index()

# 3.4. MERGE ALL
chars = price_m.merge(fund_m, on=["Instrument", "YearMonth"], how="left", suffixes=('', '_fund'))
chars = chars.merge(own_m, on=["Instrument", "YearMonth"], how="left")

# 3.5. DERIVED FIELDS
# Ensure Market_Cap is available (fund_m has Market_Cap_Bil)
if "Market_Cap" not in chars.columns:
    chars["Market_Cap"] = chars["Market_Cap_Bil"] * 1e9

# Filter out non-positive market cap to avoid log errors and weighting issues
chars = chars[chars["Market_Cap"] > 0].copy()

# Size = log of Market_Cap_Bil
chars["Size"] = np.log(chars["Market_Cap_Bil"].clip(lower=0.1))

# Book-to-Market
chars["BM_Ratio"] = chars["BVPS"] / chars["End_Price"].clip(lower=0.1)

# Quality filter: minimum 15 trading days in a month for volatility/max to be valid
chars = chars[chars["Trading_Days"] >= 15]

# =====================================================================
# 4. IMPLEMENT LAGS (Portfolio sort at end of m-1, returns in m)
# =====================================================================
# For a portfolio in month T, we use characteristics known at T-1
chars["Sort_YearMonth"] = (
    pd.to_datetime(chars["YearMonth"]) + pd.DateOffset(months=1)
).dt.to_period("M").astype(str)

print(f"Final Characteristic Panel: {len(chars):,} rows")

# =====================================================================
# 5. SAVE
# =====================================================================
panel.to_csv(DATA / "analysis_daily.csv", index=False)
chars.to_csv(DATA / "stock_characteristics.csv", index=False)

print("\nSuccess!")
print(f"Saved analysis_daily.csv ({len(panel):,} rows)")
print(f"Saved stock_characteristics.csv ({len(chars):,} rows)")
