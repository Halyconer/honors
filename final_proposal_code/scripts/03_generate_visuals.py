import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. GET DATA (Using ETFs as proxies for "Speculative" vs "Safe")
# SPHB = High Beta (Speculative/Risky)
# SPLV = Low Volatility (Safe/Defensive)
tickers = ['SPHB', 'SPLV']
try:
    data = yf.download(tickers, start="2012-01-01", end="2023-12-31")['Adj Close']
    if data.empty:
        raise ValueError("No data downloaded")
except Exception as e:
    print(f"Error downloading data: {e}")
    exit(1)

# 2. CALCULATE RETURNS
daily_returns = data.pct_change().dropna()

# 3. CONSTRUCT THE STRATEGY
# Strategy: Long the Risky (Speculative) / Short the Safe
# Theoretical Prediction: Should do well on Mondays (Speculative rally?), poorly on Fridays? 
# (Note: In reality, the specific "Monday effect" flips over decades, but this illustrates the METHOD)
strategy_returns = daily_returns['SPHB'] - daily_returns['SPLV']

# 4. FILTER BY DAY OF WEEK
# 0 = Monday, 4 = Friday
monday_returns = strategy_returns[strategy_returns.index.dayofweek == 0]
friday_returns = strategy_returns[strategy_returns.index.dayofweek == 4]
all_returns = strategy_returns

# --- ILLUSTRATION 1: THE BAR CHART ---
avg_monday = monday_returns.mean() * 100 # Convert to %
avg_friday = friday_returns.mean() * 100
avg_all = all_returns.mean() * 100

plt.figure(figsize=(10, 6))
days = ['Mondays', 'Fridays', 'All Days']
values = [avg_monday, avg_friday, avg_all]
colors = ['green', 'red', 'gray']

plt.bar(days, values, color=colors, alpha=0.7)
plt.axhline(0, color='black', linewidth=1)
plt.title('Average Daily Strategy Return: Long Speculative / Short Safe', fontsize=14)
plt.ylabel('Average Return (%)')
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Add labels
for i, v in enumerate(values):
    plt.text(i, v + (0.005 if v > 0 else -0.015), f"{v:.3f}%", ha='center', fontweight='bold')

plt.show()

# --- ILLUSTRATION 2: THE CUMULATIVE DIVERGENCE ---
# Calculate growth of $1 invested ONLY on specific days
cum_monday = (1 + monday_returns).cumprod()
cum_friday = (1 + friday_returns).cumprod()

plt.figure(figsize=(10, 6))
plt.plot(cum_monday.index, cum_monday, label='Monday Only Trading', color='green', linewidth=2)
plt.plot(cum_friday.index, cum_friday, label='Friday Only Trading', color='red', linewidth=2)

plt.title('The Tale of Two Markets: Cumulative Growth of $1', fontsize=14)
plt.ylabel('Portfolio Value ($)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()