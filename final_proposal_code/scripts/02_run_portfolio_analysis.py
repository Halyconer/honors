"""
02_RUN_PORTFOLIO_ANALYSIS.PY
Cross-Sectional Analysis — Birru-Style Portfolio Sorts (JFE 2018)
================================================================
Value-weighted quintile portfolios, excess return mean tests,
individual leg decomposition, Newey-West HAC standard errors.

L-S Spread Calculation: Safe minus Speculative (Positive = Safe outperforms)

Usage:
    python scripts/02_run_portfolio_analysis.py
"""

from pathlib import Path

from cs_utils.config import CHARS, DAYS, N_PORTFOLIOS, PRIMARY_BREAK, SENSITIVITY_BREAKS
from cs_utils.data_loading import load_data, build_date_info
from cs_utils.portfolios import (
    apply_anomaly_filter,
    assign_quintiles_monthly,
    assign_quintiles_annual,
    compute_daily_ls_vw,
    compute_binary_ls_vw,
)
from cs_utils.regression import (
    aggregate_monthly_legs, run_mean_test, run_capm, run_ff3,
    run_mean_test_period, run_capm_period, run_ff3_period,
    run_mean_test_dummy, run_capm_dummy, run_ff3_dummy,
)
from cs_utils.formatting import (
    print_results, save_latex,
    print_results_capm, save_latex_capm,
    print_results_capm_decomp, save_latex_capm_decomp,
    print_results_ff3, save_latex_ff3,
    print_split_sample, print_ff3_split_sample,
    print_dummy_results, print_capm_dummy_results, print_ff3_dummy_results,
    save_latex_split, save_latex_ff3_split,
    save_latex_dummy, save_latex_capm_dummy, save_latex_ff3_dummy,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

# ── Load data ─────────────────────────────────────────────────────────
daily, chars = load_data(DATA)
date_info = build_date_info(daily, DATA)

# ── Main loop ─────────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  CROSS-SECTIONAL ANALYSIS: EXCESS RETURNS BY DAY-OF-WEEK")
print("  Value-weighted, quintile sorts, Birru (2018) rebalancing")
print("=" * 80)

results = {}             # (char_name, day_group, leg) -> (result_obj, n_obs)
capm_results = {}        # full-month MktRF (Birru Table 2 primary)
capm_decomp_results = {} # day-decomposed MktRF (Birru Table 6 robustness)
ff3_results = {}         # FF3 alpha (Foye & Valentinčič 2020)
monthly_by_day = {}
excess_series = {}       # (char_name, day_group, leg) -> Series of excess returns
mktrf_series = {}        # (char_name, day_group, leg) -> Series of MktRF (full-month)
smb_series = {}          # (char_name, day_group, leg) -> Series of monthly SMB
hml_series = {}          # (char_name, day_group, leg) -> Series of monthly HML

# ── Full-month factor series ──────────────────────────────────────────
fullmonth_mktrf = date_info.groupby("YM")["Market_Excess"].sum()
fullmonth_mktrf.name = "MktRF_FullMonth"

# SMB/HML are NaN when ff3_factors.csv hasn't been built yet;
# run_ff3 handles that gracefully (returns None after dropna).
fullmonth_smb = date_info.groupby("YM")["SMB"].sum()
fullmonth_smb.name = "SMB_FullMonth"
fullmonth_hml = date_info.groupby("YM")["HML"].sum()
fullmonth_hml.name = "HML_FullMonth"

for char_name, config in CHARS.items():
    col = config["col"]
    spec_is = config["spec_is"]
    rebal = config["rebalance"]
    filt = config["filter"]

    print(f"\n--- {char_name} ({col}, spec={spec_is}, rebal={rebal}, filter={filt}) ---")

    chars_filtered = apply_anomaly_filter(chars, filt)

    if spec_is == "binary":
        legs_daily = compute_binary_ls_vw(daily, chars_filtered, col)
        print(f"  Binary split, daily obs: {len(legs_daily):,}")
    else:
        if rebal == "annual":
            quintiles = assign_quintiles_annual(chars_filtered, col, N_PORTFOLIOS)
        else:
            quintiles = assign_quintiles_monthly(chars_filtered, col, N_PORTFOLIOS)

        n_months = quintiles["Sort_YearMonth"].nunique()
        avg_per_quintile = len(quintiles) / max(1, n_months) / N_PORTFOLIOS
        print(f"  Quintile-months: {n_months}, avg stocks/quintile: {avg_per_quintile:.0f}")

        legs_daily = compute_daily_ls_vw(daily, quintiles, spec_is, N_PORTFOLIOS)
        print(f"  Daily obs: {len(legs_daily):,}")

    monthly = aggregate_monthly_legs(legs_daily, date_info)

    # ── Day-specific regressions ──────────────────────────────────────
    for day_group in DAYS:
        if day_group == "Tue-Thu":
            day_data = monthly[monthly["DayName"].isin(
                ["Tuesday", "Wednesday", "Thursday"]
            )]
            tue_thu_agg = dict(
                LS_Monthly=("LS_Monthly", "sum"),
                Spec_Monthly=("Spec_Monthly", "sum"),
                Safe_Monthly=("Safe_Monthly", "sum"),
                Rf_Monthly=("Rf_Monthly", "sum"),
                MktRF_Monthly=("MktRF_Monthly", "sum"),
                N_Days=("N_Days", "sum"),
            )
            for fac in ["SMB_Monthly", "HML_Monthly"]:
                if fac in monthly.columns:
                    tue_thu_agg[fac] = (fac, "sum")
            day_data = day_data.groupby("YM").agg(**tue_thu_agg).reset_index()
        else:
            day_data = monthly[monthly["DayName"] == day_group].copy()

        monthly_by_day[(char_name, day_group)] = day_data

        for leg, col_name in [("LS", "LS_Monthly"), ("Spec", "Spec_Monthly"), ("Safe", "Safe_Monthly")]:
            indexed = day_data.set_index("YM")
            
            # LS is already an excess return (Safe - Spec), so we don't subtract Rf.
            # Individual legs (Safe, Spec) require Rf subtraction for excess returns.
            if leg == "LS":
                excess = indexed[col_name]
            else:
                excess = indexed[col_name] - indexed["Rf_Monthly"]
            
            mktrf_day = indexed["MktRF_Monthly"]

            # Store series for split-sample / dummy regressions later
            excess_series[(char_name, day_group, leg)] = excess
            mktrf_series[(char_name, day_group, leg)] = fullmonth_mktrf
            smb_series[(char_name, day_group, leg)]   = fullmonth_smb
            hml_series[(char_name, day_group, leg)]   = fullmonth_hml

            # Excess return test
            result_obj, n = run_mean_test(excess)
            results[(char_name, day_group, leg)] = (result_obj, n)

            # Primary CAPM: full-month MktRF (Birru Table 2)
            capm_obj, n_capm = run_capm(excess, fullmonth_mktrf)
            capm_results[(char_name, day_group, leg)] = (capm_obj, n_capm)

            # Day-decomposed CAPM: day-specific MktRF (Birru Table 6)
            capm_d_obj, n_d = run_capm(excess, mktrf_day)
            capm_decomp_results[(char_name, day_group, leg)] = (capm_d_obj, n_d)

            # FF3 alpha: full-month MktRF + IDX SMB + IDX HML (Foye 2020)
            ff3_obj, n_ff3 = run_ff3(excess, fullmonth_mktrf, fullmonth_smb, fullmonth_hml)
            ff3_results[(char_name, day_group, leg)] = (ff3_obj, n_ff3)

    # ── Fri - Mon difference ──────────────────────────────────────────
    mon = monthly_by_day[(char_name, "Monday")].set_index("YM")
    fri = monthly_by_day[(char_name, "Friday")].set_index("YM")
    diff = mon.join(fri, lsuffix="_mon", rsuffix="_fri", how="inner")

    for leg, col_name in [("LS", "LS_Monthly"), ("Spec", "Spec_Monthly"), ("Safe", "Safe_Monthly")]:
        # For LS: (Safe_fri - Spec_fri) - (Safe_mon - Spec_mon)
        # For individual legs: (Leg_fri - Rf_fri) - (Leg_mon - Rf_mon)
        if leg == "LS":
            excess_diff = diff[f"{col_name}_fri"] - diff[f"{col_name}_mon"]
        else:
            excess_diff = (
                (diff[f"{col_name}_fri"] - diff["Rf_Monthly_fri"])
                - (diff[f"{col_name}_mon"] - diff["Rf_Monthly_mon"])
            )
            
        mktrf_day_diff = diff["MktRF_Monthly_fri"] - diff["MktRF_Monthly_mon"]

        # For Fri-Mon SMB/HML: full-month factors cancel (same calendar month),
        # so only the day-difference is meaningful — same logic as MktRF.
        smb_day_diff = (diff["SMB_Monthly_fri"] - diff["SMB_Monthly_mon"]
                        if "SMB_Monthly_fri" in diff.columns
                        else mktrf_day_diff * float("nan"))
        hml_day_diff = (diff["HML_Monthly_fri"] - diff["HML_Monthly_mon"]
                        if "HML_Monthly_fri" in diff.columns
                        else mktrf_day_diff * float("nan"))

        # Store for split-sample / dummy regressions
        excess_series[(char_name, "Fri-Mon", leg)] = excess_diff
        mktrf_series[(char_name, "Fri-Mon", leg)]  = mktrf_day_diff
        smb_series[(char_name, "Fri-Mon", leg)]    = smb_day_diff
        hml_series[(char_name, "Fri-Mon", leg)]    = hml_day_diff

        result_obj, n = run_mean_test(excess_diff)
        results[(char_name, "Fri-Mon", leg)] = (result_obj, n)

        # For Fri-Mon difference, full-month MktRF cancels (both legs fall in
        # the same calendar month), so day-decomposed MktRF (Fri − Mon) is the
        # only meaningful regressor. Both capm_results and capm_decomp_results
        # receive the same regression here — this is intentional; the
        # "primary" and "robustness" columns will be identical for the Fri-Mon
        # contrast. Note this in any table footnote to avoid reader confusion.
        capm_obj, n_capm = run_capm(excess_diff, mktrf_day_diff)
        capm_results[(char_name, "Fri-Mon", leg)] = (capm_obj, n_capm)

        capm_d_obj, n_d = run_capm(excess_diff, mktrf_day_diff)
        capm_decomp_results[(char_name, "Fri-Mon", leg)] = (capm_d_obj, n_d)

        ff3_obj, n_ff3 = run_ff3(excess_diff, mktrf_day_diff, smb_day_diff, hml_day_diff)
        ff3_results[(char_name, "Fri-Mon", leg)] = (ff3_obj, n_ff3)

# ── Output: Full-sample tables (existing) ────────────────────────────
print_results(results)
save_latex(results, OUT / "dow_excess_returns.tex")

print_results_capm(capm_results)
save_latex_capm(capm_results, OUT / "dow_capm_alphas.tex")

print_results_capm_decomp(capm_decomp_results)
save_latex_capm_decomp(capm_decomp_results, OUT / "dow_capm_decomp_alphas.tex")

print_results_ff3(ff3_results)
save_latex_ff3(ff3_results, OUT / "dow_ff3_alphas.tex")


# ══════════════════════════════════════════════════════════════════════
#  PRE/POST STRUCTURAL CHANGE ANALYSIS
# ══════════════════════════════════════════════════════════════════════

all_breaks = [PRIMARY_BREAK] + SENSITIVITY_BREAKS

for break_ym in all_breaks:
    print(f"\n{'#' * 80}")
    print(f"  STRUCTURAL CHANGE ANALYSIS — Break at {break_ym}")
    print(f"{'#' * 80}")

    pre_results = {}
    post_results = {}
    dummy_mean_results = {}
    dummy_capm_results = {}
    ff3_pre_results = {}
    ff3_post_results = {}
    dummy_ff3_results = {}

    for key, excess in excess_series.items():
        char_name, day_group, leg = key
        mktrf = mktrf_series[key]
        smb   = smb_series[key]
        hml   = hml_series[key]

        # Split-sample mean tests
        pre_obj, n_pre = run_mean_test_period(excess, break_ym, "Pre")
        pre_results[(char_name, day_group, leg)] = (pre_obj, n_pre)

        post_obj, n_post = run_mean_test_period(excess, break_ym, "Post")
        post_results[(char_name, day_group, leg)] = (post_obj, n_post)

        # Pooled dummy mean test
        dummy_obj, n_dummy = run_mean_test_dummy(excess, break_ym)
        dummy_mean_results[(char_name, day_group, leg)] = (dummy_obj, n_dummy)

        # Pooled dummy CAPM (HAC Wald structural break test)
        dummy_c_obj, n_c_dummy = run_capm_dummy(excess, mktrf, break_ym)
        dummy_capm_results[(char_name, day_group, leg)] = (dummy_c_obj, n_c_dummy)

        # FF3 split-sample
        ff3_pre_obj, _  = run_ff3_period(excess, mktrf, smb, hml, break_ym, "Pre")
        ff3_post_obj, _ = run_ff3_period(excess, mktrf, smb, hml, break_ym, "Post")
        ff3_pre_results[(char_name, day_group, leg)]  = (ff3_pre_obj, _)
        ff3_post_results[(char_name, day_group, leg)] = (ff3_post_obj, _)

        # FF3 pooled dummy (HAC Wald structural break test)
        dummy_ff3_obj, n_ff3d = run_ff3_dummy(excess, mktrf, smb, hml, break_ym)
        dummy_ff3_results[(char_name, day_group, leg)] = (dummy_ff3_obj, n_ff3d)

    # ── Terminal output ──────────────────────────────────────────────
    print_split_sample(pre_results, post_results, break_ym)
    print_ff3_split_sample(ff3_pre_results, ff3_post_results, break_ym)
    print_dummy_results(dummy_mean_results, break_ym)
    print_capm_dummy_results(dummy_capm_results, break_ym)
    print_ff3_dummy_results(dummy_ff3_results, break_ym)

    # ── LaTeX output ─────────────────────────────────────────────────
    tag = break_ym.replace("-", "")
    save_latex_split(pre_results, post_results, break_ym,
                     OUT / f"split_sample_{tag}.tex")
    save_latex_ff3_split(ff3_pre_results, ff3_post_results, break_ym,
                         OUT / f"split_ff3_{tag}.tex")
    save_latex_dummy(dummy_mean_results, break_ym,
                     OUT / f"dummy_mean_{tag}.tex")
    save_latex_capm_dummy(dummy_capm_results, break_ym,
                          OUT / f"dummy_capm_{tag}.tex")
    save_latex_ff3_dummy(dummy_ff3_results, break_ym,
                         OUT / f"dummy_ff3_{tag}.tex")
