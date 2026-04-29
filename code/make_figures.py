"""
Generate 4 key figures for the paper.

Outputs to ./figures/ as PNG (300 DPI) and SVG.

Figures:
  fig1_config_composition.{png,svg}  — 9 configurations × 4 components
  fig2_2x2_symmetric.{png,svg}       — 2×2 cross-model heatmap
  fig3_expert_vs_llm.{png,svg}       — per-paper scatter (expert panel vs LLM judge)
  fig4_token_vs_quality.{png,svg}    — token size vs LLM & expert scores (dual y-axis)
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
FIG = BASE / "figures"
FIG.mkdir(exist_ok=True)

# Publication-ready style (neutral, works for Nature/CCLM/JAMIA)
plt.rcParams.update({
    "font.family": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "axes.linewidth": 0.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "legend.frameon": False,
    "figure.dpi": 120,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
})


def save(fig, name):
    fig.savefig(FIG / f"{name}.png", dpi=300)
    fig.savefig(FIG / f"{name}.svg")
    print(f"  ✅ {name}.png + {name}.svg")


# -----------------------------------------------------------------------------
# Group metadata (shared across figures)
# Order: ascending token size (left-to-right / bottom-to-top)
# -----------------------------------------------------------------------------
GROUPS = [
    # (code_name, token_K, has_rules, has_skeleton, has_detail, has_example)
    # token_K values are cl100k_base tokens / 1000 (Anthropic-tokenizer ≈ ±10%)
    ("A_bare",           0.0, 0, 0, 0, 0),
    ("B_simple",         0.3, 0.5, 0, 0, 0),
    ("E_rules",          1.2, 1, 0, 0, 0),
    ("H4_sop_only",      2.0, 1, 0.5, 0, 0),
    ("H3_skeleton",      5.0, 1, 1, 0, 0),
    ("F_template",      15.0, 0, 1, 1, 0),
    ("G_template_rules", 16.0, 1, 1, 1, 0),
    ("H2_keep_examples", 25.0, 1, 1, 1, 1),
    ("C_full",          56.0, 0.5, 1, 1, 1),
]

GROUP_COLORS = {
    "A_bare":           "#888888",
    "B_simple":         "#AAAAAA",
    "E_rules":          "#4c72b0",
    "H4_sop_only":      "#dd8452",
    "H3_skeleton":      "#e8a34e",
    "F_template":       "#937860",
    "G_template_rules": "#55a868",
    "H2_keep_examples": "#8172b3",
    "C_full":           "#c44e52",
}


# =============================================================================
# Figure 1: configuration composition
# =============================================================================
def figure1():
    print("\n── Figure 1: Configuration composition ──")

    components = ["Rules", "Skeleton", "Detailed\ncontent", "Examples"]
    names = [g[0].replace("_", " ") for g in GROUPS]
    matrix = np.array([g[2:] for g in GROUPS], dtype=float)  # 9 × 4
    token_sizes = np.array([g[1] for g in GROUPS])

    fig, (ax_grid, ax_bar) = plt.subplots(
        1, 2, figsize=(9, 5.5),
        gridspec_kw={"width_ratios": [2.2, 1]},
    )

    # Left: component matrix
    cmap = plt.cm.get_cmap("YlGn", 3)
    im = ax_grid.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    ax_grid.set_xticks(range(len(components)))
    ax_grid.set_xticklabels(components)
    ax_grid.set_yticks(range(len(GROUPS)))
    ax_grid.set_yticklabels(names)
    ax_grid.invert_yaxis()  # smaller token on top → descending from top
    ax_grid.set_title("Configuration components", loc="left", fontweight="bold")

    # Annotate each cell
    for i in range(len(GROUPS)):
        for j in range(4):
            v = matrix[i, j]
            symbol = "✓" if v == 1 else ("◐" if v == 0.5 else "—")
            color = "white" if v > 0.5 else "#333333"
            ax_grid.text(j, i, symbol, ha="center", va="center",
                         color=color, fontsize=12, fontweight="bold")
    for spine in ax_grid.spines.values():
        spine.set_visible(False)
    ax_grid.tick_params(length=0)

    # Legend for symbols
    legend_elems = [
        mpatches.Patch(facecolor=cmap(0.99), edgecolor="none", label="✓  included"),
        mpatches.Patch(facecolor=cmap(0.5), edgecolor="none", label="◐  partial"),
        mpatches.Patch(facecolor=cmap(0.0), edgecolor="none", label="—  absent"),
    ]
    ax_grid.legend(handles=legend_elems, loc="upper left",
                   bbox_to_anchor=(0, -0.10), ncol=3, frameon=False)

    # Right: token size bar — must mirror left panel's y-axis order
    # Left panel uses imshow + invert_yaxis → biggest (C_full) on top, A_bare bottom
    # For bar chart, default y=0 at bottom naturally gives A_bare at bottom
    # So we do NOT invert here (otherwise panels are flipped)
    colors = [GROUP_COLORS[g[0]] for g in GROUPS]
    ax_bar.barh(range(len(GROUPS)), token_sizes, color=colors, edgecolor="none")
    ax_bar.set_yticks(range(len(GROUPS)))
    ax_bar.set_yticklabels([])
    ax_bar.set_ylim(ax_grid.get_ylim())  # sync with left panel
    ax_bar.set_xlabel("System-prompt size (K tokens)")
    ax_bar.set_title("Size", loc="left", fontweight="bold")
    ax_bar.grid(axis="x", alpha=0.3, linewidth=0.5)
    ax_bar.set_axisbelow(True)

    # Label values
    for i, v in enumerate(token_sizes):
        if v > 0:
            label = f"{v:.1f}K" if v < 1 else f"{int(v)}K"
        else:
            label = "0"
        ax_bar.text(v + 1.5, i, label, va="center", fontsize=9)

    ax_bar.set_xlim(0, 80)

    fig.suptitle("Nine configurations tested for LLM-assisted ISO 15189 QMS generation",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "fig1_config_composition")
    plt.close(fig)


# =============================================================================
# Figure 2: 2×2 symmetric cross-model matrix (heatmap)
# =============================================================================
def figure2():
    print("\n── Figure 2: 2×2 symmetric matrix ──")
    data = json.load(open(BASE / "2x2_symmetric_complete.json"))
    matrix = data["matrix"]

    # Order groups ascending token size
    group_order = [g[0] for g in GROUPS]
    # Handle the E/G alias in 2x2 file
    alias_back = {"E_rules_v2": "E_rules", "G_template_rules": "G_template_rules"}

    quadrants = ["CC", "CG", "GC", "GG"]
    quad_labels = [
        "Claude→Claude",
        "Claude→GPT",
        "GPT→Claude",
        "GPT→GPT",
    ]

    mat = np.full((len(group_order), 4), np.nan)
    for i, g in enumerate(group_order):
        # 2x2 file uses E_rules_v2 — map back
        src_key = {"E_rules": "E_rules_v2"}.get(g, g)
        if src_key not in matrix:
            continue
        for j, q in enumerate(quadrants):
            mat[i, j] = matrix[src_key].get(q, np.nan)

    fig, ax = plt.subplots(figsize=(6.5, 5.5))

    cmap = plt.cm.get_cmap("RdYlGn", 256)
    vmin, vmax = 1.0, 5.0
    im = ax.imshow(mat, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")

    ax.set_xticks(range(4))
    ax.set_xticklabels(quad_labels, rotation=20, ha="right")
    ax.set_yticks(range(len(group_order)))
    ax.set_yticklabels([g.replace("_", " ") for g in group_order])
    ax.invert_yaxis()
    ax.set_xlabel("Generator → Judge")
    ax.set_title("2×2 symmetric cross-model validation\n(Mean score across A1/B1/C1, 0–5 scale)",
                 loc="left", fontweight="bold")

    # Annotate each cell
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            if np.isnan(v): continue
            color = "white" if v < 2.5 or v > 4.2 else "black"
            weight = "bold" if v < 2.0 else "normal"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color=color, fontsize=9, fontweight=weight)

    # Outline C_full collapse
    c_full_idx = group_order.index("C_full")
    for j in [2, 3]:  # GC, GG
        rect = mpatches.Rectangle((j-0.5, c_full_idx-0.5), 1, 1,
                                  fill=False, edgecolor="#000000",
                                  linewidth=1.8, zorder=5)
        ax.add_patch(rect)

    cbar = fig.colorbar(im, ax=ax, shrink=0.75, pad=0.02)
    cbar.set_label("Mean judge score", labelpad=8)

    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(length=0)

    # Annotation
    ax.annotate("C_full collapse\nunder GPT\ngeneration",
                xy=(2, c_full_idx), xytext=(4.7, c_full_idx - 1.5),
                arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                fontsize=9, ha="left", fontweight="bold")

    fig.tight_layout()
    save(fig, "fig2_2x2_symmetric")
    plt.close(fig)


# =============================================================================
# Figure 3: Expert panel vs LLM judge (per-paper scatter, n=10)
# =============================================================================
def figure3():
    print("\n── Figure 3: Expert vs LLM judge (per paper) ──")
    d = json.load(open(BASE / "blind_review" / "icc_results_3raters.json"))
    papers = d["per_paper"]
    icc = d["icc"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 5), sharey=True)

    for ax, (llm_name, llm_col, icc_key) in zip(
        axes,
        [("Claude Opus 4.6", "claude_mean", "expert_vs_claude"),
         ("GPT-5.4", "gpt_mean", "expert_vs_gpt")],
    ):
        xs = np.array([p["expert_mean"] for p in papers])
        ys = np.array([p[llm_col] for p in papers])
        errs = np.array([
            np.std([p["rater1_mean"], p["rater2_mean"], p["rater3_mean"]], ddof=0)
            for p in papers
        ])
        colors = [GROUP_COLORS.get(p["group"], "#666666") for p in papers]

        # 1:1 reference
        ax.plot([1.5, 5], [1.5, 5], linestyle="--", color="#888888", linewidth=0.9, label="1:1 line")

        # Error bars (expert SD across 3 raters)
        ax.errorbar(xs, ys, xerr=errs, fmt="none", ecolor="#888888",
                    elinewidth=0.7, capsize=2, zorder=2)

        for x, y, c, p in zip(xs, ys, colors, papers):
            ax.scatter(x, y, s=80, color=c, edgecolor="black", linewidth=0.5, zorder=3)

        ax.set_xlabel("Expert panel mean (3-rater average)")
        if ax is axes[0]:
            ax.set_ylabel("LLM judge mean")

        # Stats annotation
        r = icc[icc_key]
        stats_text = (f"ICC(3,1) = {r['ICC31']:.3f}\n"
                      f"Pearson r = {r['pearson']:.3f}\n"
                      f"Mean diff = {r['diff']:+.2f}")
        ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
                fontsize=9, verticalalignment="top", fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                          edgecolor="#888888", linewidth=0.6))

        ax.set_title(f"Expert panel vs {llm_name}", loc="left", fontweight="bold")
        ax.set_xlim(2.6, 4.5)
        ax.set_ylim(2.0, 5.2)
        ax.grid(alpha=0.25, linewidth=0.5)
        ax.set_axisbelow(True)
        ax.legend(loc="lower right", fontsize=8)

    # Group legend (shared)
    legend_handles = [
        plt.Line2D([], [], marker="o", color="w", markerfacecolor=GROUP_COLORS[g[0]],
                   markeredgecolor="black", markersize=8, label=g[0].replace("_", " "))
        for g in GROUPS if g[0] in {"A_bare", "C_full", "E_rules", "F_template",
                                     "G_template_rules", "H2_keep_examples", "H4_sop_only"}
    ]
    fig.legend(handles=legend_handles, loc="upper center",
               bbox_to_anchor=(0.5, -0.02), ncol=4, frameon=False, fontsize=9)

    fig.suptitle("LLM judges systematically overrate relative to expert panel "
                 "(n=10 papers × 3 raters)",
                 fontsize=12, fontweight="bold", y=1.02)
    fig.tight_layout()
    save(fig, "fig3_expert_vs_llm")
    plt.close(fig)


# =============================================================================
# Figure 4: Token size vs quality (dual perspective)
# =============================================================================
def figure4():
    print("\n── Figure 4: Token size vs quality ──")
    d = json.load(open(BASE / "blind_review" / "icc_results_3raters.json"))
    papers = d["per_paper"]

    # Aggregate per-group means (from expert panel)
    df = pd.DataFrame(papers)
    by_group = df.groupby("group").agg(
        expert=("expert_mean", "mean"),
        claude=("claude_mean", "mean"),
        gpt=("gpt_mean", "mean"),
        n=("blind_id", "count"),
    ).reset_index()

    # Merge with token sizes
    token_map = {g[0]: g[1] for g in GROUPS}
    # Handle E_rules_v2 vs E_rules aliasing in icc data
    token_map["E_rules_v2"] = 1.2
    by_group["tokens"] = by_group["group"].map(token_map)
    by_group = by_group.sort_values("tokens")

    fig, ax = plt.subplots(figsize=(9, 5.5))

    # Expert (left y)
    ax.plot(by_group["tokens"], by_group["expert"],
            marker="s", markersize=10, linewidth=1.8,
            color="#2a6a3e", label="Expert panel (3-rater avg)")
    # Claude (right y)
    ax.plot(by_group["tokens"], by_group["claude"],
            marker="o", markersize=9, linewidth=1.5,
            color="#c44e52", label="Claude Opus 4.6 judge", alpha=0.85)
    ax.plot(by_group["tokens"], by_group["gpt"],
            marker="^", markersize=9, linewidth=1.5,
            color="#4c72b0", label="GPT-5.4 judge", alpha=0.85)

    # Annotate each point with group name
    for _, r in by_group.iterrows():
        ax.annotate(r["group"].replace("_", " "),
                    (r["tokens"], r["expert"]),
                    xytext=(4, -14), textcoords="offset points",
                    fontsize=8, color="#2a6a3e", alpha=0.85)

    ax.set_xscale("symlog", linthresh=0.5)
    ax.set_xticks([0, 0.5, 1, 2, 5, 15, 25, 56])
    ax.set_xticklabels(["0", "0.5K", "1K", "2K", "5K", "15K", "25K", "56K"])
    ax.set_xlim(-0.2, 80)
    ax.set_ylim(2.5, 5.2)
    ax.set_xlabel("System-prompt size (tokens, symlog scale; cl100k_base)")
    ax.set_ylabel("Mean quality score (0–5)")
    ax.grid(alpha=0.3, linewidth=0.5)
    ax.set_axisbelow(True)

    # Highlight token-efficiency vs clinical-usability tradeoff
    ax.axvspan(1, 5, alpha=0.08, color="#dd8452",
               label="_", zorder=0)
    ax.axvspan(13, 27, alpha=0.08, color="#55a868",
               label="_", zorder=0)
    ax.text(2.5, 5.05, "Efficient zone\n(H4 / H3)", ha="center",
            fontsize=9, style="italic", color="#a05a2c")
    ax.text(19, 5.05, "Expert-optimal zone\n(F / G)", ha="center",
            fontsize=9, style="italic", color="#2a6a3e")

    ax.legend(loc="lower right", fontsize=9)
    ax.set_title("Token size vs quality: LLM judges peak at 2–5K; experts prefer 15–25K",
                 loc="left", fontweight="bold")

    fig.tight_layout()
    save(fig, "fig4_token_vs_quality")
    plt.close(fig)


# =============================================================================
def main():
    print(f"📊 Generating figures to {FIG}\n")
    figure1()
    figure2()
    figure3()
    figure4()
    print(f"\n✅ All 4 figures generated in {FIG}")


if __name__ == "__main__":
    main()
