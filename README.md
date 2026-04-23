# Honors Proposal TSX

This repository is for sensitive Honors-level academic research. Every decision made by an AI MUST be explained clearly before being executed. This includes:

- **What** is being changed.
- **How** the implementation works.
- **Why** this specific approach is necessary and how it respects the **Birru (2018)** statistical methodology.

See `CLAUDE.md` and `GEMINI.md` for the full set of interaction protocols.

## Project Structure
```text
Honors/
├── final_proposal_code/
│   ├── scripts/
│   │   ├── 01_prepare_panel.py           # Step 1: Data prep & lagging
│   │   ├── 02_run_portfolio_analysis.py  # Step 2: Birru (2018) analysis
│   │   ├── 03_generate_visuals.py        # Step 3: Charts & visualization
│   │   └── cs_utils/                     # Core analysis logic
│   ├── data/                             # Large CSV files (gitignored)
│   ├── notebooks/                        # Data download notebooks
│   └── output/                           # Results & LaTeX tables
├── final_paper/                          # Thesis LaTeX source
├── papers/                               # Literature library
└── deprecated/                           # Archived investigative scripts/data
```


## Edit content

Open `HonorsProposal.tsx` and modify the `content` object at the top:

- `titleMain` and `titleSubtitle` control the title
- `sections.intro` and `sections.literature` are plain text. Use a blank line to start a new paragraph.
- `sections.references` is an array of reference strings; each entry becomes a numbered list item.
