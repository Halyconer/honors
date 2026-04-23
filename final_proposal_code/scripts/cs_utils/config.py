"""
Characteristic definitions and constants for cross-sectional analysis.
Based on Birru (2018) JFE Appendix pp.209-212.
"""

CHARS = {
    "Ivol": {
        "col": "Ivol",
        "spec_is": "high",
        "rebalance": "monthly",
        "filter": "min15",
    },
    "Max": {
        "col": "Max_Return",
        "spec_is": "high",
        "rebalance": "monthly",
        "filter": "min15",
    },
    "Size": {
        "col": "Log_MCap",
        "spec_is": "low",
        "rebalance": "annual",
        "filter": None,
    },
    "Price": {
        "col": "End_Price",
        "spec_is": "low",
        "rebalance": "annual",
        "filter": None,
    },
    "Age": {
        "col": "Months_Since_Listing",
        "spec_is": "low",
        "rebalance": "annual",
        "filter": None,
    },
    "ROA": {
        "col": "ROA",
        "spec_is": "low",
        "rebalance": "annual",
        "filter": "no_financials",
    },
    "Dividend": {
        "col": "Div_Payer",
        "spec_is": "binary",
        "rebalance": "annual",
        "filter": None,
    },
    "BM": {
        "col": "BM_Ratio",
        "spec_is": "high",
        "rebalance": "annual",
        "filter": "no_neg_bvps",
    },
}

DAYS = ["Monday", "Friday", "Tue-Thu"]
TABLE_COLS = ["Monday", "Friday", "Tue-Thu", "Fri-Mon"]
N_PORTFOLIOS = 5  # quintiles for non-binary characteristics

# ── Pre/Post breakpoints for structural-change analysis ──────────────
# Each breakpoint defines the first month of the "Post" period.
# Primary breakpoint: 2017-01 (current thesis design, 1M SID milestone).
# Sensitivity breakpoint: 2016-01 (YNS campaign / SID doubling).
PRIMARY_BREAK = "2017-01"
SENSITIVITY_BREAKS = ["2016-01"]
