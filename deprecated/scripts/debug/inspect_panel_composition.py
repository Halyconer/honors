"""
Pre vs post stock composition — which stocks overlap, which are period-specific.
"""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

panel = pd.read_csv(DATA / "idx_master_panel.csv", parse_dates=["Date"])
valid = panel.dropna(subset=["Stock_Return"])

pre_stocks  = set(valid[(valid["Date"] >= "2012-01-01") & (valid["Date"] <= "2016-12-31")]["Instrument"])
post_stocks = set(valid[(valid["Date"] >= "2017-01-01") & (valid["Date"] <= "2024-12-31")]["Instrument"])

both     = pre_stocks & post_stocks
pre_only = pre_stocks - post_stocks
post_only = post_stocks - pre_stocks

print("=" * 60)
print("  STOCK COMPOSITION: PRE (2012-2016) vs POST (2017-2024)")
print("=" * 60)
print(f"Pre-period stocks:  {len(pre_stocks)}")
print(f"Post-period stocks: {len(post_stocks)}")
print(f"In BOTH periods:    {len(both)}")
print(f"Pre-only (delisted): {len(pre_only)}")
print(f"Post-only (new IPOs): {len(post_only)}")

# Year-by-year
print("\n" + "=" * 60)
print("  STOCKS WITH VALID RETURNS BY YEAR")
print("=" * 60)
yearly = valid.groupby(valid["Date"].dt.year).agg(
    n_obs=("Stock_Return", "count"),
    n_stocks=("Instrument", "nunique"),
    mean_ret=("Stock_Return", lambda x: f"{x.mean()*100:.3f}%"),
)
print(yearly.to_string())

# Obs per stock
print("\n" + "=" * 60)
print("  OBS PER STOCK (2012-2024)")
print("=" * 60)
sample = valid[(valid["Date"] >= "2012-01-01") & (valid["Date"] <= "2024-12-31")]
print(sample.groupby("Instrument").size().describe())
