

import pandas as pd
import numpy as np
import yfinance as yf
import os

# Define file paths
daily_data_path = '../final_proposal_code/jci_test_daily_3yr.csv'
output_path = '../final_proposal_code/daily_returns_merged.csv'

print("Starting the process to calculate and merge daily returns...")

try:
    # --- 1. Load and process individual stock data ---
    print(f"Loading individual stock data from {os.path.basename(daily_data_path)}...")
    daily_df = pd.read_csv(daily_data_path)
    daily_df['Date'] = pd.to_datetime(daily_df['Date'])

    # Pivot the table to have instruments as columns and dates as index
    # This makes calculating returns and merging much easier
    price_pivot = daily_df.pivot(index='Date', columns='Instrument', values='Price')

    # Calculate log returns for each stock
    # np.log(price) - np.log(price.shift(1)) is equivalent to np.log(price / price.shift(1))
    stock_returns = np.log(price_pivot).diff()
    
    print(f"Calculated log returns for {len(stock_returns.columns)} instruments.")

    # --- 2. Download and process JCI data ---
    start_date = stock_returns.index.min()
    end_date = stock_returns.index.max()
    
    print(f"Downloading JCI data (^JKSE) from {start_date.date()} to {end_date.date()}...")
    jci_data = yf.download('^JKSE', start=start_date, end=end_date)

    if jci_data.empty:
        raise Exception("Failed to download JCI data. Please check the ticker '^JKSE' and your internet connection.")

    # Calculate log return for JCI
    jci_returns = np.log(jci_data['Close']).diff()
    jci_returns.name = 'JCI_Return' # Rename the series for clarity

    print("Calculated log returns for JCI.")

    # --- 3. Merge the datasets ---
    print("Merging individual stock returns with JCI returns...")
    # Merge using an outer join to keep all dates, then forward-fill JCI returns for any non-trading days
    merged_df = stock_returns.join(jci_returns, how='left')
    
    # The returns are NaN for the first day, so we can drop it
    merged_df = merged_df.iloc[1:]

    # --- 4. Save the new CSV ---
    merged_df.to_csv(output_path)
    
    print("\nProcess complete!")
    print(f"New CSV file created at: {output_path}")
    print("\n--- Sample of the merged data ---")
    print(merged_df.head())
    print("\n--- Data summary ---")
    print(merged_df.info())


except FileNotFoundError:
    print(f"Error: Could not find the file at {daily_data_path}")
except Exception as e:
    print(f"An error occurred: {e}")

