# Maths Manual

**Last Updated:** 2026-04-23 EST

This document provides the exhaustive econometric specifications for the thesis, derived from the core literature (Birru 2018; French 1980; Newey–West 1987; Gibbons–Ross–Shanken 1989; Chow 1960; Bai–Perron 1998, 2003). Every derivation is written so a reviewer can trace each equality back to an explicit assumption.

---

## Step 1: Data Pre-Processing & Quality Filters

### 1.1 The "15-Day Rule"

A stock-month $(i, m)$ enters the panel only if $N_{\text{trading},i,m} \geq 15$.

**Formal justification.** Let $\hat{\sigma}_{i,m}^2 = \frac{1}{N-1}\sum_{t=1}^{N}(r_{i,t} - \bar{r}_i)^2$ be the sample variance used to build both $\text{IVOL}$ and $\text{MAX}$. The standard error of $\hat{\sigma}_{i,m}^2$ scales as $\sigma^2\sqrt{2/(N-1)}$ under normality. At $N=5$, the standard error is $\sim 71\%$ of the parameter; at $N=15$ it falls to $\sim 38\%$; at $N=22$ (full month) to $\sim 31\%$. The 15-day threshold is the knee of this curve — the inflection point past which adding more days yields diminishing precision, and the same threshold Birru (2018) adopts for CRSP.

### 1.2 Winsorization (1%/99% Knot)

Let $P_{1}$ and $P_{99}$ denote the 1st and 99th percentiles of the *pooled* daily return distribution across all stocks and all days. Define:
$$r_{i,t}^{\text{winsor}} = \max\!\big(P_{1}, \min(P_{99}, r_{i,t})\big)$$

**Why pooled, not per-stock.** A per-stock winsorisation would attenuate exactly the cross-sectional dispersion we want to study (the speculative leg's tails *are* the signal). Pooled winsorisation clips only *systemically* extreme observations — IDX limit-up/limit-down cascades and listing-day print artefacts.

**Why 1%/99% and not 5%/95%.** At the 5% cut we would truncate roughly 200,000 observations on a $\sim 2$M observation panel; the resulting distribution becomes approximately Gaussian, which is convenient but destroys the leptokurtosis that the Monday mood-reversal theory predicts. At 1%/99% we retain the fat-tailed structure while neutralising about 20,000 "limit-hit" outliers. We report 0.5/99.5 and 2.5/97.5 as robustness per Harvey & Liu (2020).

### 1.3 Liquidity Proxy: Zero-Return Proportion (ZR)

Following Bekaert, Harvey & Lundblad (2005):
$$\text{ZR}_{i,m} = \frac{\#\{t \in m : r_{i,t} = 0\}}{N_{\text{trading},i,m}}$$

**Interpretation.** Under a frictionless Walrasian market, $\Pr(r_{i,t} = 0) \approx 0$ because public-information arrival is continuous. A positive $\text{ZR}$ therefore measures the *absence* of trading rather than the absence of news — precisely the friction Bekaert et al. argue drives illiquidity premia in emerging markets.

**IDX baseline.** Empirical $\overline{\text{ZR}}_{\text{IDX}} \approx 0.640$ in our sample — higher than any developed market and a direct consequence of the $\sim 800$ listed tickers sharing thin dealer capacity.

---

## Step 2: Characteristic Construction & Timing

### 2.1 The "Birru Lag"

Define the measurement operator $\mathcal{C}_{i, M-1}$ as any function of prices, volumes, or fundamentals *realised* strictly before the opening of month $M$. The portfolio assignment function $\pi$ is:
$$\pi_{i, M} = \pi\!\big(\mathcal{C}_{i, M-1}\big)$$
and the observed portfolio return is:
$$R_{p,t \in M} \;=\; \sum_{i : \pi_{i, M} = p} w_{i, M-1}\, r_{i,t}$$
with $w_{i, M-1}$ known at time $M{-}1$.

**Look-ahead test.** For any forecasting claim to be legitimate, we require $\mathbb{E}[R_{p,t}\,|\,\mathcal{F}_{M-1}] \neq \mathbb{E}[R_{p,t}]$ while $w_{i, M-1}, \pi_{i, M} \in \mathcal{F}_{M-1}$. If any component of $\mathcal{C}_{i, M-1}$ were to leak into month $M$ — e.g., using end-of-month fundamentals released *during* $M$ — the regression alphas would be contaminated by in-sample fit.

### 2.2 Rebalancing Frequency

Market-sensitive characteristics ($\text{IVOL}$, $\text{MAX}$, $\text{Price}$) are re-sorted each month-end. Accounting-based characteristics ($\text{BM}$, $\text{ROA}$, $\text{Size}$) are re-sorted every July using the previous December's fiscal year-end data — the Fama–French (1993) six-month disclosure-lag convention. Indonesia's OJK mandates annual statement filing within four months of fiscal year-end, so a July rebalance gives a comfortable one-month buffer beyond the disclosure deadline.

---

## Step 3: Portfolio Aggregation & Weighting

### 3.1 Value-Weighting Derivation

Start from the definition of a portfolio return as a weighted mean of constituent returns:
$$R_{p,t} = \sum_{i \in p} w_{i,t} \, r_{i,t}, \qquad \sum_{i \in p} w_{i,t} = 1$$

Under value-weighting, weights are proportional to lagged market capitalisation:
$$w_{i,t} = \frac{\text{MCap}_{i, M-1}}{\sum_{j \in p} \text{MCap}_{j, M-1}}$$

**Why not equal-weighting.** Fama & French (1993) and Hou, Xue & Zhang (2020) show EW portfolios of microcaps dominate anomaly strength in US data — because EW assigns a $1.0\%$ weight to both a $\$10$bn firm and a $\$5$m firm. On the IDX the problem is worse: the bottom quintile by MCap has a median trading value of $<\!\$10,000$/day, so EW makes the portfolio *un-implementable*. VW ensures each reported alpha is economically investible.

### 3.2 2×3 Sorts vs. Quintiles

Fama & French (1993) use $2 \times 3$ sorts precisely because independent bivariate sorts minimise the covariance between the two resulting long-short factors. Formally, if $f_1 = r_{B,1} - r_{S,1}$ and $f_2 = r_{B,2} - r_{S,2}$ are independently constructed, and the sort variables are orthogonal in the cross-section, then $\text{Cov}(f_1, f_2) \to 0$. Our primary design uses quintiles for clarity and $2 \times 3$ as a Fama–French benchmark robustness.

### 3.3 Variance Decomposition and Diversification

The value-weighted portfolio return inherits a variance structure that justifies treating each monthly portfolio observation as informationally dense — the core reason time-series inference on $\sim 150$ monthly observations is adequate.

Assume the single-index (Sharpe, 1963) decomposition for each stock $i$:
$$r_{i,t} = \alpha_i + \beta_i F_t + \varepsilon_{i,t}$$
with the two defining assumptions of idiosyncratic risk:
$$\text{Cov}(\varepsilon_i, F) = 0 \quad \text{and} \quad \text{Cov}(\varepsilon_i, \varepsilon_j) = 0 \; \text{for } i \neq j$$

For an equal-weighted portfolio of $n$ stocks, the return is:
$$r_p = \bar{\alpha} + \bar{\beta} F + \frac{1}{n}\sum_{i=1}^n \varepsilon_i$$

Expanding the idiosyncratic variance term step by step (assuming homogeneous $\text{Var}(\varepsilon_i) = \sigma^2_\varepsilon$):
$$\text{Var}\!\left[\frac{1}{n}\sum_i \varepsilon_i\right] = \frac{1}{n^2}\sum_i\sum_j \text{Cov}(\varepsilon_i, \varepsilon_j) = \frac{1}{n^2}\sum_i \text{Var}(\varepsilon_i) = \frac{1}{n^2} \cdot n\sigma^2_\varepsilon = \frac{\sigma^2_\varepsilon}{n}$$

The double sum collapses because all $i \neq j$ cross-terms are zero by assumption. The full portfolio variance is therefore:
$$\sigma^2_p = \underbrace{\bar{\beta}^2 \sigma^2_F}_{\text{systematic}} + \underbrace{\frac{\sigma^2_\varepsilon}{n}}_{\text{idiosyncratic}}$$

As $n \to \infty$, the idiosyncratic term vanishes. Only unavoidable systematic exposure survives.

For the value-weighted portfolios used in this study, the generalisation is:
$$\sigma^2_p = \underbrace{\bar{\beta}_w^2 \sigma^2_F}_{\text{systematic}} + \underbrace{\sum_i w_i^2 \, \sigma^2_{\varepsilon_i}}_{\text{idiosyncratic}}$$

where $\bar{\beta}_w = \sum_i w_i \beta_i$. With equal weights, $\sum_i w_i^2 = 1/n$, recovering the result above. With value weights, $\sum_i w_i^2$ depends on cross-sectional concentration. **IDX caveat:** the Jakarta Stock Exchange is dominated by a small number of large-cap stocks, so $\sum_i w_i^2 > 1/n$, and idiosyncratic diversification is less complete than the equal-weight formula implies. This is an honest limitation of applying value-weighting in a concentrated market.

The practical consequence for inference: each monthly portfolio return already aggregates the idiosyncratic noise of all constituent stocks, leaving a signal-to-noise ratio substantially higher than individual stock returns. This is why $T = 150$ monthly portfolio observations support meaningful time-series inference despite being small by microeconometrician standards.

---

## Step 4: Time-Series Regression & Alpha Testing

### 4.1 Day-of-Week CAPM Regression

For each portfolio $p$ and each day-of-week $d \in \{\text{Mon}, \text{Tue}, \text{Wed}, \text{Thu}, \text{Fri}\}$, restrict the sample to trading days of type $d$ and estimate:
$$R_{p,t} - R_{f,t} \;=\; \alpha_d + \beta_d (R_{m,t} - R_{f,t}) + \epsilon_{d,t}, \qquad t \in \mathcal{T}_d$$

By conditioning on $\mathcal{T}_d$, each regression's alpha is interpretable as the Jensen alpha of the portfolio *on that specific weekday*. The Birru (2018) prediction is $\alpha_{\text{Mon}} > 0$ and $\alpha_{\text{Fri}} < 0$ for a safe-minus-speculative portfolio, driven by the weekend mood cycle (Hirshleifer et al. 2020).

**Estimator.** OLS applied to the restricted subsample yields:
$$\hat{\alpha}_d = \bar{y}_d - \hat{\beta}_d \bar{x}_d, \qquad \hat{\beta}_d = \frac{\sum_{t \in \mathcal{T}_d}(x_t - \bar{x}_d)(y_t - \bar{y}_d)}{\sum_{t \in \mathcal{T}_d}(x_t - \bar{x}_d)^2}$$
where $y_t = R_{p,t} - R_{f,t}$ and $x_t = R_{m,t} - R_{f,t}$.

### 4.2 Newey–West (1987) HAC Standard Errors — Step by Step

Daily return residuals exhibit two nuisances that break the OLS variance formula $\text{Var}(\hat{\beta}) = \sigma^2 (X'X)^{-1}$:

1. **Heteroskedasticity** — $\text{Var}(\epsilon_t | x_t) \neq \sigma^2$ (conditional volatility varies).
2. **Autocorrelation** — $\text{Cov}(\epsilon_t, \epsilon_{t-j}) \neq 0$ (momentum/reversal microstructure).

Start from the sandwich identity for any asymptotically linear estimator:
$$\sqrt{T}(\hat{\theta} - \theta) \xrightarrow{d} \mathcal{N}\!\big(0, \; A^{-1} B A^{-1}\big)$$
where $A = \mathbb{E}[X'X/T]$ and $B = \text{Var}(X'\epsilon/\sqrt{T})$. Under autocorrelation:
$$B \;=\; \Gamma_0 + \sum_{j=1}^{\infty}\big(\Gamma_j + \Gamma_j'\big), \qquad \Gamma_j = \mathbb{E}[x_t x_{t-j}' \epsilon_t \epsilon_{t-j}]$$

Direct estimation of $B$ by sample analogues of this infinite sum is not positive-semidefinite. Newey & West (1987) impose a **Bartlett kernel** weighting that guarantees PSD:
$$\hat{B} \;=\; \hat{\Gamma}_0 + \sum_{j=1}^{L}\Big(1 - \tfrac{j}{L+1}\Big)\big(\hat{\Gamma}_j + \hat{\Gamma}_j'\big)$$

**Why the triangular weights.** The Bartlett weight $k(j) = 1 - j/(L+1)$ is the Fourier transform of a triangular spectral window. Because $k(j)$ is a positive-definite kernel, the quadratic form $\hat{B}$ inherits PSD-ness; unweighted sums do not.

**Lag truncation.** Under Andrews (1991), the MSE-optimal bandwidth for an AR(1) residual with persistence $\rho$ is $L^* \propto T^{1/3}$. The simplified Newey–West (1994) default:
$$L = \big\lfloor 0.75 \, T^{1/3} \big\rfloor$$

For our daily sample $T \approx 4{,}000$, this yields $L = \lfloor 0.75 \cdot 15.87 \rfloor = 11$. We report $L \in \{6, 11, 22\}$ as robustness.

### 4.3 The GRS Test (Gibbons, Ross & Shanken 1989)

Stack the $N$ portfolio-specific regressions into a system. Under the null that *all* alphas are jointly zero, the GRS statistic is:
$$\text{GRS} \;=\; \frac{T - N - K}{N} \cdot \frac{1}{1 + \hat{\theta}_K^2} \cdot \hat{\alpha}' \hat{\Sigma}^{-1} \hat{\alpha} \;\sim\; F_{N,\, T-N-K}$$

**Term-by-term decoding.**

- $\hat{\alpha}$ is the $N \times 1$ vector of estimated portfolio alphas from Eq. 4.1.
- $\hat{\Sigma}$ is the $N \times N$ sample residual covariance matrix.
- $\hat{\theta}_K^2 = \bar{f}' \hat{\Omega}_f^{-1} \bar{f}$ is the squared Sharpe ratio of the $K$ factors (only the market here, so $K=1$).
- The scalar $(T-N-K)/N$ is the usual finite-sample degrees-of-freedom correction.
- The factor $1/(1 + \hat{\theta}_K^2)$ penalises alpha dispersion that could be mechanically produced by high factor Sharpe ratios.

**Intuition.** GRS asks: can we reject that *all* eight anomaly alphas are simultaneously zero after controlling for market risk? A rejection ($p < 0.05$) confirms the Monday-Friday speculative pattern is a joint feature of the IDX, not an artefact of one cherry-picked anomaly.

---

## Step 5: Structural Break Testing (Binary — Current Spec)

### 5.1 The Interaction-Dummy Specification

$$R_{p,t} \;=\; \gamma_0 + \gamma_1 \text{MON}_t + \gamma_2 \big(\text{MON}_t \times \text{POST}_t\big) + \beta \, \text{MktRF}_t + \epsilon_t$$

with:
$$\text{MON}_t = \mathbf{1}\{\text{day}(t) = \text{Monday}\}, \qquad \text{POST}_t = \mathbf{1}\{t \geq \text{Jan 2017}\}$$

**Coefficient decomposition by regime.**

- **Pre, non-Monday:** $\mathbb{E}[R_{p,t}] = \gamma_0 + \beta\,\text{MktRF}_t$
- **Pre, Monday:** $\mathbb{E}[R_{p,t}] = \gamma_0 + \gamma_1 + \beta\,\text{MktRF}_t$
- **Post, non-Monday:** $\mathbb{E}[R_{p,t}] = \gamma_0 + \beta\,\text{MktRF}_t$ *(note: no $\text{POST}$ main effect — see caveat below)*
- **Post, Monday:** $\mathbb{E}[R_{p,t}] = \gamma_0 + \gamma_1 + \gamma_2 + \beta\,\text{MktRF}_t$

The $\gamma_2$ coefficient is therefore the *change in the Monday premium* between regimes. A negative $\hat{\gamma}_2$ with $\hat{\gamma}_1 > 0$ would indicate the Monday effect attenuating or flipping sign post-2017 — the core empirical prediction of the mobile-revolution thesis.

**Methodological honesty — why this is *Chow-style*, not a full Chow test.** The specification above allows only two parameters ($\gamma_0$ effectively via omitted $\text{POST}$ main effect and $\gamma_1$ via $\gamma_2$) to break. A proper Chow test permits the *entire* parameter vector — including $\beta$, the market beta — to differ across regimes. Our current design restricts $\beta$ to be constant; this is a defensible identifying assumption (market beta should not jump mechanically at 2017) but it is a restriction nonetheless. We address this below in §6.

### 5.2 Recommended Addition: $\text{POST}_t$ Main Effect

The spec above omits a stand-alone $\text{POST}_t$ regressor. We should add it:
$$R_{p,t} = \gamma_0 + \gamma_1 \text{MON}_t + \gamma_3 \text{POST}_t + \gamma_2 (\text{MON}_t \times \text{POST}_t) + \beta \, \text{MktRF}_t + \epsilon_t$$

Without $\gamma_3$, the regression is forced to load any level shift in average returns onto $\gamma_2$, biasing the interaction estimate. Including $\gamma_3$ isolates the pure interaction from the level shift.

---

## Step 6: Formal Structural-Break Tests — Chow & Bai–Perron

### 6.1 The Chow (1960) F-Test — Derivation

**Setup.** Partition the sample at a *known* break date $t^*$ into $T_1$ and $T_2$ observations. Let $\text{SSR}_P$ be the residual sum of squares from the pooled regression (imposing identical coefficients in both periods), and let $\text{SSR}_1, \text{SSR}_2$ be the residual sums from each period estimated separately (letting all $k$ coefficients vary).

**Test statistic.**
$$F_{\text{Chow}} \;=\; \frac{\big(\text{SSR}_P - (\text{SSR}_1 + \text{SSR}_2)\big)/k}{(\text{SSR}_1 + \text{SSR}_2)/(T_1 + T_2 - 2k)} \;\sim\; F_{k,\, T_1 + T_2 - 2k}$$

**What the numerator measures.** The increase in residual variance from *forcing* the coefficients to be equal, scaled by the $k$ restrictions imposed. If the true coefficients differ across regimes, the pooled model fits poorly and $\text{SSR}_P$ balloons.

**Homoskedasticity assumption.** The classical Chow test requires equal residual variances across the two periods. Daily returns almost certainly violate this — volatility regimes differ pre/post-2017, pre/post-COVID. We therefore use the **Wald form with heteroskedasticity-robust covariance:**
$$W = (R\hat{\delta})' \big(R \hat{V}_{\text{HC}} R'\big)^{-1} (R\hat{\delta}) \;\sim\; \chi^2_k$$
where $R\delta = 0$ encodes the restriction "pre-period coefficients = post-period coefficients" in a stacked regression.

**What Chow can do for you.**

1. **Joint test** that *all* coefficients (not just Monday) are stable across 2017. If Chow rejects but your $\gamma_2$ doesn't, something else is moving — likely $\beta$ or the weekly return level.
2. **Comparison of candidate break dates.** Run the test at 2015, 2016, 2017, 2018, 2019 and report the F-statistic at each. The maximum should land near 2017 if the mobile-revolution narrative is right. This is essentially a manual Quandt–Andrews (see 6.2).
3. **Out-of-sample robustness.** Chow tests with placebo break dates (e.g., 2014) should *not* reject; if they do, the 2017 break is a coincidence.

### 6.2 Bai–Perron (1998, 2003) — Multiple Unknown Breaks

**The problem Chow can't solve.** Chow requires you to *pre-commit* to a break date. If you run Chow at every candidate date and take the max, the resulting distribution is no longer $F$; it's the supremum of correlated F-statistics — the Quandt–Andrews sup-F distribution (Andrews 1993), which has fatter tails than F.

**Bai–Perron's innovation.** Jointly estimate $m$ break dates $\{t_1^*, \ldots, t_m^*\}$ and their associated coefficient vectors by minimising the total SSR across all possible partitions:
$$\{\hat{t}_1, \ldots, \hat{t}_m\} \;=\; \arg\min_{t_1 < \cdots < t_m} \; \sum_{j=0}^{m} \text{SSR}_j(t_j, t_{j+1})$$
where $t_0 = 1$ and $t_{m+1} = T$. Dynamic programming makes this computationally feasible in $O(T^2)$ rather than $O(T^m)$.

**Three tests Bai–Perron provides.**

1. **Sup-F test** of $H_0$: no breaks vs. $H_A$: exactly $k$ breaks, with critical values that correctly account for the search over break dates.
2. **Double-maximum (UDmax, WDmax)** test of $H_0$: no breaks vs. $H_A$: at least one break, without pre-specifying $k$.
3. **Sequential test** of $\ell$ vs. $\ell + 1$ breaks — the standard way to pick the number of breaks.

**Confidence intervals for break dates.** Bai (1997) derives the asymptotic distribution of $\hat{t}_j$, giving proper confidence intervals. If the 95% CI for the estimated break is, say, Mar 2016–Sep 2017, your "Jan 2017" narrative is comfortably inside it; if it's 2019–2021, you have a problem.

**What Bai–Perron can do for you.**

1. **Let the data pick the break date.** If the estimated break is Jan 2017 ± a few months, your narrative is data-validated. If the estimated break is, say, Mar 2020 (COVID), you've discovered the dominant structural break is something else.
2. **Identify multiple breaks.** There are at least three candidates: 2017 (YNS / 1M SID), Nov 2018 (T+2 settlement), Mar 2020 (COVID / Robinhood-style retail surge). Bai–Perron can tell you whether the data supports one, two, or three regimes.
3. **Avoid data-snooping critique.** Sullivan, Timmermann & White (2001) hammer calendar-effect papers for searching over dates. Bai–Perron's correctly-sized critical values are the defence against exactly this critique.

**Implementation.** Python's `ruptures` package implements the dynamic-programming kernel; R's `strucchange` package has full Bai–Perron with inference. For a thesis, `strucchange::breakpoints()` + `confint()` is the path of least resistance.

### 6.3 Recommendation — Chow vs. Bai–Perron, given your timeline

Given you have constrained time and already have the interaction-dummy results:

- **Run Chow first** (one afternoon of coding). Report the F-statistic at Jan 2016, Jan 2017, Jan 2018 to show 2017 is the local maximum. This directly validates your choice of break date and is the minimum a reviewer will expect.
- **Run Bai–Perron second** if you have two days. Report the estimated break date, its 95% CI, and whether the sequential procedure supports one or multiple breaks. This transforms your "I chose 2017 because of the mobile narrative" claim into "the data independently identified a break near 2017, consistent with the mobile narrative."
- **Skip multi-break estimation** unless the single-break Bai–Perron CI is wide — in which case you should acknowledge COVID as a second regime.

---

## Step 7: Non-Binary Regressors for the Structural Break

The binary $\text{POST}_t$ dummy imposes two strong assumptions: (i) the break is instantaneous, and (ii) it happens *exactly* at Jan 2017. Both are falsifiable. A continuous moderator relaxes both.

### 7.1 The Candidate Continuous Moderators

| Variable | Source | Reasoning | Caveat |
|---|---|---|---|
| $\text{SID}_t$ — KSEI Single Investor IDs | KSEI monthly reports | Direct proxy for retail participation; 281k (2012) → 10M (2024) | Monotonic time trend — confounded with $t$ |
| $\log(\text{SID}_t)$ | Derived | Linearises the 35× growth | Still monotonic; use detrended version |
| $\Delta \text{SID}_t$ | Derived | Stationary (growth rate) | Noisy month-to-month |
| $\text{MobileShare}_t$ | KSEI app vs. desktop data | Most direct proxy for the mechanism | Available only from 2018+ |
| $\text{RetailVol}_t / \text{TotalVol}_t$ | IDX trading value data | Retail-flow share; captures the mechanism | Approximation; IDX doesn't tag every trade cleanly |
| $\text{SmartphonePen}_t$ | World Bank / ITU | Exogenous to IDX; purely technological | Slow-moving annual data |

### 7.2 The Continuous-Moderator Specification

Replace the binary $\text{POST}_t$ with a continuous regressor $Z_t$ (standardised to mean zero, unit variance for interpretability):
$$R_{p,t} = \gamma_0 + \gamma_1 \text{MON}_t + \gamma_3 Z_t + \gamma_2 (\text{MON}_t \times Z_t) + \beta \, \text{MktRF}_t + \epsilon_t$$

**Interpretation of $\gamma_2$.** A one-standard-deviation increase in $Z_t$ (e.g., 3M additional SIDs) shifts the Monday premium by $\hat{\gamma}_2$. This is a *dose–response* coefficient, far richer than a binary "before/after" estimate.

**Econometric warning — non-stationarity.** If $Z_t$ is $I(1)$ (e.g., raw $\text{SID}_t$), the interaction $\text{MON}_t \times Z_t$ inherits non-stationarity and OLS standard errors are invalid. Two fixes:

1. Use $\Delta Z_t$ (differenced) — stationary but noisy.
2. Use $Z_t - \hat{Z}_t^{\text{trend}}$ (detrended) — removes the mechanical time effect.

For robustness, include a time trend $t$ as a control; if $\hat{\gamma}_2$ survives the inclusion of $t$ and $t \times \text{MON}_t$, the effect is not spurious.

### 7.3 Smooth-Transition Regression (Optional, Higher Effort)

If you want to model the *shape* of the transition — not just its level — a Smooth Transition Regression (STAR; Teräsvirta 1994) parameterises the break as a logistic function of time:
$$G(t; c, \lambda) = \frac{1}{1 + \exp(-\lambda (t - c))}, \qquad \lambda > 0$$

with specification:
$$R_{p,t} = \gamma_0 + \gamma_1 \text{MON}_t + \gamma_2 \big(\text{MON}_t \times G(t; c, \lambda)\big) + \beta\,\text{MktRF}_t + \epsilon_t$$

**What the parameters give you.**

- $\hat{c}$ — the *estimated midpoint* of the transition (data-driven break date).
- $\hat{\lambda}$ — the *speed* of the transition; $\lambda \to \infty$ is a binary step, $\lambda \to 0$ is linear.
- $\hat{\gamma}_2$ — the total change in the Monday premium across the full transition.

**Cost.** STAR requires non-linear least squares and is sensitive to starting values. Estimable in Python via `scipy.optimize.curve_fit` or R's `tsDyn::lstar()`.

### 7.4 My Recommendation, Given Your Timeline

Rank-ordered by effort-adjusted value:

1. **Add $\log(\text{SID}_t)$ or $\Delta \log(\text{SID}_t)$ as a continuous moderator** (one day of work). Run the §7.2 spec, report $\hat{\gamma}_2$, compare its significance to the binary $\text{POST}_t$ version. If both specifications agree, your result is robust to the choice of regressor form — reviewer gold. The KSEI SID data is the *cleanest* proxy for the retail revolution you have available; it is literally the dependent variable your narrative cares about.
2. **Add Chow F-tests at 2015/2016/2017/2018** (an afternoon). Defends your break-date choice against the "why this year?" critique.
3. **Bai–Perron with one break** (one day in R). Gives data-validated break date + CI.
4. **STAR/LSTR with $t$ as the transition variable** (two to three days). High cost; worth it only if §7.1–§7.3 results are messy. For a reviewer who wants to see the *shape* of the transition, this is the most elegant answer — but it is also the easiest to estimate badly.

**What I would personally do in your position.** Do (1) + (2) this week. That turns "I chose 2017 for narrative reasons" into "my binary result replicates under a continuous proxy for retail participation, and the Chow F-statistic peaks at 2017." If time remains, add (3). Save STAR for a journal revision.

**One thing not to do.** Do *not* try to layer all four approaches into the main tables — it crowds the paper and invites the reviewer to ask why each gives slightly different numbers. Pick the binary dummy as primary, the continuous $\log(\text{SID}_t)$ as robustness, and mention Chow / Bai–Perron in a footnote / appendix. A thesis that defends one result well beats a thesis that hedges across four specifications.

---

## Summary: Where Each Piece Fits

| Step | Purpose | Primary Output |
|---|---|---|
| 1 | Data filters | Clean panel, ~2M obs |
| 2 | Timing | Lagged characteristics, no look-ahead |
| 3 | Aggregation | Value-weighted quintile portfolios |
| 4 | Alpha testing | $\hat{\alpha}_{\text{Mon}}$ per portfolio, GRS joint test |
| 5 | Binary break | $\hat{\gamma}_2$ from interaction dummy |
| 6 | Break validation | Chow F-sequence + Bai–Perron estimated break date |
| 7 | Continuous break | $\hat{\gamma}_2$ from $\log(\text{SID}_t)$ moderator |

Each row is falsifiable. If §5 gives you $\hat{\gamma}_2 < 0$ but §6 locates the break in 2020 and §7 finds $\hat{\gamma}_2 \approx 0$ under the continuous moderator, the "mobile revolution in 2017" narrative is in trouble — but the thesis is still interesting, because you've *discovered* the actual break. Design for honesty, not for confirmation.
