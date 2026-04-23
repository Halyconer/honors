"""
Investigate price data sparsity — NaN patterns, batch stacking artifacts,
return chain breaks. Useful for verifying the redownloaded data is clean.
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 140)

daily = pd.read_csv(DATA / "idx_daily_prices.csv", parse_dates=["Date"])
panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"])

# ── 1. NaN Pattern ──────────────────────────────────────────────────
print("=" * 80)
print("  1. RAW DAILY PRICES — NaN PATTERN")
print("=" * 80)

# Trace a blue chip (should have full data)
for ticker in ["AALI.JK", "BBCA.JK", "TLKM.JK"]:
    s = daily[daily["Instrument"] == ticker]
    if len(s) == 0:
        continue
    n_price = s["Price"].notna().sum()
    n_null = s["Price"].isna().sum()
    print(f"\n{ticker}: {len(s)} rows, {n_price} with price, {n_null} null")
    print(f"  Date range: {s['Date'].min().date()} to {s['Date'].max().date()}")

# ── 2. Return Calculation Pipeline ──────────────────────────────────
print("\n" + "=" * 80)
print("  2. RETURN CALCULATION — PRICE → RETURN PIPELINE")
print("=" * 80)

aali = panel[panel["Instrument"] == "AALI.JK"][["Date", "Price", "Stock_Return"]]
print(f"\nAALI.JK in master panel:")
print(f"  Total rows: {len(aali)}")
print(f"  With Price: {aali['Price'].notna().sum()}")
print(f"  With Return: {aali['Stock_Return'].notna().sum()}")

no_ret = aali[aali["Price"].notna() & aali["Stock_Return"].isna()]
print(f"  Price but no return (first obs per stock): {len(no_ret)}")

# ── 3. Price Continuity for Top Stocks ──────────────────────────────
print("\n" + "=" * 80)
print("  3. PRICE CONTINUITY FOR TOP STOCKS")
print("=" * 80)

top = panel.dropna(subset=["Stock_Return"]).groupby("Instrument").size().nlargest(20)
for stock, n in top.items():
    s = daily[daily["Instrument"] == stock]
    prices = s["Price"].notna()
    total_valid = prices.sum()
    total_rows = len(s)
    transitions = int(prices.astype(int).diff().abs().sum() / 2)
    print(f"  {stock:15s}  returns={n:5d}  prices={total_valid:5d}/{total_rows:5d}  gaps={transitions}")

# ── 4. Data Shape ───────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  4. DATA SHAPE")
print("=" * 80)

n_dates = daily["Date"].nunique()
n_instr = daily["Instrument"].nunique()
print(f"Unique dates: {n_dates}")
print(f"Unique instruments: {n_instr}")
print(f"Expected if rectangular: {n_dates * n_instr:,}")
print(f"Actual rows: {len(daily):,}")
print(f"Fill ratio: {len(daily) / (n_dates * n_instr):.1%}")
