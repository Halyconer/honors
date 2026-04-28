"""
01b_BUILD_FF3_FACTORS.PY
IDX Fama-French SMB and HML factor construction.

Source: Foye & Valentinčič (2020) "Testing factor models in Indonesia,"
        Emerging Markets Review 42, 100628 — Section 3.2.

Construction rules:
  - BP = book equity (Dec t-1) / market equity (Dec t-1)
    Both at fiscal year-end. [Foye convention — differs from FF1993 which
    uses December book / June market cap. Foye uses December/December
    as the Indonesia-specific adaptation.]
  - Size and BP breakpoints from the 100 largest stocks by Dec t-1 market cap.
  - Size: S = below median, B = at or above median.
  - BP:   L = at/below 30th pctile, H = at/above 70th pctile, M = middle.
  - All eligible stocks assigned to the 6 independent 2x3 portfolios.
  - Value-weighted using December t-1 market cap throughout holding year.
  - Holding period: July(year+1) through June(year+2).
  - Exclusions: negative/zero BVPS, financial sector firms.
  - SMB = (SH + SM + SL)/3 - (BH + BM + BL)/3
  - HML = (BH + SH)/2  - (BL + SL)/2

Inputs:  data/analysis_daily.csv, data/idx_fundamentals.csv
Output:  data/ff3_factors.csv  [Date, SMB, HML]

Usage:
    python scripts/01b_build_ff3_factors.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

DROP_RICS  = ["MYRX_p.JK^G25", "RMKOn.JK", "CNTX_p.JK", "SQBI_p.JK^C18"]
DATE_START = "2008-01-01"
DATE_END   = "2024-12-31"


# ── 1. Load ───────────────────────────────────────────────────────────
print("Loading data for FF3 factor construction...")
daily = pd.read_csv(DATA / "analysis_daily.csv", parse_dates=["Date"], low_memory=False)
fund  = pd.read_csv(DATA / "idx_fundamentals.csv", parse_dates=["Date"], low_memory=False)

fund  = fund[~fund["Instrument"].isin(DROP_RICS)].copy()
daily = daily[~daily["Instrument"].isin(DROP_RICS)].copy()
daily = daily[(daily["Date"] >= DATE_START) & (daily["Date"] <= DATE_END)].copy()

if "YearMonth" not in daily.columns:
    daily["YearMonth"] = daily["Date"].dt.to_period("M").astype(str)

# Ensure Market_Cap column exists in IDR
if "Market_Cap" not in fund.columns:
    fund["Market_Cap"] = fund["Market_Cap_Bil"] * 1e9

print(f"  Daily : {len(daily):,} rows, {daily['Instrument'].nunique()} stocks")
print(f"  Fund  : {len(fund):,} rows")


# ── 2. Extract December year-end fundamentals ─────────────────────────
# Foye §3.2: "book value of equity at the end of year t-1" and
# "market value of equity at the end of year t-1" — both at December.
fund["_month"] = fund["Date"].dt.month
fund["_year"]  = fund["Date"].dt.year

keep = ["Instrument", "_year", "BVPS", "Shares_Outstanding", "Market_Cap", "Sector"]
dec_fund = (
    fund[fund["_month"] == 12]
    .sort_values("Date")
    .groupby(["Instrument", "_year"])
    .last()
    .reset_index()
)[keep].rename(columns={"_year": "Year"})

print(f"\n  December year-end rows : {len(dec_fund):,} "
      f"({dec_fund['Year'].min()}–{dec_fund['Year'].max()})")


# ── 3. Exclusions ─────────────────────────────────────────────────────
before = len(dec_fund)
dec_fund = dec_fund[dec_fund["BVPS"] > 0].copy()
print(f"  Negative/zero BVPS removed: {before - len(dec_fund):,}")

before = len(dec_fund)
dec_fund = dec_fund[~dec_fund["Sector"].str.contains("Financ", case=False, na=False)]
print(f"  Financials removed        : {before - len(dec_fund):,}")

before = len(dec_fund)
dec_fund = dec_fund[dec_fund["Market_Cap"] > 0].copy()
print(f"  Non-positive MCap removed : {before - len(dec_fund):,}")

# BP = Total Book Equity / Total Market Equity
# BVPS is in IDR/share; Market_Cap is total IDR; so:
#   Total Book = BVPS × Shares_Outstanding  [IDR/share × shares = IDR]
#   BP = Total Book / Market_Cap             [dimensionless]
dec_fund["Total_Book"] = dec_fund["BVPS"] * dec_fund["Shares_Outstanding"]
dec_fund["BP"] = dec_fund["Total_Book"] / dec_fund["Market_Cap"]


# ── 4. Build 2×3 portfolio assignments ───────────────────────────────
print("\nBuilding 2×3 assignments (Foye §3.2 breakpoints from top-100)...")
print(f"  {'Year':>6}  {'N':>5}  {'SL':>5}  {'SM':>5}  {'SH':>5}  "
      f"{'BL':>5}  {'BM':>5}  {'BH':>5}")

blocks = []
for year in sorted(dec_fund["Year"].unique()):
    ref = dec_fund[dec_fund["Year"] == year].copy()
    if len(ref) < 10:
        print(f"  {year}: only {len(ref)} stocks — skipping")
        continue

    top100  = ref.nlargest(min(100, len(ref)), "Market_Cap")
    size_bp = top100["Market_Cap"].median()
    bp_lo   = top100["BP"].quantile(0.30)
    bp_hi   = top100["BP"].quantile(0.70)

    ref["Size_Group"] = np.where(ref["Market_Cap"] >= size_bp, "B", "S")
    ref["BP_Group"]   = np.where(ref["BP"] >= bp_hi, "H",
                        np.where(ref["BP"] <= bp_lo, "L", "M"))
    ref["FF3_Port"]   = ref["Size_Group"] + ref["BP_Group"]

    # Cross-join stocks × holding months (July year+1 → June year+2)
    start  = pd.Period(f"{year + 1}-07", freq="M")
    months = [str(start + i) for i in range(12)]
    block  = ref[["Instrument", "FF3_Port", "Market_Cap"]].copy()
    block["_k"] = 1
    mdf = pd.DataFrame({"YearMonth": months, "_k": 1})
    blocks.append(block.merge(mdf, on="_k").drop(columns="_k"))

    c = ref["FF3_Port"].value_counts()
    print(f"  {year}: {len(ref):5d}  "
          f"{c.get('SL',0):5d}  {c.get('SM',0):5d}  {c.get('SH',0):5d}  "
          f"{c.get('BL',0):5d}  {c.get('BM',0):5d}  {c.get('BH',0):5d}")

assignments = pd.concat(blocks, ignore_index=True)
print(f"\n  Total assignment rows: {len(assignments):,}")


# ── 5. Merge with daily returns ───────────────────────────────────────
merged = daily[["Date", "Instrument", "YearMonth", "Stock_Return"]].merge(
    assignments, on=["Instrument", "YearMonth"], how="inner"
)
print(f"  Merged daily rows    : {len(merged):,}  "
      f"({merged['Date'].min().date()} – {merged['Date'].max().date()})")


# ── 6. Daily VW returns per portfolio ────────────────────────────────
def _vw(grp):
    w = grp["Market_Cap"]
    total = w.sum()
    return np.nan if total <= 0 else (grp["Stock_Return"] * w / total).sum()

ports = (
    merged.groupby(["Date", "FF3_Port"])
    .apply(_vw, include_groups=False)
    .unstack("FF3_Port")
)

for p in ["SL", "SM", "SH", "BL", "BM", "BH"]:
    if p not in ports.columns:
        ports[p] = np.nan
        print(f"  WARNING: portfolio {p} empty — check data coverage")


# ── 7. SMB and HML ────────────────────────────────────────────────────
ports["SMB"] = (
    (ports["SH"] + ports["SM"] + ports["SL"]) / 3
    - (ports["BH"] + ports["BM"] + ports["BL"]) / 3
)
ports["HML"] = (
    (ports["BH"] + ports["SH"]) / 2
    - (ports["BL"] + ports["SL"]) / 2
)

ff3 = ports[["SMB", "HML"]].dropna().reset_index()

print(f"\nFF3 factors ({len(ff3):,} daily obs, "
      f"{ff3['Date'].min().date()} – {ff3['Date'].max().date()}):")
print(f"  SMB: mean={ff3['SMB'].mean()*100:+.4f}%/day  "
      f"std={ff3['SMB'].std()*100:.4f}%/day")
print(f"  HML: mean={ff3['HML'].mean()*100:+.4f}%/day  "
      f"std={ff3['HML'].std()*100:.4f}%/day")


# ── 8. Save ───────────────────────────────────────────────────────────
out = DATA / "ff3_factors.csv"
ff3[["Date", "SMB", "HML"]].to_csv(out, index=False)
print(f"\nSaved → {out}")
