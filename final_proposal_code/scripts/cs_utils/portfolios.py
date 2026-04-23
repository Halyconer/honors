"""
Portfolio construction: anomaly filters, decile assignment, L-S returns.
"""

import pandas as pd
import numpy as np


def apply_anomaly_filter(chars_df, filter_type):
    """
    Apply anomaly-specific filters before portfolio sorting.

    filter_type:
      'min15'         -- require >= 15 daily obs in prior month (Ivol, Max)
      'no_financials' -- exclude financial sector firms (ROA)
      'no_neg_bvps'   -- exclude firms with negative BVPS (BM)
      None            -- no filter
    """
    if filter_type is None:
        return chars_df

    df = chars_df.copy()

    if filter_type == "min15":
        before = len(df)
        df = df[df["Trading_Days"] >= 15]
        print(f"    min15 filter: {before:,} -> {len(df):,} stock-months "
              f"(dropped {before - len(df):,})")

    elif filter_type == "no_financials":
        before = len(df)
        df = df[~df["Sector"].str.contains("Financ", case=False, na=False)]
        print(f"    no_financials filter: {before:,} -> {len(df):,} stock-months "
              f"(dropped {before - len(df):,})")

    elif filter_type == "no_neg_bvps":
        before = len(df)
        df = df[~(df["BVPS"] < 0)]
        print(f"    no_neg_bvps filter: {before:,} -> {len(df):,} stock-months "
              f"(dropped {before - len(df):,})")

    return df


def assign_deciles_monthly(chars_df, col, n_portfolios):
    """Assign decile ranks (1..n_portfolios) per Sort_YearMonth."""
    c = chars_df[["Instrument", "Sort_YearMonth", col, "Market_Cap"]].dropna(subset=[col]).copy()

    def qcut_safe(x):
        try:
            return pd.qcut(x.rank(method="first"), n_portfolios,
                           labels=range(1, n_portfolios + 1))
        except ValueError:
            return pd.Series(np.nan, index=x.index)

    c["Decile"] = (
        c.groupby("Sort_YearMonth")[col]
        .transform(qcut_safe)
        .astype(float)
    )
    return c[["Instrument", "Sort_YearMonth", "Decile", "Market_Cap"]].dropna()


def assign_deciles_annual(chars_df, col, n_portfolios):
    """
    Annual rebalancing: use June characteristics (Sort_YearMonth ending in -07,
    since June chars have Sort_YearMonth = July due to 1-month lag).
    Hold from July to following June.
    """
    c = chars_df[["Instrument", "Sort_YearMonth", col, "Market_Cap"]].dropna(subset=[col]).copy()

    # Keep only July sort months (= June measurement months)
    c["sort_month"] = pd.to_datetime(c["Sort_YearMonth"]).dt.month
    june_sorts = c[c["sort_month"] == 7].copy()

    if len(june_sorts) == 0:
        print(f"    WARNING: No July sort months found for {col}")
        return pd.DataFrame(columns=["Instrument", "Sort_YearMonth", "Decile", "Market_Cap"])

    def qcut_safe(x):
        try:
            return pd.qcut(x.rank(method="first"), n_portfolios,
                           labels=range(1, n_portfolios + 1))
        except ValueError:
            return pd.Series(np.nan, index=x.index)

    june_sorts["Decile"] = (
        june_sorts.groupby("Sort_YearMonth")[col]
        .transform(qcut_safe)
        .astype(float)
    )
    june_sorts = june_sorts[["Instrument", "Sort_YearMonth", "Decile", "Market_Cap"]].dropna()

    # Expand: each July sort holds through the following June
    expanded = []
    for _, row in june_sorts.iterrows():
        july_date = pd.to_datetime(row["Sort_YearMonth"])
        for offset in range(12):
            ym = (july_date + pd.DateOffset(months=offset)).to_period("M")
            expanded.append({
                "Instrument": row["Instrument"],
                "Sort_YearMonth": str(ym),
                "Decile": row["Decile"],
                "Market_Cap": row["Market_Cap"],
            })

    return pd.DataFrame(expanded)


def _vw_return(group):
    """Value-weighted return: sum(w_i * r_i) where w_i = mcap_i / sum(mcap)."""
    mcap = group["Market_Cap"]
    total = mcap.sum()
    if total <= 0:
        return np.nan
    return (group["Stock_Return"] * mcap / total).sum()


def compute_daily_ls_vw(daily_df, decile_df, spec_is, n_portfolios):
    """
    Compute daily VALUE-WEIGHTED L-S returns with individual legs.

    Returns DataFrame indexed by Date with columns:
        Spec_Return, Safe_Return, LS_Return (= Safe - Spec)
    """
    d_merge = decile_df.rename(columns={"Sort_YearMonth": "YearMonth"})
    merged = daily_df[["Date", "Instrument", "YearMonth", "Stock_Return"]].merge(
        d_merge[["Instrument", "YearMonth", "Decile", "Market_Cap"]],
        on=["Instrument", "YearMonth"], how="inner"
    )

    if spec_is == "high":
        spec_decile, safe_decile = n_portfolios, 1
    else:  # 'low'
        spec_decile, safe_decile = 1, n_portfolios

    spec = merged[merged["Decile"] == spec_decile].groupby("Date").apply(_vw_return, include_groups=False)
    safe = merged[merged["Decile"] == safe_decile].groupby("Date").apply(_vw_return, include_groups=False)

    result = pd.DataFrame({"Spec_Return": spec, "Safe_Return": safe})
    result["LS_Return"] = result["Safe_Return"] - result["Spec_Return"]
    return result.dropna()


def compute_binary_ls_vw(daily_df, chars_df, col):
    """
    For binary characteristics: value-weighted within each group.

    Returns DataFrame indexed by Date with columns:
        Spec_Return, Safe_Return, LS_Return (= Safe - Spec)
    """
    c = chars_df[["Instrument", "Sort_YearMonth", col, "Market_Cap"]].dropna(subset=[col]).copy()
    c_merge = c.rename(columns={"Sort_YearMonth": "YearMonth"})
    merged = daily_df[["Date", "Instrument", "YearMonth", "Stock_Return"]].merge(
        c_merge, on=["Instrument", "YearMonth"], how="inner"
    )

    # Dividend: payer (1) = safe (long), non-payer (0) = speculative (short)
    safe = merged[merged[col] == 1].groupby("Date").apply(_vw_return, include_groups=False)
    spec = merged[merged[col] == 0].groupby("Date").apply(_vw_return, include_groups=False)

    result = pd.DataFrame({"Spec_Return": spec, "Safe_Return": safe})
    result["LS_Return"] = result["Safe_Return"] - result["Spec_Return"]
    return result.dropna()
