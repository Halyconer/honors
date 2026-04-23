
import pandas as pd
import os

# Define file path
script_dir = os.path.dirname(os.path.abspath(__file__))
fundamentals_data_path = os.path.join(script_dir, '../final_proposal_code/jci_test_fundamentals_3yr.csv')

try:
    # Load the dataset
    df = pd.read_csv(fundamentals_data_path)
    
    # Select key numeric columns for the summary
    key_numeric_cols = ['Market_Cap_Bil', 'ROA', 'Months_Since_Listing', 'BVPS']
    key_numeric_cols = [col for col in key_numeric_cols if col in df.columns]

    if key_numeric_cols:
        # Generate the LaTeX code for the summary statistics table
        # Using booktabs=True for a nicer format that matches the manual table
        latex_table = df[key_numeric_cols].describe().to_latex()
        
        print(latex_table)
    else:
        print("No key numeric columns found to generate a table.")

except FileNotFoundError:
    print(f"Error: Could not find the file at {fundamentals_data_path}")
except Exception as e:
    print(f"An error occurred: {e}")
