

import pandas as pd
import matplotlib.pyplot as plt
import os

# Define file paths
daily_data_path = '../final_proposal_code/jci_test_daily_3yr.csv'
fundamentals_data_path = '../final_proposal_code/jci_test_fundamentals_3yr.csv'
output_dir = 'charts'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- Load and display daily data ---
print("--- Sample of Daily Data ---")
try:
    daily_df = pd.read_csv(daily_data_path)
    print(daily_df.head())

    # --- Generate graphs for daily data ---
    if not daily_df.empty:
        # Convert 'Date' column to datetime
        daily_df['Date'] = pd.to_datetime(daily_df['Date'])

        # Calculate daily return for each instrument
        daily_df['daily_return'] = daily_df.groupby('Instrument')['Price'].pct_change()

        # Get the first instrument to plot its price history
        first_instrument = daily_df['Instrument'].iloc[0]
        instrument_df = daily_df[daily_df['Instrument'] == first_instrument]

        # Plot 1: Time series of closing price for the first instrument
        plt.figure(figsize=(10, 6))
        plt.plot(instrument_df['Date'], instrument_df['Price'])
        plt.title(f'Daily Closing Price for {first_instrument}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, 'instrument_closing_price.png'))
        plt.close()
        print(f"\nChart saved to {os.path.join(output_dir, 'instrument_closing_price.png')}")

        # Plot 2: Histogram of daily returns for all instruments
        if 'daily_return' in daily_df.columns:
            plt.figure(figsize=(10, 6))
            daily_df['daily_return'].dropna().hist(bins=50)
            plt.title('Distribution of Daily Returns (All Instruments)')
            plt.xlabel('Daily Return')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.savefig(os.path.join(output_dir, 'daily_returns_histogram.png'))
            plt.close()
            print(f"Chart saved to {os.path.join(output_dir, 'daily_returns_histogram.png')}")

except FileNotFoundError:
    print(f"Error: Could not find the file at {daily_data_path}")
except Exception as e:
    print(f"An error occurred while processing the daily data: {e}")


# --- Load and display fundamentals data ---
print("\n--- Sample of Fundamentals Data ---")
try:
    fundamentals_df = pd.read_csv(fundamentals_data_path)
    print(fundamentals_df.head())

    # --- Generate graphs for fundamentals data ---
    if not fundamentals_df.empty:
        # Plot 3: Bar chart of a categorical variable (example: dividend payers)
        if 'Div_Payer' in fundamentals_df.columns:
            # Create a mapping for more descriptive labels
            dividend_labels = fundamentals_df['Div_Payer'].map({1: 'Payer', 0: 'Non-Payer'})
            
            plt.figure(figsize=(8, 5))
            dividend_labels.value_counts().plot(kind='bar')
            plt.title('Count of Dividend vs. Non-Dividend Payers')
            plt.xlabel('Dividend Status')
            plt.ylabel('Number of Firms')
            plt.xticks(rotation=0)
            plt.grid(axis='y')
            plt.savefig(os.path.join(output_dir, 'dividend_payers_count.png'))
            plt.close()
            print(f"\nChart saved to {os.path.join(output_dir, 'dividend_payers_count.png')}")
        else:
            print("\nNote: Could not find a 'Div_Payer' column to plot.")

except FileNotFoundError:
    print(f"Error: Could not find the file at {fundamentals_data_path}")
except Exception as e:
    print(f"An error occurred while processing the fundamentals data: {e}")

print("\nData presentation script finished.")

