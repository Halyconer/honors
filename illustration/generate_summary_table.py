

import pandas as pd
import os

def generate_quintile_summary_latex(characteristic_data, characteristic_col, caption):
    """
    Generates a LaTeX table summarizing the characteristics of each quintile.
    """
    # 1. Get the data from the most recent month
    latest_date = characteristic_data['Date'].max()
    latest_data = characteristic_data[characteristic_data['Date'] == latest_date].copy()

    # 2. Create quintiles
    try:
        latest_data['Quintile'] = pd.qcut(latest_data[characteristic_col], 5, labels=False, duplicates='drop') + 1
    except ValueError:
        print(f"Could not form 5 quintiles for {characteristic_col}. Not enough distinct values.")
        return ""

    # 3. Calculate summary statistics for each quintile
    summary = latest_data.groupby('Quintile')[characteristic_col].agg(['mean', 'min', 'max', 'count'])
    summary.reset_index(inplace=True)
    
    # 4. Format into a LaTeX table string
    latex_string = summary.to_latex(
        header=['Quintile', 'Mean', 'Min', 'Max', 'N (Stocks)'],
        float_format="%.2f",
        index=False
    )
    
    return latex_string

def main():
    """ Main execution function """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fundamentals_path = os.path.join(script_dir, '../final_proposal_code/jci_test_fundamentals_3yr.csv')
        fundamentals = pd.read_csv(fundamentals_path, parse_dates=['Date'])
    except FileNotFoundError as e:
        print(f"Error: Could not find data file. {e}")
        return

    # --- Generate Size Anomaly Table ---
    print("--- LaTeX Table for Size Anomaly Quintiles ---")
    size_table = generate_quintile_summary_latex(
        characteristic_data=fundamentals,
        characteristic_col='Market_Cap_Bil',
        caption='Summary Statistics for Size Quintiles (Market Cap, IDR Billions)'
    )
    print(size_table)

    # --- Generate Age Anomaly Table ---
    print("\n--- LaTeX Table for Age Anomaly Quintiles ---")
    age_table = generate_quintile_summary_latex(
        characteristic_data=fundamentals,
        characteristic_col='Months_Since_Listing',
        caption='Summary Statistics for Age Quintiles (Months Since Listing)'
    )
    print(age_table)

if __name__ == '__main__':
    main()

