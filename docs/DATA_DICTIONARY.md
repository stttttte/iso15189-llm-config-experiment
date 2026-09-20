# Data Dictionary

This document describes the principal archived data and corrected reproduction outputs. This working copy is pending release; historical manuscript and submission files retain their original contents for provenance.

LLM dimension ratings are integers from 0 to 5; expert dimension ratings allow decimals. Means, weighted scores, normalized composites, counts, and ICCs have their own scales as specified below.

---

## 1. Auto-scorer outputs

Produced by `code/auto_scorer.py` — rule-based Python scorer for format, clause coverage, and terminology compliance.

### `data/scores/all_scores_6groups.json`

- **Type**: `list[dict]`, 270 records (6 groups × 15 tasks × 3 reps)
- **Groups**: `A_bare`, `B_simple`, `C_full`, `E_rules_v2`, `F_template`, `G_template_rules`

### `data/scores/all_scores_h2h3.json`

- **Type**: `list[dict]`, 90 records (2 groups × 15 tasks × 3 reps)
- **Groups**: `H2_keep_examples`, `H3_skeleton`

### `data/scores/all_scores_h4.json`

- **Type**: `list[dict]`, 45 records (1 group × 15 tasks × 3 reps)
- **Group**: `H4_sop_only`

**Record schema** (shared by all three files):

| Field | Type | Description |
|-------|------|-------------|
| `group` | str | Configuration group name |
| `file` | str | Source file name (e.g., `H4_sop_only-A1-2.md`) |
| `task` | str | Task ID (A1…C5) |
| `category` | str | Task category (`A`/`B`/`C`) |
| `格式` / `format_score` | int 0–5 | Document structure completeness |
| `条款` / `clause_score` | int 0–5 | ISO 15189 clause coverage |
| `术语` / `terminology_score` | int 0–5 | Terminology compliance (per expert-reviewed map) |
| `违规` / `violation_count` | int ≥0 | Number of banned-term violations |
| `模糊` / `vagueness_count` | int ≥0 | Number of vague-expression violations |
| `auto_weighted` | float | Archived automatic weighted score; one input to the Table 1 composite, not an LLM rating |

---

## 2. LLM judge evaluations

There are **759 unique archived document-level judge records**: 486 GPT and 273 Claude. The Claude records cover only Claude-generated documents: 270 main-group records plus 3 H-group supplements. The earlier reported total of 378 Claude evaluations combined coverage of 270 main-group, 27 H-group, and 81 GPT-generated evaluations. The surviving three supplements cannot automatically be treated as a subset of that total. Additional historical Claude means survive only in aggregate; their document-level data and denominators cannot be fully reconstructed.

### `data/scores/cnas_judge_final_15tasks.json`

- **Type**: `dict`
- **Source**: Claude Opus 4.6 as judge, CNAS senior reviewer prompt
- **Coverage**: 6 main groups (A/B/C/E/F/G) × 15 tasks × 3 reps = 270 evaluations
- **Note**: Historical H-group means are retained in aggregate files, while the three surviving document-level H-group supplements used in the expert comparison are stored separately. Neither source constitutes a complete raw 2×2 archive.

**Top-level keys**:
| Key | Type | Description |
|-----|------|-------------|
| `data` | dict | `data[task_id][group_name][rep-1]` → `[条款满足度, 可操作性, 内部一致性, PDCA闭环, 专业深度]` (five integers, 0–5); array index is zero-based |
| `overall` | dict | `overall[group]` → overall mean score |
| `per_file` | dict of lists | `per_file[group]` contains 45 per-document means without filename keys; use `data[task][group][rep-1]` for explicit task/rep lookup |
| `winners` | dict | Task-by-task winning group |
| `win_count` | dict | Win count by group |

**Historical group names in this file** (important):

- `E_rules` = current `E_rules_v2`
- `G_combined` = current `G_template_rules`

### `data/scores/h_claude_judge_supplement.json`

- **Type**: `dict`
- **Source**: Claude sub-agents via Claude Code Agent tool (2026-04-14/15)
- **Purpose**: Supplements Claude judge data for three H-group papers used in expert-vs-LLM ICC analysis
- **Schema**:
  ```json
  {
    "_note": "...",
    "_method": "...",
    "scores": [
      {
        "group": "H2_keep_examples|H4_sop_only",
        "task": "A1|A3",
        "rep": 1|2|3,
        "file": "...",
        "dims": {
          "条款满足度": {"score": int 0-5, "reason": str},
          "可操作性":   {"score": int 0-5, "reason": str},
          "内部一致性": {"score": int 0-5, "reason": str},
          "PDCA闭环":  {"score": int 0-5, "reason": str},
          "专业深度":   {"score": int 0-5, "reason": str}
        }
      }, ...
    ]
  }
  ```

### `data/scores/gpt_judge_summary.json`

- **Type**: `list[dict]`, 486 records
- **Source**: GPT-5.4 as judge, same CNAS prompt as Claude judge
- **Coverage**: all 486 generated documents (405 Claude-gen + 81 GPT-gen)

**Record schema**:
| Field | Type | Description |
|-------|------|-------------|
| `group` | str | Generation group (incl. `gpt4o_*` for GPT-gen) |
| `task` | str | Task ID |
| `rep` | int | Repetition index (1/2/3) |
| `file` | str | Source file name |
| `条款满足度` | int 0–5 | Clause satisfaction |
| `可操作性` | int 0–5 | Operability |
| `内部一致性` | int 0–5 | Internal consistency |
| `PDCA闭环` | int 0–5 | PDCA loop completeness |
| `专业深度` | int 0–5 | Professional depth |
| `mean` | float | Arithmetic mean of 5 dimensions |

---

## 3. Analysis outputs

### `data/analysis/2x2_symmetric_complete.json`

- **Type**: `dict`
- **Purpose**: Historical 2×2 group-mean summary (2 generation models × 2 judges × 9 groups).
- **Scope**: Cross-model task subset A1/B1/C1. Some historical Claude cells lack recoverable raw records and denominators; the file is not complete document-level data. The H4 `CC` cell is the archived value 4.175.

| Field | Type | Meaning |
|-------|------|---------|
| `matrix[group].CC` | float | Claude-generated → Claude-judged mean |
| `matrix[group].CG` | float | Claude-generated → GPT-judged mean |
| `matrix[group].GC` | float | GPT-generated → Claude-judged historical mean |
| `matrix[group].GG` | float | GPT-generated → GPT-judged mean |
| `claude_bias` | float | Legacy scalar: across-group mean of `CC−CG` = +0.464 |
| `gpt_bias` | float | Legacy scalar: across-group mean of `GG−GC` = −0.472 |
| `cross_ranking` | list of two-item lists | `[group, (CG+GC)/2]`, descending |

The primary within-judge generator contrasts are `mean(CC−GC)` = +0.294 for the Claude judge and `mean(GG−CG)` = −0.301 for the GPT judge. The two legacy `*_bias` fields instead compare judges on the same generation model and are sensitivity contrasts. They are scalar numbers, not per-group dictionaries. All four contrast summaries can be recalculated from `matrix`, but missing raw records prevent full reconstruction of every historical cell.

### `data/analysis/final_9groups_ranking.json`

- **Type**: `dict`
- **Purpose**: Table 1 composite of automatic scores and GPT-judge scores on 405 Claude-generated documents (45 per group). It does not include Claude-judge scores.
- **Formula**: average each score within each group; min–max normalize automatic and GPT group means separately across all nine groups; take the unweighted mean of the two normalized values.
- **`ranking` schema**: each five-item list is `[group, composite, archived_configuration_mean_k_tokens, auto_weighted_mean, gpt_judge_mean]`. The original ranking order and all score values are preserved. Only the size column was corrected from legacy byte-based labels to configuration-text k-tokens (1 k-token=1,000 cl100k_base tokens).
- **`comparisons`**: each entry contains `a`, `b`, and `delta`, where `delta` is GPT-judge mean(a) minus mean(b), not a composite-score difference.
- **`_metadata`**: units, source, column meanings, and limits of configuration-size interpretation.
- **`legacy_token_labels_preserved`**: original third-column labels by group, retained only for provenance; they are not measured token counts.

### `data/analysis/configuration_token_inventory.json`

- **Purpose**: Audited sizes of archived configuration text using tiktoken `cl100k_base`.
- **Top-level fields**: `tokenizer`, `unit`, `scope`, `groups`, and `legacy_fixed_references`.
- **`groups[group]`**: `basis`, `n`, `mean`, `min`, and `max`; `per_file` maps archived paths to counts where a physical text file is the source. B is measured from `load_simple_prompt()`; A has no experimental configuration text.
- **Basis**: fixed texts for A/B/C/E; all 15 task-specific files for F/G/H2/H3/H4. These are configuration-text statistics, not the three-task GPT subset's mean input usage.
- **Limit**: excludes task messages, agent wrappers, tools, and other unarchived context. Actual Claude input sizes and cross-generator input equivalence remain unverified.
- **Legacy references**: standalone F/G files have 14,947/16,138 tokens; they are not substitutes for the task-specific means.

### `reproduced/table1_ranking.json` and `.csv`

- Produced by `code/reproduce_ranking.py` from archived automatic/GPT document-level scores.
- Named fields record the group means, normalized components, composite, and document counts; these newly computed outputs are distinct from the preserved historical five-column ranking file.

### `data/analysis/ablation_h2h3_results.json`

- **Type**: `dict`
- **Purpose**: Historical eight-group ranking summary produced before inclusion of H4; keys are `ranking`, `auto_avgs`, and `gpt_avgs`.
- This file does not contain a four-factor orthogonal design or the complete component-contrast inference. The structured contrast subset is E−A, H4−E, G−H3, and H2−G; bootstrap intervals are recomputed by `code/bootstrap_ci.py`.
- Rules: Δ=+0.511, BH-adjusted p=0.00056166. Skeleton: Δ=+0.213, BH-adjusted p=0.109195, not significant after adjustment; bootstrap 95% CI rounds to [0.05, 0.38].

### `data/analysis/dual_judge_comparison.json`

- **Type**: `dict`
- **Purpose**: Claude-vs-GPT judge agreement statistics for the six main groups (270 paired Claude-generated documents).
- **Keys**: `comparison_table`, `pearson_paired`, `spearman_paired`, `icc_21`, `spearman_group_means`

---

## 4. Expert blind review

### `data/expert_blind_review/papers/paper_01..10.md`

- 10 Claude-generated Class A documents (tasks A1/A2/A3) selected from seven groups and shuffled for expert scoring.
- Source documents are stored under `data/generated/<group>/<file>.md`; the packet uses blinded filenames.
- Configuration labels were concealed during scoring. The source mapping is recoverable from released analysis results, so a new review needs a fresh blinded packet.

### `data/expert_blind_review/rating_sheet_rater{1,2,3}_filled.md`

- Primary expert records: three same-institution coauthor raters × 10 documents = 30 forms, each with five dimension ratings (150 ratings in total).
- Scale: 0–5, allowing decimals; free-text rationales may also be present.
- The same-institution coauthor panel supports exploratory internal validation, not independent external validation.
- Older instructions refer to `rating_sheet_filled.md`, which is not included under that filename; use the three explicitly named rater files above.

### `data/expert_blind_review/blind_key.json`

- List of mappings with `blind_id`, `group`, `task`, and `rep`.
- Recovered solely from the already released `icc_results_3raters.json` per-paper mapping. It supports the corrected ICC reproduction script and does not provide future blinding.

### `data/expert_blind_review/icc_results_3raters.json`

- Archived primary panel analysis; keys are `n_papers`, `per_paper`, `icc`, and `by_group`.
- `per_paper` includes the source mapping, individual expert scores, expert mean, and LLM scores. Archived displayed means may be rounded.
- Expert-panel ICC(2,k)=0.982; expert-mean vs Claude/GPT ICC(3,1)=0.548/0.217. The stored pairwise `diff` uses expert minus judge; mean judge overrating is +0.90/+0.52.
- Group comparisons cover seven groups with unequal small samples. H4 ranks fifth (3.20).
- The corrected `code/compute_icc_3raters.py` writes a new result to `reproduced/icc_results_3raters.json` by default. Historical single-rater `icc_results.json` files remain legacy artifacts.

---

## 5. Generated QMS documents

### `data/generated/<group>/<group>-<task>-<rep>.md`

- Complete generated QMS document (Chinese)
- 486 files total: 405 Claude documents (9 groups × 15 tasks × 3 repetitions), plus 81 GPT documents (9 groups × A1/B1/C1 × 3 repetitions).
- File naming: `<group>-<task>-<rep>.md`, e.g., `H4_sop_only-A1-2.md`
- Groups prefixed with `gpt4o_` are GPT-5.4 generations (as distinguished from the Claude Opus primary experiment)

### `configs/rules.md`

- Archived rule layer (terminology bans + vagueness bans), measuring 1,236 cl100k_base tokens; earlier byte-based labels were incorrectly called tokens.
- Used in E_rules_v2, G_template_rules, H2/H3/H4 configurations

### `configs/task_messages/<task_id>.txt`

- User-role prompt for each of the 15 tasks

---

## 6. Scoring dimensions reference

**Five CNAS-reviewer dimensions** (identical in Claude judge, GPT judge, and expert blind review):

| # | Dimension (ZH) | Dimension (EN) | Anchor at 5 | Anchor at 1 |
|---|---------------|----------------|-------------|-------------|
| 1 | 条款满足度 | Clause satisfaction | All SHALL requirements have concrete implementations | Clauses cited but not implemented |
| 2 | 可操作性 | Operability | Every step has specific role, timing, output form | Vague "timely / relevant personnel / periodic" language |
| 3 | 内部一致性 | Internal consistency | All cross-references closed, no role conflicts | Dangling references or role conflicts |
| 4 | PDCA 闭环 | PDCA loop | Complete plan-do-check-act chain | Only execution, no check/act |
| 5 | 专业深度 | Professional depth | Laboratory-specific detail (Westgard/HIL/PCR zoning/uncertainty) | Generic content, not laboratory-specific |

---

## 7. Group naming conventions

Sizes below are archived configuration-text counts in cl100k_base tokens, not verified model input usage. F/G/H2/H3/H4 show the mean across all 15 tasks and the task range; A/B/C/E use fixed texts. They do not define minimum effective token thresholds.

| Group | Fixed count or 15-task mean | Task range | Rule | Skeleton | Detail | Example |
|-------|----------------------------:|------------|------|----------|--------|---------|
| `A_bare` | 0 | Fixed | ❌ | ❌ | ❌ | ❌ |
| `B_simple` | 348 | Fixed | partial | ❌ | ❌ | ❌ |
| `C_full` | 56,151 | Fixed | partial | ✓ | ✓ | ✓ |
| `E_rules_v2` (alias: `E_rules`) | 1,236 | Fixed | ✓ | ❌ | ❌ | ❌ |
| `F_template` | 23,089.7 | 12,160–42,885 | ❌ | ✓ | ✓ | ❌ |
| `G_template_rules` (alias: `G_combined`) | 24,234.7 | 13,305–44,030 | ✓ | ✓ | ✓ | ❌ |
| `H2_keep_examples` | 25,052.4 | 13,397–44,345 | ✓ | ✓ | ✓ | ✓ |
| `H3_skeleton` | 5,375.3 | 4,262–6,916 | ✓ | ✓ | ❌ | ❌ |
| `H4_sop_only` | 2,373.1 | 1,939–3,937 | ✓ | partial | ❌ | ❌ |

Groups prefixed `gpt4o_*` are GPT-5.4 generations with the same configuration labels. GPT's loader uses task-specific assembled texts; absent Claude request logs prevent verification that the two generators received equivalent actual inputs. Standalone F/G reference files (14,947/16,138 tokens) are retained separately as legacy configurations.
