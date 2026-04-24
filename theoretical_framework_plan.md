# Theoretical Framework: The "Speculative Sentiment" Thesis
**Project:** The Impact of the Mobile Trading Revolution on the Monday Effect (IDX)
**Last Updated:** 2026-04-23
**Author:** Adrian Eddy (Expanded synthesis)

This document lays out the behavioral, arbitrage-theoretic, and institutional foundations of the thesis. It is organized around six pillars: (1) Baker & Wurgler's cross-sectional theory of sentiment; (2) Birru's day-of-week mood mechanism; (3) the formal limits-to-arbitrage apparatus (De Long et al., Shleifer & Vishny) that lets the two prior pillars survive in equilibrium; (4) the attention/gamification literature that describes the *delivery mechanism* through which the Indonesian mobile revolution interacts with (1)–(3); (5) emerging-markets asset pricing findings that caution against lifting the US framework wholesale; and (6) the Indonesian institutional synthesis that ties the mechanism to measurable market-structure facts.

The structure is intentionally maximalist: each pillar states the proposition, the formal mechanism, the empirical evidence underlying it, and the specific testable prediction it generates for the IDX.

> **Methodological caveat (see `CLAUDE.md`).** The empirical pipeline for this thesis is an aggregate/panel time-series study of day-of-week effects, not a replication of the Birru cross-sectional portfolio-sort + factor-regression apparatus. Where Birru's framework delivers *predictions* the thesis tests (e.g., that the Monday effect should be driven by the speculative leg), those predictions are treated as imported rather than derived. The thesis does not run Birru's factor regressions — Indonesia lacks the canonical Fama–French–Carhart factors — and therefore the framework below is used to *motivate* design choices (which characteristics to sort on, how to define "speculative"), not to label the methodology.

---

## Pillar 1: Baker & Wurgler (2006, 2007) — The Cross-Section of Sentiment

### 1.1 Two Conceptions of Sentiment: Propensity to Speculate vs. Generic Optimism

Baker & Wurgler (2006, pp. 1648–1650) are explicit that "investor sentiment" admits two distinct theoretical definitions, and the two are carefully distinguished because they generate the *same* cross-sectional prediction through *different* channels:

1. **Sentiment as the propensity to speculate (the demand channel).** Sentiment is a market-wide appetite for speculative payoffs. It varies over time, and it shifts relative demand *across* stocks toward those whose payoff profile is salient to speculators — small, young, volatile, lottery-like, non-dividend-paying, distress-adjacent, or extreme growth. Critically, the cross-section moves *even if arbitrage frictions are uniform*, because demand shocks are not uniform.

2. **Sentiment as undifferentiated optimism/pessimism (the arbitrage channel).** Sentiment is a generic wave that lifts or depresses the whole market; the cross-section moves because arbitrage frictions are non-uniform. Stocks that are costly, risky, or impossible to short do not get corrected, so they drift more with sentiment than stocks that are easy to arbitrage.

In practice these channels overlap almost perfectly — the stocks that are hardest to value are, empirically, the same stocks that are hardest to arbitrage — which is why Baker & Wurgler treat them as mutually reinforcing rather than mutually exclusive. The point that matters for this thesis is that *either* framing delivers the prediction that sentiment-driven mispricing concentrates in a specific, recurring bundle of firm characteristics.

### 1.2 The Conditional Characteristics Model

Baker & Wurgler's central empirical specification (2006, eq. 1, p. 1652) is:

```
E_{t-1}[R_{it}] = a + a_1 T_{t-1} + b_1 x_{it-1} + b_2 (T_{t-1} · x_{it-1}) + ε_{it}
```

where `x_{it-1}` is a vector of firm characteristics and `T_{t-1}` is a proxy for sentiment. The coefficient of interest is **b_2**, the interaction: does the cross-sectional predictive power of characteristics depend on the time-series level of sentiment? The null is that any nonzero `b_2` is rational compensation for systematic risk; the alternative is that `b_2` captures sentiment-driven mispricing correction.

Birru (2018) adopts the same template but replaces the continuous sentiment proxy `T` with a day-of-week indicator, on the theory that Monday-to-Friday mood variation *is* a (high-frequency, exogenous-from-fundamentals) sentiment shock. **This is exactly the template the thesis inherits for its triple interaction `Mon × Speculative × Post`.**

### 1.3 The Six-Proxy Sentiment Index (1963–2001)

Baker & Wurgler construct a composite sentiment measure by taking the first principal component of six proxies (Baker & Wurgler 2006, §III.C, eq. 2):

```
SENTIMENT_t = −0.241 CEFD_t   + 0.242 TURN_{t−1} + 0.253 NIPO_t
              + 0.257 RIPO_{t−1} + 0.112 S_t      − 0.283 P^{D−ND}_{t−1}
```

The six proxies are:

- **CEFD** — value-weighted closed-end fund discount (Lee, Shleifer & Thaler 1991 argue sentiment drives the discount).
- **TURN** — detrended log NYSE turnover (Baker & Stein 2004: under short-sale constraints, noise traders add liquidity only when optimistic, so turnover proxies for sentiment).
- **NIPO** — annual number of IPOs (high counts = "hot" issuance window).
- **RIPO** — average first-day return on IPOs (pricing pressure from speculative demand).
- **S** — equity share of total new issues (market-timing proxy: managers issue equity when sentiment is high).
- **P^{D−ND}** — dividend premium, i.e. log difference in market-to-book between dividend payers and non-payers (Baker & Wurgler 2004: proxies relative demand for "safe" stocks).

Each proxy is standardized before the PCA so loadings are comparable. The first PC explains ~49% of variance in the raw proxies and ~53% after orthogonalizing each proxy against business-cycle controls (industrial production growth, durables/non-durables/services consumption growth, NBER recession dummy) — the orthogonalized index `SENTIMENT^⊥` is what Baker & Wurgler treat as "cleaner" sentiment.

**Relevance for this thesis.** None of the six proxies is constructible for pre-2017 IDX in a way that would stand up as a literal replication. But their *logic* justifies why the thesis uses day-of-week as a sentiment shock (following Birru) rather than attempting to build a local Baker–Wurgler index on Indonesian data: day-of-week variation is arguably exogenous of fundamentals and common to every investor, whereas constructing an IDX sentiment index would import every identification problem B&W spend §III.C trying to defuse.

### 1.4 Conduits of Mispricing: What Makes a Stock "Speculative"

Baker & Wurgler (2006, p. 1648 and §I.A) identify the characteristics that make a stock a conduit of sentiment. The full list is tighter than it is usually summarized:

| Characteristic | Why it conducts sentiment | B&W (2006) empirical finding |
|---|---|---|
| **Small (low ME)** | Retail habitat; high arbitrage cost; wide bid-ask; harder to short. | Size effect appears *only* in low-sentiment periods (Table III). |
| **Young (low Age)** | No earnings history anchor; valuations unconstrained. | Young-firm returns are high (low) when sentiment was previously low (high), with nearly monotonic reversal. |
| **High volatility (high σ)** | High idiosyncratic risk makes relative-value arbitrage risky (Wurgler & Zhuravskaya 2002). | High-σ stocks earn +2.41% monthly post low-sentiment vs. +0.30% post high-sentiment; the sharpest sign-flip in the paper. |
| **Unprofitable (E ≤ 0) / Low OP** | No cash flow anchor; depends entirely on growth narratives. | Unprofitable firms drive the conditional sign-flip. |
| **Non-dividend-paying (D = 0)** | Salient "unsafe" label; D > 0 defines a bond-like security in investors' minds. | Non-payers earn returns 0.89% lower on average post-low-sentiment, 0.75% higher post-high-sentiment. |
| **Extreme growth / Extreme distress** | U-shaped: both tails are *harder to value* than the middle. | U-shaped conditional-difference row for BE/ME, EF/A, and GS — the two extremes move *together* relative to the middle. This is a key subtlety: B&W do *not* claim "growth always speculative"; they claim "extreme anything is speculative." |
| **High R&D, low PPE/A (intangible)** | Asset opacity; valuation depends on unverifiable investment opportunities. | Mild sentiment conditioning, consistent with direction. |

The canonical "safe" stock is the converse: large, old, low-volatility, profitable, dividend-paying, with tangible assets and middling (not extreme) growth. This is the "bond-like equity" portrait (Baker & Wurgler 2006, p. 1650).

### 1.5 The Sign-Flip Prediction

The single most underappreciated finding in B&W (2006) is that **several characteristics have zero unconditional predictive power but strong sign-flipping predictive power once conditioned on sentiment** (Table III). Age is the clearest: old-minus-young returns −0.54% per month following negative sentiment and +0.85% per month following positive sentiment, with a near-monotonic reversal across deciles. This "averaging out" is why a naïve unconditional cross-sectional study finds nothing and a sentiment-conditional study finds a lot.

This matters for the thesis' interpretation of pre/post results: even if a characteristic (say, Age or Ivol) shows a muted unconditional Monday spread in one subperiod, the *sign-flip* pattern — sign in the pre-period flipping (or its magnitude amplifying) in the post-period — is the behaviorally meaningful result, not the level in any one subperiod.

### 1.6 Why Sentiment Gives Clean *Cross-Sectional* Predictions but Messy *Aggregate* Predictions

Baker & Wurgler (2007, JEP) make the point explicit: a decrease in sentiment pulls speculative stocks down *and* pushes safe stocks up through flight-to-quality. These two effects cancel (at least partially) at the market-average level. This is why (a) the aggregate weekend effect in the US weakened post-1975 even as the cross-sectional sentiment mechanism kept operating (Birru 2018, Robins & Smith 2016), and (b) this thesis' aggregate-plus-cross-sectional design is the correct empirical form for the underlying theory — neither alone is sufficient.

---

## Pillar 2: Birru (2018) — Day-of-the-Week as a High-Frequency Sentiment Shock

### 2.1 The Psychological Foundation: What the Mood Literature Actually Says

The mood literature disaggregates "mood" into two independent dimensions (Watson & Tellegen 1985, extended through Watson 2000):

- **Positive Affect (PA).** Engagement, enthusiasm, alertness, determination, pride. *Low PA is the absence of positive emotion, not the presence of negative emotion.*
- **Negative Affect (NA).** Fear, nervousness, irritability, hostility, guilt, distress. *Low NA is the absence of negative emotion, not the presence of positive emotion.*

PA and NA vary roughly independently. The day-of-week pattern is: **PA is higher on Friday than Monday–Thursday; NA is lower on Friday than Monday–Thursday**. This is the pattern both Stone et al. (2012, Gallup, N ≈ 340,000) and Golder & Macy (2011, Twitter, N ≈ 2.4M individuals, 500M tweets) find. The Golder & Macy study is methodologically decisive because it (a) captures mood in real time (no recall bias), (b) controls for diurnal (within-day) variation by timestamping every tweet, and (c) exploits within-individual variation by having repeated observations per user. Birru (2018, §2) confirms that at the specific 3 pm US closing-bell window — the only window that matters for stock returns — the Mon→Fri PA-rising / NA-falling pattern holds.

**Biological corroboration.** The psychology finding is not a soft one: Mondays show statistically elevated rates of myocardial infarction (Willich et al. 1994; Witte et al. 2005; Collart et al. 2014) and completed suicide (Bollen 1983; MacMahon 1983; Massing & Angermeyer 1985; Maldonado & Kraus 1991; Jessen & Jessen 1999). The week, crucially, has *no astronomical or environmental basis* — it is a purely sociocultural rhythm — so the effect has no "sunlight" or "weather" confound. Day-of-week mood variation is stronger among full-time workers than part-time, and stronger among employed than unemployed (Stone et al. 2012; Helliwell & Wang 2015), confirming that the rhythm is lifestyle-driven rather than biological.

### 2.2 Why Mood Translates into Prices: The "Ambiguous Stimuli" Channel

Mood affects decision-making *most* in situations that are ambiguous and lacking concrete information (Clore et al. 1994; Forgas 1995; Hegtvedt & Parris 2014). People use current mood as an input to evaluating uncertain stimuli — what psychologists call the *affect-as-information* heuristic. This is the theoretical bridge from mood (psychology) to prices (finance): the stocks whose valuations are most ambiguous (Pillar 1's speculative conduits) are, by construction, the ones whose prices will co-move most with mood. This is not coincidence — it is the same mechanism, with Baker & Wurgler contributing the cross-sectional geography and Birru contributing the time-series heartbeat.

### 2.3 The Cross-Sectional Monday Mechanism

Birru's core claim (Birru 2018, §§3–4): on Mondays, the speculative leg of each cross-sectional anomaly *underperforms* its non-speculative counterpart; on Fridays it outperforms. The 19 "speculative" anomalies Birru identifies (2018, Table 1) partition into:

**Sixteen anomalies where the short leg is the speculative leg** (high Monday L–S, low Friday L–S):

| Anomaly | Speculative leg | Category |
|---|---|---|
| Ivol (idiosyncratic volatility) | High Ivol | Volatile |
| Max (max daily return in past month) | High Max | Lottery |
| Price (nominal price level) | Low Price | Lottery |
| Age (months since first CRSP listing) | Young | Young |
| FP (Campbell et al. failure probability) | High FP | Distress |
| O-score (Ohlson 1980) | High O-score | Distress |
| ROA | Low ROA | Unprofitable |
| OP (operating profitability) | Low OP | Unprofitable |
| E (profitability dummy) | Unprofitable | Unprofitable |
| CF (cash-flow dummy) | Negative CF | Unprofitable |
| D (dividend dummy) | Non-payers | Non-dividend |
| NXF (net external financing) | High NXF | Extreme growth |
| Disp (analyst forecast dispersion) | High Disp | Hard to value |
| CFV (cash-flow volatility) | High CFV | Hard to value |
| 52-Wk (distance from 52-week high) | Far from high | Speculative demand / anchoring (Byun & Jeon 2014) |
| Beta | High Beta | Speculative demand / benchmarking constraint (Baker, Bradley & Wurgler 2011) |

**Three anomalies where the long leg is the speculative leg** (low Monday L–S, high Friday L–S):

| Anomaly | Speculative leg | Category |
|---|---|---|
| Size (SMB-style) | Small | Small |
| Illiq (Amihud 2002 illiquidity) | Illiquid | Limits to arbitrage |
| Bid-Ask (Corwin & Schultz 2012) | Wide spread | Limits to arbitrage |

### 2.4 The Magnitude: Monday/Friday Accounts for >100% of Anomaly Returns

Birru (2018, Table 2) — Carhart four-factor alpha, monthly:

| Anomaly | Mon L–S | Fri L–S | Fri − Mon |
|---|---|---|---|
| Ivol | +1.049% | −0.581% | −1.630% |
| Price | +0.851% | −0.890% | −1.740% |
| FP | +1.071% | −0.555% | −1.627% |
| OP | +0.746% | −0.507% | −1.253% |
| Size | −0.335% | +0.885% | +1.221% |
| Bid-Ask | −0.839% | +0.934% | +1.773% |

For every one of the 19 anomalies the Monday and Friday long-short alphas have *opposite signs*, and the Tuesday–Thursday alphas are uniformly small. t-statistics typically run from 4 to 10. The economic content: Monday (or Friday, for the three inverted anomalies) accounts for >100% of the anomaly's total return — the other four days actively erode it.

### 2.5 The Four Falsification Tests Birru Uses to Rule Out Non-Sentiment Explanations

These are the tests that make Birru's paper persuasive, and each generates a prediction for the thesis.

**(a) Intraday vs. overnight decomposition (Birru 2018, Table 10; sample July 1992–Dec 2013 when CRSP open prices are available).** Return decomposition: `Intraday = (Close − Open) / Open`; `Overnight = Total − Intraday`. Finding: *all* day-of-week variation is intraday. No anomaly has a statistically significant Mon–Fri overnight difference at 5%. This rules out "weekend news accumulation" as the driver — if the crash were caused by information released over the weekend, it would be priced at Monday's open, not during Monday's trading session. **Prediction for IDX:** if the mechanism is the same, Monday-effect L–S returns should be intraday-only on IDX as well.

**(b) Holiday-adjacency tests (Birru 2018, Table 16).** If Monday is a holiday, the *first workday* (Tuesday) should behave like Monday; if Friday is a holiday, the *last workday* (Thursday) should behave like Friday. Pre-Thanksgiving Wednesdays (market closed Thu-Fri) should behave like Fridays. Results: 56 of 57 anomaly-day combinations go in the predicted direction. This is the cleanest possible test of "mood vs. ordinal day": the ordinal day doesn't care about holidays, but mood does. **Prediction for IDX:** Tuesdays after Indonesian public holidays (and IDX has many — Eid al-Fitr, Eid al-Adha, Christmas, Chinese New Year, Nyepi, Independence Day) should show Monday-like L–S patterns.

**(c) News exclusion (Birru 2018, Tables 8–9).** Re-run after excluding (i) macro announcement days (CPI, PPI, employment, FOMC) and (ii) firm-specific news days (earnings, M&A, management forecasts). Results are unchanged. This rules out the hypothesis that the Monday effect is a reaction to news that happens to cluster on Mondays.

**(d) Institutional ownership split (Birru 2018, Table 11).** Effect is stronger for stocks with *low* institutional ownership, consistent with a retail-sentiment story and inconsistent with an institutional-rebalancing story. **Prediction for IDX:** given IDX's large retail base (and growing), the mechanism should be powerful. Within IDX, the effect should be stronger among stocks favored by retail (which also tend to be the speculative-leg stocks — tight consistency).

### 2.6 Supporting Evidence: VIX and Treasuries

Birru (2018, Table 14). If sentiment falls on Monday, fear gauges should rise and safe-haven assets should rally:

- **VIX** rises +2.16% on average on Mondays and falls ~70 bp on Fridays.
- **Treasury returns** are highest on Mondays and lowest on Fridays across all maturities from 1 month to 5 years — ~4× the Friday level on 1-year Treasuries.

Both patterns are exactly what a flight-to-quality story predicts, and both are hard to explain under any non-sentiment story. For Indonesia, the natural analog would be IDR government bond returns (SUN) or IDX volatility index (IDXVOLA) — a worthwhile secondary check if the data are obtainable.

### 2.7 The Monotonicity Prediction: Tuesday–Thursday

Golder & Macy's mood curve is monotonic: Mon < Tue < Wed < Thu < Fri (for PA; NA mirror-image). Birru (2018, §5.1) confirms the return analogue: long-short anomaly returns monotonically fall (for short-leg speculative anomalies) or rise (for long-leg speculative anomalies) across the five days:

- Ivol L–S daily excess return: +22.6 bp Mon, +11.4 bp Tue, −5.9 bp Wed, −7.9 bp Thu, −15.1 bp Fri.
- Size L–S daily excess return: −8.3 bp Mon, −6.8 bp Tue, +0.4 bp Wed, +10.5 bp Thu, +20.7 bp Fri.

This rules out a "Monday is special" story in favor of a "mood is a continuous function of the work/rest cycle" story. **Prediction for IDX:** monotonic (not step) Mon→Fri pattern in speculative-leg L–S returns.

### 2.8 The Mood-Beta Extension (Hirshleifer, Jiang & Zhang 2020, *JFE*)

Hirshleifer, Jiang & Zhang (2020) extend Birru by showing that stocks exhibiting high sensitivity to *past* mood fluctuations also exhibit high sensitivity to *future* mood fluctuations — i.e., "mood beta" is a persistent stock characteristic. This is the natural extension of Pillar 1 + Pillar 2: certain stocks are *structurally* the recipients of mood-driven flow, and the set of such stocks is precisely Baker & Wurgler's speculative-characteristic bundle. The thesis could (as a future extension) estimate a mood beta for each IDX stock by regressing individual-stock returns on weekend-timing dummies in a rolling window, and then test whether mobile adoption tightened the relationship between mood beta and expected-return dispersion.

### 2.9 Why the *Aggregate* Monday Effect Weakens Even When Mood Is Constant

Birru (2018, §4.2) emphasizes a point that is critical to the thesis' pre/post Indonesian design:

> "While a decrease in sentiment will lead to a decline in prices for speculative stocks, it can also lead to a flight to quality, causing the prices of safe stocks to increase. As a result, sentiment predictions are clearest in the cross-section."
> — paraphrasing Baker & Wurgler (2007)

So: (i) the aggregate Monday effect can vanish while the cross-sectional Monday effect persists; (ii) conversely, the aggregate Monday effect can *intensify* (as the thesis hypothesizes for IDX post-2017) if the composition of the marginal investor shifts toward noise traders who lack the offsetting flight-to-quality reflex. The *direction* of the aggregate prediction is not pinned down a priori by mood theory alone — it depends on the relative masses of sentimental and flight-to-quality-seeking investors, which is precisely what the mobile revolution is hypothesized to change.

---

## Pillar 3: Limits to Arbitrage — Why the Mispricing Isn't Corrected

Without formal limits to arbitrage, Pillars 1 and 2 cannot survive: a sufficiently deep-pocketed rational trader would arbitrage away the Monday/Friday spread. The literature supplies two distinct constraints.

### 3.1 Noise Trader Risk (De Long, Shleifer, Summers & Waldmann 1990, *JPE*)

The DSSW (1990) model's key insight: a rational arbitrageur who bets against noise traders bears **noise trader risk** — the risk that sentiment becomes *more* irrational in the short term before it reverts. If the arbitrageur has a finite horizon (forced to mark-to-market, subject to client redemptions, constrained by margin), this risk is priced, and arbitrage is limited even in expectation. The model's equilibrium prediction is that securities with greater noise-trader exposure earn higher unconditional expected returns — consistent with the "low-volatility" and related anomalies.

**Relevance for IDX.** The mobile revolution (Pillar 4) directly increases the noise-trader mass. By DSSW, this should:
- Raise the noise-trader risk premium on speculative stocks (higher expected returns on paper, but also higher dispersion).
- Widen the volatility of mispricing without eliminating it — meaning the *amplitude* of the Monday/Friday spread can increase.

### 3.2 Synchronization and Horizon Risk (Shleifer & Vishny 1997, *JF*)

> Note: the prior version of this document mis-cited this paper as "Abtruse & Vishny (1997)." The correct citation is Shleifer & Vishny (1997), "The Limits of Arbitrage," *Journal of Finance* 52(1): 35–55.

Shleifer & Vishny (1997) formalize the principal-agent problem between arbitrageurs and their capital providers. When an arbitrage position moves against them, capital is withdrawn precisely when it should be added (performance-chasing client behavior). The implications: (i) arbitrageurs *cannot* scale into a losing position even when the expected return is most attractive; (ii) this creates a *synchronization problem* — arbitrageurs know others face the same constraint, so nobody wants to be early; (iii) in the limit, a persistent irrational mispricing is sustained. Abreu & Brunnermeier (2002, 2003) formalize the synchronization problem as a timing game; the equilibrium is delayed, partial, and fragile arbitrage.

**Relevance for IDX.** Indonesian institutional infrastructure is weak relative to the US. The *Bursa Efek Indonesia* (IDX) has (a) short-sale restrictions (only a list of designated liquid stocks are eligible, OJK Regulation IX.A.7; implementation remains patchy post-2015 overhaul), (b) no deep equity derivatives market, (c) no well-developed prime brokerage, and (d) small domestic institutional capital base relative to retail flow. Every one of these *amplifies* Shleifer–Vishny frictions. The specific prediction: Pillar 1 + Pillar 2 mispricing will be larger in IDX than in the US of comparable date, and will persist across the full sample rather than decay toward zero.

### 3.3 Emerging-Market Specific Frictions (Bekaert, Harvey & Lundblad 2007; Harvey 1995)

Bekaert, Harvey & Lundblad (2007, *RFS*; NBER WP 11413) document that liquidity (measured as transformed proportion of zero-return days) significantly predicts returns in emerging markets even after market liberalization. Harvey (1995) finds that emerging-market returns exhibit predictability patterns *orthogonal* to the developed-market factor structure, with local information dominating. Two implications:

1. The Fama–French factor structure imported from the US may not span the IDX risk space, which is why the thesis correctly avoids an FF3/Carhart alpha apparatus and uses CAPM-on-JCI plus market-adjusted returns as robustness (see `papers/birru_econometric_specifications.md` §9).
2. *Illiquidity itself* is a risk factor in emerging markets, so the Amihud/bid-ask anomalies (Birru's three "long-leg speculative" anomalies) may behave differently on IDX than in Birru's sample — this is a built-in robustness check, not a weakness.

---

## Pillar 4: The Mobile Revolution — Delivery Mechanism for Sentiment

Pillars 1–3 describe a mechanism. Pillar 4 describes the *shock* that the Indonesian thesis exploits — the change in noise-trader mass and attention technology that alters the amplitude of the mechanism from 2017 onwards.

### 4.1 The KSEI Investor Demographics Shift (2012–2024)

Single Investor Identification (SID) counts from the Indonesia Central Securities Depository (KSEI):

| Year | SIDs | Context |
|---|---|---|
| 2012 | ~281,000 | Pre-mobile baseline |
| 2016 | 894,116 | — |
| 2017 | >1,000,000 | Launch year for key mobile apps (Ajaib 2018; Stockbit grew aggressively 2017–19) |
| 2020 | ~3,100,000 | COVID retail boom |
| 2023 | 7,000,000+ | — |
| 2024 | ~10,000,000 | ≈60% of investors aged 18–35 |

This is a ~35× expansion of the investor base over 12 years, concentrated in cohorts with the demographic and technological profile of sentiment-driven noise traders.

### 4.2 Attention-Induced Trading (Barber & Odean 2008, *RFS*)

Barber & Odean (2008) document that individual investors are net buyers of *attention-grabbing* stocks (top gainers, top losers, high-volume). The mechanism: when faced with thousands of tradeable stocks, retail investors satisfice by choosing from the small set that happens to grab attention that day. They do not face the same problem on the sell side (they sell only what they already own), which creates an asymmetry — attention drives net buying pressure.

Mobile trading apps *engineer* attention deliberately. Ajaib, Stockbit, Bibit, IPOT, MotionTrade and similar Indonesian platforms feature:
- "Top Gainers" / "Top Losers" leaderboards (direct Barber-Odean channel).
- "Most Traded" / volume leaders (another attention signal).
- Social streams with influencer commentary (information cascades, meme dynamics).
- Push notifications, streak gamification, and portfolio-performance dashboards.
- Frictionless account opening and low/zero minimums.

Each feature is an attention-intensifier pointed squarely at the speculative conduits — the MAX, high-volatility, low-price, young stocks that Baker & Wurgler identify. The prediction: post-2017 IDX Monday effects should concentrate in exactly the anomalies most sensitive to retail attention flow.

### 4.3 Smartphone Trading Effects (Gao & Huang 2020; Kalda, Loos, Previtero & Hackethal 2021)

Smartphone-trading studies — Gao & Huang (2020) and the within-investor identification design of Kalda, Loos, Previtero & Hackethal — use within-investor variation — an investor who adopts a mobile app can be compared to his own pre-adoption behavior — and find that smartphone adoption leads to:
- More trading overall (higher turnover).
- A shift toward lottery-like and attention-driven trades.
- *Lower* risk-adjusted returns for the smartphone-executed portion of the portfolio.
- Thicker tails — higher participation in extreme return stocks.

Taken with the Barber–Odean attention mechanism, this literature gives a precise micro-foundation for why the mobile revolution should *amplify* rather than eliminate the Monday effect. Efficient markets would predict elimination (more participants, more arbitrage); attention-driven noise-trading predicts amplification (more speculative flow aimed at the same speculative conduits).

### 4.4 The Robinhood Comparison (Barber, Huang, Odean & Schwartz 2022, *JF*)

Barber et al. (2022) examine Robinhood user flows and find strong herding: thousands of users pile into the same small set of names on the same days, and the subsequent return pattern is negative. The closest Indonesian equivalent is Stockbit's social feed and Ajaib's community-ranked lists. The Robinhood mechanism is a specific micro-foundation for why the mobile-era Monday effect may be driven by a small set of highly-attention-captured names, which in turn suggests sorting IDX stocks by a *retail-attention* proxy (Google Trends for ticker, social-media mention count, relative volume shock) as a robustness complement to the Birru speculative characteristics.

### 4.5 The Paradox of Access (Thesis Synthesis)

Three theoretical traditions converge on the prediction that the mobile revolution should *amplify* the Monday effect on IDX:

1. **DSSW (1990):** more noise traders ⇒ more price impact of noise ⇒ larger mispricing amplitude.
2. **Baker & Wurgler (2006):** sentiment mispricing concentrates in the speculative bundle; the mobile investor is the canonical "hard-to-value-hard-to-arbitrage" habitat's natural customer.
3. **Barber & Odean (2008) / Gao & Huang (2020):** attention gamification funnels retail flow into speculative names, not uniformly across the cross-section.

The counter-hypothesis (that the mobile revolution would shrink the Monday effect via increased aggregate participation and faster arbitrage) requires (a) the marginal new investor to be sophisticated *and* arbitrage-capacity-adding, and (b) the institutional arbitrage infrastructure to have kept pace with the retail shock. Both assumptions are weak in the Indonesian context (Pillar 3.3), which is why the thesis' primary hypothesis is *amplification*.

---

## Pillar 5: The Aggregate Weekend Effect — History and Its Disappearance

### 5.1 The US Aggregate Finding (1970s–1990s literature)

Cross (1973), French (1980, *JFE*), and Gibbons & Hess (1981, *JFQA*) established that US aggregate market returns on Mondays are systematically negative. French (1980) found mean Monday returns of −0.17% on the S&P 500, 1953–1977, against positive means on all other days. The early literature canvassed and rejected institutional explanations: settlement timing (Lakonishok & Levi 1982 — too small to account for the magnitude; Dyl & Martin 1985 — insufficient), specialist behavior and measurement error (Keim & Stambaugh 1984 — refuted), short-selling activity (Blau, Van Ness & Van Ness 2009 — no short-selling spike on Mondays; Gao, Hao, Kalcheva & Ma 2015 — weekend effect exists in Hong Kong even before short-selling was legal).

### 5.2 The Disappearance in the US Post-1975

Robins & Smith (2016, *Critical Finance Review*) "No More Weekend Effect" documents that the aggregate US weekend effect has been indistinguishable from zero since roughly 1975. Olson, Mossman & Chou (2015, *QREF*) apply cointegration and breakpoint analysis and conclude that the US Monday differential has been mean-reverting toward zero since 1975, with the disappearance appearing within about two years of Cross (1973)'s publication — consistent with an efficient-markets adjustment to the anomaly's discovery.

This is itself important: the Monday effect is empirically a *perishable* anomaly in developed markets. But Birru's point (Pillar 2) is that the cross-sectional version persists because its mechanism is structural (mood + speculative-characteristic geography) rather than an exploitable aggregate trading rule.

### 5.3 The Indonesian Puzzle: Contested Evidence

| Study | Period | Method | Aggregate Monday effect? |
|---|---|---|---|
| Khan et al. (2023) | 2013–2019 | OLS, GARCH(1,1), Kruskal–Wallis | Yes |
| Suryanegara et al. (2024) | 2017–2022 | ANOVA | No |
| Emerald (2024) | 2000–2022 | GJR-GARCH | Only in the Islamic index (JII) |
| LQ45 COVID study | COVID era | OLS | No |

The contested Indonesian finding *is the thesis' opportunity.* If the aggregate Monday effect is strong 2012–2016 and weak or absent 2017–2024, the disappearance (interpreted through Pillar 2.9) may reflect the flight-to-quality cancellation — the mobile-era noise traders push speculative stocks down *and* institutional money flees to safe stocks up, canceling at the index level while the cross-section widens. If the aggregate Monday effect *strengthens* post-2017, the mobile investor is not balanced by an institutional flight-to-quality, and DSSW amplification dominates. **Either outcome is consistent with Pillars 1–4**, and the distinction between them is the central empirical question.

---

## Pillar 6: Indonesian Institutional Detail

### 6.1 Trading-Hour Asymmetries

Historical IDX trading sessions (pre-COVID):
- Mon–Thu: 09:00–12:00, 13:30–15:49 (~5.3 hours)
- Fri: 09:00–11:30, 14:00–15:49 (~4.3 hours, shorter for Friday prayers)

Post-COVID (2020 onwards): simplified 09:00–15:00 continuous session.

Implication: Friday has ~20% fewer trading hours pre-COVID. This is a *structural* asymmetry, not a sentiment effect. The Friday coefficient interpretation must be made relative to this mechanical constraint. The Monday interpretation is unaffected because Mondays have full trading hours in every era. This also argues for focusing the thesis on the *Monday* coefficient rather than the Friday–Monday difference, as Birru does for the US.

### 6.2 Settlement Cycle Change (26 Nov 2018, T+3 → T+2)

The T+3 → T+2 change falls within the post-period. Settlement-risk-based explanations of the weekend effect (Lakonishok & Levi 1982) would predict a step change at the cutover date. A robustness check: add a T+2 dummy and test for a discrete break on 26 Nov 2018, or estimate a three-regime model (pre-2017, 2017–Nov-2018, post-Nov-2018). If settlement is the driver, the Mon × Post interaction should be concentrated in one sub-regime.

### 6.3 Short-Sale Restrictions (OJK Regulation IX.A.7)

Short-selling in Indonesia is permitted only for a designated list of stocks (updated periodically by OJK and IDX), requires prior margin/securities-lending relationships, and is effectively unavailable to retail investors. The arbitrage constraint is *binding* for the speculative-leg stocks that Pillars 1–2 identify as sentiment conduits, which is exactly the condition Baker & Wurgler's arbitrage-channel mechanism requires.

### 6.4 The Islamic-Index Subsample (JII)

Emerald (2024)'s GJR-GARCH finding that the Monday effect appears in JII but not JCI is provocative. JII constituents are screened for compliance with *sharia* — excluding financials (no interest), highly leveraged firms, and certain "impure" sectors. The residual is a relatively clean "non-financial, low-leverage, conservative-accounting" subsample. This may be a natural robustness test for the thesis: the cross-sectional Monday effect should survive the JII screen (no banks is not a speculative-vs-safe issue), which would be a clean falsification target if it doesn't.

---

## Pillar 7: Bibliography (By Pillar)

### Cross-Section of Sentiment (Pillar 1)
- Baker, M., & Wurgler, J. (2006). Investor sentiment and the cross-section of stock returns. *Journal of Finance*, 61(4), 1645–1680.
- Baker, M., & Wurgler, J. (2007). Investor sentiment in the stock market. *Journal of Economic Perspectives*, 21(2), 129–151.
- Baker, M., Bradley, B., & Wurgler, J. (2011). Benchmarks as limits to arbitrage: Understanding the low-volatility anomaly. *Financial Analysts Journal*, 67(1), 40–54.
- Baker, M., Wurgler, J., & Yuan, Y. (2012). Global, local, and contagious investor sentiment. *Journal of Financial Economics*, 104(2), 272–287.
- Lee, C. M. C., Shleifer, A., & Thaler, R. H. (1991). Investor sentiment and the closed-end fund puzzle. *Journal of Finance*, 46(1), 75–109.
- Kumar, A. (2009). Who gambles in the stock market? *Journal of Finance*, 64(4), 1889–1933.
- Kumar, A., & Lee, C. M. C. (2006). Retail investor sentiment and return comovements. *Journal of Finance*, 61(5), 2451–2486.

### Day-of-Week / Mood (Pillar 2)
- Birru, J. (2018). Day of the week and the cross-section of returns. *Journal of Financial Economics*, 130(1), 182–214.
- Golder, S. A., & Macy, M. W. (2011). Diurnal and seasonal mood vary with work, sleep, and daylength across diverse cultures. *Science*, 333(6051), 1878–1881.
- Stone, A. A., Schneider, S., & Harter, J. K. (2012). Day-of-week mood patterns in the United States. *Journal of Positive Psychology*, 7(4), 306–314.
- Hirshleifer, D., Jiang, D., & Zhang, Y. (2020). Mood beta and seasonalities in stock returns. *Journal of Financial Economics*, 137(1), 272–295.
- Watson, D. (2000). *Mood and temperament.* Guilford Press.
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.
- Clore, G. L., Schwarz, N., & Conway, M. (1994). Affective causes and consequences of social information processing. In *Handbook of Social Cognition*.
- Kamstra, M. J., Kramer, L. A., & Levi, M. D. (2003). Winter blues: A SAD stock market cycle. *American Economic Review*, 93(1), 324–343.

### Limits to Arbitrage (Pillar 3)
- De Long, J. B., Shleifer, A., Summers, L. H., & Waldmann, R. J. (1990). Noise trader risk in financial markets. *Journal of Political Economy*, 98(4), 703–738.
- Shleifer, A., & Vishny, R. W. (1997). The limits of arbitrage. *Journal of Finance*, 52(1), 35–55.
- Abreu, D., & Brunnermeier, M. K. (2002). Synchronization risk and delayed arbitrage. *Journal of Financial Economics*, 66(2–3), 341–360.
- Abreu, D., & Brunnermeier, M. K. (2003). Bubbles and crashes. *Econometrica*, 71(1), 173–204.
- Wurgler, J., & Zhuravskaya, E. (2002). Does arbitrage flatten demand curves for stocks? *Journal of Business*, 75(4), 583–608.

### Mobile / Attention (Pillar 4)
- Barber, B. M., & Odean, T. (2008). All that glitters: The effect of attention and news on the buying behavior of individual and institutional investors. *Review of Financial Studies*, 21(2), 785–818.
- Gao, M., & Huang, J. (2020). The effects of smartphone trading on stock returns. *Journal of Financial and Quantitative Analysis* (as cited in the project's methodology notes). See also Kalda, A., Loos, B., Previtero, A., & Hackethal, A. (2021). Smart(Phone) Investing? *Working Paper* — for the within-investor identification design on smartphone-adoption effects.
- Barber, B. M., Huang, X., Odean, T., & Schwartz, C. (2022). Attention-induced trading and returns: Evidence from Robinhood users. *Journal of Finance*, 77(6), 3141–3190.
- Bali, T. G., Cakici, N., & Whitelaw, R. F. (2011). Maxing out: Stocks as lotteries and the cross-section of expected returns. *Journal of Financial Economics*, 99(2), 427–446.

### Aggregate DOW and Its Disappearance (Pillar 5)
- Cross, F. (1973). The behavior of stock prices on Fridays and Mondays. *Financial Analysts Journal*, 29(6), 67–69.
- French, K. R. (1980). Stock returns and the weekend effect. *Journal of Financial Economics*, 8(1), 55–69.
- Gibbons, M. R., & Hess, P. (1981). Day of the week effects and asset returns. *Journal of Business*, 54(4), 579–596.
- Robins, R. P., & Smith, G. P. (2016). No more weekend effect. *Critical Finance Review*, 5(2), 417–424.
- Olson, D., Mossman, C., & Chou, N.-T. (2015). The evolution of the weekend effect in US markets. *Quarterly Review of Economics and Finance*, 58, 56–63.
- Plastun, A., Sibande, X., Gupta, R., & Wohar, M. E. (2019). Rise and fall of calendar anomalies over a century. *North American Journal of Economics and Finance*, 49, 181–205.

### Emerging Markets (Pillar 5 / 6)
- Harvey, C. R. (1995). Predictable risk and returns in emerging markets. *Review of Financial Studies*, 8(3), 773–816.
- Bekaert, G., Harvey, C. R., & Lundblad, C. (2007). Liquidity and expected returns: Lessons from emerging markets. *Review of Financial Studies*, 20(6), 1783–1831. (Earlier version: NBER WP 11413, 2005.)
- Khan, K., et al. (2023). Day-of-the-week effect and market liquidity in Asia. *International Journal of Finance & Economics*.
- Suryanegara, Y. T., et al. (2024). Monday effect on IDX before and during COVID-19. *Diponegoro International Journal of Business*.
- Chiah, M., & Zhong, A. (2019). Day-of-week effect in anomaly returns: International evidence. *Economics Letters*, 182, 106–108.

### Methodology (ancillary — see `papers/methodology_research.md` for full treatment)
- Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.
- Petersen, M. A. (2009). Estimating standard errors in finance panel data sets. *Review of Financial Studies*, 22(1), 435–480.
- Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust inference with multiway clustering. *Journal of Business & Economic Statistics*, 29(2), 238–249.
- Andrews, D. W. K. (1993). Tests for parameter instability and structural change with unknown change point. *Econometrica*, 61(4), 821–856.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). ...and the cross-section of expected returns. *Review of Financial Studies*, 29(1), 5–68.
- Sullivan, R., Timmermann, A., & White, H. (2001). Dangers of data mining: The case of calendar effects in stock returns. *Journal of Econometrics*, 105(1), 249–286.
- Winkelried, D., & Iberico, L. A. (2018). Calendar effects in Latin American stock markets. *Empirical Economics*, 54(3), 1215–1235.

---

## Appendix: What the Empirical Design Actually Tests

To make the mechanism→prediction chain explicit:

| Pillar | Prediction | Where it is tested in the empirical design |
|---|---|---|
| 1 (B&W cross-section) | Speculative-leg stocks (high Ivol, high Max, low Age, low Price, high Beta, non-dividend-payers) earn lower Monday returns than safe-leg counterparts. | `scripts/02_run_portfolio_analysis.py` quintile sorts on each characteristic; `config.py` encodes the speculative direction for each. |
| 1 (sign-flip) | The cross-sectional conditional characteristic effect may have opposite sign in pre vs. post, even if the unconditional level is similar. | Pre/post separate estimation; triple interaction Mon × Spec × Post in panel spec. |
| 2 (Birru mood) | Monday L–S > 0 for short-leg-speculative anomalies; Friday L–S < 0; monotone decline across the week. | Day-specific monthly L–S returns in `regression.py`; daily panel monotonicity check. |
| 2 (intraday) | Monday effect is intraday, not overnight. | Robustness test requiring open-to-close and close-to-open return decomposition; currently a planned extension if IDX open prices are obtainable. |
| 2 (holiday) | Tuesdays after Indonesian public holidays behave like Mondays. | Holiday-adjacency dummy regression; 56/57 rule as an informal benchmark. |
| 2 (institutional) | Effect is stronger in low-institutional-ownership stocks. | Stock-level panel split on `institutional_ownership` variable (from notebooks `03_fetch_institutional_ownership.ipynb`). |
| 3 (limits to arbitrage) | The Indonesian effect should *persist* across subperiods, even though the US aggregate effect vanished post-1975. | Full-sample aggregate regression + both pre and post OLS confirm persistence. |
| 4 (mobile amplification) | Monday × Post interaction is negative and large in magnitude on the aggregate; triple interaction with speculativeness is large in the panel. | `regression.py` interaction specs; rolling 252-day Monday β plot showing dynamic evolution. |
| 5 (composition) | Results hold on the balanced-panel subsample of 525 stocks present in both pre and post, ruling out "new mobile-era IPOs are mechanically more speculative." | Balanced-panel regression in Part C, `methodology_research.md` §Part C. |
| 6 (institutional detail) | T+2 robustness dummy, JII subsample check, trading-hour asymmetry caveat on Friday. | Robustness section; Friday coefficient interpreted with explicit trading-hour caveat. |

The thesis' single-sentence contribution: *Baker & Wurgler tell us where in the cross-section sentiment bites; Birru tells us when during the week it bites; the mobile revolution tells us how hard it bites in Indonesia post-2017; and the limits-to-arbitrage literature tells us why an emerging-market exchange never corrects it.*
