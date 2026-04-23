"""
Overview of all datasets — shapes, date ranges, coverage, nulls.
Run from anywhere: python scripts/debug/inspect_data.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

# ── Load ──────────────────────────────────────────────────────────────
jci   = pd.read_csv(DATA / "jci_index.csv", parse_dates=["Date"])
rf    = pd.read_csv(DATA / "bi_riskfree_rate.csv", parse_dates=["Date"])
panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"])
fund  = pd.read_csv(DATA / "idx_fundamentals.csv", parse_dates=["Date"])

# ── 1. JCI Index ─────────────────────────────────────────────────────
print("=" * 70)
print("  1. JCI INDEX")
print("=" * 70)
print(f"Shape: {jci.shape}")
print(f"Date range: {jci['Date'].min().date()} to {jci['Date'].max().date()}")
print(f"Nulls:\n{jci.isnull().sum()}")
print(f"\nMarket_Return stats:\n{jci['Market_Return'].describe()}")

jci["Year"] = jci["Date"].dt.year
print(f"\nObs per year:\n{jci.groupby('Year').size()}")

# ── 2. BI Risk-Free Rate ────────────────────────────────────────────
print("\n" + "=" * 70)
print("  2. BI RISK-FREE RATE")
print("=" * 70)
print(f"Shape: {rf.shape}")
print(f"Date range: {rf['Date'].min().date()} to {rf['Date'].max().date()}")
print(f"Nulls:\n{rf.isnull().sum()}")
print(f"Unique annual rates: {sorted(rf['Annual_BI_Rate'].unique())}")

# ── 3. Master Panel ─────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  3. MASTER PANEL")
print("=" * 70)
print(f"Shape: {panel.shape}")
print(f"Columns: {list(panel.columns)}")
print(f"Date range: {panel['Date'].min().date()} to {panel['Date'].max().date()}")
print(f"Unique instruments: {panel['Instrument'].nunique()}")
print(f"\nNull counts:\n{panel.isnull().sum()}")
print(f"\nNull %:\n{(panel.isnull().mean() * 100).round(1)}")

valid = panel.dropna(subset=["Stock_Return"])
print(f"\nValid Stock_Return: {len(valid):,} / {len(panel):,} ({len(valid)/len(panel)*100:.1f}%)")

panel["Year"] = panel["Date"].dt.year
print(f"\nStocks with valid returns by year:")
print(valid.groupby(valid["Date"].dt.year)["Instrument"].nunique())

print(f"\nDayName distribution:\n{panel['DayName'].value_counts()}")

# ── 4. Fundamentals ─────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  4. FUNDAMENTALS")
print("=" * 70)
print(f"Shape: {fund.shape}")
print(f"Columns: {list(fund.columns)}")
print(f"Date range: {fund['Date'].min().date()} to {fund['Date'].max().date()}")
print(f"Unique instruments: {fund['Instrument'].nunique()}")
print(f"\nNull counts:\n{fund.isnull().sum()}")
print(f"\nNull %:\n{(fund.isnull().mean() * 100).round(1)}")
print(f"\nSectors:\n{fund['Sector'].value_counts()}")

# ── 5. Pre vs Post Coverage ─────────────────────────────────────────
print("\n" + "=" * 70)
print("  5. PANEL COVERAGE: PRE (2012-2016) vs POST (2017-2024)")
print("=" * 70)
pre  = valid[(valid["Date"] >= "2012-01-01") & (valid["Date"] <= "2016-12-31")]
post = valid[(valid["Date"] >= "2017-01-01") & (valid["Date"] <= "2024-12-31")]
print(f"Pre  (2012-2016): {len(pre):,} obs, {pre['Instrument'].nunique()} stocks")
print(f"Post (2017-2024): {len(post):,} obs, {post['Instrument'].nunique()} stocks")

both = set(pre["Instrument"]) & set(post["Instrument"])
print(f"In both periods:  {len(both)} stocks")

# ── 6. Fundamentals–Panel overlap ────────────────────────────────────
print("\n" + "=" * 70)
print("  6. FUNDAMENTALS–PANEL OVERLAP")
print("=" * 70)
panel_stocks = set(panel["Instrument"].unique())
fund_stocks  = set(fund["Instrument"].unique())
print(f"Panel stocks: {len(panel_stocks)}")
print(f"Fundamentals stocks: {len(fund_stocks)}")
print(f"Overlap: {len(panel_stocks & fund_stocks)}")
print(f"Panel-only (no fundamentals): {len(panel_stocks - fund_stocks)}")
if panel_stocks - fund_stocks:
    print(f"  {sorted(panel_stocks - fund_stocks)[:20]}...")
