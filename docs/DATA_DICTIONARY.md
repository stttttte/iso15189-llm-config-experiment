# Data Dictionary

This document describes the schema of every JSON and structured markdown file in the release.

All scores are on a **0–5 integer scale** unless noted otherwise.

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
| `auto_weighted` | float | Composite weighted score |

---

## 2. LLM judge evaluations

### `data/scores/cnas_judge_final_15tasks.json`
- **Type**: `dict`
- **Source**: Claude Opus 4.6 as judge, CNAS senior reviewer prompt
- **Coverage**: 6 main groups (A/B/C/E/F/G) × 15 tasks × 3 reps = 270 evaluations
- **Note**: H groups (H2/H3/H4) were evaluated in sub-agent conversations; per-file Claude judge scores for three specific H-group papers (for ICC analysis) are stored in `h_claude_judge_supplement.json`

**Top-level keys**:
| Key | Type | Description |
|-----|------|-------------|
| `data` | dict | `data[task_id][group_name][rep_index]` → `[条款满足度, 可操作性, 内部一致性, PDCA闭环, 专业深度]` (list of 5 ints, 0–5) |
| `overall` | dict | `overall[group]` → overall mean score |
| `per_file` | dict | `per_file[group][file_name]` → per-file mean |
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
- **Purpose**: 2×2 symmetric validation matrix (2 generation models × 2 judges × 9 groups)
- **Schema**:
  ```json
  {
    "matrix": {
      "<group>": {
        "CC": float,  // Claude-gen → Claude-judge
        "CG": float,  // Claude-gen → GPT-judge
        "GC": float,  // GPT-gen → Claude-judge
        "GG": float   // GPT-gen → GPT-judge
      }, ...
    },
    "claude_bias": {<group>: float, ...},  // CC − GC
    "gpt_bias":    {<group>: float, ...},  // GG − CG
    "cross_ranking": [{<group>, <cross_eval_mean>}, ...]
  }
  ```

### `data/analysis/final_9groups_ranking.json`
- **Type**: `dict`
- **Purpose**: Composite ranking across auto + Claude + GPT judges

### `data/analysis/ablation_h2h3_results.json`
- **Type**: `dict`
- **Purpose**: 4-factor orthogonal ablation results (rule × skeleton × content × examples)

### `data/analysis/dual_judge_comparison.json`
- **Type**: `dict`
- **Purpose**: Claude-vs-GPT judge agreement statistics
- **Keys**: `comparison_table`, `pearson_paired`, `spearman_paired`, `icc_21`, `spearman_group_means`

---

## 4. Expert blind review

### `data/expert_blind_review/papers/paper_01..10.md`
- 10 QMS documents, anonymized and randomly shuffled
- Content is identical to source `outputs/<group>/<file>.md`; only filename is changed
- No group/task identifiers embedded in content

### `data/expert_blind_review/rating_sheet_filled.md`
- Expert's 5-dimension scores for each of 10 papers
- Scale: 0–5, allowing decimals (e.g., 3.5)
- Optional free-text rationale for each score

### `blind_review/key.json` ❌ **NOT released**
- Maps `paper_NN` → `(group, task, rep)`
- Intentionally excluded to preserve blind-review integrity for potential third-party validation studies

### `data/analysis/icc_results.json`
- Output of `code/compute_icc.py`
- ICC(2,1) and ICC(3,1) between expert and each LLM judge
- Pearson, Spearman, mean-difference statistics

---

## 5. Generated QMS documents

### `data/generated/<group>/<group>-<task>-<rep>.md`
- Complete generated QMS document (Chinese)
- 486 files total
- File naming: `<group>-<task>-<rep>.md`, e.g., `H4_sop_only-A1-2.md`
- Groups prefixed with `gpt4o_` are GPT-5.4 generations (as distinguished from the Claude Opus primary experiment)

### `configs/rules.md`
- The 3.1K expert-reviewed rule layer (terminology bans + vagueness bans)
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

| Group | Token count | Rule | Skeleton | Detail | Example |
|-------|-------------|------|----------|--------|---------|
| `A_bare` | 0 | ❌ | ❌ | ❌ | ❌ |
| `B_simple` | 0.4K | partial | ❌ | ❌ | ❌ |
| `C_full` | 71K | partial | ✓ | ✓ | ✓ |
| `E_rules_v2` (alias: `E_rules`) | 3.1K | ✓ | ❌ | ❌ | ❌ |
| `F_template` | 35K | ❌ | ✓ | ✓ | ❌ |
| `G_template_rules` (alias: `G_combined`) | 38K | ✓ | ✓ | ✓ | ❌ |
| `H2_keep_examples` | 61K | ✓ | ✓ | ✓ | ✓ |
| `H3_skeleton` | 13K | ✓ | ✓ | ❌ | ❌ |
| `H4_sop_only` | 6K | ✓ | partial | ❌ | ❌ |

Groups prefixed `gpt4o_*` are GPT-5.4 generations of the same 9 configurations.
