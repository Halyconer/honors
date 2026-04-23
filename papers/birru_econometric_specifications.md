# Birru (2018) — Exact Econometric Specifications
## "Day of the week and the cross-section of returns" JFE 130:182-214

This document extracts the precise econometric methodology from the published paper
and develops an Indonesian adaptation without Fama-French factors.

---

## 1. Portfolio Construction

### Sample
- **Source**: CRSP (returns), Compustat (accounting data)
- **Universe**: NYSE, Amex, Nasdaq common stocks, share code 10 or 11
- **Period**: July 1963 -- December 2013 (varies by anomaly; see below)

### Sorting
- **Breakpoints**: NYSE stocks only (excludes Amex/Nasdaq from breakpoint computation to avoid microcap distortion)
- **Number of portfolios**: Decile sorts (10 portfolios) for continuous variables; binary sorts for dummies (E, CF, D)
- **Weighting**: Value-weighted (market-cap-weighted) within each portfolio

### Rebalancing Frequency (from Appendix)
Rebalancing differs by anomaly type:

**Monthly rebalancing** (market-based / high-frequency variables):
- 52-Week high (52-Wk)
- Beta
- Bid-Ask spread
- Cash flow variance (CFV) -- starts July 1976
- Dispersion of opinion (Disp) -- starts Feb 1976 (when forecast data starts)
- Idiosyncratic volatility (Ivol)
- Illiquidity (Illiq)
- Max daily return (Max)

**Annual rebalancing at end of June** (accounting-based / annual variables):
- Age
- Asset growth (AG)
- Book-to-market (BM)
- Cash flow dummy (CF) -- uses fiscal year t-1
- Dividend dummy (D)
- Failure probability (FP) -- starts July 1976
- Net external financing (NXF) -- starts July 1972
- O-score
- Operating profitability (OP)
- Price
- Return on assets (ROA) -- starts July 1972

### Long-Short Portfolio
- **Long leg**: Decile 1 or 10 depending on anomaly (see Table 1 in paper)
- **Short leg**: Opposite decile
- **L-S return**: R_long - R_short (value-weighted within each decile)

---

## 2. Day-Specific Monthly Return Construction

This is the most critical methodological detail. Birru constructs "monthly returns from investing only on specified days."

### Construction Method: Summation of Daily Returns

From the paper (Section 4.4, p.193):
> "The current risk-adjusted results use the Fama-French monthly factors to risk-adjust the **monthly returns calculated for subsets of days**."

And from Table 6 caption:
> "Alphas are calculated using factors that are **decomposed into daily components**."

And from Table 15 caption:
> "For each anomaly, the long minus short portfolio return is **calculated for each day and then averaged across each day of the week for each month**."

**Procedure for Tables 2-7 (monthly time series)**:

For each calendar month m:
1. Identify all trading days in month m that fall on the target day-of-week (e.g., all Mondays)
2. For each such day t, compute the value-weighted portfolio return for the long leg and short leg
3. The "Monday monthly return" for the L-S portfolio = **sum of all Monday daily L-S returns within month m**

Formally:
```
R^{Mon}_{LS,m} = SUM over all Mondays t in month m of [R_{Long,t} - R_{Short,t}]
```

This is a **simple arithmetic sum** of daily returns (not geometric compounding), which is standard for short holding periods and small daily returns. The resulting series is a monthly time series of "Monday-only" L-S returns with one observation per calendar month.

**For daily return tables (Tables 15-16)**:

From Table 15 caption: "For each anomaly, the long minus short portfolio return is calculated for each day and then **averaged** across each day of the week for each month."

This means for the daily tables, the average daily return on (e.g.) Monday is:
```
r^{Mon}_{LS,m} = (1/N_Mon,m) * SUM over all Mondays t in month m of [R_{Long,t} - R_{Short,t}]
```
where N_Mon,m is the number of Mondays in month m (typically 4 or 5).

**Relationship between monthly and daily figures**:
```
R^{Mon}_{LS,m}  (monthly)  =  N_{Mon,m} * r^{Mon}_{LS,m}  (daily average * count)
```

Example verification: Ivol daily excess return on Monday = +22.6 bp/day. With ~4.3 Mondays per month on average, the monthly figure is approximately 4.3 * 22.6 = ~97 bp, close to the reported 91.6 bp excess return in Table 2 (slight difference from Mondays-per-month variation and weighting).

---

## 3. Factor Regression Specifications

### 3a. Excess Return (no regression needed)

The monthly "Monday-only" L-S return is simply:
```
R^{Mon}_{LS,m} - R_{f,m}^{Mon}
```
where R_f,m^{Mon} is the sum of daily risk-free rates on all Mondays in month m.

Actually, since CRSP returns are already excess returns (or the risk-free rate is subtracted day by day), the "excess return" column in Table 2 is:
```
ExRet^{Mon}_{LS,m} = SUM_{t in Mon(m)} [R_{Long,t} - R_{f,t}] - SUM_{t in Mon(m)} [R_{Short,t} - R_{f,t}]
```

### 3b. CAPM Alpha

Time-series regression (one per anomaly, one per day-of-week):
```
R^{d}_{LS,m} - R^{d}_{f,m} = alpha + beta * (R^{d}_{Mkt,m} - R^{d}_{f,m}) + epsilon_m
```
where:
- d = day of week (Mon, Fri, Tue-Thu)
- R^{d}_{LS,m} = monthly L-S portfolio return from investing only on day d
- R^{d}_{f,m} = monthly risk-free rate from day d (sum of daily rf on day d in month m)
- R^{d}_{Mkt,m} = monthly market return from day d (sum of daily market returns on day d in month m)
- alpha = the CAPM alpha (the reported coefficient)

**Primary specification (Tables 2-5, 7)**: Uses standard monthly Fama-French factors (not decomposed by day). The monthly factor return is matched to the monthly day-specific portfolio return.

**Alternative specification (Table 6)**: Decomposes the monthly factors into their day-specific components:
```
R^{Mon}_{LS,m} - R^{Mon}_{f,m} = alpha + beta * (R^{Mon}_{Mkt,m} - R^{Mon}_{f,m}) + epsilon_m
```
This addresses the concern that risk premiums could vary by day.

### 3c. Fama-French 3-Factor (FF3) Alpha

```
R^{d}_{LS,m} - R^{d}_{f,m} = alpha + beta_1 * MktRF_m + beta_2 * SMB_m + beta_3 * HML_m + epsilon_m
```

where MktRF_m, SMB_m, HML_m are the standard monthly Fama-French factors from Kenneth French's data library.

**Exception**: SMB is excluded when analyzing the size anomaly.

### 3d. Carhart 4-Factor Alpha

```
R^{d}_{LS,m} - R^{d}_{f,m} = alpha + beta_1 * MktRF_m + beta_2 * SMB_m + beta_3 * HML_m + beta_4 * UMD_m + epsilon_m
```

where UMD_m is the monthly momentum factor (Carhart, 1997).

**Exceptions**:
- SMB excluded for size anomaly
- MktRF excluded for beta-sorted portfolios (footnote 4, p.190)

### 3e. Day-Specific Factor Decomposition (Table 6)

For robustness, factors are decomposed into their Monday and Friday monthly components:
```
MktRF^{Mon}_m = SUM_{t in Mon(m)} MktRF_t    (using daily Fama-French factor returns)
SMB^{Mon}_m   = SUM_{t in Mon(m)} SMB_t
HML^{Mon}_m   = SUM_{t in Mon(m)} HML_t
UMD^{Mon}_m   = SUM_{t in Mon(m)} UMD_t
```

Then the regression becomes:
```
R^{Mon}_{LS,m} - R^{Mon}_{f,m} = alpha + b1*MktRF^{Mon}_m + b2*SMB^{Mon}_m + b3*HML^{Mon}_m + b4*UMD^{Mon}_m + epsilon_m
```

---

## 4. Standard Error Treatment

### HAC Standard Errors

All tables report "t-statistics adjusted for heteroskedasticity and autocorrelation" (exact wording from every table caption).

**The paper does not specify the exact Newey-West lag structure.**

The phrase "adjusted for heteroskedasticity and autocorrelation" is the standard way to describe Newey-West (1987) HAC standard errors in JFE papers.

**Standard practice for monthly time series** (which is what Birru has after summing daily returns within months):
- Common choices: Newey-West with lag = floor(0.75 * T^(1/3)) or lag = floor(4 * (T/100)^(2/9))
- For T approximately 606 months (July 1963 - Dec 2013): lag approximately 6 using the 0.75*T^(1/3) rule
- Many JFE papers of this era use Newey-West with a small number of lags (e.g., 6 or 12) for monthly data
- The exact choice is unreported, but results at t-stats of 4-10 would not be sensitive to reasonable lag choices

### For Daily Regressions (Table 13 — Liquidity Controls)

Table 13 runs daily regressions of speculative-leg returns on day-of-week dummies plus controls. For daily data over 50 years (approximately 12,600 observations), HAC standard errors are again used with wording "t-statistics adjusted for heteroskedasticity and autocorrelation."

---

## 5. Table 2 Structure

### What Is Reported
- **Rows**: 19 anomalies (16 where short leg is speculative, then 3 where long leg is speculative)
- **Column groups**: Monday L-S | Friday L-S | Tuesday-through-Thursday L-S
- **Within each group**: Excess return, CAPM alpha, FF3 alpha, Carhart alpha
- **Panel A**: Coefficient estimates (monthly L-S portfolio returns in percent)
- **Panel B**: HAC-adjusted t-statistics

### Key Reading
For each anomaly, the alpha (intercept) from the factor regression is the day-specific monthly L-S return after risk adjustment. So "Ivol Monday Carhart = 1.049" means:
- Sort stocks into decile portfolios on Ivol using NYSE breakpoints
- Compute the monthly return from investing only on Mondays in the L-S (low Ivol minus high Ivol) portfolio
- Regress this monthly Monday L-S return on the four Carhart factors
- The intercept (alpha) is 1.049% per month

---

## 6. Holiday Analysis (Table 16)

### What Is Tested
The mood hypothesis predicts that the day-of-week pattern reflects mood, not the ordinal day. Therefore:
- **Tuesdays after Monday holidays**: Should behave like Mondays (first workday after weekend + holiday)
- **Thursdays before Friday holidays**: Should behave like Fridays (last workday before long weekend)
- **Wednesday before Thanksgiving** (market closed Thu-Fri): Should behave like/exceed Friday

### Regression Specification
Table 16 reports **average daily excess returns** for the L-S portfolio on specific holiday-adjacent days:
```
For each anomaly, the long minus short portfolio return is calculated for each day and then averaged
```
This is NOT a regression — it is a simple average of daily L-S excess returns computed for:
1. All Tuesdays that immediately follow Monday holidays
2. All Thursdays that immediately precede Friday holidays
3. All Wednesdays that immediately precede Thanksgiving

The t-statistics are HAC-adjusted, testing whether the average holiday-adjacent return differs from zero.

### Results
- 56 of 57 anomaly-day combinations go in the predicted direction
- Holiday-Tuesday returns are larger than typical Tuesdays for 17/19 anomalies
- 12/19 anomalies have holiday-Tuesday magnitudes larger than average Monday
- All pre-Friday-holiday Thursday returns go in the predicted direction and exceed typical Fridays
- Pre-Thanksgiving Wednesday returns go in predicted direction for all 19 anomalies; 17/19 exceed typical Friday

---

## 7. Subsample Analysis (Table 7)

### Method: Separate Re-Estimation (Not Interaction Terms)

Birru splits the sample into three subperiods and **re-runs the full analysis separately** in each:

1. **July 1963 -- December 1974** (pre-Robins-Smith disappearance of aggregate weekend effect)
2. **January 1975 -- December 1994** (post-disappearance, pre-internet)
3. **January 1995 -- December 2013** (modern period)

For each subperiod, he reports Carhart 4-factor alphas for:
- Monday L-S returns
- Friday L-S returns
- Friday minus Monday L-S returns

**Note**: 5 anomalies with later data starts are excluded from the 1963-1974 subperiod (NXF, ROA start July 1972; Disp starts Feb 1976; CFV and FP start July 1976).

### Key Result
- 103 of 104 anomaly-period combinations go in the same direction as the full sample
- Only illiquidity Monday in 1963-1974 goes in the wrong direction
- Effect is robustly present in all subperiods

---

## 8. Additional Regressions

### 8a. Intraday vs Overnight Decomposition (Table 10)

**Period**: July 1992 -- December 2013 (CRSP open prices available from 1992)

**Return decomposition**:
```
Intraday_t = (Close_t - Open_t) / Open_t
Overnight_t = CRSP_return_t - Intraday_t
```
Dividend adjustments assumed to occur overnight.

**Finding**: ALL day-of-week variation occurs intraday, not overnight. No anomaly has a statistically significant Friday-Monday overnight difference even at 5%.

### 8b. Macroeconomic News Exclusion (Tables 8-9)

**Method**: Re-run the full analysis after excluding days with:
- CPI announcements
- PPI announcements
- Employment reports
- FOMC announcement days

Results unchanged.

### 8c. Firm-Specific News Exclusion (Tables 8-9)

**Method**: Re-run after excluding days surrounding:
- Earnings announcements
- M&A announcements
- Management forecasts

Results unchanged.

### 8d. Institutional Ownership (Table 11)

**Method**: Each quarter, split stocks into low vs high institutional ownership (relative to median). Institutional ownership = aggregate shares owned by institutions / total shares outstanding.

Separately run the full Monday/Friday factor regressions for:
- Low institutional ownership stocks only
- High institutional ownership stocks only

**Finding**: Effect present in both groups; larger for low institutional ownership (consistent with retail-driven sentiment).

### 8e. Saturday Trading Period (Table 12)

**Period**: January 1927 -- September 1952 (markets open Saturdays)

Tests whether the Friday pattern persists when Friday is NOT the last trading day of the week. If the effect were driven by end-of-week rebalancing, it should not appear on Fridays during this period.

**Finding**: Friday-Monday differences still go in the expected direction, often with larger magnitudes.

### 8f. Liquidity Controls (Table 13)

**Specification** (daily regression, not monthly):
```
R_{speculative,t} = b_Mon * Mon_t + b_Tue * Tue_t + b_Wed * Wed_t + b_Thu * Thu_t
                    + c_1 * MktRF_t + c_2 * SMB_t + c_3 * HML_t + c_4 * UMD_t
                    + c_5 * Delta_Volume_t + c_6 * Delta_Liquidity_t
                    + epsilon_t
```

where:
- Friday is the omitted day (so Monday coefficient measures Monday minus Friday difference)
- R_{speculative,t} = daily return of the speculative leg of each anomaly
- MktRF_t, SMB_t, HML_t, UMD_t = daily Fama-French-Carhart factors
- Delta_Volume_t = daily change in value-weighted market volume (NYSE stocks, demeaned by calendar year)
- Delta_Liquidity_t = daily change in value-weighted market liquidity (NYSE stocks, demeaned by calendar year; following Chordia et al. 2001)

**Finding**: Monday coefficients remain negative and significant at 1% for nearly all anomalies, with 52-Wk the only exception.

### 8g. VIX and Treasury Regressions (Table 14)

**VIX regression (Panel C)**:
```
VIX_t = b_Mon * Mon_t + b_Tue * Tue_t + b_Thu * Thu_t + b_Fri * Fri_t
        + c_1 * Macro_t + c_2 * VIX_{t-1:t-5} + c_3 * VIX^2_{t-1:t-5}
        + [YearMonth FE]  + epsilon_t
```

**Treasury regression (Panel C)**:
```
Treasury_t = b_Mon * Mon_t + b_Tue * Tue_t + b_Thu * Thu_t + b_Fri * Fri_t
             + c_1 * Macro_t + c_2 * Treasury_{t-1:t-5} + c_3 * Treasury^2_{t-1:t-5}
             + [YearMonth FE] + epsilon_t
```

where:
- Wednesday is the omitted day
- Macro_t = dummy for CPI, PPI, employment, FOMC announcement days
- Lagged terms use returns from t-1 to t-5 (one week of lagged returns)
- Year-month fixed effects included in some specifications

### 8h. 44 Other Anomalies Without Clear Speculative Leg (Section 5.5)

Birru also tests 44 additional anomalies (momentum, B/M, accruals, earnings surprise, etc.) that do NOT have a clear speculative vs safe leg. The Monday/Friday pattern does NOT exist for these anomalies, confirming it is specific to the speculative/non-speculative distinction.

---

## 9. Indonesian Adaptation Without Fama-French Factors

### The Problem
- No established Indonesian Fama-French factors (SMB, HML, UMD) exist
- Cannot replicate Birru's factor regression approach directly
- Need substitute methods for risk adjustment

### 9a. Substitute Approach 1: Market-Adjusted Returns

**Instead of Carhart alpha, use market-adjusted returns**:
```
R^{adj}_{LS,m,d} = R^{d}_{LS,m} - R^{d}_{Mkt,m}
```

This is equivalent to a CAPM alpha with beta constrained to 1. For the L-S portfolio (which is approximately market-neutral), the market adjustment is minor. The excess return and market-adjusted return columns will be very similar.

**Justification**: Birru's own Table 2 shows that results are qualitatively identical across all four risk adjustments (excess, CAPM, FF3, Carhart). The alpha values barely change from excess return to Carhart alpha. This is because the L-S portfolio is roughly market-neutral by construction, and factor loadings are small for the long-short spread.

### 9b. Substitute Approach 2: CAPM Alpha Using JCI

```
R^{d}_{LS,m} - R^{d}_{f,m} = alpha + beta * (R^{d}_{JCI,m} - R^{d}_{f,m}) + epsilon_m
```

where R^{d}_{JCI,m} is the JCI (Jakarta Composite Index) return from investing only on day d in month m, and R^{d}_{f,m} is the sum of daily risk-free rates (Bank Indonesia overnight rate / 252) on day d in month m.

**This is the cleanest adaptation**: single-factor model using the local market index.

### 9c. Substitute Approach 3: Construct Local Factors

If you have enough cross-sectional data, you can construct Indonesian SMB and HML factors:
- **SMB**: Sort IDX stocks by market cap at end of June; top 50% = Big, bottom 50% = Small; SMB = R_Small - R_Big
- **HML**: Sort by book-to-market (requires fundamental data); top 30% = Value, bottom 30% = Growth; HML = R_Value - R_Growth
- Use 2x3 independent sorts (standard Fama-French methodology)

**Caveat**: With ~800 IDX stocks (fewer with complete data), the factors will be noisy. The 2x3 sorts produce 6 portfolios, each with ~130 stocks at best. This is feasible but less reliable than US factors.

### 9d. Recommendation for Adrian's Thesis

**Report all three for robustness**:
1. Excess returns (R_LS - R_f) -- always report
2. Market-adjusted returns (R_LS - R_Mkt) -- primary risk-adjusted measure
3. CAPM alpha (regression-based) -- secondary

The key results should be robust across all three. If they are not, that itself is informative.

---

## 10. Panel Interaction Approach: Monday x Speculative

### Why a Panel Approach
Birru runs separate portfolio sorts + time-series regressions for each anomaly. With Indonesian data, you may have:
- Fewer stocks per decile (especially for fundamental variables)
- No Fama-French factors
- Interest in a formal test of the Monday x Speculative interaction

A panel regression provides a single unified test.

### Specification

**Core panel regression**:
```
R_{i,t} = alpha_i + beta_1 * Mon_t + beta_2 * Spec_i,t + beta_3 * (Mon_t x Spec_i,t) + Controls + epsilon_{i,t}
```

where:
- R_{i,t} = daily excess return of stock i on day t
- alpha_i = stock fixed effect
- Mon_t = dummy = 1 if day t is Monday
- Spec_i,t = speculative characteristic (continuous or dummy)
- beta_3 = the key coefficient: does the Monday effect differ for speculative vs safe stocks?

### Extended Specification with Pre/Post

```
R_{i,t} = alpha_i + beta_1 * Mon_t + beta_2 * Spec_{i,t} + beta_3 * Post_t
         + beta_4 * (Mon_t x Spec_{i,t})
         + beta_5 * (Mon_t x Post_t)
         + beta_6 * (Spec_{i,t} x Post_t)
         + beta_7 * (Mon_t x Spec_{i,t} x Post_t)
         + Controls + epsilon_{i,t}
```

**Key coefficients**:
- beta_4: Monday effect differential for speculative stocks (full sample)
- beta_5: Change in Monday effect post-2017 (all stocks)
- beta_7: **Triple interaction** -- did the speculative-stock Monday effect change post-2017?

### Speculative Characteristic Options

Measurable from IDX data:
1. **Idiosyncratic volatility** (Ivol): Std dev of residuals from CAPM over past 60 trading days
2. **Price** (Price): Stock price level -- low-price stocks are speculative
3. **Size** (Size): Market capitalization -- small stocks are speculative
4. **Beta** (Beta): Market beta -- high-beta stocks are speculative
5. **Max** (Max): Maximum daily return in past month -- high Max stocks are speculative
6. **Bid-Ask** (Bid-Ask): Bid-ask spread proxy from Corwin-Schultz (2012) using daily high-low prices
7. **Age** (Age): Months since first appearance on IDX
8. **Illiquidity** (Illiq): Amihud (2002) illiquidity ratio
9. **52-Week high** (52-Wk): Current price / 52-week high
10. **Dividend payer** (D): Dummy for dividend payers vs non-payers
11. **ROA** (if fundamental data available)

### Operationalization

**Approach A -- Continuous interaction** (preferred):
```
Spec_{i,t} = percentile rank of stock i on characteristic (scaled 0 to 1)
```
This avoids arbitrary cutoffs and uses all cross-sectional variation.

**Approach B -- Quintile dummies** (easier interpretation):
```
Spec_{i,t} = dummy for top quintile (most speculative)
Safe_{i,t} = dummy for bottom quintile (least speculative)
```
Then compare Monday coefficients across quintiles.

**Approach C -- Birru-style portfolio sorts** (closest to original):
Form decile portfolios on each characteristic; compute daily L-S portfolio returns; aggregate to Monday-monthly returns; regress on market factor. Requires enough stocks per decile.

### Standard Errors for Panel

Two-way clustering by stock and date, following Petersen (2009):
```python
from linearmodels.panel import PanelOLS
mod = PanelOLS(y, X, entity_effects=True)
result = mod.fit(cov_type='clustered', cluster_entity=True, cluster_time=True)
```

**DO NOT use time fixed effects** -- they absorb the Monday dummy.

---

## 11. Complete Equation Summary

### Birru's Approach (US)

**Step 1**: Form decile portfolios (VW, NYSE breakpoints, rebalanced monthly or annually)

**Step 2**: For each day-of-week d and month m:
```
R^d_{LS,m} = SUM_{t in d(m)} [R_{Long,t} - R_{Short,t}]
```

**Step 3**: Time-series regression (T approximately 600 months):
```
R^d_{LS,m} - R^d_{f,m} = alpha^d + b1*MktRF_m + b2*SMB_m + b3*HML_m + b4*UMD_m + epsilon_m
```
Report alpha^d for d = {Mon, Fri, Tue-Thu}

**Step 4**: Test alpha^{Mon} vs alpha^{Fri} (Friday-minus-Monday difference)

### Indonesian Adaptation

**Approach 1 -- Portfolio sorts with CAPM**:

Step 1: Form quintile portfolios (VW or EW, rebalanced monthly) on available characteristics
Step 2: Compute R^d_{LS,m} as above
Step 3: Regress:
```
R^d_{LS,m} - R^d_{f,m} = alpha^d + beta * (R^d_{JCI,m} - R^d_{f,m}) + epsilon_m
```

**Approach 2 -- Panel interaction**:
```
R_{i,t} - R_{f,t} = alpha_i + b1*Mon_t + b2*Tue_t + b3*Thu_t + b4*Fri_t
                    + b5*Post_t
                    + g1*(Mon_t x Post_t) + g2*(Tue_t x Post_t) + g3*(Thu_t x Post_t) + g4*(Fri_t x Post_t)
                    + d1*Spec_{i,t} + d2*(Spec_{i,t} x Mon_t) + d3*(Spec_{i,t} x Post_t)
                    + d4*(Spec_{i,t} x Mon_t x Post_t)
                    + epsilon_{i,t}
```

Key coefficients:
- g1: Change in aggregate Monday effect post-2017
- d2: Speculative stocks' extra Monday effect (Birru channel)
- d4: Did mobile trading change the speculative-Monday effect?

Standard errors: Two-way clustered (stock + date)

---

## Sources

- [Birru 2018 full text (PDF)](https://english.ckgsb.edu.cn/sites/default/files/files/Day%20of%20the%20Week%20and%20the%20Cross-Section%20of%20Returns%20-%20Birru.pdf)
- [Birru 2018 SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2715063)
- [Birru 2018 ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301570)
- [Internet Appendix (Dropbox)](https://www.dropbox.com/s/lcnli8mcpdzoc2c/Birru_app.pdf?dl=0)
- [Alpha Architect summary](https://alphaarchitect.com/how-the-day-of-the-week-affects-stock-market-anomalies/)
- [Chiah & Zhong 2019 International Extension](https://www.sciencedirect.com/science/article/abs/pii/S0165176519302010)
- [Hirshleifer, Jiang & Zhang 2020 Mood Betas](https://www.sciencedirect.com/science/article/abs/pii/S0304405X20300362)
