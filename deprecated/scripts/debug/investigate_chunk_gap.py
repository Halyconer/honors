"""
Check for time gaps in the daily price data — verifies no missing year ranges
after the redownload. Originally written to debug a 2017-2019 gap in v1 data.
"""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

daily = pd.read_csv(DATA / "idx_daily_prices.csv", parse_dates=["Date"])

# ── 1. Date Distribution ────────────────────────────────────────────
print("=" * 70)
print("  DATE DISTRIBUTION IN DAILY PRICES")
print("=" * 70)

yearly = daily.groupby(daily["Date"].dt.year).agg(
    total_rows=("Date", "count"),
    with_price=("Price", lambda x: x.notna().sum()),
    stocks=("Instrument", "nunique"),
)
yearly["price_pct"] = (yearly["with_price"] / yearly["total_rows"] * 100).round(1)
print(yearly.to_string())

# ── 2. Check Each 3-Year Chunk ──────────────────────────────────────
print("\n" + "=" * 70)
print("  COVERAGE BY DOWNLOAD CHUNK")
print("=" * 70)

chunks = [
    ("2012-2014", "2012-01-01", "2014-12-31"),
    ("2015-2017", "2015-01-01", "2017-12-31"),
    ("2018-2020", "2018-01-01", "2020-12-31"),
    ("2021-2023", "2021-01-01", "2023-12-31"),
    ("2024-2025", "2024-01-01", "2025-12-31"),
]

for label, start, end in chunks:
    chunk = daily[(daily["Date"] >= start) & (daily["Date"] <= end)]
    n_price = chunk["Price"].notna().sum()
    n_stocks = chunk.dropna(subset=["Price"])["Instrument"].nunique()
    print(f"  {label}: {n_price:>8,} prices, {n_stocks:>4} stocks")

# ── 3. Cross-Chunk Continuity ───────────────────────────────────────
print("\n" + "=" * 70)
print("  CROSS-CHUNK STOCK CONTINUITY")
print("=" * 70)

# Check stocks present in adjacent chunks
for i in range(len(chunks) - 1):
    _, s1, e1 = chunks[i]
    _, s2, e2 = chunks[i + 1]
    c1_stocks = set(daily[(daily["Date"] >= s1) & (daily["Date"] <= e1)].dropna(subset=["Price"])["Instrument"])
    c2_stocks = set(daily[(daily["Date"] >= s2) & (daily["Date"] <= e2)].dropna(subset=["Price"])["Instrument"])
    overlap = c1_stocks & c2_stocks
    print(f"  {chunks[i][0]} → {chunks[i+1][0]}: {len(c1_stocks)} → {len(c2_stocks)} stocks, {len(overlap)} overlap")

# ── 4. Returns Near Chunk Boundaries ────────────────────────────────
print("\n" + "=" * 70)
print("  EXTREME RETURNS AT CHUNK BOUNDARIES")
print("=" * 70)

panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"])
for boundary in ["2014-12-15", "2017-12-15", "2020-12-15", "2023-12-15"]:
    window = panel[(panel["Date"] >= boundary) & (panel["Date"] <= pd.Timestamp(boundary) + pd.Timedelta(days=30))]
    extreme = window[window["Stock_Return"].abs() > 0.30]
    print(f"  Near {boundary}: {len(extreme)} returns with |r| > 30%")
