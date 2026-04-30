# A Compliance Study of LLM-Generated Medical Laboratory QMS Documents Under Different Configurations

**Author**: Sidi Liu¹

**Affiliation**: ¹ Department of Laboratory Medicine, West China Hospital Xiamen, Sichuan University, Xiamen, Fujian 361024, China

**Corresponding author**: Sidi Liu, lllsssddd@icloud.com, ORCID: 0009-0006-1695-5372

**Short title**: LLM configuration for ISO 15189 document compliance

**Keywords**: ISO 15189; medical laboratory; quality management system; large language model; prompt engineering; LLM-as-Judge; expert validation

---

## Abstract

**Objectives**: This study aimed to systematically compare the compliance of large language model (LLM)-generated ISO 15189:2022 medical laboratory quality management system (QMS) documents under different configuration strategies, to identify the optimal configuration range, and to expose systematic biases in current evaluation methods through a multi-tier evaluation framework.

**Methods**: An asymmetric two-model design produced 486 QMS documents in total: Claude Opus 4.6 × 9 configurations × 15 tasks × 3 replicates (405 documents), and, for cross-model validation, GPT-5.4 × 9 configurations × 3 tasks (A1/B1/C1) × 3 replicates (81 documents). The nine configurations were obtained by systematic substitution along four binary dimensions—rules, skeleton, detailed content, and examples—with token sizes ranging from 0 to 56 K. Three evaluation tiers were applied: (1) a Python automated compliance scorer; (2) dual LLM-as-Judge review by Claude and GPT-5.4 (864 ratings = 378 Claude-judge + 486 GPT-judge, including a 2 × 2 symmetric cross-model design); and (3) independent scoring by three ISO 15189-qualified experts on 10 stratified-randomly sampled, blinded documents. Inter-rater agreement was assessed by Pearson correlation, Spearman correlation, and intraclass correlation coefficients [ICC(2,1) and ICC(3,1)].

**Results**: (1) Four-factor substitution-contrast ablation (Benjamini–Hochberg FDR-adjusted) showed that, at the LLM-judge tier, only the rules layer reached significance (Δ = +0.511; BH-adjusted p < 0.001); the skeleton layer (Δ = +0.213; BH-adjusted p = 0.11), detailed content (Δ = −0.031; BH-adjusted p = 0.79), and examples (Δ = −0.053; BH-adjusted p = 0.61) did not. (2) The full-context configuration C_full (56 K) yielded cross-evaluated scores of 3.22–4.56 under Claude generation but dropped to 1.40–1.84 under GPT-5.4 generation, indicating that long-context exploitation in this scenario is model-specific to Claude Opus. (3) Claude-as-judge exhibited a self-preference bias of approximately +0.46, whereas GPT-as-judge showed an inverse bias of approximately −0.47. (4) Inter-rater agreement among the three experts reached ICC(2,k) = 0.982; expert mean versus Claude-as-judge gave ICC(3,1) = 0.548 (p = 0.04), versus GPT-as-judge ICC(3,1) = 0.217 (p = 0.26); both LLM judges systematically overestimated by 0.52–0.90 points. (5) The configuration ranked first by LLM judges, H4_sop_only (2 K skeleton), ranked second-to-last under expert evaluation (3.20, n = 2), whereas template-based configurations F_template (15 K), H2_keep_examples (25 K), and G_template_rules (16 K) ranked highest under expert evaluation (4.06–4.24).

**Conclusions**: The "optimal configuration" for LLM-assisted QMS document generation depends on the evaluation perspective. Scenarios prioritizing token efficiency and cost control should adopt H4_sop_only (2 K) or E_rules (3 K); scenarios involving formal submission and CNAS accreditation application should adopt G_template_rules (16 K) or F_template (15 K). C_full (56 K) should be avoided under current GPT-class models given the instability of their long-context capability. LLM-as-Judge can serve as a first-pass screening tool but cannot replace expert final review; Claude-as-judge ranks moderately consistently with experts and may serve as a coarse proxy, whereas GPT-as-judge is unsuitable for this purpose.

---

## 1. Introduction

ISO 15189:2022 *Medical laboratories — Requirements for quality and competence* is the international standard for medical laboratory accreditation, and adoption by Chinese medical laboratories has continued to expand under the China National Accreditation Service for Conformity Assessment (CNAS) framework [14]. CNAS-CL02:2023, the corresponding implementation document, was released in parallel. Such standards prescribe what laboratories *should do* but not *how to do it*, requiring each laboratory to construct, on its own, a complete **quality management system (QMS) documentation** covering the quality manual, procedure documents, and standard operating instructions. Based on the corresponding author's experience as an ISO 15189 assessor, such a system in a typical tertiary-level hospital clinical laboratory contains on the order of 100–300 controlled documents and spans structural organisation, clause mapping, form numbering, and responsibility assignment; manual drafting by the quality team typically takes several months, followed by several rounds of internal audit before the system can be finalised. Laboratories pursuing CNAS accreditation generally engage technical experts or trainers to guide them through this process.

The advancement of large language models (LLMs) has opened the possibility of automating this process. New-generation models such as Claude Opus 4.6 and GPT-5.4 have demonstrated competence in long-document generation, structured output, and domain terminology use [1, 2]. However, one question that has not been systematically studied is what kind of system prompt should be supplied to an LLM in order to produce a compliant and usable QMS document. Two extreme strategies are observed in practice: the "full-context hypothesis," which loads all potentially relevant material (the ISO standard text, CNAS criteria, the existing document library, and examples) into the system prompt, with token counts often reaching 50–100 K; and the "minimal hypothesis," which provides only rule constraints and section skeletons and relies on the model's internalized knowledge to generate content, with token counts of only a few thousand. Empirical evidence for either strategy remains limited because existing surveys of LLM behaviour and prompting [4, 12] have focused on general-purpose tasks and have not systematically compared specialized document scenarios such as QMS.

The bias inherent in evaluation methods is another deeper problem. LLM-generated quality is currently most often evaluated using the LLM-as-Judge approach (i.e., another LLM acts as the rater) [5]. Prior work has documented that LLM judges exhibit a self-preference bias (preferring text generated by their own model family) [6], but the manifestation of such bias in specialized domains—such as medical laboratory QMS—and its effect on configuration-comparison conclusions has not been empirically characterized.

Against this background, the present study was designed to use 486 generated documents, 864 LLM judge ratings, and 30 expert blind ratings to address the following research questions: (i) Which components of a system-prompt configuration (rules, skeleton, detailed content, examples) contribute to the quality of LLM-generated QMS documents? (ii) What is the minimum effective token budget? (iii) Does the optimal configuration generalize across generation models (Claude vs. GPT)? (iv) What is the magnitude of LLM judge self-preference bias? (v) Under cross-comparison of multi-tier evaluation (automated scoring, LLM judges, expert ratings), which configuration is the most robust?

---

## 2. Materials and methods

### 2.1 Configuration design

Nine controlled configurations were designed by systematic substitution along four binary dimensions: rules, skeleton, detailed content, and examples (Figure 1). Among them, A_bare (0 K) and B_simple (0.3 K) served as baselines; C_full (56 K) represented the full-context input strategy; E_rules (1.2 K) contained only the rules layer; F_template (15 K) contained the complete template without rules; G_template_rules (16 K) combined rules and template; H2_keep_examples (25 K) retained examples in addition to G; H3_skeleton (5 K) preserved the module skeleton while removing detailed content; and H4_sop_only (2 K) preserved only the single SOP skeleton most relevant to the task. The letter D is intentionally skipped in the alphabetic sequence: D_rules was an earlier rules variant that was deprecated after expert validation revealed terminology errors, and was replaced by E_rules_v2; the gap is retained to preserve the chronological identifier scheme.

![Figure 1](figures/fig1_config_composition.png)

**Figure 1.** Nine configurations tested for LLM-assisted ISO 15189 QMS generation. Left: inclusion of each configuration along the four dimensions of rules, skeleton, detailed content, and examples (✓ included, half-circle partial, — absent); right: the system-prompt size of each configuration (K tokens).

The rules layer was based on rules.md (1.2 K) and revised through domain-expert review: three incorrect terminology mappings were removed (instrument → equipment, calibrator product → calibrator, inter-laboratory comparison → proficiency testing); three target terms were corrected (specimen → sample, test item → measurand, linear range → reportable range); and 10 verified mappings together with 7 categories of vague-expression prohibitions were retained. The skeleton layer was extracted from the template library by the strip_to_skeleton algorithm, which preserved section headings, the introductory paragraph of each section, and form numbering lists, while removing verbatim clause excerpts, detailed table content, examples, detailed step lists, and fenced code blocks (markdown ```...``` constructs containing process diagrams, JSON snippets, or pseudocode).

All token counts reported in this study (K = thousand tokens) were computed using the cl100k_base tokenizer (OpenAI tiktoken library) and divided by 1000; for mixed Chinese–English medical text, this tokenizer typically differs from the Anthropic-native tokenizer by ≤10%, and is used as a reproducible approximation.

### 2.2 Generation models and tasks

The primary experiment used Claude Opus 4.6 (Anthropic, San Francisco, CA, USA), accessed through the Claude Code Agent interface (Anthropic's command-line agent framework) operated in text-generation mode: sub-agents returned text-only responses and no agentic tool calls (file system, web access, code execution) were performed during document generation, although the Claude Code framework's tool definitions remain present in the framework-level system prompt (see §4.5 limitation xiii). The model was evaluated across 9 prompting configurations, 15 QMS authoring tasks, and 3 independent replicates per cell, yielding 405 documents. The 15 tasks were stratified by CNAS audit scenarios into three classes of five tasks each: Class A (document drafting; e.g., personnel-training and competence-evaluation control procedures), Class B (system operation; e.g., annual internal-audit checklists), and Class C (audit simulation; e.g., review reports for internal quality-control procedure documents). The full task list and the original prompts are openly archived in the GitHub repository under `task_messages/` and `configs/`. For cross-model validation, GPT-5.4 (OpenAI, San Francisco, CA, USA) was accessed through the official openai Python SDK (≥ v1.0) configured with the AIHubMix endpoint (https://aihubmix.com) as the base URL; this routing was used because direct access to the OpenAI API was unavailable from the authors' geographic region during the study period. (Output directories use a legacy `gpt4o_*` prefix carried over from an earlier scripting iteration; the actual runtime model in all calls was GPT-5.4 as supplied to the SDK `model` parameter.) GPT-5.4 was evaluated on the same 9 configurations across one representative task from each class (A1, B1, and C1, defined as the first task in each class by index) with 3 replicates, yielding 81 documents. Both models received identical system-prompt configurations within each experimental cell and were run with identical generation parameters: temperature = 1.0 and max_tokens = 12,000; all other generation parameters used model defaults. The relatively high sampling temperature was chosen to reflect realistic interactive use, and three independent replicates per cell were included to capture the resulting stochastic variability. All API calls were executed between 2 April 2026 and 14 April 2026.

### 2.3 Three-tier evaluation framework

Compliance was evaluated through a complementary three-tier framework: an automated rule-based scorer (Tier 1), dual LLM-as-judge review (Tiers 2a and 2b), and independent blinded expert review (Tier 3). All three tiers reported scores on a common 0–5 integer scale; Tier 1 used an algorithmic rubric tailored to features that can be reliably detected by rule-based code, whereas Tiers 2 and 3 shared the descriptive five-dimensional rubric defined in Table 2.

#### 2.3.1 Tier 1 — Automated compliance scoring

A Python automated compliance scorer (`auto_scorer.py`, openly released; see Data availability) rated all 486 documents on **three primary dimensions**, which were combined into a weighted composite score.

**Format.** Required section headings were matched against task-class-specific lists (Class A procedure documents: 8 sections; Class B checklists/reports: 6 sections; Class C audit reports: 7 sections; common synonyms accepted), with additional checks for numbering depth and empty sections. Documents missing ≥3 required sections scored 1; those missing exactly one section scored 3.

**Clause coverage.** Regular-expression matching identified ISO 15189:2022 clause identifiers from chapters 4–8 (e.g., 5.4.1), filtered by a ±40-character context window to suppress spurious matches. Documents citing ≥10 unique clauses with at least one CNAS-CL02:2023 reference scored 5; documents containing no standard reference scored 1.

**Terminology compliance.** This dimension internally aggregates two complementary checks. (i) *Terminology mapping*: a 14-term mapping table aligned with the ISO 15189:2022 / CNAS-CL02:2023 vocabulary was applied; for example, 分析前过程 ("pre-analytical process") → 检验前过程 ("pre-examination process"), 标本 ("specimen") → 样品 ("sample"), and 不确定度 ("uncertainty") → 测量不确定度 ("measurement uncertainty"). Context-exclusion rules were applied to avoid false positives — for instance, 不确定度 occurring within the longer phrase 测量不确定度 was not flagged. (ii) *Vague-expression detection*: stock vague expressions characteristic of low-quality QMS drafts—including 及时 ("in a timely manner"), 相关人员 ("relevant personnel"), and 定期 ("periodically")—were detected using two complementary filters: a compound-word whitelist and a 30-character trailing window for explicit frequency quantifiers (e.g., a phrase anchored to "weekly" or "annually" was not flagged).

**Composite score.** The three measured dimensions were combined into a weighted aggregate (`auto_weighted`) using fixed weights defined in the `WEIGHTS` dictionary of `auto_scorer.py`. The dictionary contains entries for an originally planned 7-dimension scheme (format, clause coverage, terminology, logical consistency, operability, safety compliance, and manual-revision burden); the four entries beyond the three measured dimensions were not implemented in the current scorer and default to a neutral 3.0, which therefore introduces a constant offset across all 9 configurations and does not affect the relative ranking between them.

#### 2.3.2 Tier 2 — LLM-as-judge

Two LLM judges were deployed in a 2 × 2 symmetric cross-model design—Claude-generated × Claude-judge, Claude-generated × GPT-judge, GPT-generated × Claude-judge, and GPT-generated × GPT-judge—enabling orthogonal decomposition of self-preference bias.

**Tier 2a (Claude-as-judge).** Claude Opus 4.6 served as judge under a "CNAS chief assessor" role prompt (the `JUDGE_PROMPT_TEMPLATE` defined in `gpt_cnas_judge.py`, identical to the prompt used in Tier 2b), scoring each document on the five-dimensional rubric (Table 2) on a 0–5 scale. Generation parameters were temperature = 1.0 and max_tokens = 4,096; one rating was produced per document via a single API call. A total of 378 Claude-judge ratings were obtained, distributed as: 270 ratings covering the six core configurations (A_bare, B_simple, C_full, E_rules, F_template, G_template_rules) × 15 tasks × 3 replicates of Claude-generated documents (per-document raw JSON fully released); 81 ratings covering all 9 configurations × A1/B1/C1 × 3 replicates of GPT-generated documents (archived as aggregated means; see §4.5, Limitation x); and 27 ratings covering the H-group configurations (H2_keep_examples, H3_skeleton, H4_sop_only) × A1/B1/C1 × 3 replicates of Claude-generated documents (also archived as aggregated means).

**Tier 2b (GPT-as-judge).** GPT-5.4, accessed through the AIHubMix endpoint as described in §2.2, served as judge using exactly the same prompt, rubric, and 0–5 scale as Tier 2a, with identical generation parameters (temperature = 1.0, max_tokens = 4,096). All 486 generated documents were rated (405 Claude-generated + 81 GPT-generated), with one rating per document; per-document raw JSON files are fully retained and openly released.

Combined, Tiers 2a and 2b yielded 864 LLM-judge ratings (378 Claude-judge + 486 GPT-judge). The asymmetric counts reflect that the Claude judge was not run on the H-group × full-15-task subset or on the complete GPT-generated set (see §4.5, Limitation x); critically, all four 2 × 2 cells were populated, although some at aggregated-mean level only (see §4.5, Limitation x), ensuring that the self-preference bias decomposition could be performed at the cell-mean level.

**Scoring scale.** Each dimension was scored on a 0–5 integer scale: 5 = fully compliant (5-point anchor in Table 2); 4 = mostly compliant (between the 5- and 3-point anchors, minor issues only); 3 = partially compliant (3-point anchor); 2 = noticeably non-compliant (between the 3- and 1-point anchors); 1 = severely non-compliant (1-point anchor); and 0 = the dimension could not be evaluated because the document was essentially absent or non-substantive (e.g., the model returned only a planning query rather than the requested document). The 5/3/1 anchor descriptors were issued in identical wording to all judges (LLM and human); the intermediate scores 2 and 4 were assigned when the document fell between two adjacent anchors.

**Table 2.** Five-dimensional descriptive rubric shared by Tiers 2a, 2b, and 3.

| Dimension | Anchor at 5 | Anchor at 3 | Anchor at 1 |
|-----------|-------------|-------------|-------------|
| Clause coverage | All "shall" requirements of the relevant clauses are operationalised through concrete measures | Major clauses are covered but with omissions or surface-level treatment | Most clauses are merely cited without implementation, or major omissions are evident |
| Operability | Every step has a named role (job title), a quantified deadline, and an explicit output (form ID) | Most steps are actionable; a few remain vague | Pervasive use of "in a timely manner", "relevant personnel", and "periodically" without operational detail |
| Internal consistency | All referenced documents and forms appear in the corresponding sections; responsibilities are cleanly assigned | A few dangling references or minor textual contradictions | Many dangling references or conflicting responsibility assignments |
| PDCA closure | An explicit Plan–Do–Check–Act chain with execution records, effectiveness evaluation, non-conformity handling, and improvement | P–D–C are present but A (improvement/feedback) is missing | Execution steps only; no checking or improvement |
| Professional depth | Contains laboratory-specific detail (e.g., Westgard rules, measurement uncertainty, Sigma metrics, HIL indices, blind testing, PCR zoning, cold chain) | Some professional flavour, but largely generic | Generic content equally applicable to any laboratory |

#### 2.3.3 Tier 3 — Expert review

Three qualified ISO 15189 internal auditors independently scored 10 blinded, stratified-randomly sampled documents using the same five-dimensional rubric (Table 2) as the LLM judges. Rater 1 was the first author, who holds prior ISO 15189 accreditation-assessment experience; Raters 2 and 3 were qualified ISO 15189 internal auditors from the same institution. To minimise self-influence, Rater 1 completed scoring without inspecting any Tier 1 or Tier 2 outputs in advance; the Tier 1/2 outputs for the sampled papers were reviewed only after all three rater sheets had been submitted. The three raters scored independently and without communication; Raters 2 and 3 completed their scoring with no access to Rater 1's ratings, and the three rating sets were merged only after all submissions had been received. Written informed consent was obtained from Raters 2 and 3 before scoring. During scoring, the experts were free to consult the complete texts of ISO 15189:2022 and CNAS-CL02:2023, including their annexes.

**Sampling strategy.** Ten documents were drawn from the 486-document pool by stratified random sampling with a fixed Python random seed (`seed = 42`), stratified across seven core configurations × Class A procedure-document tasks (A1, A2, A3) — yielding a 21-stratum frame. The sample size of 10 was chosen to balance expert workload against stratification coverage; not all 21 strata are represented in the final sample (one or two documents per realised stratum). Class A was chosen because it constitutes the most stable and audit-relevant document type in CNAS reviews; cross-class generalisation is acknowledged as a limitation in §4.5.

**Conflict-of-interest declaration.** None of the three raters has any commercial, research, or consulting relationship with Anthropic, OpenAI, or any other LLM provider; none received funding or in-kind support from these entities for this study.

**Pre-scoring calibration.** No formal pre-scoring calibration session was conducted; the three raters scored independently using only the published five-dimensional rubric (Table 2) and the ISO 15189:2022 / CNAS-CL02:2023 standards. The absence of formal calibration is acknowledged as a methodological limitation in §4.5 (xii).

**Blinding procedure.** Blinding was implemented at four levels (script: `prepare_blind_review.py`, openly released):

(i) *File renaming.* Each sampled document was copied from its original path `outputs/{group}/{group}-{task}-{rep}.md` to a flat anonymised series `paper_01.md` … `paper_10.md`, removing the configuration-group and replicate identifiers from both the filename and the directory structure presented to the experts.

(ii) *Content sanitisation.* An automated text scan of all 10 blinded files confirmed zero occurrences of any model identifier ("Claude", "GPT", "Opus") or configuration-group token ("H4", "C_full", "G_template", "F_template", "H2_keep", "E_rules", "A_bare", "H3_skeleton") within the document body, ensuring that the model and configuration source could not be inferred from the text.

(iii) *Order randomisation.* The assignment of (group, task, replicate) triples to `paper_01`–`paper_10` was shuffled using a fixed Python random seed (`seed = 42`), producing an identical presentation order for all three experts. Only the task category (e.g., "Personnel training and competence-evaluation control procedure") was disclosed in the rating sheet, because this information is intrinsic to the document content and necessary for assessment; the underlying configuration group remained hidden.

(iv) *Key isolation.* The (paper_id → group, task, replicate) mapping (`blind_review/key.json`) was sealed before scoring began and was unsealed only after all three expert rating sheets had been submitted.
### 2.4 Statistical analysis

Pairwise between-group comparisons used the two-sided Mann–Whitney U test (scipy.stats.mannwhitneyu) on per-paper GPT-judge scores (n = 45 per group: 15 tasks × 3 replicates). Multiple-comparison adjustment within the four-factor ablation used the Benjamini–Hochberg false-discovery-rate (FDR) procedure (statsmodels.stats.multitest.multipletests, method='fdr_bh', α = 0.05); BH was preferred over Bonferroni given the exploratory nature of the four-contrast ablation. The four configuration-component effects were quantified under an orthogonal substitution scheme using targeted configuration contrasts: rules = E_rules_v2 vs A_bare; skeleton = H4_sop_only vs E_rules_v2; detailed content = G_template_rules vs H3_skeleton; examples = H2_keep_examples vs G_template_rules. Each effect Δ was defined as a *simple arithmetic mean difference*, Δ = mean(group_B) − mean(group_A), where each group mean is the unweighted average of the 45 per-paper GPT-judge scores in that configuration; no covariates, random effects, weighting, or shrinkage were applied. The same 45-per-group sample served as input to the corresponding Mann–Whitney U test reported alongside each Δ. No L9 orthogonal-array decomposition, least-squares-means estimation, or mixed-effects modelling was used. Inter-rater agreement was assessed by three complementary measures: Pearson correlation captures linear association while tolerating systematic shift between raters; Spearman correlation assesses rank-order agreement without assuming linearity; and intraclass correlation coefficients quantify reliability under the standard framework. We report all three to give a complete picture of inter-rater patterns. Four ICC variants defined by Shrout and Fleiss [13] are used: **ICC(2,1)** (single-rater absolute agreement, two-way random effects) and **ICC(3,1)** (single-rater consistency, two-way mixed effects) for pairwise comparisons (e.g., expert mean vs LLM judge, and rater-pair comparisons within the expert panel); and **ICC(2,k)** and **ICC(3,k)** — the corresponding *averaged k-rater* reliability variants with k = 3 — for the overall reliability of the three-rater expert panel. ICC computation used the pingouin 0.5 Python library. Self-preference bias was quantified by cross-model differencing as bias = (mean own-own) − (mean cross-own). The 9 configurations are not a Taguchi L9 orthogonal array; they form a structured subset of the 4-dimensional configuration space (rules / skeleton / detailed content / examples, each at three levels: absent / partial / full), selected to isolate each dimension through the targeted pairwise contrasts above rather than to satisfy the balanced-orthogonality requirement of an L9 design.

---

## 3. Results

### 3.1 Nine-group ranking at the LLM-judge tier

Across the 405 Claude-generated documents, the composite three-track score (automated scoring + Claude judge + GPT judge) ranked the configurations as follows: H4_sop_only (2 K) first (0.994), H3_skeleton (5 K) second, G_template_rules (16 K) third, H2_keep_examples (25 K) fourth, E_rules (1.2 K) fifth, C_full (56 K) sixth, F_template (15 K) seventh, B_simple eighth, and A_bare ninth. At the LLM-judge tier, H4 reached the highest composite score with the smallest token budget.

### 3.2 Four-factor substitution-contrast ablation

All four ablation effects are reported with both raw and Benjamini–Hochberg-adjusted p-values. The rules layer was the only factor reaching significance after correction (Δ = +0.511; raw p < 0.001; BH-adjusted p < 0.001). The skeleton layer (Δ = +0.213; raw p = 0.055; BH-adjusted p = 0.11) showed a directional positive effect that did not reach the conventional 0.05 threshold after multiple-comparison correction; we interpret this as suggestive evidence requiring replication. Detailed content (G vs. H3: Δ = −0.031; raw p = 0.79; BH-adjusted p = 0.79) and examples (H2 vs. G: Δ = −0.053; raw p = 0.46; BH-adjusted p = 0.61) showed no statistical contribution. H4 and H3 did not differ (Δ = −0.009, raw p = 0.80; this contrast is descriptive and lies outside the four-factor BH set, hence reported uncorrected), suggesting that the task-specific SOP skeleton (2 K) and the full module skeleton (5 K) are functionally equivalent. This ablation result holds only at the LLM-judge tier; expert-tier analysis is reported in Section 3.5.

### 3.3 2 × 2 symmetric cross-model validation

Figure 2 presents the 2 × 2 symmetric matrix (n = 9 configurations × 4 quadrants). C_full exhibited a marked drop in performance under GPT generation (GPT-gen × Claude-judge mean 1.40; GPT-gen × GPT-judge mean 1.84), whereas the same C_full under Claude generation produced cross-evaluated scores of 3.22–4.56. This indicates that the apparent usability of the 56 K full-context configuration under Claude Opus is model-specific rather than a general result. GPT-5.4 under the 56 K configuration exhibited failure modes including instruction forgetting, structural breakdown, and clause confusion.

![Figure 2](figures/fig2_2x2_symmetric.png)

**Figure 2.** Heatmap of the 2 × 2 cross-model symmetric design. Mean score (across tasks A1/B1/C1, 0–5 scale) for nine configurations (rows) × four generator–judge combinations (columns). C_full collapses markedly in the two GPT-generated columns (1.40 and 1.84, black-bordered cells), in sharp contrast with the two Claude-generated columns (4.56 and 3.22).

### 3.4 Self-preference bias of LLM judges

Computed as bias = (own-own) − (cross-own), the mean bias of the Claude judge was +0.464 (positive in 8 of 9 groups; the maximum, +1.33, occurred at C_full), and that of the GPT judge was −0.472 (negative in 8 of 9 groups, i.e., GPT preferred Claude-generated text). The two biases formed a symmetric, opposite-signed pattern of comparable magnitude, indicating that the bias originates at the judge end as a systematic phenomenon rather than from any genuine quality difference at the generation end. Skeleton-type configurations (E, H3, H4) showed the smallest bias (< 0.15).

After removing self-preference bias (by retaining only the cross-evaluation mean, i.e., the average of Claude-judge → GPT-gen and GPT-judge → Claude-gen), the nine groups ranked as follows: G_template_rules first (4.211), H3_skeleton second (4.167), E_rules third (4.133), H4_sop_only fourth (4.100). The four configurations G, H3, E, and H4 became statistically equivalent after debiasing (Δ < 0.11). C_full dropped to ninth (2.310) under this ranking.

### 3.5 Expert-tier validation

Inter-rater agreement among the three experts was excellent: ICC(2,k) = 0.982 (95% CI [0.95, 1.00]); ICC(3,k) = 0.981; pairwise ICC(2,1) values were 0.948 (R1–R2), 0.928 (R1–R3), and 0.969 (R2–R3), all reaching the excellent range (> 0.90). This indicates that the five-dimensional rubric is highly objective in design while also suggesting that consensus among same-institution experts may overestimate cross-institution agreement (see Section 5).

The expert mean compared with the Claude judge gave ICC(3,1) = 0.548 (p = 0.04), Pearson r = 0.573, Spearman ρ = 0.509, mean difference −0.905; the expert mean compared with the GPT judge gave ICC(3,1) = 0.217 (p = 0.26), Pearson r = 0.259, mean difference −0.525 (Figure 3). Both LLM judges systematically overestimated by 0.52–0.90 points; Claude versus expert ranking agreement was at a moderate level, whereas GPT versus expert agreement was poor.

![Figure 3](figures/fig3_expert_vs_llm.png)

**Figure 3.** Systematic overestimation of LLM judges relative to a three-rater expert panel (n = 10 papers × 3 raters). Horizontal axis: mean rating of the three experts. Vertical axis: LLM-judge rating. Left: vs Claude Opus 4.6 [ICC(3,1) = 0.548; Pearson r = 0.573; mean diff = −0.90]. Right: vs GPT-5.4 [ICC(3,1) = 0.217; Pearson r = 0.259; mean diff = −0.52]. Dashed line: 1:1 perfect agreement; configurations colour-coded.

The expert mean by configuration ranked as follows: F_template 4.24 (n = 1) first, H2_keep_examples 4.07 (n = 1) second, G_template_rules 4.06 (n = 2) third, C_full 3.45 (n = 2) fourth, H4_sop_only 3.20 (n = 2) fifth, E_rules 3.19 (n = 1) sixth, A_bare 3.04 (n = 1) seventh. The first-ranked configuration at the LLM-judge tier (H4_sop_only, 2 K) ranked second-to-last under expert evaluation (only 0.16 above A_bare). Overestimation by the LLM judges was largest for C_full and H4 (Δ = expert − LLM-judges mean = −1.00 and −1.05, respectively), suggesting that although these two configurations exhibit structural completeness and terminological compliance, their insufficient depth in clinical practice is detectable to experts.

### 3.6 Token size versus quality: a dual-perspective relationship

Figure 4 shows the relationship between token size and quality scores from two perspectives. The Claude-judge curve increases monotonically with token size, remaining at 4.90 even at C_full; the GPT-judge curve peaks near H4 (2 K) and then descends, collapsing at C_full; the expert curve peaks at the F/G template region (15–16 K) at 4.24 but reaches only 3.20 at H4 (2 K). The three curves diverge most prominently in the 2–5 K interval: the LLM judges already consider this region near peak, whereas experts judge it as still substantially below the optimum. This result indicates that token-efficiency-oriented configuration optimization and clinical-usability-oriented configuration optimization correspond to two different objective functions in the QMS generation scenario.

![Figure 4](figures/fig4_token_vs_quality.png)

**Figure 4.** Token size versus quality score — LLM judges peak at 2–5 K while experts prefer 15–25 K. Horizontal axis: system-prompt size (symlog scale). Vertical axis: quality score (0–5). Solid green line (squares): three-rater expert mean. Solid red line (circles): Claude Opus 4.6 judge. Solid blue line (triangles): GPT-5.4 judge. Orange-shaded band marks the token-efficient optimum (H4 / H3); green-shaded band marks the expert-judged clinical-usability optimum (F / G).

---

## 4. Discussion

### 4.1 Configuration minimization holds at the LLM tier but not at the expert tier

Four-factor ablation at the LLM-judge tier yields a parsimonious conclusion: the rules layer is necessary (BH-adjusted p < 0.001), the skeleton layer shows a directional benefit that did not reach significance after correction (BH-adjusted p = 0.11), while detailed content and examples contribute nothing. This conclusion is consistent with the lost-in-the-middle theory [3] and with prompt-minimization practice [12]. However, expert-tier analysis overturns this simplification: detailed content (the full template in F and G) substantially improves clinical usability (F 4.24 vs. H4 3.20, a difference of 1.04), because the LLM's internalized knowledge does not cover all sub-scenarios of clinical practice—including emergency-sample handling, patient-self-collected specimens, courier-personnel qualification, and rejection criteria. Such information must be explicitly supplied through the system prompt.

### 4.2 The full-context trap is model-dependent

C_full (56 K) is a typical "looks-safe" configuration option: it includes all potentially relevant material and aligns with the "more is safer" intuition. Yet under GPT-5.4 generation (cross-evaluated scores 1.40–1.84), it failed completely. A possible explanation is that Claude Opus has been more thoroughly trained for long-context attention and is able to extract effective signal from 56 K of context, whereas GPT-5.4 exhibits instruction forgetting under such long configurations. The methodological lesson is that any conclusion that "configuration X is acceptable" must be validated across generation models; single-model results are entangled with model characteristics and should not be extrapolated.

### 4.3 Limitations and appropriate use of LLM-as-Judge

The present study quantified two important categories of bias: cross-LLM bias (Claude overestimates its own family by +0.46; GPT shows the inverse −0.47) and machine-versus-expert bias (both LLM judges overestimate by 0.52–0.90 points). The Claude-judge ranking was moderately consistent with the three-expert mean (ICC = 0.548) and may serve as a coarse proxy: in large-scale generation scenarios, Claude judging can first filter out clearly low-quality outputs, sparing expert time. The GPT judge's ranking agreement with experts was only ICC = 0.217 and is unsuitable as a proxy. Critical documents (those for submission, formal system files, and operational deployment) must undergo expert final review.

### 4.4 Configuration recommendations stratified by scenario

Synthesizing evidence from all three tiers, configuration recommendations for different use scenarios are summarized below (Table 6):

| Use scenario | Recommended configuration | Tokens | Rationale | Trade-off |
|--------------|---------------------------|--------|-----------|-----------|
| Rapid first-draft generation; internal iteration | H4_sop_only or E_rules | 1–2 K | Near-optimal at LLM tier; highest efficiency | Requires manual supplementation of clinical detail |
| Multiple SOP drafting | H4 or H3 | 2–5 K | Task-specific skeleton plus rules | Same as above |
| Formal documents for CNAS submission | G_template_rules | 16 K | Highest expert acceptance; cross-model robust | Higher token cost |
| Complete quality manual | F_template or G | 15–16 K | Highest expert scores | Same as above |
| Not recommended | C_full (56 K) | — | Collapses under GPT generation; lowest cross-evaluation rank | — |
| Not recommended | A_bare, B_simple | — | Baseline too low; lacks compliance | — |

The recommended practical workflow is to generate the first draft with H4, supplement clinical detail by manual review, and finally regenerate or refine critical documents with G.

### 4.5 Limitations

The present study has the following limitations. (i) Limited expert sample size: n = 3 raters × 10 documents, with only 1 to 2 documents per group, supporting only directional ranking conclusions and not strict statistical inference. Multi-center validation with 3–5 experts × 30–50 documents across institutions is a key direction for future work. (ii) Two-edged effect of same-institution agreement: the very high agreement among the three experts [ICC(2,k) = 0.982] is both evidence of the validity of the five-dimensional rubric and a possible reflection of shared professional culture, training lineage, and clause-interpretation habits within the same institution, which may overestimate cross-institution generalizability. (iii) Dual role of the first author: the first author acted both as Rater 1 and as study designer. Raters 2 and 3 completed their scoring without knowledge of Rater 1's ratings, and the data of all raters are fully released. (iv) Shared rubric between experts and LLM judges: there is a risk of shared-measurement bias; future work should add expert-native dimensions such as clinical usability. (v) Limited GPT-5.4 task coverage: only A1/B1/C1 (81 documents) were generated. (vi) Domain specificity: results are restricted to ISO 15189 medical laboratories, and transferability to other standards such as ISO 17025 or ISO 9001 remains to be validated. (vii) Absence of third-party LLM judges: only Claude and GPT were used as judges. (viii) Language scope: all QMS documents were in Chinese; the effects in English or other languages have not been verified. (ix) Model temporality: the quality of generated documents depends on the model used, and the conclusions of the present study may need to be re-validated as LLMs continue to iterate. (x) Raw-data retention for cross-judge cells: per-paper raw scores for the Claude-judge × GPT-gen quadrant and for the Claude-judge × H-group Claude-gen subset were archived only as aggregated means; the per-paper JSON files were not retained. The 2 × 2 self-preference matrix therefore cannot be independently recomputed from the lowest-level data, although per-paper raw Claude-judge ratings for the six core configuration groups (A/B/C/E/F/G; 270 ratings) and all 486 GPT-judge per-paper ratings are fully released. (xi) Intra-judge reliability not assessed: each LLM judge scored each document exactly once; judges were not asked to re-score documents to quantify intra-judge variance. Inter-judge reliability is captured via the 2 × 2 cross-comparison between Claude and GPT judges and via the three-expert ICC analysis. (xii) No pre-scoring expert calibration: the three raters scored independently from the published five-dimensional rubric and the ISO 15189:2022 / CNAS-CL02:2023 standards without a prior calibration session in which a few example documents would be scored together to align interpretation. The very high inter-rater agreement [ICC(2,k) = 0.982] indicates that the rubric was sufficiently self-explanatory in this institutional context, but a formal calibration step would strengthen replication in future multi-centre studies. (xiii) Claude Code Agent wrapper: Claude Opus 4.6 generation and Claude-judge ratings were performed via Claude Code's Agent tool rather than through a direct Anthropic REST SDK call. The Claude Code framework adds a constant framework-level system prompt (tool definitions and file-system guidance) on top of each configured QMS-generation or judge prompt; the absolute prompt length seen by the model is therefore larger than the per-configuration token counts reported in §2.1. Because this framework overhead is identical across all 9 configurations and across all judging calls, between-configuration relative comparisons and the relative judge–expert agreement findings remain valid; however, exact reproduction of absolute scores requires the same Claude Code version, and re-running the same configurations through a direct Anthropic SDK call may yield slightly different absolute scores. (xiv) AIHubMix routing not independently audited: GPT-5.4 was accessed via the AIHubMix proxy endpoint, which advertises transparent forwarding to the upstream OpenAI API. We did not independently verify response equivalence against direct OpenAI calls; subtle routing-level differences (request batching, header handling) cannot be ruled out, although the GPT-5.4 model identifier was preserved end-to-end. (xv) Temperature setting: all generations used temperature = 1.0 to reflect realistic interactive use. This introduces stochastic variance (mitigated by the 3 replicates per cell), but reduces strict bit-level reproducibility; future studies seeking deterministic comparison should re-run with temperature = 0.

---

## 5. Conclusions

The optimal configuration for LLM-assisted ISO 15189 QMS document generation depends on the evaluation perspective. At the LLM-judge tier, H4_sop_only (2 K) achieves the highest composite score; under expert evaluation, F_template (15 K), H2_keep_examples (25 K), and G_template_rules (16 K) tie at the top (mean 4.06–4.24), with H4 ranked second-to-last. Scenarios prioritizing token efficiency and cost control should adopt H4 or E_rules (1–2 K); scenarios requiring formal submission and CNAS accreditation application should adopt G or F (15–16 K); C_full (56 K) should be avoided. LLM-as-Judge can serve as a first-pass screening proxy (Claude is more effective than GPT), but critical documents must undergo expert final review.

---

## Declarations

**Research funding**: The study received no external research funding.

**Author contributions**: Sidi Liu independently designed the study, conducted the experiments, analyzed the data, drafted the manuscript, and finalized the text, and takes full responsibility for the content of the article.

**Competing interests**: The author declares no competing interests.

**Informed consent**: Written informed consent was obtained from Raters 2 and 3 prior to their participation in expert blind review. The consent form described the study purpose, the use of the ratings, the anonymity safeguards, and the right to withdraw at any time.

**Ethical approval**: This study did not involve patient data, biological samples, or human intervention. The QMS documents generated and evaluated used fictitious placeholder names (e.g., "Doctor Li," "Doctor Zhang") and did not contain any identifiable personal information. The inter-rater data fall within methodological research and were collected with informed consent.

**Data availability**: The 486 generated documents, 864 LLM-as-Judge ratings, 30 expert blind ratings, and all analysis scripts are publicly available on GitHub (https://github.com/stttttte/iso15189-llm-config-experiment) under a dual MIT (code) and CC BY 4.0 (data) licence.

---

## Acknowledgements

The author thanks the two colleagues who participated in expert blind review (Raters 2 and 3) for providing an independent expert perspective on a fully informed-consent basis.

---

## References

1. Anthropic. Claude Opus 4.6 System Card. 2025. Available at: https://www.anthropic.com/claude

2. OpenAI. GPT-5 System Card. 2025. Available at: https://openai.com/

3. Liu NF, Lin K, Hewitt J, Paranjape A, Bevilacqua M, Petroni F, et al. Lost in the middle: how language models use long contexts. Trans Assoc Comput Linguist 2024;12:157–73.

4. Zhao WX, Zhou K, Li J, Tang T, Wang X, Hou Y, et al. A survey of large language models. arXiv preprint 2023; arXiv:2303.18223.

5. Zheng L, Chiang WL, Sheng Y, Zhuang S, Wu Z, Zhuang Y, et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In: Advances in Neural Information Processing Systems. 2023.

6. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. arXiv preprint 2024; arXiv:2404.13076.

7. ISO 15189:2022. Medical laboratories — Requirements for quality and competence. Geneva: International Organization for Standardization; 2022.

8. Boiko DA, MacKnight R, Kline B, Gomes G. Autonomous chemical research with large language models. Nature 2023;624:570–8.

9. Jin D, Pan E, Oufattole N, Weng WH, Fang H, Szolovits P. What disease does this patient have? A large-scale open domain question answering dataset from medical exams. Appl Sci 2021;11:6421.

10. Tan H, Guo Z, Shi Z, Xu L, Liu Z, Li X, et al. ProxyQA: an alternative framework for evaluating long-form text generation with large language models. In: Proceedings of ACL. 2024.

11. Chiang WL, Zheng L, Sheng Y, Angelopoulos AN, Li T, Li D, et al. Chatbot Arena: an open platform for evaluating LLMs by human preference. arXiv preprint 2024; arXiv:2403.04132.

12. Schulhoff S, Ilie M, Balepur N, Kahadze K, Liu A, Si C, et al. The prompt report: a systematic survey of prompting techniques. arXiv preprint 2024; arXiv:2406.06608.

13. Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. Psychol Bull 1979;86:420–8.

14. Yang S, Zhou Y, Wang C, Luo M. The 'Double Helix' model of quality monitoring: risk mapping of quality management system during initial ISO 15189 implementation in a medical laboratory. PLoS One 2026;21:e0342129.

---

**Word count (main text including references)**: ~5400 words
**Tables**: 1 (Table 6 — configuration recommendations stratified by scenario)
**Figures**: 4
**References**: 14
