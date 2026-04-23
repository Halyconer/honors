"""
Results formatting: terminal tables and LaTeX output.
"""

from .config import CHARS, TABLE_COLS


def stars(t):
    at = abs(t)
    if at > 2.576: return "***"
    if at > 1.96:  return "**"
    if at > 1.645: return "*"
    return ""


def _get_alpha_t(results, char_name, day_group, leg):
    """Extract alpha (bps) and t-stat from results dict."""
    obj, n = results.get((char_name, day_group, leg), (None, 0))
    if obj is None:
        return None, None
    return obj.params["const"] * 10_000, obj.tvalues["const"]


def print_panel(results, title, leg):
    """Print one panel of the terminal results table."""
    print(f"\n  {title}")
    header = f"  {'':13s}"
    for d in TABLE_COLS:
        header += f"  {d:>12s}"
    print(header)
    print("  " + "-" * 52)

    for char_name in CHARS:
        row_alpha = f"  {char_name:13s}"
        row_t     = f"  {'':13s}"
        for day_group in TABLE_COLS:
            a, t = _get_alpha_t(results, char_name, day_group, leg)
            if a is not None:
                row_alpha += f"  {a:>9.1f}{stars(t):3s}"
                row_t     += f"  {'(' + f'{t:.2f}' + ')':>12s}"
            else:
                row_alpha += f"  {'':>12s}"
                row_t     += f"  {'':>12s}"
        print(row_alpha)
        print(row_t)


def print_results(results):
    """Print all three panels to terminal."""
    print("\n" + "=" * 60)
    print("  Excess Returns (bps/month), Equal-Weighted")
    print("  Newey-West HAC t-stats in parentheses")
    print("=" * 60)

    print_panel(results, "Panel A: L-S (Safe minus Speculative)", "LS")
    print_panel(results, "\n  Panel B: Speculative Leg", "Spec")
    print_panel(results, "\n  Panel C: Safe Leg", "Safe")

    print("\n" + "=" * 60)


def print_results_capm(results):
    """Print all three panels for CAPM alphas (full-month MktRF)."""
    print("\n" + "=" * 60)
    print("  CAPM Alphas — Full-Month MktRF (bps/month)")
    print("  Birru Table 2 primary specification")
    print("  Newey-West HAC t-stats in parentheses")
    print("=" * 60)

    print_panel(results, "Panel A: L-S (Safe minus Speculative)", "LS")
    print_panel(results, "\n  Panel B: Speculative Leg", "Spec")
    print_panel(results, "\n  Panel C: Safe Leg", "Safe")

    print("\n" + "=" * 60)


def print_results_capm_decomp(results):
    """Print all three panels for day-decomposed CAPM alphas."""
    print("\n" + "=" * 60)
    print("  CAPM Alphas — Day-Decomposed MktRF (bps/month)")
    print("  Birru Table 6 robustness specification")
    print("  Newey-West HAC t-stats in parentheses")
    print("=" * 60)

    print_panel(results, "Panel A: L-S (Safe minus Speculative)", "LS")
    print_panel(results, "\n  Panel B: Speculative Leg", "Spec")
    print_panel(results, "\n  Panel C: Safe Leg", "Safe")

    print("\n" + "=" * 60)


# ── LaTeX ─────────────────────────────────────────────────────────────

def _latex_panel(results, title, leg):
    """Generate LaTeX rows for one panel."""
    rows = []
    n_cols = len(TABLE_COLS)
    rows.append(rf"\multicolumn{{{n_cols + 1}}}{{l}}{{\textit{{{title}}}}} \\")
    for char_name in CHARS:
        alpha_cells = []
        t_cells = []
        for day_group in TABLE_COLS:
            a, t = _get_alpha_t(results, char_name, day_group, leg)
            if a is not None:
                s = stars(t)
                alpha_cells.append(f"${a:.1f}{s}$")
                t_cells.append(f"$({t:.2f})$")
            else:
                alpha_cells.append("")
                t_cells.append("")
        rows.append(rf"{char_name} & {' & '.join(alpha_cells)} \\")
        rows.append(rf" & {' & '.join(t_cells)} \\")
    return rows


def save_latex(results, output_path):
    """Save LaTeX table with all three panels (booktabs formatting)."""
    n_cols = len(TABLE_COLS)
    col_spec = "l" + " c" * n_cols

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{Day-of-Week Excess Returns by Speculative Characteristic (bps/month)}")
    lines.append(r"\label{tab:dow_excess_returns}")
    lines.append(r"\footnotesize")
    lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\toprule")
    header_cells = " & ".join(TABLE_COLS)
    lines.append(rf" & {header_cells} \\")
    lines.append(r"\midrule")

    lines.extend(_latex_panel(results, r"Panel A: L--S (Safe $-$ Speculative)", "LS"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel(results, "Panel B: Speculative Leg", "Spec"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel(results, "Panel C: Safe Leg", "Safe"))

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\vspace{4pt}")
    lines.append(r"\begin{minipage}{0.9\textwidth}")
    lines.append(r"\footnotesize")
    lines.append(r"Value-weighted quintile portfolios. Newey--West HAC $t$-statistics in parentheses.")
    lines.append(r"$^{*}p<0.10$;\quad $^{**}p<0.05$;\quad $^{***}p<0.01$")
    lines.append(r"\end{minipage}")
    lines.append(r"\end{table}")

    output_path.write_text("\n".join(lines))
    print(f"\nLaTeX saved to {output_path}")


def save_latex_capm(results, output_path):
    """Save LaTeX table for CAPM alphas."""
    n_cols = len(TABLE_COLS)
    col_spec = "l" + " c" * n_cols

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{Day-of-Week CAPM Alphas by Speculative Characteristic (bps/month)}")
    lines.append(r"\label{tab:dow_capm_alphas}")
    lines.append(r"\footnotesize")
    lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\toprule")
    header_cells = " & ".join(TABLE_COLS)
    lines.append(rf" & {header_cells} \\")
    lines.append(r"\midrule")

    lines.extend(_latex_panel(results, r"Panel A: L--S (Safe $-$ Speculative)", "LS"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel(results, "Panel B: Speculative Leg", "Spec"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel(results, "Panel C: Safe Leg", "Safe"))

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\vspace{4pt}")
    lines.append(r"\begin{minipage}{0.9\textwidth}")
    lines.append(r"\footnotesize")
    lines.append(r"Value-weighted quintile portfolios. CAPM alpha using full-month JCI market excess return.")
    lines.append(r"Newey--West HAC $t$-statistics in parentheses.")
    lines.append(r"$^{*}p<0.10$;\quad $^{**}p<0.05$;\quad $^{***}p<0.01$")
    lines.append(r"\end{minipage}")
    lines.append(r"\end{table}")

    output_path.write_text("\n".join(lines))
    print(f"\nLaTeX saved to {output_path}")


# ── Split-sample formatting ───────────────────────────────────────────

def _get_alpha_t_param(results, char_name, day_group, leg, param="const"):
    """Extract a named coefficient (bps) and t-stat from results dict."""
    obj, n = results.get((char_name, day_group, leg), (None, 0))
    if obj is None or param not in obj.params:
        return None, None
    return obj.params[param] * 10_000, obj.tvalues[param]


def print_split_sample(pre_results, post_results, break_ym):
    """Print Pre vs Post side-by-side for L-S excess returns."""
    print(f"\n{'=' * 80}")
    print(f"  SPLIT-SAMPLE EXCESS RETURNS (bps/month) — Break at {break_ym}")
    print(f"  Newey-West HAC t-stats in parentheses")
    print(f"{'=' * 80}")

    for period_label, res in [("Pre", pre_results), ("Post", post_results)]:
        print(f"\n  --- {period_label}-period ---")
        print_panel(res, f"Panel A: L-S (Safe minus Speculative)", "LS")


def print_dummy_results(dummy_results, break_ym):
    """Print Post dummy coefficient (delta) for each characteristic × day."""
    print(f"\n{'=' * 80}")
    print(f"  POST DUMMY COEFFICIENT (bps/month) — Break at {break_ym}")
    print(f"  delta = change in mean excess return from Pre to Post")
    print(f"  Newey-West HAC t-stats in parentheses")
    print(f"{'=' * 80}")

    print(f"\n  {'Panel A: L-S (Safe minus Speculative)'}")
    header = f"  {'':13s}"
    for d in TABLE_COLS:
        header += f"  {d:>12s}"
    print(header)
    print("  " + "-" * 52)

    for char_name in CHARS:
        row_delta = f"  {char_name:13s}"
        row_t     = f"  {'':13s}"
        for day_group in TABLE_COLS:
            a, t = _get_alpha_t_param(dummy_results, char_name, day_group, "LS", "Post")
            if a is not None:
                row_delta += f"  {a:>9.1f}{stars(t):3s}"
                row_t     += f"  {'(' + f'{t:.2f}' + ')':>12s}"
            else:
                row_delta += f"  {'':>12s}"
                row_t     += f"  {'':>12s}"
        print(row_delta)
        print(row_t)
    print()


# ── Split-sample LaTeX ────────────────────────────────────────────────

def save_latex_split(pre_results, post_results, break_ym, output_path):
    """LaTeX tables: Pre and Post as separate table environments."""
    n_cols = len(TABLE_COLS)
    col_spec = "l" + " c" * n_cols
    tag = break_ym.replace("-", "")
    note_lines = [
        r"\begin{minipage}{0.9\textwidth}",
        r"\footnotesize",
        rf"Value-weighted quintile portfolios. Break date: {break_ym}.",
        r"Newey--West HAC $t$-statistics in parentheses.",
        r"$^{*}p<0.10$;\quad $^{**}p<0.05$;\quad $^{***}p<0.01$",
        r"\end{minipage}",
    ]

    lines = []
    for period_label, res, suffix in [
        ("Pre", pre_results, "pre"),
        ("Post", post_results, "post"),
    ]:
        lines.append(r"\begin{table}[htbp]")
        lines.append(r"\centering")
        lines.append(rf"\caption{{Day-of-Week Excess Returns: {period_label}-Period ({break_ym} break, bps/month)}}")
        lines.append(rf"\label{{tab:split_{tag}_{suffix}}}")
        lines.append(r"\footnotesize")
        lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
        lines.append(r"\toprule")
        header_cells = " & ".join(TABLE_COLS)
        lines.append(rf" & {header_cells} \\")
        lines.append(r"\midrule")
        lines.extend(_latex_panel(res, r"Panel A: L--S (Safe $-$ Speculative)", "LS"))
        lines.append(r"\midrule")
        lines.extend(_latex_panel(res, "Panel B: Speculative Leg", "Spec"))
        lines.append(r"\midrule")
        lines.extend(_latex_panel(res, "Panel C: Safe Leg", "Safe"))
        lines.append(r"\bottomrule")
        lines.append(r"\end{tabular}")
        lines.append(r"\vspace{4pt}")
        lines.extend(note_lines)
        lines.append(r"\end{table}")
        lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"\nLaTeX saved to {output_path}")


def _latex_panel_dummy(results, title, leg):
    """LaTeX rows showing the Post dummy coefficient (delta) for one panel."""
    rows = []
    n_cols = len(TABLE_COLS)
    rows.append(rf"\multicolumn{{{n_cols + 1}}}{{l}}{{\textit{{{title}}}}} \\")
    for char_name in CHARS:
        delta_cells = []
        t_cells = []
        for day_group in TABLE_COLS:
            a, t = _get_alpha_t_param(results, char_name, day_group, leg, "Post")
            if a is not None:
                s = stars(t)
                delta_cells.append(f"${a:.1f}{s}$")
                t_cells.append(f"$({t:.2f})$")
            else:
                delta_cells.append("")
                t_cells.append("")
        rows.append(rf"{char_name} & {' & '.join(delta_cells)} \\")
        rows.append(rf" & {' & '.join(t_cells)} \\")
    return rows


def save_latex_dummy(dummy_results, break_ym, output_path):
    """LaTeX table: Post dummy coefficient (delta) with t-stats."""
    n_cols = len(TABLE_COLS)
    col_spec = "l" + " c" * n_cols

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(rf"\caption{{Post-Period Dummy Coefficient $\delta$ (bps/month) --- Break at {break_ym}}}")
    tag = break_ym.replace("-", "")
    lines.append(rf"\label{{tab:dummy_{tag}}}")
    lines.append(r"\footnotesize")
    lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\toprule")
    header_cells = " & ".join(TABLE_COLS)
    lines.append(rf" & {header_cells} \\")
    lines.append(r"\midrule")

    lines.extend(_latex_panel_dummy(dummy_results, r"Panel A: L--S (Safe $-$ Speculative)", "LS"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel_dummy(dummy_results, "Panel B: Speculative Leg", "Spec"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel_dummy(dummy_results, "Panel C: Safe Leg", "Safe"))

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\vspace{4pt}")
    lines.append(r"\begin{minipage}{0.9\textwidth}")
    lines.append(r"\footnotesize")
    lines.append(rf"Post dummy $=1$ from {break_ym} onward. $\delta$ measures change in mean return from Pre to Post.")
    lines.append(r"Value-weighted quintile portfolios. Newey--West HAC $t$-statistics in parentheses.")
    lines.append(r"$^{*}p<0.10$;\quad $^{**}p<0.05$;\quad $^{***}p<0.01$")
    lines.append(r"\end{minipage}")
    lines.append(r"\end{table}")

    output_path.write_text("\n".join(lines))
    print(f"\nLaTeX saved to {output_path}")


def save_latex_capm_decomp(results, output_path):
    """Save LaTeX table for day-decomposed CAPM alphas."""
    n_cols = len(TABLE_COLS)
    col_spec = "l" + " c" * n_cols

    lines = []
    lines.append(r"\begin{table}[htbp]")
    lines.append(r"\centering")
    lines.append(r"\caption{Day-of-Week CAPM Alphas --- Day-Decomposed Market Factor (bps/month)}")
    lines.append(r"\label{tab:dow_capm_decomp_alphas}")
    lines.append(r"\footnotesize")
    lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
    lines.append(r"\toprule")
    header_cells = " & ".join(TABLE_COLS)
    lines.append(rf" & {header_cells} \\")
    lines.append(r"\midrule")

    lines.extend(_latex_panel(results, r"Panel A: L--S (Safe $-$ Speculative)", "LS"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel(results, "Panel B: Speculative Leg", "Spec"))
    lines.append(r"\midrule")
    lines.extend(_latex_panel(results, "Panel C: Safe Leg", "Safe"))

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\vspace{4pt}")
    lines.append(r"\begin{minipage}{0.9\textwidth}")
    lines.append(r"\footnotesize")
    lines.append(r"Value-weighted quintile portfolios. CAPM alpha using day-decomposed JCI market excess return.")
    lines.append(r"Newey--West HAC $t$-statistics in parentheses.")
    lines.append(r"$^{*}p<0.10$;\quad $^{**}p<0.05$;\quad $^{***}p<0.01$")
    lines.append(r"\end{minipage}")
    lines.append(r"\end{table}")

    output_path.write_text("\n".join(lines))
    print(f"\nLaTeX saved to {output_path}")
