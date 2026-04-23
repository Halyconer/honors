# Cowork Session Memory — Honors Thesis Project

## Last Updated
2026-04-23

## Project Summary
Honors thesis examining whether Indonesia's mobile trading revolution (2017–2024) reduced or eliminated the **Monday effect** on the Jakarta Stock Exchange (IDX). Built on Birru (2018)'s behavioral framework — speculative retail investors drive the Monday effect; if mobile trading increased retail speculation, the effect may have *persisted or amplified*, not weakened.

## Current Methodological Approach
- **Core design:** Quintile sorts on speculative characteristics (Ivol, Max, etc.) + dummy variable regression (Pre/Post mobile trading era)
- **Advisor guidance:** Stick with dummy variables (do NOT switch to continuous regressors despite their power advantages)
- **Regression framework:** Monthly aggregation of daily returns by day-of-week; Newey-West HAC; CAPM alpha tests
- **NOT Fama-MacBeth:** Advisor previously corrected this label. Describe literally what the code does.

## Key Open Methodological Questions (as of 2026-04-23)

### 1. Statistical Power Problem
Running 8 separate regressions with ~60 pre / ~96 post monthly observations is underpowered. Prior discussion identified these levers (ranked by payoff-per-hour):
- [RULED OUT for now] Continuous regressor (log SID) — advisor wants dummies
- [LIVE] Extend data backward to ~2005 via Refinitiv rerun (~55% precision gain)
- [LIVE] **One-sided tests** — mobile trading hypothesis predicts *weakening*, not unspecified change; justified theoretically; ~20% free power gain
- [LIVE] Add noise controls (market vol, time trend) as covariates
- [LIVE] Pool 8 characteristics into joint test (GRS-style or PCA composite)
- [DEFERRED] Stock-day observations with cluster-robust SEs — departure from Birru, flag with advisor first

### 2. Structural Break Approach (NEW — discussed 2026-04-23)
**Proposal:** Use **Bai-Perron test** to data-drive the break location rather than imposing it a priori.
- Compatible with dummy variable framework: use Bai-Perron to *justify and locate* the break, then construct dummy accordingly
- Key advantage: if empirical break coincides with 2017-2019 mobile trading proliferation, that's confirmatory evidence
- Key assumptions to check: stationarity of residuals within regimes, minimum segment length (~15% of sample)
- Does NOT require abandoning dummies — it validates and locates them

### 3. Birru (2018) Assumption Audit (PENDING)
Need to systematically examine which of Birru's assumptions hold for the IDX context:
- Indonesian market microstructure vs. US
- Retail investor composition on IDX
- Which speculative characteristics translate cross-culturally
- Weekend effect literature for emerging vs. developed markets

## Data Notes
- Raw data in `data/chunks/` (gitignored due to size)
- Panel covers IDX stocks 2017–2024 approximately
- Refinitiv Codebook notebooks exist for pulling extended history

## File Architecture Reminder
See CLAUDE.md for full pipeline and directory details.

## Action Items (Next Steps)
- [ ] User: work through Bai-Perron math (segment penalty, minimum segment length condition)
- [ ] Claude: audit Birru (2018) assumptions for IDX applicability
- [ ] Claude: examine existing regression code to identify where Bai-Perron break could be integrated
- [ ] Decide: one-sided vs. two-sided tests (quick win, should resolve before next analysis run)
- [ ] Consider: Refinitiv data extension scope and feasibility
