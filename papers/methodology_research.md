# Econometric Methodology Research — Monday Effect in Indonesia

## What Birru (2018) Actually Does

### Core Method: Portfolio Sorts + Time-Series Factor Regressions
Birru does **not** run a day-of-week dummy regression on index returns. His approach is:
1. Sort stocks into decile portfolios by each anomaly characteristic (using NYSE breakpoints, value-weighted)
2. For each portfolio, compute **monthly returns from only specific days** — e.g., the "Monday monthly return" = sum of all Monday daily returns within that month
3. Regress these day-specific monthly L-S returns on factor models (CAPM, FF3, Carhart 4-factor)
4. Compare Monday alpha vs Friday alpha

### Key Specs
- **Portfolios**: Value-weighted, NYSE breakpoints, decile sorts (binary for some: E, CF, D)
- **Risk adjustment**: 4 levels — excess returns, CAPM alpha, FF3 alpha, Carhart 4-factor alpha
- **Standard errors**: Newey-West HAC (lag count not specified in paper)
- **Sample**: CRSP (NYSE/Amex/Nasdaq), share code 10 or 11, July 1963–Dec 2013
- **Factor exclusions**: SMB excluded for size anomaly; market factor excluded for beta sorts
- **Rebalancing**: Monthly for market-based sorts (Ivol, Max, Beta, etc.); annual (end of June) for accounting-based sorts (Size, ROA, OP, etc.)

### What Birru Does NOT Do
- No day-of-week dummy regression on aggregate market returns
- No GARCH models
- No structural break tests
- No panel regressions

His approach is fundamentally **cross-sectional** (speculative vs safe stocks), not aggregate. This is a different question from yours.

---

## What the DOW Effect Literature Does (and What You Should Do)

### Your Study vs Birru
| Feature | Birru (2018) | Your Thesis |
|---------|-------------|-------------|
| Market | US (developed) | Indonesia (emerging) |
| Question | Which stocks drive DOW patterns? | Did mobile trading change the Monday effect? |
| Primary analysis | Cross-sectional portfolio sorts | Aggregate time-series + panel |
| Risk adjustment | FF/Carhart factors | Not available for Indonesia |
| Innovation | Day-specific monthly returns | Pre/post structural break |

You are asking a **time-series structural change** question, not a cross-sectional sorting question. Your methodology should follow the DOW aggregate literature (French 1980, Gibbons & Hess 1981, Berument & Kiymaz 2001, Robins & Smith 2016) more than Birru.

---

## Recommended Methodology (Section by Section)

### Section 1: Descriptive Statistics
- JCI daily return by day-of-week: mean, median, std dev, skewness, kurtosis
- t-test of each day's mean vs zero
- Split by pre (2012–2016) vs post (2017–2024)
- Kruskal-Wallis nonparametric test for equality across days (used by Khan et al. 2023 for Indonesia)
- Boxplot of returns by day, side-by-side pre vs post

### Section 2: Baseline OLS — Day-of-Week Dummies

**Specification:**
```
R_t = α + β₁Mon_t + β₂Tue_t + β₃Thu_t + β₄Fri_t + ε_t
```
- Wednesday omitted (standard — middle of week, "unremarkable")
- α = mean Wednesday return
- β₁ = Monday excess over Wednesday (should be negative)
- Run three times: full sample, pre-period, post-period
- **Newey-West HAC standard errors**

**Lag selection for Newey-West:**
Rule of thumb: `m = floor(0.75 × T^(1/3))`
- Full sample (T ≈ 3,200): m = 11
- Pre (T ≈ 1,200): m = 7
- Post (T ≈ 2,000): m = 9

**Alternative (report both):** No-intercept with all 5 day dummies, then F-test for equality:
```
R_t = γ₁Mon_t + γ₂Tue_t + γ₃Wed_t + γ₄Thu_t + γ₅Fri_t + ε_t
```
Each γᵢ directly estimates mean return on day i.

### Section 3: Effect Coding (Winkelried & Iberico 2018)

Replace standard dummies with effect-coded regressors: `D_i - 1/5`
```
R_t = μ + δ₁(Mon_t - 1/5) + δ₂(Tue_t - 1/5) + δ₃(Thu_t - 1/5) + δ₄(Fri_t - 1/5) + ε_t
```
- μ = grand mean across all 5 days (not Wednesday-specific)
- δ₁ = how much Monday deviates from the weekly average
- More interpretable than dummy coding
- Especially useful for interaction terms (Section 4) because main effects retain their ANOVA-sense interpretation

### Section 4: Structural Break / DiD

**Primary — Interaction model:**
```
R_t = α + β₁Mon_t + δ·Post_t + γ(Mon_t × Post_t) + ε_t
```
- γ = change in Monday effect after 2017 ← **your key coefficient**
- Newey-West HAC SEs

**Full specification (all days):**
```
R_t = α + Σβᵢ·Dᵢ + δ·Post + Σγᵢ·(Dᵢ × Post) + ε_t
```
- γᵢ for each day shows how that day's effect changed

**Supplementary — Chow test:**
- F-test comparing pooled vs separate pre/post regressions
- Use heteroskedasticity-robust version (daily returns violate homoskedasticity)

**Robustness — Unknown break date:**
- Quandt-Andrews supremum test: compute Wald stats at every candidate breakpoint, see if the max falls near 2017
- If the data-identified break is near 2017, it strengthens your narrative
- Python: `statsmodels` has limited support; may need `ruptures` package or manual implementation

### Section 5: Rolling Window

**Window**: 252 trading days (≈ 1 year) — standard for daily data
- Each window contains ~50 Mondays, sufficient for estimation
- Robustness: repeat with 504-day window

**Procedure:**
1. For each date t (from t=253 to T), estimate DOW regression on [t-252, t-1]
2. Extract Monday coefficient β_Mon(t) and its SE
3. 95% CI: β_Mon(t) ± 1.96 × SE(t)
4. Plot as time series with shaded confidence band
5. Vertical dashed line at Jan 2017
6. Horizontal line at zero

**Step size**: Every trading day (step=1) for smooth plot. Step=5 if computational cost matters.

### Section 6: GARCH

**Key methodological point from the literature**: Day-of-week dummies should go in **both** the mean and variance equations (Berument & Kiymaz 2001, Kiymaz & Berument 2003).

**Primary — GARCH(1,1) with day dummies in mean + variance:**
```
Mean:     R_t = γ₁Mon + γ₂Tue + γ₃Wed + γ₄Thu + γ₅Fri + ε_t
Variance: σ²_t = ω₁Mon + ω₂Tue + ω₃Wed + ω₄Thu + ω₅Fri + α·ε²_{t-1} + β·σ²_{t-1}
```
- No intercept, all 5 dummies (no-intercept approach)
- **Student-t distribution** (not normal) — daily returns have fat tails; report estimated df
- Estimate separately for pre and post periods

**Robustness — GJR-GARCH (handles leverage effect):**
```
σ²_t = ω + (α + γ·I_{t-1})·ε²_{t-1} + β·σ²_{t-1}
```
where I_{t-1} = 1 if ε_{t-1} < 0. Tests asymmetric volatility (negative shocks → higher volatility).

The Indonesia GJR-GARCH study (Emerald 2024) found the Monday effect only in the Islamic index (JII), not in JCI. This is worth discussing.

**Python `arch` package:**
```python
from arch import arch_model
am = arch_model(returns, mean='ARX', vol='GARCH', p=1, q=1, dist='t')
# For GJR: vol='GARCH', p=1, o=1, q=1
```
Note: Day dummies in the variance equation require manual setup with `arch`. The `ConstantVariance` model won't work — you need to specify the variance regressors.

### Section 7: Stock-Level Panel

**Specification:**
```
R_{i,t} = αᵢ + β₁Mon_t + β₂Tue_t + β₃Thu_t + β₄Fri_t + δ·Post_t + γ(Mon_t × Post_t) + ε_{i,t}
```
- αᵢ = stock fixed effects (controls for unobserved stock characteristics)
- Use Excess_Return as DV (controls for risk-free rate)
- Do NOT include time fixed effects — they would absorb the day-of-week dummies

**Standard errors — Two-way clustering (stock + date):**
Following Petersen (2009) and Cameron, Gelbach & Miller (2011):
- Cluster by stock: corrects within-stock autocorrelation
- Cluster by date: corrects cross-sectional dependence (stocks move together)
- Two-way: corrects both — most conservative, recommended

In `linearmodels`:
```python
from linearmodels.panel import PanelOLS
mod = PanelOLS(y, X, entity_effects=True)
result = mod.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)
```

**Robustness — Balanced panel:**
Run on the 525 stocks present in both periods to rule out composition effects (new IPOs in post-period are smaller/more speculative).

**Why NOT Fama-MacBeth here:**
On any given date, all stocks share the same day-of-week. There's no within-day cross-sectional variation in the Monday dummy. Fama-MacBeth would only work for cross-sectional sorting exercises (e.g., testing Birru-style speculative vs safe interactions), not for estimating the aggregate Monday coefficient.

---

## Indonesia-Specific Considerations

### Friday Trading Hours
- Mon–Thu: 9:00–12:00, 1:30–3:49 (total: ~5.3 hours)
- Friday: 9:00–11:30, 2:00–3:49 (total: ~4.3 hours) — shorter for Friday prayers
- Post-COVID (2020): simplified to continuous 9:00–15:00

**Implication**: Friday has ~20% fewer trading hours. This is a confound — lower Friday returns could be mechanical (less trading time), not sentiment. Address in methodology section: note that the Monday effect is measured relative to other days, so this affects interpretation of Friday specifically, not Monday.

### T+2 Settlement Change (26 November 2018)
- Before: T+3 settlement
- After: T+2 settlement
- This is within your post-period and could affect day-of-week patterns (settlement risk changes)
- **Consider**: Adding a T+2 dummy or noting it as a within-post-period event

### Existing Indonesia Findings (Key Literature)
| Study | Period | Method | Monday Effect? |
|-------|--------|--------|----------------|
| Khan et al. (2023) | 2013–2019 | OLS, GARCH(1,1), Kruskal-Wallis | Yes |
| Suryanegara et al. (2024) | 2017–2022 | ANOVA | **No** |
| Emerald (2024) | 2000–2022 | GJR-GARCH | Only in Islamic index |
| ResearchGate | Various | OLS + EGARCH | Yes (individual stocks) |
| LQ45 COVID study | COVID era | OLS | No |

**The Indonesia Monday effect is contested.** This supports your thesis — if some recent studies find it gone, your pre/post comparison can help explain when and why it disappeared.

### Investor Growth (KSEI data)
- 2012: ~281,000 investors
- 2016: 894,116
- 2017: crossed 1 million
- 2020: ~3.1 million
- 2023: 7 million+
- 2024: ~10 million (60% aged 18–35)

This is your identification strategy — the scale of demographic shift is massive.

---

## Data Preprocessing Before Analysis

### Winsorizing
- 94 obs with |r| > 50%, 489 with |r| > 30%
- **Winsorize at 1st/99th percentile** before all regressions
- Report sensitivity to 0.5th/99.5th and 2.5th/97.5th as robustness

### 2025 Partial Year
- Your data goes to Dec 2025 but 2025 has high mean return (+0.19%/day)
- **Exclude 2025** from the main analysis. Post-period = 2017-01 to 2024-12.

### Returns
- Stock returns are log returns: ln(P_t/P_{t-1})
- JCI Market_Return — verify if log or simple returns (matters for aggregation)
- For aggregate JCI analysis, use JCI Market_Return directly
- For panel, use Stock_Return or Excess_Return

---

## Harvey's Multiple Testing Framework

### Harvey, Liu, and Zhu (2016) "...and the Cross-Section of Expected Returns" RFS
- Cataloged **316 factors** in the literature; argues the t > 2.0 threshold is far too lenient
- Recommends **t > 3.0** for newly discovered factors (p ≈ 0.0027)
- Three correction methods applied at 316 factors:
  - **Bonferroni**: t > 4.01 (controls family-wise error rate)
  - **Holm**: t > 3.96
  - **BHY (Benjamini-Hochberg-Yekutieli)**: t > 2.78–3.68 (controls false discovery rate)
- Estimate: **158 of 296 published significant factors are false discoveries** (>50%)

### Harvey (2017) JF Presidential Address
- Proposes **Minimum Bayes Factor**: MBF = −e × p × ln(p) where p is the p-value
- Posterior odds = Prior odds × MBF
- At p = 0.05 with 50/50 priors: posterior probability null is true ≈ 26–29% (NOT 5%)
- Key point: t > 3 is "necessary but not sufficient" — depends on prior plausibility
- Recommendation: report MBF alongside p-values

### Harvey and Liu (2020) "False (and Missed) Discoveries" JF
- Double-bootstrap method calibrating both Type I and Type II errors
- Optimal threshold lies **between 2.0 and 3.0** (not rigidly 3.0)
- The right threshold depends on relative costs of false vs missed discoveries

### Sullivan, Timmermann, and White (2001) "Dangers of Data Mining: Calendar Effects"
- **Most relevant paper for the data-snooping critique of calendar anomalies**
- Tests universe of **9,452 calendar trading rules** on ~100 years of DJIA data
- Individual calendar effects (including Monday) are highly significant with nominal p-values
- BUT after White's Reality Check bootstrap (adjusting for the full search): **calendar effects no longer significant**
- Out-of-sample: best rule from pre-1986 fails post-1987
- **Defense for Adrian's thesis**: (a) testing a pre-specified hypothesis, not searching 9,452 rules; (b) Indonesia is a fresh sample, not used in original discovery; (c) clear economic rationale (mobile trading) for the structural break date

### Implications for Your Thesis
1. Your aggregate Monday t-stats are strong (t ≈ −10 stock-level pooled) — well above even Harvey's t > 3 threshold
2. When testing across multiple specifications/periods, acknowledge multiple testing; consider BHY FDR correction
3. Report the MBF: for your key results, compute MBF = −e × p × ln(p)
4. Defend against Sullivan et al.: pre-specified hypothesis on a fresh market with economic rationale
5. The Monday effect's **disappearance** in developed markets (Robins & Smith 2016: gone in US since 1975; Plastun et al. 2019: "golden age" was mid-20th century) actually raises the prior that it may also be disappearing in Indonesia — supporting your thesis

---

## Birru (2018) — Exact Econometric Specifications

Detailed specifications saved separately at: `papers/birru_econometric_specifications.md`

### Key Details Extracted from Paper
1. **Day-specific monthly returns**: Simple arithmetic SUM of all Monday daily L-S returns within each month (not averaged, not compounded)
2. **Standard errors**: Newey-West HAC; exact lag not specified, standard practice ≈ 6–8 for ~600 monthly obs
3. **Factor regressions use standard monthly factors** (not day-decomposed) as primary; day-decomposed factors as robustness (Table 6)
4. **Holiday analysis (Table 16)**: Simple averages (not regressions) — 56/57 combos go in predicted direction
5. **Subsample analysis (Table 7)**: Separate re-estimation in 3 subperiods (not interaction terms)
6. **Liquidity controls (Table 13)**: Daily regression with DOW dummies + Carhart factors + ΔVolume + ΔLiquidity; Friday omitted
7. **44 non-speculative anomalies** show NO Monday/Friday pattern — confirms it's specific to speculative vs safe distinction

### Indonesian Adaptation (Without FF Factors)
Three risk-adjustment approaches (report all):
1. **Excess returns**: R_LS − R_f (always report)
2. **Market-adjusted**: R_LS − R_JCI (primary; equivalent to CAPM with β=1)
3. **CAPM alpha**: Regress R^d_LS on R^d_JCI (regression-based)

Birru's own Table 2 shows results barely change across risk adjustments — the L-S portfolio is roughly market-neutral, so factor loadings are small.

---

## Summary: What to Implement

### Part A: Aggregate Analysis (JCI Index)

| # | Section | Model | SEs | Key Output |
|---|---------|-------|-----|------------|
| 1 | Descriptives | Summary stats + Kruskal-Wallis | — | Day-of-week return table, pre vs post |
| 2 | Baseline OLS | Dummies (Wed omitted) | Newey-West HAC | Monday β in full/pre/post |
| 3 | Effect coding | Deviation from grand mean | Newey-West HAC | Monday δ in full/pre/post |
| 4 | Structural break | Mon × Post interaction | Newey-West HAC | γ coefficient + Chow test |
| 5 | Rolling window | 252-day rolling OLS | Per-window | Time-varying Monday β plot |
| 6 | GARCH(1,1) | Dummies in mean + variance | Student-t MLE | Monday γ in mean, pre/post |

### Part B: Cross-Sectional Analysis (Birru-Inspired)

| # | Section | Model | SEs | Key Output |
|---|---------|-------|-----|------------|
| 7 | Portfolio sorts | Quintile sorts → day-specific monthly L-S | Newey-West HAC | Monday vs Friday L-S alphas |
| 8 | Panel FE | Stock FE + Mon × Spec interaction | Two-way clustered | Speculative-Monday β |
| 9 | Triple interaction | Mon × Spec × Post | Two-way clustered | Did mobile trading change speculative-Monday effect? |

### Part C: Stock-Level Aggregate Panel

| # | Section | Model | SEs | Key Output |
|---|---------|-------|-----|------------|
| 10 | Panel DOW | Stock FE + DOW dummies + Post | Two-way clustered | Monday β at stock level |
| 11 | Balanced panel | Same, 525 stocks in both periods | Two-way clustered | Rules out composition effects |

### Part D: Summary

| # | Section | Key Output |
|---|---------|------------|
| 12 | Summary table | All Monday coefficients side-by-side across models/periods |
| 13 | MBF reporting | Minimum Bayes Factor for key results per Harvey (2017) |

### Robustness Tests
1. GJR-GARCH (leverage effect)
2. Quandt-Andrews unknown breakpoint test (following Robins & Smith 2016)
3. 504-day rolling window
4. Balanced panel (525 stocks in both periods)
5. Winsorization sensitivity (0.5/99.5, 1/99, 2.5/97.5 percentiles)
6. Kruskal-Wallis nonparametric test
7. Exclude 2025 from analysis
8. Multiple testing: BHY FDR correction across specifications
9. Effect coding (Winkelried & Iberico 2018)

---

## Key References

### Foundational DOW Effect
- French (1980) — "Stock Returns and the Weekend Effect" JFE
- Gibbons & Hess (1981) — "Day of the Week Effects on Stock Returns" JFQA
- Connolly (1989) — "An Examination of the Robustness of the Weekend Effect" JFQA

### GARCH for DOW
- Berument & Kiymaz (2001) — "The Day of the Week Effect on Stock Market Volatility" J Econ & Finance
- Kiymaz & Berument (2003) — "The Day of the Week Effect on Volatility and Volume" Rev Fin Econ

### Methodology
- Winkelried & Iberico (2018) — "Calendar Effects in Latin American Stock Markets" Empirical Economics
- Petersen (2009) — "Estimating Standard Errors in Finance Panel Data Sets" RFS
- Cameron, Gelbach & Miller (2011) — "Robust Inference with Multiway Clustering" JBES
- Newey & West (1987) — "A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix" Econometrica

### Multiple Testing / Data Snooping
- Harvey, Liu & Zhu (2016) — "...and the Cross-Section of Expected Returns" RFS
- Harvey (2017) — "The Scientific Outlook in Financial Economics" JF (presidential address)
- Harvey & Liu (2020) — "False (and Missed) Discoveries in Financial Economics" JF
- Sullivan, Timmermann & White (2001) — "Dangers of Data Mining: Calendar Effects" J Econometrics
- Hansen & Lunde (2003) — "Testing the Significance of Calendar Effects" (working paper)

### Structural Breaks
- Andrews (1993) — "Tests for Parameter Instability and Structural Change with Unknown Change Point" Econometrica
- Bai & Perron (2003) — "Computation and Analysis of Multiple Structural Change Models" J Applied Econometrics

### Anomaly Disappearance
- Robins & Smith (2016) — "No More Weekend Effect" Critical Finance Review
- Birru (2018) — "Day of the Week and the Cross-Section of Returns" JFE
- Grebe & Schiereck (2024) — "Day-of-the-Week Effect: A Meta-Analysis" Eurasian Economic Review
- Plastun, Sibande, Gupta & Wohar (2019) — "Rise and Fall of Calendar Anomalies Over a Century" N Am J Econ & Finance

### Indonesia / Emerging Markets
- Khan et al. (2023) — "Day-of-the-week effect and market liquidity: Asia" Int J Finance & Econ
- Suryanegara et al. (2024) — "Monday effect on IDX before and during COVID-19" Diponegoro Int J Bus
- Choudhry (2000) — "Day of the Week Effect in Emerging Asian Stock Markets: GARCH" Applied Fin Econ
- Brooks & Persand (2001) — "Seasonality in Southeast Asian Stock Markets" Applied Fin Econ
- Chiah & Zhong (2019) — "Day-of-week effect in anomaly returns: International evidence" Economics Letters

### Adaptive Markets / Mobile Trading
- Lo (2004) — "The Adaptive Markets Hypothesis" J Portfolio Management
- Barber et al. — "Attention Induced Trading and Returns: Evidence from Robinhood Users"

### Sentiment
- Baker & Wurgler (2006) — "Investor Sentiment and the Cross-Section of Stock Returns" JF
- Baker & Wurgler (2007) — "Investor Sentiment in the Stock Market" JEP
- Golder & Macy (2011) — "Diurnal and Seasonal Mood Vary with Work, Sleep, and Daylength" Science
- Hirshleifer, Jiang & Zhang (2020) — "Mood Beta and Seasonalities in Stock Returns" JFE
