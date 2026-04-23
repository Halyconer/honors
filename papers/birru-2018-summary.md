# Birru (2018) — "Day of the week and the cross-section of returns"
**Journal of Financial Economics 130, 182–214**

## Core Finding
Long-short anomaly returns are strongly related to the day of the week. Speculative stocks earn low returns on Mondays and high returns on Fridays relative to non-speculative stocks. The effect is driven entirely by the speculative leg (not the safe leg), consistent with a sentiment/mood explanation.

## Key Result: Monday accounts for >100% of strategy returns
- For all 16 anomalies where the **short leg is speculative**: Monday alone accounts for >100% of total long-short returns (Tuesday-Friday returns are negative)
- For 3 anomalies where the **long leg is speculative** (size, illiquidity, bid-ask): Friday alone accounts for >100% of strategy returns
- Monday and Friday long-short returns have **opposite signs** for every anomaly

## Hypothesis: Investor Mood / Sentiment
- Psychology literature: mood increases Thursday→Friday, decreases on Monday
- Source: Golder & Macy (2011) — 2.4M Twitter users, 500M tweets; mood (PA and NA) at 3pm US time monotonically improves Mon→Fri
- Sentiment affects speculative stocks most (hard to value, hard to arbitrage) per Baker & Wurgler (2006, 2007)
- Low mood Monday → pessimism → speculative stocks decline
- High mood Friday → optimism → speculative stocks rise

## The 19 "Speculative" Anomalies (Table 1)

### Short leg is speculative (16 anomalies) — High Monday L-S returns:
| Anomaly | Speculative Leg | Category |
|---------|----------------|----------|
| Ivol (idiosyncratic volatility) | High Ivol (short) | Volatile |
| Max (max daily return) | High Max (short) | Lottery |
| Price | Low Price (short) | Lottery |
| Age | Young (short) | Young |
| FP (failure probability) | High FP (short) | Distress |
| O-score | High O-score (short) | Distress |
| ROA | Low ROA (short) | Unprofitable |
| OP (operating profitability) | Low OP (short) | Unprofitable |
| E (earnings dummy) | Unprofitable (short) | Unprofitable |
| CF (cash flow dummy) | Negative CF (short) | Unprofitable |
| D (dividend dummy) | Non-payers (short) | Non-dividend |
| NXF (net external financing) | High NXF (short) | Extreme growth |
| Disp (forecast dispersion) | High Disp (short) | Hard to value |
| CFV (cash flow volatility) | High CFV (short) | Hard to value |
| 52-Wk (52-week high) | Far from high (short) | Speculative demand |
| Beta | High Beta (short) | Speculative demand |

### Long leg is speculative (3 anomalies) — High Friday L-S returns:
| Anomaly | Speculative Leg | Category |
|---------|----------------|----------|
| Size | Small (long) | Small |
| Illiq (Amihud illiquidity) | Illiquid (long) | Limits to arbitrage |
| Bid-Ask | Wide spread (long) | Limits to arbitrage |

## Data & Methodology
- **Data**: CRSP (NYSE, Amex, Nasdaq), Compustat; July 1963 – December 2013
- **Portfolios**: Value-weighted, NYSE breakpoints, decile sorts
- **Risk adjustment**: Excess returns, CAPM alpha, FF3 alpha, Carhart 4-factor alpha
- **Standard errors**: HAC-adjusted (heteroskedasticity + autocorrelation)
- **Monthly strategy returns**: Calculated by investing only on specified day(s)

## Magnitude Examples (Table 2, Carhart 4-factor alpha, monthly)
| Anomaly | Monday L-S | Friday L-S | Fri−Mon |
|---------|-----------|-----------|---------|
| Ivol | +1.049% | −0.581% | −1.630% |
| Price | +0.851% | −0.890% | −1.740% |
| FP | +1.071% | −0.555% | −1.627% |
| OP | +0.746% | −0.507% | −1.253% |
| Size | −0.335% | +0.885% | +1.221% |
| Bid-Ask | −0.839% | +0.934% | +1.773% |

All t-statistics highly significant (typically 4–10+).

## Robustness Tests — All passed:

### 1. Subsample periods (Table 7)
- 1963–1974, 1975–1994, 1995–2013: effect present in ALL subperiods
- Important: aggregate weekend effect disappeared after 1975 (Robins & Smith 2016), but cross-sectional Monday/Friday effect persists
- Sentiment delivers cross-sectional predictions, not necessarily aggregate predictions

### 2. News (Section 4.6)
- **Macroeconomic news**: Results robust to excluding CPI, PPI, employment, FOMC announcement days
- **Firm-specific news**: Results robust to excluding earnings announcements, M&A, management forecasts
- **Overnight vs intraday**: Effect entirely in intraday returns (not overnight), ruling out news released outside trading hours

### 3. Institutional trading (Section 4.7)
- Effect stronger for low institutional ownership stocks
- Effect present in pre-1952 period when markets were open Saturdays (ruling out end-of-week rebalancing)
- Institutions prefer large/liquid stocks; the effect is in speculative (small, volatile) stocks

### 4. Liquidity (Section 4.8)
- Controlling for daily changes in market volume and liquidity: Monday coefficient remains significant at 1% for almost all anomalies

### 5. Daily risk premiums (Section 4.4)
- Decomposing Fama-French factors into Monday/Friday components: results unchanged

## Additional Supporting Evidence (Section 5)

### VIX
- VIX increases 2.16% on average on Mondays (consistent with declining sentiment/rising fear)
- VIX decreases ~70 bps on Fridays

### Treasury bonds
- Treasury returns highest on Mondays (flight to safety with declining sentiment)
- Treasury returns lowest on Fridays
- Pattern holds for all maturities (1 month to 5 years)

### Tuesday–Thursday (mood monotonically increases)
- Using Golder & Macy Twitter data: PA increases and NA decreases monotonically Mon→Fri
- Long-short returns mirror this: monotonic pattern across all 5 weekdays
- Example (Ivol, daily excess returns): Mon +22.6bp, Tue +11.4bp, Wed −5.9bp, Thu −7.9bp, Fri −15.1bp
- Example (Size, daily excess returns): Mon −8.3bp, Tue −6.8bp, Wed +0.4bp, Thu +10.5bp, Fri +20.7bp

### Holidays (Table 16)
- Tuesdays after Monday holidays: returns look like typical Mondays (56/57 anomaly-day combos in predicted direction)
- Thursdays before Friday holidays: returns look like/exceed typical Fridays
- Pre-Thanksgiving Wednesday: returns larger than typical Friday for 17/19 anomalies

### 44 Other anomalies without clear speculative leg (Section 5.5)
- Momentum, book-to-market, accruals, earnings surprise, etc.
- These do NOT exhibit the Monday/Friday pattern → confirms it's driven by speculative vs non-speculative distinction, not a generic day-of-week pattern

## Key Distinction: Aggregate vs Cross-Section
- The aggregate "weekend effect" (market returns low on Monday) has weakened/disappeared post-1975
- But the **cross-sectional** Monday/Friday effect (speculative vs safe stocks) remains strong throughout
- Baker & Wurgler (2007): sentiment doesn't deliver clear aggregate predictions because declining sentiment hurts speculative stocks but can cause flight-to-quality benefiting safe stocks

## Relevance to Adrian's Thesis
- Birru studies US cross-section; Adrian studies Indonesia aggregate + cross-section
- Adrian's hypothesis: mobile trading democratization changed investor composition → may alter the Monday effect
- Birru's framework suggests: if mobile trading increases retail/speculative participation, it could amplify or alter the cross-sectional Monday effect
- Adrian's aggregate Monday effect (mean return −0.069%, t=−10.4) is consistent with the traditional aggregate weekend effect, which Birru notes still exists in some markets
- Key test: does the aggregate Monday effect weaken post-2017 in Indonesia as mobile adoption rises?
- Extension: if fundamentals data available, test cross-sectional predictions (speculative vs safe stocks × Monday)
