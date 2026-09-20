# Reproducibility Guide

This guide separates analyses reproducible from archived document-level records from historical summaries that cannot be fully reconstructed. It applies to the author-approved v1.2.0 correction release dated 20 September 2026. The historical v1.1.0 DOI does not identify this correction release.

The current manuscript is `paper/CCA_manuscript_consistency_revised.md` and its matching `.docx`. Earlier `paper/manuscript_v2_en_CCLM.*` and `Liu_2026_CCLM_*` submission files are retained historical artifacts, whose claims do not define this revision.

## 1. Environment

- Python 3.11+ and the packages in `requirements.txt`.
- Offline analysis uses NumPy, pandas, SciPy, and Pingouin; figure generation uses Matplotlib. Pillow supports image inspection, and tiktoken measures archived configuration text.
- API credentials are unnecessary for the offline commands below.

From the root of this corrected working copy:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

The dependency list specifies minimum versions, not a fully pinned environment. The corrected ICC and ranking workflow was checked with Python 3.12.14, pandas 2.2.3, NumPy 2.3.5, SciPy 1.18.1, and both Pingouin 0.5.5 and 0.6.1. The public repository and historical archive may still contain the earlier scripts until this revision is released.

## 2. Offline reproductions (no API calls)

### 2.1 Three-rater expert-vs-LLM ICC analysis

```bash
python3 code/compute_icc_3raters.py
```

Reads the three `rating_sheet_raterN_filled.md` files and `blind_key.json` in `data/expert_blind_review/`, plus the Claude main/supplemental scores and GPT summary in `data/scores/`. It writes `reproduced/icc_results_3raters.json`; `--output-dir DIR` selects another output directory.

Expected rounded results: 10 documents, 3 raters, expert-panel ICC(2,k)=0.982, expert-mean vs Claude ICC(3,1)=0.548, and expert-mean vs GPT ICC(3,1)=0.217. Mean judge-minus-expert differences are +0.90 for Claude and +0.52 for GPT. The JSON `diff` field uses the opposite direction, expert minus judge. Expert-group means place H4 fifth among seven represented groups.

`code/compute_icc.py` and single-rater result files are historical artifacts, not the primary three-rater reproduction workflow.

### 2.2 Nine-group composite ranking (Table 1)

```bash
python3 code/reproduce_ranking.py
```

Reads `all_scores_6groups.json`, `all_scores_h2h3.json`, `all_scores_h4.json`, and `gpt_judge_summary.json` in `data/scores/`. Each group contributes 45 Claude-generated documents. For each group, the script averages archived `auto_weighted` and GPT `mean` scores, normalizes the two sets of nine group means separately to [0,1], then averages the two normalized values:

```text
composite(g) = [minmax_9groups(auto_mean(g)) + minmax_9groups(GPT_mean(g))] / 2
```

Claude-judge scores do not enter this composite. This is not the mean of two LLM judges. Outputs are `reproduced/table1_ranking.json` and `reproduced/table1_ranking.csv` (or `--output-dir DIR`). Expected order: H4, H3, G, H2, E, C, F, B, A. Archived scores and ranks in `data/analysis/final_9groups_ranking.json` are retained; its third column now describes archived configuration-text size in thousands of cl100k_base tokens.

### 2.3 Historical 2×2 matrix and two different bias contrasts

```bash
python3 -c '
import json
from statistics import mean
from pathlib import Path
d = json.loads(Path("data/analysis/2x2_symmetric_complete.json").read_text())
m = list(d["matrix"].values())
print("Within-judge generator contrasts:")
print("Claude CC-GC:", mean(r["CC"]-r["GC"] for r in m))
print("GPT GG-CG:", mean(r["GG"]-r["CG"] for r in m))
print("Same-generator, between-judge sensitivity contrasts:")
print("Claude-generated CC-CG:", mean(r["CC"]-r["CG"] for r in m))
print("GPT-generated GG-GC:", mean(r["GG"]-r["GC"] for r in m))
'
```

Expected across-group means: +0.294, −0.301, +0.464, and −0.472, respectively. The legacy scalar fields `claude_bias` and `gpt_bias` store the latter two sensitivity contrasts, not the primary within-judge generator contrasts.

This command recalculates contrasts from archived group means. It does not reconstruct all means from raw ratings: some historical Claude cells lack underlying document-level records and verifiable denominators. The archived H4 CC value is 4.175 and must not be silently replaced with the mean of the surviving supplemental ratings. Cross-ranking is `(CG + GC) / 2` per group.

### 2.4 Structured component contrasts and bootstrap intervals

```bash
python3 code/bootstrap_ci.py
```

This reads the 405 Claude-generated documents in the GPT-judge summary and prints four contrasts with percentile bootstrap 95% intervals (10,000 independent document resamples, seed 42): E−A (rules), H4−E (skeleton), G−H3 (detailed content), and H2−G (examples). Each pair has 45 documents per group.

The rules difference is +0.511. The skeleton difference is +0.213, with rounded bootstrap interval [0.05, 0.38]. In the manuscript's four-contrast Mann–Whitney family with Benjamini–Hochberg correction, adjusted p values are 0.00056166 (rules) and 0.109195 (skeleton); the skeleton contrast is not significant after correction. The bootstrap interval and adjusted hypothesis test are different procedures. These component contrasts form a structured subset of configurations, not a Taguchi orthogonal array, and document-level resampling does not model task clustering.

### 2.5 Figures and archived auxiliary results

```bash
python3 code/make_figures.py
```

The corrected figure workflow writes under `reproduced/figures/`: archived configuration-text sizes, between-judge contrasts, expert-vs-judge Bland–Altman plots, and score/rank comparisons. No fixed token optimum or minimum input threshold is inferred. Historical images in `figures/` are retained for provenance.

`data/analysis/dual_judge_comparison.json` contains six-group agreement summaries (270 paired Claude-generated documents). `ablation_h2h3_results.json` is a historical eight-group ranking summary, not a complete four-factor inferential-analysis file. Reading these JSON files displays archived results; it should not be described as independently reproducing every statistic.

## 3. Online generation and judging (separate replication workflow)

`gpt_generate.py` and `gpt_cnas_judge.py` preserve the historical generation/judging workflow. They retain original path assumptions (`code/outputs`, `code/configs`, and other script-local locations), so the archived layout must be explicitly adapted before use. The archived model label is GPT-5.4; `gpt4o_` is a legacy filename prefix.

The historical GPT scripts read `GPT_API_KEY` and optionally `OPENAI_BASE_URL` (original default: AIHubMix). Current provider/model availability must be checked before any new run. New API calls incur costs and produce a new dataset; identical outputs are not expected. The original Claude workflow used Claude Code agents, and complete Claude request logs are absent. Substituting another API/model is a new experiment, not exact reproduction of the historical requests.

## 4. Configuration provenance and text sizes

The fixed configuration texts are A (empty), B (the string returned by `gpt_generate.load_simple_prompt()`), E (`configs/rules.md`), and C (`configs/full_config.txt`). F/G/H2/H3/H4 have 15 task-specific files each in `configs/per_task_assembled/`. The legacy GPT loader selects configurations by task; complete Claude input logs are unavailable, so identical input delivery across generators is unverified.

`data/analysis/configuration_token_inventory.json` records `len(tiktoken.get_encoding("cl100k_base").encode(text))` for the archived configuration text, plus task means and ranges. The counts exclude task messages, wrappers, tool instructions, and other unarchived context. They are not verified API input tokens. Old size labels were based on byte measurements and must not be interpreted as tokens or a minimum effective dose.

The standalone `F_template_config.txt` (14,947 tokens) and `G_template_rules_config.txt` (16,138) are legacy reference files. They do not replace the 15-task means of 23,089.7 and 24,234.7. See the [group table](DATA_DICTIONARY.md#7-group-naming-conventions) for every group's mean/range.

The `prepare_*.py` scripts also retain original local source-template paths. The referenced source-template collection is not included as `configs/source_templates/`; obtain any required licensed source materials and adapt paths before regenerating configurations. Existing assembled configurations support inspection without claiming a complete source-template rebuild.

## 5. Expert blind review

The archived panel comprised three same-institution coauthors who rated 10 Claude-generated Class A documents from seven groups, producing 30 forms and 150 dimension scores. The configuration labels were concealed during scoring; this is exploratory internal validation, not independent external validation. Sampling covers A1/A2/A3 and is not representative of every task or configuration.

The source mapping already appears in the released per-paper results. `blind_key.json` makes that existing mapping explicit for offline reproduction. Keeping a separate key file out of an old release did not preserve future blinding. For new independent ratings, create a fresh blinded packet and keep its mapping separate until scoring is complete. `prepare_blind_review.py` is a historical preparation script that requires path adaptation.

## 6. Statistical interpretation

Pingouin calculates ICC, while SciPy provides supporting statistical functions. ICC(2,1) describes two-way random-effects, single-rating absolute agreement; ICC(3,1) describes two-way mixed-effects, single-rating consistency. ICC(2,k) describes agreement for the mean of the three expert ratings. A high expert-panel ICC does not establish external validity or remove shared-institution bias.

The corrected ICC script handles Pingouin's older `ICC2`/`ICC3`/`ICC2k`/`ICC3k` labels and newer `ICC(A,1)`/`ICC(C,1)`/`ICC(A,k)`/`ICC(C,k)` labels. LLM-expert agreement and configuration rankings remain exploratory given the ten-document expert sample.

## 7. Archive limits

1. The generated corpus has 486 documents: 405 Claude (15 tasks) and 81 GPT (A1/B1/C1 only).
2. There are 759 unique document-level judge records: 486 GPT and 273 Claude. All 273 Claude-judged documents were Claude-generated: 270 main-group records plus 3 supplemental H-group records.
3. The earlier reported Claude coverage of 378 combined 270 main-group, 27 H-group, and 81 GPT-generated evaluations. The surviving supplemental three cannot automatically be treated as a subset of that historical total; subtraction does not establish an exact missing-record count. Some historical Claude means survive only in aggregate, with unreconstructable denominators.
4. Historical group aliases `E_rules` and `G_combined` correspond to `E_rules_v2` and `G_template_rules`. The corrected ICC workflow handles these aliases.
5. No verified Claude input-token logs are available. Archived text sizes support configuration description, not input equivalence, cost estimates, or token thresholds.
6. All generated documents are Chinese. The automated scorer contains Chinese terminology and phrasing rules, so its validity is language- and task-dependent.

## 8. Contact / questions

See [README.md](../README.md) and `CITATION.cff` for project and author information. This local correction has no new release DOI.
