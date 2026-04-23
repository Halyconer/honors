

import pandas as pd
import matplotlib.pyplot as plt
import os

# Define file paths
fundamentals_data_path = '../final_proposal_code/jci_test_fundamentals_3yr.csv'
output_dir = 'charts'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("--- Generating Data Quality Report for Fundamentals Data ---")

try:
    # Load the dataset
    df = pd.read_csv(fundamentals_data_path)
    
    # --- 1. Data Coverage ---
    coverage = df.notnull().mean() * 100
    coverage = coverage.sort_values(ascending=True) # Sort for better visualization

    # --- 2. Key Summary Statistics ---
    num_instruments = df['Instrument'].nunique()
    
    # Ensure 'Date' column is in datetime format to find min/max
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    min_date = df['Date'].min().strftime('%Y-%m-%d')
    max_date = df['Date'].max().strftime('%Y-%m-%d')
    
    # --- 3. Display Statistics in a Presentable Text Format ---
    
    print("\n" + "="*50)
    print("      DATASET OVERVIEW & QUALITY REPORT")
    print("="*50)
    
    print(f"\nSource File: {os.path.basename(fundamentals_data_path)}")
    print(f"Total Records: {len(df)}")
    
    print("\n--- Key Metrics ---")
    print(f"Number of Unique Instruments: {num_instruments}")
    print(f"Date Range: {min_date} to {max_date}")

    print("\n--- Data Coverage by Column ---")
    print("This shows the percentage of non-missing data for each attribute.")
    for col, perc in coverage.items():
        print(f"{col:>25}: {perc:6.2f}%")
        
    print("\n--- Summary Statistics for Key Numerical Columns ---")
    # Using a subset of important columns for a cleaner summary
    key_numeric_cols = ['Market_Cap_Bil', 'ROA', 'Months_Since_Listing', 'BVPS']
    # Filter out columns that don't exist in the dataframe
    key_numeric_cols = [col for col in key_numeric_cols if col in df.columns]
    if key_numeric_cols:
        print(df[key_numeric_cols].describe().to_string())
    else:
        print("No key numeric columns found for summary.")

    print("\n" + "="*50)
    
    # --- 4. Generate Bar Chart for Data Coverage ---
    plt.figure(figsize=(12, 8))
    coverage.plot(kind='barh', color='skyblue')
    plt.title('Data Coverage for Fundamentals Dataset', fontsize=16)
    plt.xlabel('Percentage of Data Available (%)', fontsize=12)
    plt.ylabel('Data Fields', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    # Add percentage labels to the bars
    for index, value in enumerate(coverage):
        plt.text(value, index, f' {value:.2f}%', va='center')
        
    plt.xlim(0, 110) # Give some space for labels
    plt.tight_layout()
    
    chart_path = os.path.join(output_dir, 'data_coverage_report.png')
    plt.savefig(chart_path)
    plt.close()
    
    print(f"\nA visual report of data coverage has been saved to:\n{chart_path}")

except FileNotFoundError:
    print(f"Error: Could not find the file at {fundamentals_data_path}")
except Exception as e:
    print(f"An error occurred: {e}")

