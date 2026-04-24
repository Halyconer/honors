# IDX Monday Effect: Mobile Trading Revolution Study

This repository investigates whether Indonesia's mobile trading revolution (beginning c. 2017) amplified or diminished the **Monday Effect** on the Jakarta Stock Exchange (IDX).

The analysis is heavily based on the methodology of **Birru (2018)**; this analysis implements his methodology on Indonesia with the added complexity of structural breaks in retail investor participation.

---

## Execution Workflow

The project follows a strict sequential pipeline to ensure data integrity and prevent look-ahead bias.

### Phase 1: Data Acquisition (Jupyter Notebooks)

Before running any analysis, raw data must be fetched from Refinitiv.

1.  `notebooks/01_fetch_daily_prices.ipynb`: Downloads daily adjusted prices and volume for all IDX instruments (2008–2024).
2.  `notebooks/02_fetch_fundamentals.ipynb`: Downloads monthly fundamental data (Market Cap, ROA, BVPS).
3.  `notebooks/03_fetch_institutional_ownership.ipynb`: Downloads foreign vs. domestic ownership percentages.

### Phase 2: Data Preparation

Consolidates raw chunks into a unified analysis panel.

- **Command:** `python scripts/01_prepare_panel.py`
- **Logic:**
  - Cleans and winsorizes daily returns.
  - Calculates speculative characteristics (IVOL, MAX, Size, Foreign Ownership %).
  - **The Birru Lag:** Characteristics measured at month $T-1$ are mapped to portfolio returns in month $T$ to avoid look-ahead bias.

### Phase 3: Portfolio Analysis & Regression

Tests the Monday Effect hypothesis and structural breaks.

- **Command:** `python scripts/02_run_portfolio_analysis.py`
- **Logic:**
  - Sorts stocks into deciles based on speculative characteristics.
  - Constructs "Speculative Minus Safe" (SMS) spread portfolios.
  - Runs day-of-the-week regressions with **Newey-West (HAC)** standard errors.
  - Implements the **2017 Structural Break** dummy and the **Bai-Perron** discovery test.

### Phase 4: Visualization & LaTeX Output

Generates publication-ready artifacts.

- **Command:** `python scripts/03_generate_visuals.py`
- **Logic:**
  - Produces return histograms and decile performance charts.
  - Exports regression results directly to LaTeX tables for the final paper.

---

## Setup

1.  **Environment:**
    ```bash
    source ./final_proposal_code/venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Configuration:**
    - Global settings (filters, financial stock exclusions) are managed in `scripts/cs_utils/config.py`.

---

## Theoretical Foundation

See `theoretical_framework_plan.md` for a detailed breakdown of the behavioral finance logic (Birru 2018, Baker & Wurgler 2006) and the justification for the IDX "Mobile Revolution" hypothesis.
