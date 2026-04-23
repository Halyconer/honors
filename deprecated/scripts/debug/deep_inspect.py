"""
Detailed stock-level inspection — return distributions, day-of-week patterns,
extreme returns, volume, correlations.
"""
import pandas as pd
import numpy as np
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

pd.set_option("display.max_columns", 20)
pd.set_option("display.width", 140)

panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"])
daily = pd.read_csv(DATA / "idx_daily_prices.csv", parse_dates=["Date"])
valid = panel.dropna(subset=["Stock_Return"])

n_stocks = panel["Instrument"].nunique()

# ── 1. Instrument-Level Summary ─────────────────────────────────────
print("=" * 80)
print(f"  1. INSTRUMENT-LEVEL SUMMARY ({n_stocks} stocks)")
print("=" * 80)

inst = panel.groupby("Instrument").agg(
    first_date=("Date", "min"),
    last_date=("Date", "max"),
    total_rows=("Date", "count"),
    price_nonnull=("Price", lambda x: x.notna().sum()),
    return_nonnull=("Stock_Return", lambda x: x.notna().sum()),
    mean_return=("Stock_Return", "mean"),
    std_return=("Stock_Return", "std"),
    median_price=("Price", "median"),
).sort_values("first_date")

inst["price_pct"] = (inst["price_nonnull"] / inst["total_rows"] * 100).round(1)
inst["return_pct"] = (inst["return_nonnull"] / inst["total_rows"] * 100).round(1)

print(inst[["first_date", "last_date", "total_rows",
            "price_pct", "return_pct", "mean_return", "median_price"]].describe().to_string())

# ── 2. Return Distributions ─────────────────────────────────────────
print("\n" + "=" * 80)
print("  2. RETURN DISTRIBUTIONS")
print("=" * 80)

print(f"Total valid returns: {len(valid):,}")
print(f"\nStock_Return stats:\n{valid['Stock_Return'].describe()}")

# Extreme returns
for threshold in [0.50, 0.30, 0.20]:
    n = (valid["Stock_Return"].abs() > threshold).sum()
    print(f"  |r| > {threshold*100:.0f}%: {n:,} obs")

extreme = valid[valid["Stock_Return"].abs() > 0.30]
if len(extreme) > 0:
    print(f"\nExtreme returns (|r| > 30%, showing 10 most negative + 10 most positive):")
    worst = extreme.nsmallest(10, "Stock_Return")
    best  = extreme.nlargest(10, "Stock_Return")
    print(pd.concat([worst, best])[["Date", "Instrument", "Price", "Stock_Return", "Volume"]].to_string(index=False))

# ── 3. Day-of-Week Patterns ─────────────────────────────────────────
print("\n" + "=" * 80)
print("  3. DAY-OF-WEEK PATTERNS (stock-level pooled)")
print("=" * 80)

dow = valid.groupby("DayName")["Stock_Return"].agg(["count", "mean", "median", "std"])
dow = dow.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
dow["mean_bps"] = dow["mean"] * 10000
dow["t_stat"] = dow["mean"] / (dow["std"] / np.sqrt(dow["count"]))
print(dow[["count", "mean_bps", "median", "std", "t_stat"]].to_string())

# Monday effect per stock
print("\nPer-stock Monday effect (Mon mean - non-Mon mean):")
mon_eff = []
for name, grp in valid.groupby("Instrument"):
    mon = grp[grp["DayName"] == "Monday"]["Stock_Return"]
    other = grp[grp["DayName"] != "Monday"]["Stock_Return"]
    if len(mon) >= 20 and len(other) >= 80:
        mon_eff.append({"Instrument": name, "Diff_bps": (mon.mean() - other.mean()) * 10000, "Mon_N": len(mon)})

me = pd.DataFrame(mon_eff).sort_values("Diff_bps")
print(f"Stocks with enough data: {len(me)}")
print(f"  Negative Monday diff: {(me['Diff_bps'] < 0).sum()}")
print(f"  Positive Monday diff: {(me['Diff_bps'] >= 0).sum()}")
print(f"\n  Strongest Monday effect (top 5):")
print(me.head(5).to_string(index=False))
print(f"\n  Strongest reverse Monday (top 5):")
print(me.tail(5).to_string(index=False))

# ── 4. Volume Analysis ──────────────────────────────────────────────
print("\n" + "=" * 80)
print("  4. VOLUME ANALYSIS")
print("=" * 80)

has_price = daily.dropna(subset=["Price"])
price_zero_vol = has_price[has_price["Volume"].eq(0)]
print(f"Rows with price but zero volume: {len(price_zero_vol):,} / {len(has_price):,} "
      f"({len(price_zero_vol)/len(has_price)*100:.1f}%)")

vol_by_stock = has_price.groupby("Instrument").agg(
    days=("Price", "count"),
    zero_vol_days=("Volume", lambda x: x.eq(0).sum()),
)
vol_by_stock["zero_pct"] = (vol_by_stock["zero_vol_days"] / vol_by_stock["days"] * 100).round(1)
illiquid = vol_by_stock[vol_by_stock["zero_pct"] > 50].sort_values("zero_pct", ascending=False)
print(f"Illiquid stocks (>50% zero-volume days): {len(illiquid)}")
if len(illiquid) > 0 and len(illiquid) <= 30:
    print(illiquid.to_string())

# ── 5. Stock vs Market Correlation ──────────────────────────────────
print("\n" + "=" * 80)
print("  5. STOCK–MARKET RETURN CORRELATIONS")
print("=" * 80)

corr_dict = {}
for name, grp in valid.groupby("Instrument"):
    if len(grp) > 50:
        corr_dict[name] = grp["Stock_Return"].corr(grp["Market_Return"])
corrs = pd.Series(corr_dict).dropna().sort_values()

print(f"Stocks with >50 obs: {len(corrs)}")
print(f"  Mean:   {corrs.mean():.3f}")
print(f"  Median: {corrs.median():.3f}")
print(f"  Min:    {corrs.min():.3f} ({corrs.idxmin()})")
print(f"  Max:    {corrs.max():.3f} ({corrs.idxmax()})")
