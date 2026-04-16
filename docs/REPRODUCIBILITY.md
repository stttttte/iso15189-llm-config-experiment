# Reproducibility Guide

This document describes how to reproduce every table, figure, and statistic in the paper.

## 1. Environment

- **OS**: macOS / Linux (tested on macOS Darwin 25.3)
- **Python**: 3.11 (tested on 3.11.x via Anaconda)
- **LLM APIs**:
  - Claude Opus 4.6 — via Claude Code Agent tool (no SDK)
  - GPT-5.4 — via OpenAI-compatible endpoint (AIHubMix proxy used in the original experiment; any OpenAI-compatible endpoint works)

### Installation

```bash
git clone https://github.com/stttttte/iso15189-llm-config-experiment.git
cd iso15189-llm-config-experiment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment variables (required only for re-running LLM calls)

```bash
export GPT_API_KEY='sk-...'
export OPENAI_BASE_URL='https://aihubmix.com/v1'   # or any OpenAI-compatible endpoint
```

Claude Opus generation in the original experiment used Claude Code's Agent tool (not a REST SDK). To re-run with a different Claude-family model, substitute `anthropic` SDK calls; the CNAS judge prompt in `gpt_cnas_judge.py` is model-agnostic.

---

## 2. Offline reproductions (no API calls)

All analyses below read from the released JSON data and require only Python dependencies.

### 2.1 Expert-vs-LLM ICC analysis (Table 4.9 in paper)

```bash
python3 code/compute_icc.py
```

Reads:
- `data/expert_blind_review/rating_sheet_filled.md`
- `data/scores/cnas_judge_final_15tasks.json`
- `data/scores/h_claude_judge_supplement.json`
- `data/scores/gpt_judge_summary.json`

Outputs:
- Console: per-paper comparison table + ICC(2,1)/ICC(3,1) for 4 rater pairs
- File: `data/analysis/icc_results.json`

Expected: ICC(3,1) expert vs Claude ≈ 0.613 (p=0.02), expert vs GPT ≈ 0.195.

### 2.2 Group-level composite ranking (Table 4.1)

```bash
python3 -c "
import json
d = json.load(open('data/analysis/final_9groups_ranking.json'))
for row in d['ranking']:
    print(row)
"
```

### 2.3 2×2 symmetric matrix (Table 4.6, 4.7, 4.8)

```bash
python3 -c "
import json
d = json.load(open('data/analysis/2x2_symmetric_complete.json'))
print('Matrix:'); [print(g, v) for g, v in d['matrix'].items()]
print('\nClaude bias:', d['claude_bias'])
print('\nGPT bias:',    d['gpt_bias'])
print('\nCross-ranking:'); [print(row) for row in d['cross_ranking']]
"
```

### 2.4 Dual-judge agreement (§4.4)

```bash
python3 -c "
import json
d = json.load(open('data/analysis/dual_judge_comparison.json'))
print('Paired Pearson:',  d['pearson_paired'])
print('Paired Spearman:', d['spearman_paired'])
print('ICC(2,1):',        d['icc_21'])
print('Group-mean Spearman:', d['spearman_group_means'])
"
```

### 2.5 Auto-scorer on a single document

```bash
python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('auto_scorer', 'code/auto_scorer.py')
scorer = importlib.util.module_from_spec(spec); spec.loader.exec_module(scorer)

with open('data/generated/H4_sop_only/H4_sop_only-A1-2.md') as f:
    text = f.read()

print('Format:',      scorer.score_format(text, 'A'))
print('Clause:',      scorer.score_clause(text))
print('Terminology:', scorer.score_terminology(text))
"
```

---

## 3. Online reproductions (require API keys)

### 3.1 Re-run GPT-5.4 generation (81 docs)

```bash
export GPT_API_KEY='sk-...'
python3 code/gpt_generate.py --tasks A1,B1,C1 --model gpt-5.4 --concurrency 3
```

Expected runtime: ~15–25 minutes at concurrency 3. Outputs under `data/generated/gpt4o_*/`.

### 3.2 Re-run GPT judge on all 486 docs

```bash
python3 code/gpt_cnas_judge.py --all --model gpt-5.4 --concurrency 5
python3 code/gpt_cnas_judge.py --summarize
```

Expected runtime: ~30 minutes. Outputs per-file JSON under `data/scores/gpt_judge_scores/` and aggregated `gpt_judge_summary.json`.

### 3.3 Re-run Claude judge on selected files (Agent-based)

The original Claude judge was invoked through Claude Code's Agent tool (see `h_claude_judge_supplement.json._method`). To re-run:
- Copy the prompt template from `code/gpt_cnas_judge.py` (`JUDGE_PROMPT_TEMPLATE`)
- Replace `{content}` with the target file
- Send to any Claude-family model (e.g., via Anthropic SDK)
- Expect identical JSON schema: `{"条款满足度": {"score": 0–5, "reason": "..."}, ...}`

---

## 4. Regenerating configuration groups

If you want to rebuild the 9 group configurations from scratch:

```bash
# Groups A/B/C/E (simple / ablation baselines)
python3 code/prepare_template_config.py       # F, G for A1 only
python3 code/prepare_all_configs.py           # F, G for all 15 tasks

# Groups H2 / H3 (ablation)
python3 code/prepare_ablation_configs.py

# Group H4 (SOP-only skeleton — 6K optimum)
python3 code/prepare_h4_configs.py
```

These read `configs/rules.md`, `configs/task_messages/`, and the 10 source template files (included in `configs/source_templates/`) to produce each group's system prompt.

---

## 5. Expert blind review (third-party replication)

Anyone with a CNAS-qualified expert can reproduce the expert layer:

```bash
python3 code/prepare_blind_review.py
# Produces blind_review/paper_{01..10}.md + rating_sheet.md (blank template)
```

The expert then fills in `rating_sheet.md` (5 dimensions × 10 papers, 0–5 scale, decimals allowed). Run `code/compute_icc.py` to get ICCs vs. our LLM judges.

**Intentional omission**: `blind_review/key.json` (the group mapping) is **not included in the release**, preserving blind-review integrity for independent experts. Our expert's filled `rating_sheet_filled.md` (with our key) is included so that reproducers can compare their ratings with ours.

---

## 6. Statistical methods

All ICC / Pearson / Spearman / Kruskal–Wallis / Mann–Whitney / ANOVA calculations use:
- `pingouin` (v ≥ 0.5) for ICC
- `scipy.stats` for everything else

The ICC(2,1) and ICC(3,1) reporting follows Shrout & Fleiss (1979) conventions:
- ICC(2,1) = two-way random effects, absolute agreement, single rater — pingouin label `ICC(A,1)`
- ICC(3,1) = two-way mixed effects, consistency, single rater — pingouin label `ICC(C,1)`

---

## 7. Known issues / caveats

1. **Expert sample size n=10, n=1 rater** — the expert-layer analysis is underpowered for strong group-level claims. Results are directional, not definitive.
2. **GPT-5.4 generation covers only A1/B1/C1** (3 of 15 tasks) — by design, to control API cost. Full 15-task coverage is a planned extension.
3. **Claude judge historical group aliases**: `E_rules` (current: `E_rules_v2`), `G_combined` (current: `G_template_rules`). Scripts handle this automatically (`CLAUDE_GROUP_ALIAS` dict in `compute_icc.py`).
4. **LLM APIs are non-deterministic at temperature > 0**. Re-running generation will produce different documents. All fixed-seed sampling (blind-review paper selection) uses `random.Random(42)`.
5. **Chinese content**: all generated documents are in Chinese. The analysis pipeline is language-agnostic (operates on file content as strings).

---

## 8. Contact / questions

See [README.md](../README.md) for author contact. Issues and pull requests are welcome on GitHub.
