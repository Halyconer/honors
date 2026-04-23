
import pandas as pd
import os

# Get the absolute path of the directory containing the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths
daily_data_path = os.path.join(script_dir, '../final_proposal_code/jci_test_daily_3yr.csv')
fundamentals_data_path = os.path.join(script_dir, '../final_proposal_code/jci_test_fundamentals_3yr.csv')

def summarize_dataframe(df_name, df):
    """Prints a summary of the given DataFrame."""
    print(f"--- Summary for {df_name} ---")
    
    print("\n[1] First 5 Rows:")
    print(df.head())
    
    print("\n[2] Dataframe Info (Data Types & Nulls):")
    df.info()
    
    print(f"\n[3] Descriptive Statistics for Numerical Columns:")
    # Note: Using try/except in case there are no numeric columns
    try:
        print(df.describe())
    except ValueError:
        print("No numerical columns to describe.")
        
    print("-" * (len(df_name) + 16))


# --- Load and summarize daily data ---
try:
    daily_df = pd.read_csv(daily_data_path)
    summarize_dataframe("Daily Data", daily_df)
    
    # Specific essence for daily data: Number of unique instruments
    print("\n[4] Essence of Daily Data:")
    print(f"Number of unique instruments: {daily_df['Instrument'].nunique()}")
    
except FileNotFoundError:
    print(f"Error: Could not find the file at {daily_data_path}")
except Exception as e:
    print(f"An error occurred while processing the daily data: {e}")


# --- Load and summarize fundamentals data ---
try:
    fundamentals_df = pd.read_csv(fundamentals_data_path)
    summarize_dataframe("\nFundamentals Data", fundamentals_df)

    # Specific essence for fundamentals data: Value counts for categorical columns
    print("\n[4] Essence of Fundamentals Data:")
    if 'Div_Payer' in fundamentals_df.columns:
        print("Value counts for 'Div_Payer':")
        print(fundamentals_df['Div_Payer'].value_counts())
        
except FileNotFoundError:
    print(f"Error: Could not find the file at {fundamentals_data_path}")
except Exception as e:
    print(f"An error occurred while processing the fundamentals data: {e}")

print("\nData summarization script finished.")
