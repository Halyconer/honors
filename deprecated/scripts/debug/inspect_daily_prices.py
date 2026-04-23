"""
Quick look at idx_daily_prices.csv — coverage, stocks, date range.
"""
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data"

dp = pd.read_csv(DATA / "idx_daily_prices.csv", parse_dates=["Date"])

print(f"Shape: {dp.shape}")
print(f"Columns: {list(dp.columns)}")
print(f"Unique instruments: {dp['Instrument'].nunique()}")
print(f"Date range: {dp['Date'].min().date()} to {dp['Date'].max().date()}")

has_price = dp.dropna(subset=["Price"])
print(f"\nValid prices: {len(has_price):,} / {len(dp):,} ({len(has_price)/len(dp)*100:.1f}%)")
print(f"Stocks with data: {has_price['Instrument'].nunique()}")

# Per-stock summary
per_stock = has_price.groupby("Instrument").agg(
    n_obs=("Price", "count"),
    min_date=("Date", "min"),
    max_date=("Date", "max"),
)
print(f"\nObs per stock:\n{per_stock['n_obs'].describe()}")

# By year
yearly = has_price.groupby(has_price["Date"].dt.year)["Instrument"].nunique()
print(f"\nStocks with valid prices by year:\n{yearly}")

# Stocks with no data
no_data = set(dp["Instrument"]) - set(has_price["Instrument"])
print(f"\nStocks with ZERO prices: {len(no_data)}")
if no_data:
    print(f"  {sorted(no_data)}")
