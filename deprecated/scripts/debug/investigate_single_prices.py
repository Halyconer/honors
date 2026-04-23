"""
Check for stocks with very few or zero valid prices — batch stacking artifacts.
Useful for verifying no stocks were silently dropped in the download.
"""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

pd.set_option("display.width", 140)

daily = pd.read_csv(DATA / "idx_daily_prices.csv", parse_dates=["Date"])

# ── 1. Rows vs Valid Prices Per Stock ────────────────────────────────
print("=" * 80)
print("  1. ROWS vs VALID PRICES PER STOCK")
print("=" * 80)

summary = daily.groupby("Instrument").agg(
    total_rows=("Date", "count"),
    prices=("Price", lambda x: x.notna().sum()),
    first_date=("Date", "min"),
    last_date=("Date", "max"),
).sort_values("prices")

summary["price_pct"] = (summary["prices"] / summary["total_rows"] * 100).round(1)

# Stocks with zero prices
zero = summary[summary["prices"] == 0]
print(f"\nStocks with ZERO valid prices: {len(zero)}")
if len(zero) > 0:
    print(zero.to_string())

# Stocks with very few prices
few = summary[(summary["prices"] > 0) & (summary["prices"] <= 50)]
print(f"\nStocks with 1-50 valid prices: {len(few)}")
if len(few) > 0:
    print(few.to_string())

# ── 2. Distribution ─────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  2. OVERALL DISTRIBUTION")
print("=" * 80)

bins = [0, 0.5, 50, 200, 500, 1000, 2000, 4000]
labels = ["0", "1-50", "51-200", "201-500", "501-1000", "1001-2000", "2001+"]
summary["bucket"] = pd.cut(summary["prices"], bins=bins, labels=labels)
print(f"\nStocks by valid price count:\n{summary['bucket'].value_counts().sort_index()}")
print(f"\nTotal instruments: {len(summary)}")
print(f"With any price data: {(summary['prices'] > 0).sum()}")
print(f"With >200 prices: {(summary['prices'] > 200).sum()}")
