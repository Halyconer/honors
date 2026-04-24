# Anomaly Behavior Analysis: Decoding the IDX Results

This document provides the high-precision interpretation of each anomaly, aligned with **Birru (2018)** and **Baker & Wurgler (2006)**.

---

## 1. The "Star" Anomalies: MAX, IVOL, and Age
These characteristics behave **exactly** as the Birru (2018) "Mood Mechanism" predicts.

### 1.1 MAX (Lottery-like Returns)
*   **Result:** Strong Monday Spread.
*   **Intuition:** High MAX stocks are the quintessential "retail vessels." They are visible, exciting, and gamblers chase them on Monday mornings (Kumar, 2009). The Monday crash is the reversal of this weekend-built sentiment.

### 1.2 Age (The Young Stock Anomaly)
*   **Result:** The most dramatic shift post-2017.
*   **Intuition:** Younger stocks have the shortest earnings history, making them the most "unanchored" (B&W, 2006). They are most sensitive to the influx of new retail investors who trade on "stories" rather than history.

---

## 2. Correcting the BM and Size Logic
*Correction: Previous analyses misidentified the speculative direction of BM. This has been corrected in `config.py`.*

### 2.1 The BM Ratio (Value vs. Growth)
*   **Speculative Leg:** **Low-BM (Growth/Glamour)**.
*   **Mechanism:** Growth stocks have high "Sentiment Betas" because their value is derived from future, high-variance growth. 
*   **Observation:** In our corrected run, the "Safe minus Speculative" spread (High-BM minus Low-BM) should be **positive on Mondays**, matching the Birru effect. If it remains negative, it suggests a unique "Growth-bias" in the Indonesian retail market.

### 2.2 Size (Small vs. Large)
*   **Speculative Leg:** **Small Size**.
*   **Mechanism:** Small stocks are the "natural habitat" of retail investors and the most difficult for institutions to arbitrage.
*   **The Sign Logic:** Since we use `Safe - Speculative` (Large - Small), a positive coefficient on Monday confirms the theory (Small stocks underperform Large stocks).

---

## 3. The 2017 "Mobile Revolution" Interaction
Your thesis focuses on whether the **Monday Spread** increased after 2017.

| Characteristic | Mechanism for Amplification |
| :--- | :--- |
| **MAX** | Mobile apps highlight "Top Gainers," making MAX stocks even more visible to noise traders. |
| **Age** | A surge in Tech IPOs post-2017, combined with mobile access, channeled retail sentiment into younger stocks. |
| **IVOL** | Lower barriers to entry attracted "gamblers" who favor high-volatility stocks, widening the Monday mood-driven spread. |

---

## 4. Discussion: Why Dividends and ROA are Muted
*   **Information Frequency:** MAX and IVOL change daily. ROA and Dividends change annually.
*   **Retail Focus:** A mobile trader is more likely to be influenced by a stock's "Lottery" status (MAX) than its "Accounting Profitability" (ROA). This explains why price-based anomalies show a stronger "Mobile Revolution" break than accounting-based ones.
