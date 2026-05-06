"""
Results formatting: terminal tables and LaTeX output.
"""

from .config import CHARS, TABLE_COLS

_STARS_NOTE = r"$^{*}p<0.10$;\quad $^{**}p<0.05$;\quad $^{***}p<0.01$"
_NW_NOTE    = r"Newey--West HAC $t$-statistics in parentheses."


# ── Significance helpers ───────────────────────────────────────────────

def stars(t):
    at = abs(t)
    if at > 2.576: return "***"
    if at > 1.96:  return "**"
    if at > 1.645: return "*"
    return ""


def stars_p(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.10: return "*"
    return ""


# ── Data extraction ────────────────────────────────────────────────────

def _get_alpha_t(results, char_name, day_group, leg):
    obj, _ = results.get((char_name, day_group, leg), (None, 0))
    if obj is None:
        return None, None
    return obj.params["const"] * 10_000, obj.tvalues["const"]


def _get_alpha_t_param(results, char_name, day_group, leg, param="const"):
    obj, _ = results.get((char_name, day_group, leg), (None, 0))
    if obj is None or param not in obj.params:
        return None, None
    return obj.params[param] * 10_000, obj.tvalues[param]


def _get_f_p(results, char_name, day_group, leg):
    obj, _ = results.get((char_name, day_group, leg), (None, 0))
    if obj is None or not hasattr(obj, "break_f"):
        return None, None
    return obj.break_f, obj.break_p


# ── Terminal printing ──────────────────────────────────────────────────

def print_panel(results, title, leg):
    print(f"\n  {title}")
    header = f"  {'':13s}" + "".join(f"  {d:>12s}" for d in TABLE_COLS)
    print(header)
    print("  " + "-" * 52)
    for char_name in CHARS:
        row_a = f"  {char_name:13s}"
        row_t = f"  {'':13s}"
        for day_group in TABLE_COLS:
            a, t = _get_alpha_t(results, char_name, day_group, leg)
            if a is not None:
                row_a += f"  {a:>9.1f}{stars(t):3s}"
                row_t += f"  {'(' + f'{t:.2f}' + ')':>12s}"
            else:
                row_a += f"  {'':>12s}"
                row_t += f"  {'':>12s}"
        print(row_a)
        print(row_t)


def _three_panels_print(results):
    print_panel(results, "Panel A: L-S (Safe minus Speculative)", "LS")
    print_panel(results, "\n  Panel B: Speculative Leg", "Spec")
    print_panel(results, "\n  Panel C: Safe Leg", "Safe")
    print("\n" + "=" * 60)


def _wald_panel_print(dummy_results):
    print(f"\n  Panel A: L-S (Safe minus Speculative)")
    header = f"  {'':13s}" + "".join(f"  {d:>12s}" for d in TABLE_COLS)
    print(header)
    print("  " + "-" * 52)
    for char_name in CHARS:
        row_f = f"  {char_name:13s}"
        row_p = f"  {'':13s}"
        for day_group in TABLE_COLS:
            f, p = _get_f_p(dummy_results, char_name, day_group, "LS")
            if f is not None:
                row_f += f"  {f:>9.2f}{stars_p(p):3s}"
                row_p += f"  {'[' + f'{p:.3f}' + ']':>12s}"
            else:
                row_f += f"  {'':>12s}"
                row_p += f"  {'':>12s}"
        print(row_f)
        print(row_p)
    print()


def print_alpha_results(results, title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)
    _three_panels_print(results)


def print_split_sample(pre_results, post_results, break_ym, kind="Excess Returns"):
    print(f"\n{'=' * 80}")
    print(f"  SPLIT-SAMPLE {kind.upper()} (bps/month) — Break at {break_ym}")
    print(f"{'=' * 80}")
    for label, res in [("Pre", pre_results), ("Post", post_results)]:
        print(f"\n  --- {label}-period ---")
        print_panel(res, "Panel A: L-S (Safe minus Speculative)", "LS")


def print_dummy_results(dummy_results, break_ym):
    print(f"\n{'=' * 80}")
    print(f"  POST DUMMY COEFFICIENT (bps/month) — Break at {break_ym}")
    print(f"  delta = change in mean return from Pre to Post")
    print(f"{'=' * 80}")
    print(f"\n  Panel A: L-S (Safe minus Speculative)")
    header = f"  {'':13s}" + "".join(f"  {d:>12s}" for d in TABLE_COLS)
    print(header)
    print("  " + "-" * 52)
    for char_name in CHARS:
        row_d = f"  {char_name:13s}"
        row_t = f"  {'':13s}"
        for day_group in TABLE_COLS:
            a, t = _get_alpha_t_param(dummy_results, char_name, day_group, "LS", "Post")
            if a is not None:
                row_d += f"  {a:>9.1f}{stars(t):3s}"
                row_t += f"  {'(' + f'{t:.2f}' + ')':>12s}"
            else:
                row_d += f"  {'':>12s}"
                row_t += f"  {'':>12s}"
        print(row_d)
        print(row_t)
    print()


def print_wald_results(dummy_results, break_ym, kind=""):
    label = f"{kind.upper()} " if kind else ""
    print(f"\n{'=' * 80}")
    print(f"  {label}STRUCTURAL BREAK TEST (HAC Wald F) — Break at {break_ym}")
    print(f"{'=' * 80}")
    _wald_panel_print(dummy_results)


# ── LaTeX helpers ──────────────────────────────────────────────────────

def _body(col_spec, header_cells, panel_rows, note_lines):
    """Tabular body + minipage note. No float wrapper — caption/label go in the paper."""
    lines = [
        r"\centering", r"\footnotesize",
        rf"\begin{{tabular}}{{{col_spec}}}", r"\toprule",
        rf" & {header_cells} \\", r"\midrule",
    ]
    lines += panel_rows
    lines += [
        r"\bottomrule", r"\end{tabular}", r"\vspace{4pt}",
        r"\begin{minipage}{\linewidth}", r"\footnotesize",
    ]
    lines += note_lines
    lines += [r"\end{minipage}"]
    return lines


def _save(lines, output_path):
    output_path.write_text("\n".join(lines))
    print(f"\nLaTeX saved to {output_path}")


def _latex_panel_generic(results, title, leg, extractor, fmt_v1, fmt_v2):
    n_cols = len(TABLE_COLS)
    rows = [rf"\multicolumn{{{n_cols + 1}}}{{l}}{{\textit{{{title}}}}} \\"]
    for char_name in CHARS:
        v1_cells, v2_cells = [], []
        for day_group in TABLE_COLS:
            v1, v2 = extractor(results, char_name, day_group, leg)
            if v1 is not None:
                v1_cells.append(fmt_v1(v1, v2))
                v2_cells.append(fmt_v2(v1, v2))
            else:
                v1_cells.append("")
                v2_cells.append("")
        rows.append(rf"{char_name} & {' & '.join(v1_cells)} \\")
        rows.append(rf" & {' & '.join(v2_cells)} \\")
    return rows


def _latex_panel(results, title, leg):
    return _latex_panel_generic(
        results, title, leg,
        extractor=_get_alpha_t,
        fmt_v1=lambda a, t: f"${a:.1f}{stars(t)}$",
        fmt_v2=lambda a, t: f"$({t:.2f})$",
    )


def _latex_panel_dummy(results, title, leg):
    return _latex_panel_generic(
        results, title, leg,
        extractor=lambda r, c, d, l: _get_alpha_t_param(r, c, d, l, "Post"),
        fmt_v1=lambda a, t: f"${a:.1f}{stars(t)}$",
        fmt_v2=lambda a, t: f"$({t:.2f})$",
    )


def _latex_panel_wald(results, title, leg):
    return _latex_panel_generic(
        results, title, leg,
        extractor=_get_f_p,
        fmt_v1=lambda f, p: f"${f:.2f}{stars_p(p)}$",
        fmt_v2=lambda f, p: f"$[{p:.3f}]$",
    )


def _three_panel_rows(results, panel_fn):
    rows = panel_fn(results, r"Panel A: L--S (Safe $-$ Speculative)", "LS")
    rows += [r"\midrule"] + panel_fn(results, "Panel B: Speculative Leg", "Spec")
    rows += [r"\midrule"] + panel_fn(results, "Panel C: Safe Leg", "Safe")
    return rows


# ── LaTeX save functions ───────────────────────────────────────────────

def _alpha_table(results, note_lines, output_path):
    col_spec = "l" + " c" * len(TABLE_COLS)
    header_cells = " & ".join(TABLE_COLS)
    panel_rows = _three_panel_rows(results, _latex_panel)
    _save(_body(col_spec, header_cells, panel_rows, note_lines), output_path)


def save_latex(results, output_path):
    _alpha_table(results, [
        r"Value-weighted quintile portfolios. " + _NW_NOTE,
        _STARS_NOTE,
    ], output_path)


def save_latex_capm(results, output_path):
    _alpha_table(results, [
        r"Value-weighted quintile portfolios. CAPM alpha using full-month JCI market excess return.",
        _NW_NOTE, _STARS_NOTE,
    ], output_path)


def save_latex_capm_decomp(results, output_path):
    _alpha_table(results, [
        r"Value-weighted quintile portfolios. CAPM alpha using day-decomposed JCI market excess return.",
        _NW_NOTE, _STARS_NOTE,
    ], output_path)


def save_latex_ff3(results, output_path):
    _alpha_table(results, [
        (r"Value-weighted quintile portfolios. FF3 alpha: "
         r"$R_{i,t} - R_{f,t} = \alpha_i + \beta_i \mathrm{MktRF}_t "
         r"+ s_i \mathrm{SMB}_t + h_i \mathrm{HML}_t + \varepsilon_{i,t}$. "
         r"SMB and HML constructed from IDX universe following "
         r"Foye \& Valentin\v{c}i\v{c} (2020)."),
        _NW_NOTE, _STARS_NOTE,
    ], output_path)


def save_latex_split(pre_results, post_results, break_ym, pre_path, post_path, *, ff3=False):
    """Write separate pre- and post-period tabular bodies (excess returns or FF3 alpha)."""
    col_spec = "l" + " c" * len(TABLE_COLS)
    header_cells = " & ".join(TABLE_COLS)
    suffix = " FF3 alpha." if ff3 else "."
    note = [
        rf"Value-weighted quintile portfolios. Break date: {break_ym}{suffix}",
        _NW_NOTE, _STARS_NOTE,
    ]
    for res, path in [(pre_results, pre_path), (post_results, post_path)]:
        panel_rows = _three_panel_rows(res, _latex_panel)
        _save(_body(col_spec, header_cells, panel_rows, note), path)


def save_latex_dummy(dummy_results, break_ym, output_path):
    col_spec = "l" + " c" * len(TABLE_COLS)
    header_cells = " & ".join(TABLE_COLS)
    panel_rows = _three_panel_rows(dummy_results, _latex_panel_dummy)
    note = [
        rf"Post dummy $=1$ from {break_ym} onward. $\delta$ measures change in mean return from Pre to Post.",
        r"Value-weighted quintile portfolios. " + _NW_NOTE,
        _STARS_NOTE,
    ]
    _save(_body(col_spec, header_cells, panel_rows, note), output_path)


def _wald_table(dummy_results, break_ym, note_lines, output_path):
    col_spec = "l" + " c" * len(TABLE_COLS)
    header_cells = " & ".join(TABLE_COLS)
    panel_rows = _latex_panel_wald(
        dummy_results, r"Panel A: L--S (Safe $-$ Speculative)", "LS"
    )
    _save(_body(col_spec, header_cells, panel_rows, note_lines), output_path)


def save_latex_capm_dummy(dummy_results, break_ym, output_path):
    _wald_table(dummy_results, break_ym, [
        rf"Joint Wald $F$-test for shift in both $\alpha$ and $\beta$ at {break_ym}.",
        r"Newey--West HAC standard errors used for the covariance matrix.",
        r"$p$-values in brackets. " + _STARS_NOTE,
    ], output_path)


def save_latex_ff3_dummy(dummy_results, break_ym, output_path):
    _wald_table(dummy_results, break_ym, [
        rf"Joint Wald $F$-test for shift in all FF3 parameters ($\alpha, \beta_{{mkt}}, \beta_{{smb}}, \beta_{{hml}}$) at {break_ym}.",
        r"Newey--West HAC standard errors used for the covariance matrix.",
        r"$p$-values in brackets. " + _STARS_NOTE,
    ], output_path)
