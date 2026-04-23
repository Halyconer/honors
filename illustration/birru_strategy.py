import pandas as pd
import numpy as np
import statsmodels.api as sm
import os

def construct_quintile_portfolio(returns_df, characteristic_data, characteristic_col, long_quintile=1, short_quintile=5):
    """
    Constructs a Long-Short portfolio with proper monthly rebalancing using quintiles.
    """
    print(f"\nConstructing portfolio for '{characteristic_col}' anomaly...")
    
    daily_long_stocks = {}
    daily_short_stocks = {}

    characteristic_data['Date'] = pd.to_datetime(characteristic_data['Date'])

    # Use month-end dates to define rebalancing points
    for month_end in pd.date_range(start=returns_df.index.min(), end=returns_df.index.max(), freq='ME'):
        
        char_subset = characteristic_data[characteristic_data['Date'] <= month_end]
        if char_subset.empty: continue
        
        latest_chars = char_subset.loc[char_subset.groupby('Instrument')['Date'].idxmax()]
        char_values = latest_chars.set_index('Instrument')[characteristic_col].dropna()

        available_tickers = [t for t in char_values.index if t in returns_df.columns]
        
        if len(available_tickers) < 5: continue
        
        try:
            quintile_assignments = pd.qcut(char_values[available_tickers], 5, labels=False, duplicates='drop')
            long_stocks = quintile_assignments[quintile_assignments == long_quintile - 1].index.tolist()
            short_stocks = quintile_assignments[quintile_assignments == short_quintile - 1].index.tolist()

            # --- DIAGNOSTIC TEST 2: Quintile Verification ---
            if long_stocks and short_stocks:
                long_chars = char_values[long_stocks]
                short_chars = char_values[short_stocks]
                
                print(f"\nMonth-end {month_end.strftime('%Y-%m')}:")
                print(f"  Long leg (Q{long_quintile}):  N={len(long_stocks):2d}, Avg={long_chars.mean():>10.2f}, Range=[{long_chars.min():.2f}, {long_chars.max():.2f}]")
                print(f"  Short leg (Q{short_quintile}): N={len(short_stocks):2d}, Avg={short_chars.mean():>10.2f}, Range=[{short_chars.min():.2f}, {short_chars.max():.2f}]")

        except (ValueError, IndexError):
            continue

        next_month_start = month_end + pd.Timedelta(days=1)
        next_month_end = next_month_start + pd.offsets.MonthEnd(1)
        trading_days_in_next_month = returns_df.loc[next_month_start:next_month_end].index
        
        for day in trading_days_in_next_month:
            daily_long_stocks[day] = long_stocks
            daily_short_stocks[day] = short_stocks
            
    lms_returns = {}
    for day, stocks in daily_long_stocks.items():
        if stocks and day in returns_df.index:
            long_ret = returns_df.loc[day, stocks].mean()
            short_stocks = daily_short_stocks.get(day, [])
            if short_stocks:
                short_ret = returns_df.loc[day, short_stocks].mean()
                lms_returns[day] = long_ret - short_ret

    lms_returns_series = pd.Series(lms_returns).dropna()
    
    if lms_returns_series.empty:
        print("❌ Portfolio construction resulted in zero daily observations.")
    else:
        print(f"\n✅ Constructed portfolio with {len(lms_returns_series)} daily observations.")
    
    return lms_returns_series

def run_day_specific_capm(lms_returns, market_returns, rf_annual=0.05):
    """
    Run separate CAPM regressions for each day of the week.
    """
    rf_daily = (1 + rf_annual)**(1/252) - 1
    data = pd.DataFrame({'LMS': lms_returns, 'R_Market': market_returns}).dropna()
    
    if data.empty:
        print("⚠️ No overlapping data. Cannot run regression.")
        return None

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    results_summary = []
    
    print("\n" + "="*80)
    print("DAY-SPECIFIC CAPM REGRESSIONS")
    print("="*80)
    
    for day_name in days:
        day_of_week_index = days.index(day_name)
        day_mask = data.index.dayofweek == day_of_week_index
        day_data = data[day_mask]
        
        if len(day_data) < 10:
            print(f"\n⚠️ {day_name}: Insufficient data ({len(day_data)} obs)")
            continue
        
        Y = day_data['LMS'] - rf_daily
        X = sm.add_constant(day_data['R_Market'] - rf_daily)
        
        model = sm.OLS(Y, X).fit()
        
        alpha_daily = model.params['const']
        alpha_monthly = alpha_daily * 21
        p_value = model.pvalues['const']
        stars = '***' if p_value < 0.01 else '**' if p_value < 0.05 else '*' if p_value < 0.10 else ''
        
        results_summary.append({
            'Day': day_name, 'N': int(model.nobs), 'Alpha_Monthly_%': alpha_monthly * 100,
            't_stat': model.tvalues['const'], 'Significance': stars
        })
    
    if not results_summary:
        print("\nNo regressions were run due to insufficient data.")
        return None

    df = pd.DataFrame(results_summary)
    
    print("\nSUMMARY TABLE: Day-Specific CAPM Alphas")
    print(df.to_string(index=False))
    
    return df

def main():
    """ Main execution function """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        returns_path = os.path.join(script_dir, '../final_proposal_code/daily_returns_merged.csv')
        fundamentals_path = os.path.join(script_dir, '../final_proposal_code/jci_test_fundamentals_3yr.csv')

        daily_returns = pd.read_csv(returns_path, index_col='Date', parse_dates=True)
        fundamentals = pd.read_csv(fundamentals_path)
    except FileNotFoundError as e:
        print(f"Error: Could not find data file. {e}")
        return

    market_returns = daily_returns['^JKSE']
    stock_returns = daily_returns.drop(columns=['^JKSE'])

    strategies = [
        {"name": "Size Anomaly", "characteristic_col": "Market_Cap_Bil", "speculative_leg": "long"},
        {"name": "Age Anomaly", "characteristic_col": "Months_Since_Listing", "speculative_leg": "long"}
    ]

    for strat in strategies:
        print(f"\n{'='*80}")
        print(f"ANALYZING: {strat['name']}")
        print(f"{'='*80}")

        lms_returns = construct_quintile_portfolio(
            returns_df=stock_returns, characteristic_data=fundamentals,
            characteristic_col=strat['characteristic_col'], long_quintile=1, short_quintile=5
        )

        if lms_returns.empty: continue

        # --- DIAGNOSTIC TEST 1: Portfolio Diagnostics ---
        print(f"\nPortfolio Diagnostics:")
        print(f"LMS return mean: {lms_returns.mean()*252*100:.2f}% annually")
        print(f"LMS return std: {lms_returns.std()*np.sqrt(252)*100:.2f}% annually")
        print(f"Sharpe ratio: {lms_returns.mean()/lms_returns.std()*np.sqrt(252):.3f}")
        print(f"Min daily return: {lms_returns.min()*100:.2f}%")
        print(f"Max daily return: {lms_returns.max()*100:.2f}%")
        print(f"Days with |return| > 10%: {(abs(lms_returns) > 0.10).sum()}")

        capm_results = run_day_specific_capm(lms_returns, market_returns)

        if capm_results is not None and len(capm_results) >= 2:
            print("\n" + "="*80)
            print("KEY COMPARISON: Monday vs Friday")
            print("="*80)
            
            monday_row = capm_results[capm_results['Day'] == 'Monday'].iloc[0]
            friday_row = capm_results[capm_results['Day'] == 'Friday'].iloc[0]
            
            print(f"Monday Alpha:    {monday_row['Alpha_Monthly_%']:>8.4f}%  (t = {monday_row['t_stat']:.2f})")
            print(f"Friday Alpha:    {friday_row['Alpha_Monthly_%']:>8.4f}%  (t = {friday_row['t_stat']:.2f})")
            
            print(f"\nBIRRU INTERPRETATION:")
            if strat['speculative_leg'] == 'long':
                expected = "Friday > Monday (long leg speculative)"
                actual = "✓ CONFIRMED" if friday_row['Alpha_Monthly_%'] > monday_row['Alpha_Monthly_%'] else "✗ NOT CONFIRMED"
            else:
                expected = "Monday > Friday (short leg speculative)"
                actual = "✓ CONFIRMED" if monday_row['Alpha_Monthly_%'] > friday_row['Alpha_Monthly_%'] else "✗ NOT CONFIRMED"
            
            print(f"Expected pattern: {expected}")
            print(f"Actual result: {actual}")

if __name__ == '__main__':
    main()