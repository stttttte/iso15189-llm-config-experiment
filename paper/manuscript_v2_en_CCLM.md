# Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: A Comparison of Claude and GPT Under Expert Review

**Authors**: Sidi Liu¹, Dongdong Li²,*

**Affiliations**: ¹ Department of Laboratory Medicine, West China Hospital Xiamen, Sichuan University, Xiamen, Fujian 361024, China; ² Department of Laboratory Medicine, West China Hospital, Sichuan University, Chengdu, Sichuan 610041, China

**Corresponding author**: * Dongdong Li, Department of Laboratory Medicine, West China Hospital, Sichuan University; email [to be provided]; ORCID [to be provided]

**ORCID**: Sidi Liu 0009-0006-1695-5372; Dongdong Li [to be provided]

**Short title**: LLM-assisted drafting of ISO 15189 laboratory documents

**Keywords**: ISO 15189; medical laboratory; quality management system; large language model; prompt engineering; LLM-as-judge; expert validation

---

## Abstract

**Objectives**: To evaluate the ISO 15189:2022 compliance of QMS documents drafted with LLM assistance across prompting configurations, compare Claude with GPT, and quantify the systematic bias of LLM judges (LLM-as-judge) against expert ratings.

**Methods**: We generated 486 QMS documents using Claude Opus 4.6 (9 configurations × 15 tasks × 3 replicates = 405) and GPT-5.4 (81 for cross-model validation), spanning four prompt-content dimensions (rules, document skeleton, detailed content, worked examples; 0–56,000 tokens). Compliance was rated on a 0–5 Likert scale via three tiers: an automated rule-based scorer, review by two LLM judges (864 ratings), and blinded review of 10 stratified-sampled documents by three qualified ISO 15189 internal auditors. Ablation effects used Mann–Whitney U with BH correction and bootstrap 95% CIs; inter-rater reliability used ICC variants.

**Results**: At the LLM-judge tier, only the rules component produced a significant compliance gain (Δ = +0.511, bootstrap 95% CI [+0.28, +0.75]; BH-adjusted p < 0.001). C_full (the maximal full-context configuration loading all reference material; ~56,000 tokens) scored 3.22–4.56 with Claude vs. 1.40–1.84 with GPT-5.4 (each range spanning the two judges' mean scores). Both LLM judges rated Claude-generated outputs ~0.30 points higher (Panickssery self-preference index: +0.29 Claude, −0.30 GPT), an effect concentrated at C_full; because both judges favoured Claude rather than each its own family, this is incompatible with classical self-preference. Within-institution agreement among the three experts was excellent [ICC(2,k) = 0.982], with cross-institution generalisability untested; Claude–expert agreement was moderate [ICC(3,1) = 0.548, 95% CI −0.08 to 0.86] and GPT–expert poor [ICC(3,1) = 0.217, 95% CI −0.44 to 0.72]; LLM judges overestimated experts by 0.52–0.90 points. The LLM-favoured H4_sop_only (~2,000 tokens) fell to fifth of seven under expert review (3.20), whereas template-anchored F_template, H2_keep_examples, and G_template_rules ranked highest (4.06–4.24).

**Conclusions**: In this study, the optimal configuration varied with the evaluation tier: minimal prompts (~1,000–2,000 tokens) were better suited to exploratory drafts requiring subsequent human review; template-anchored prompts (~15,000–16,000 tokens) tended to perform best for accreditation submission; and C_full (~56,000 tokens) performed markedly worse with GPT-5.4 and should be used with caution—a preliminary observation based on three tasks and not corroborated at the expert tier. LLM-as-judge can support first-pass screening, but expert final review remains indispensable.

---

## 1. Introduction

ISO 15189:2022 *Medical laboratories — Requirements for quality and competence* [1] is the international standard for medical laboratory accreditation. In China, its adoption by medical laboratories continues to expand [2]; the standard is administered by the China National Accreditation Service for Conformity Assessment (CNAS), which has issued the corresponding national implementation document, CNAS-CL02:2023. Such standards prescribe what laboratories must achieve, not how to achieve it, requiring each laboratory to construct a quality management system (QMS) documentation set comprising a quality manual, procedure documents, and standard operating instructions. Based on the first author's experience as an ISO 15189 internal auditor, such a system in a tertiary-level hospital clinical laboratory contains on the order of 100–300 controlled documents and spans structural organisation, clause-to-document mapping, form numbering, and responsibility assignment; drafting by an in-house quality team typically takes several months, followed by multiple rounds of internal audit before finalisation. Laboratories pursuing CNAS accreditation typically engage external technical experts or trainers to guide this process.

The advancement of large language models (LLMs) offers the possibility of substantially reducing this workload. State-of-the-art models such as Claude Opus 4.6 and GPT-5.4 have shown increasing competence in long-document generation, structured output, and the use of domain-specific terminology [3, 4], and LLMs have been applied to scientific research [5] and evaluated on medical question-answering benchmarks [6]. However, the optimal system-prompt design for producing compliant and operationally usable QMS documents has not been systematically investigated. Two approaches have emerged in practice: a full-context approach that loads all potentially relevant material—the ISO and CNAS standard texts, the laboratory's existing SOP documents, and worked examples—into the system prompt, often exceeding 50,000–100,000 tokens; and a minimal-prompt approach that supplies only rule constraints and section skeletons, relying on the model's own knowledge to generate the content, with prompts limited to a few thousand tokens. Empirical evidence supporting either approach remains limited, as existing surveys of LLM behaviour and prompting [7, 8] have largely addressed general-purpose tasks and have not specifically examined specialised regulatory-document scenarios such as QMS authoring.

A second issue lies in the evaluation methodology itself. LLM-generated outputs are currently most commonly assessed by the LLM-as-judge approach, in which a separate LLM assigns the scores [9]. In addition, methods for assessing long-form generation quality [10] and preference benchmarks built from large-scale human voting [11] are two other principal approaches. Studies have found that LLM judges tend to favour outputs from models in their own family (self-preference bias) [12]. However, whether and how this bias arises in specialised, regulated settings such as medical-laboratory QMS, and how it affects comparisons between configurations, has not been empirically characterised.

To address these gaps, the present study generated 486 QMS documents, collected 864 LLM-judge ratings, and obtained 30 blinded expert ratings, addressing the following five questions: (i) Which of the four prompt components—rules, document skeleton, detailed content, and worked examples—contributes most to compliance? (ii) What is the minimum number of tokens needed? (iii) Is the optimal configuration consistent between Claude Opus 4.6 and GPT-5.4? (iv) How large is the LLM-judge self-preference bias in this domain? (v) Which configuration performs robustly across all three tiers—automated scoring, LLM judges, and expert ratings?

This study uses LLMs as tools for assisting document drafting and for rapid internal audit; the actual authoring, review, and approval must still be carried out under expert supervision. ISO 15189:2022 requires these documents to reflect the laboratory's own validated processes and to be approved by competent personnel, and drafting is itself part of how staff form and demonstrate that competence. An LLM can generate a first draft within minutes, but a draft is not a controlled document: it carries no accountability, has not been checked against the laboratory's actual methods, instruments, or workflows, and has not been approved—it serves mainly as a reference. Our findings reinforce this: the LLM judges diverged from the expert raters, indicating that the model cannot reliably produce compliant documents on its own and may even generate a substantial amount of unnecessary content. We therefore recommend that every configuration be used under human supervision.

---

## 2. Materials and methods

### 2.1 Configuration design

We designed nine system-prompt configurations, each loaded with different content, which falls into four categories: rules, document skeleton, detailed content, and worked examples. The content composition and token size of each configuration are given in Figure 1. Each pair of configurations used for comparison differs in only one of these categories, so comparing them isolates the effect of that category (see §2.4.2 for the comparison design).

The letter D was skipped in the numbering: the early D_rules variant was discarded after expert validation found terminology errors and was replaced by E_rules_v2; the gap is retained to keep the configuration identifiers consistent.

The rules component is a `rules.md` file (~1,200 tokens). After domain-expert review removed three incorrect mappings and corrected three terms, the final set retained 10 terminology mappings (e.g. specimen was normalised to sample, and inter-laboratory comparison to proficiency testing) and seven categories of prohibited vague expressions. The document skeleton was extracted from the institutional templates by a custom script (*strip_to_skeleton*), keeping section headings, each section's introductory paragraph, and form numbers, and removing verbatim clauses, detailed tables, worked examples, step-by-step procedures, and code blocks.

All token counts in this study were computed with the publicly available cl100k_base tokenizer (OpenAI tiktoken). Claude's own tokenizer is not public, but on mixed Chinese–English text the two differ by less than 10%; we used the public tool so that anyone can reproduce the same counts.

### 2.2 Generation models and tasks

The primary experiment used Claude Opus 4.6 (Anthropic, San Francisco, CA, USA), accessed through the Claude Code Agent (Anthropic's command-line agent framework) in text-only mode: no tool calls (file system, web access, code execution) occurred during generation, although the framework's built-in tool definitions remain in the system prompt (see §4.6, limitation xiii). Across 9 configurations and 15 tasks, with each combination repeated 3 times, this yielded 405 documents. The 15 tasks were grouped by CNAS audit scenario into three classes of five: Class A, document drafting (e.g., a personnel-training and competence-evaluation control procedure); Class B, system operation (e.g., an annual internal-audit checklist); and Class C, audit simulation (e.g., a review report for an internal quality-control procedure). A full list of the 15 tasks (name, class, and the corresponding ISO 15189:2022 clauses) is given in Supplementary Table S1; the original prompts are in the GitHub repository under `task_messages/` and `configs/`. Note that these 15 tasks cover system-level documents concerned with document control, internal audit, and management review; they do not include technical documents such as method validation/verification reports or measurement-uncertainty procedures (see §4.6, Limitation xviii).

For cross-model validation, GPT-5.4 (OpenAI, San Francisco, CA, USA) was accessed through the official openai Python SDK (v2.30.0); because direct access to the OpenAI API was unavailable from the authors' region during the study, the base URL was pointed to the AIHubMix endpoint (https://aihubmix.com). To limit API cost, GPT-5.4 generation covered only three tasks: the first task of each class—A (document authoring), B (system operation), and C (audit simulation)—namely A1, B1, and C1, so that all three classes were represented; these three tasks were not randomly sampled. GPT-5.4 was run on the same 9 configurations, with each task repeated 3 times, yielding 81 documents. (Output directories retain a legacy `gpt4o_*` prefix from an earlier script, but the actual model in all runs was GPT-5.4.)

For every combination, both models received identical system prompts, but their generation parameters were not identical. Claude Opus 4.6 was run through the Claude Code Agent, which does not expose temperature or max_tokens; these parameters were not set explicitly in this study and their values were determined by the framework. GPT-5.4 was called through the API with temperature = 0.7 and max_completion_tokens = 16,000 set explicitly. Both settings make the same prompt produce somewhat different outputs each time, so each combination was run 3 times to reflect this variability. The consequences of this parameter mismatch for cross-model comparison are discussed in §4.6, Limitation (xvii). All API calls were made between 2 April 2026 and 14 April 2026.

### 2.3 Three-tier evaluation framework

We evaluated compliance using a complementary three-tier framework: an automated rule-based scorer (Tier 1), two LLM judges (Tiers 2a and 2b), and an independent blinded expert review (Tier 3). All three tiers scored on a common 0–5 integer scale. Tier 1 scored automatically, covering only structural features that code can detect objectively; Tiers 2 and 3 shared a single rubric—the five dimensions listed in Table 1: clause coverage, operability, internal consistency, PDCA closure, and professional depth.

#### 2.3.1 Tier 1 — Automated scoring of structural compliance

The auto-scorer (`auto_scorer.py`, open source) rated all 486 documents on three dimensions, which were combined into a weighted composite. This tier measures only structural compliance—the format, clause citations, and terminology that code can detect objectively; it does not assess the clinical operability or logical consistency of the content, which fall to Tiers 2 and 3.

**Format.** Whether the document includes the section headings, numbering depth, and non-empty content required by its task class; more omissions mean a lower score.

**Clause coverage.** Regex matching of ISO 15189:2022 (chapters 4–8) and CNAS-CL02:2023 clause identifiers; the more independent clauses a document cites, the higher its score. This metric records how many clauses a document cites, not whether those clauses are actually implemented. A document that merely states "internal quality control shall be performed in accordance with 7.3.1", without specifying an actual QC scheme, still counts as covering that clause. Tiers 2 and 3 fill this gap: the "clause coverage" dimension of Table 1 assigns a score of 1 when many clauses are cited but left unimplemented. A high Tier 1 clause-coverage score therefore does not mean a document is ready to be submitted for accreditation.

**Terminology compliance.** Two checks. (i) *Terminology mapping*: a vocabulary table validated against ISO 15189/CNAS (e.g., 标本 "specimen" normalised to 样品 "sample", and 不确定度 "uncertainty" to 测量不确定度 "measurement uncertainty") is used to flag non-preferred terms. (ii) *Vague-expression detection*: stock vague terms such as 及时 ("in a timely manner"), 相关人员 ("relevant personnel"), and 定期 ("periodically") are detected. Both apply context-exclusion rules to avoid false positives.

**Composite score.** The three dimensions were combined into a single weighted total (`auto_weighted`) using format = 0.18, clause coverage = 0.22, and terminology = 0.13; the Tier 1 rankings in §3 are based on this score. (The `WEIGHTS` dictionary in `auto_scorer.py` retains four entries from an earlier design that were not used in this study.)

#### 2.3.2 Tier 2 — LLM-as-judge

The two judges (Claude and GPT) each scored documents from both models (Claude and GPT), forming a 2 × 2 cross design; this separates a judge's self-preference (favouring its own family) from genuine differences in quality.

**Tier 2a (Claude judge).** Claude Opus 4.6, in the role of a "CNAS chief assessor", scored each document 0–5 on the five dimensions of Table 1, once per document; judging was run through Claude Code Agent sub-agents, with temperature and max_tokens not set explicitly, using the same prompt as Tier 2b. This produced 378 ratings, covering 77.8% of the 486 documents; the remaining 108 documents (22.2%) were not scored by the Claude judge. The retention of raw per-document data is described in §4.6, Limitation x.

**Tier 2b (GPT judge).** GPT-5.4 (accessed via the AIHubMix endpoint, as in §2.2) used the same prompt, rubric, and 0–5 scale as Tier 2a to rate all 486 documents once each (405 Claude-generated + 81 GPT-generated); per-document raw JSON is openly released. Its judging parameters were temperature = 0 and max_completion_tokens = 2,000, which differ from those of Tier 2a (see §4.6, Limitation xvii). We also confirmed that no output was truncated by the max_tokens cap (all 486 JSON files parsed successfully).

Together, the two judges produced 864 ratings (378 Claude + 486 GPT). The counts are unequal because the Claude judge was not run on every document (see §4.6, Limitation x); nonetheless, all four 2 × 2 cells contained data, so the self-preference decomposition could still be performed.

**Scoring scale.** Each dimension was scored on a 0–5 integer scale. Table 1 defines the 5-, 3-, and 1-point anchors (fully, partially, and severely non-compliant); the intermediate scores 4 and 2 fall between adjacent anchors, and 0 means the dimension could not be evaluated (the document was essentially absent, or the model returned only a query rather than the requested document). These anchor descriptions were identical for all judges and experts.

**Table 1.** Five-dimensional descriptive rubric shared by Tiers 2a, 2b, and 3.

| Dimension | Anchor at 5 | Anchor at 3 | Anchor at 1 |
|-----------|-------------|-------------|-------------|
| Clause coverage | All "shall" requirements of the relevant clauses are operationalised through concrete measures | Major clauses are covered but with omissions or surface-level treatment | Most clauses are merely cited without implementation, or major omissions are evident |
| Operability | Every step has a named role (job title), a quantified deadline, and an explicit output (form ID) | Most steps are actionable; a few remain vague | Pervasive use of "in a timely manner", "relevant personnel", and "periodically" without operational detail |
| Internal consistency | All referenced documents and forms appear in the corresponding sections; responsibilities are cleanly assigned | A few dangling references or minor textual contradictions | Many dangling references or conflicting responsibility assignments |
| PDCA closure | An explicit Plan–Do–Check–Act chain with execution records, effectiveness evaluation, non-conformity handling, and improvement | P–D–C are present but A (improvement/feedback) is missing | Execution steps only; no checking or improvement |
| Professional depth | Contains laboratory-specific detail (e.g., Westgard rules, measurement uncertainty, Sigma metrics, HIL indices, blind testing, PCR zoning, cold chain) | Some professional flavour, but largely generic | Generic content equally applicable to any laboratory |

#### 2.3.3 Tier 3 — Expert review

Three qualified ISO 15189 internal auditors independently scored 10 blinded, stratified-randomly sampled documents, using the same five dimensions as the LLM judges (Table 1). Rater 1 was the first author; Raters 2 and 3 were from the same institution. The three scored independently, without communicating and without seeing one another's ratings; to avoid self-influence, Rater 1 viewed the Tier 1/2 scores only after all three rater sheets had been submitted. Written informed consent was obtained from Raters 2 and 3 beforehand. During scoring, the experts could freely consult the full texts and annexes of ISO 15189:2022 and CNAS-CL02:2023.

**Sampling strategy.** Ten documents were drawn from the 486-document pool by stratified random sampling with a fixed seed (`seed = 42`), stratified across seven configurations × the three Class A tasks (A1, A2, A3), with one or two documents per realised stratum. Only Class A was sampled, as it is the most stable and representative document type in CNAS audits (cross-class generalisation is discussed as a limitation in §4.6). The seven configurations evaluated here differ slightly from the six scored at Tier 2a; the specific seven are listed in §3.5.

**Rater conflicts of interest.** None of the three raters had any commercial, research, or consulting relationship with Anthropic, OpenAI, or other LLM providers; none received funding or in-kind support from these entities.

**Pre-scoring calibration.** No formal pre-scoring calibration session was held; the three raters scored independently using only the published rubric (Table 1) and the ISO 15189:2022 / CNAS-CL02:2023 standards. This absence of calibration is noted as a limitation in §4.6 (xii).

**Blinding procedure.** Blinding was performed with the open-source script `prepare_blind_review.py`: each of the 10 documents was renamed to an anonymous identifier, all model names and configuration markers were removed from the text and verified, and the presentation order was randomised (identical for all three experts, showing only the task category). The key linking documents to their configurations was sealed until all three rater sheets had been submitted.

### 2.4 Statistical analysis

#### 2.4.1 Pairwise group comparisons and multiplicity correction

Pairwise comparisons between configurations used two-sided Mann–Whitney U tests on the GPT-judge scores for each document (n = 45 per configuration; 15 tasks × 3 replicates). Because the four component contrasts share configurations and are therefore not independent (e.g., G_template_rules appears in both the *detailed content* and *worked examples* contrasts), multiplicity was controlled with the Benjamini–Hochberg FDR procedure (α = 0.05) rather than the more conservative Bonferroni, retaining more power while controlling the false-discovery rate. A 95% confidence interval for each effect estimate (Δ) was obtained by bootstrap (nonparametric percentile method, fixed seed, B = 10,000 resamples). Software versions and scripts are given in the code repository.

#### 2.4.2 Quantification of configuration-component effects

We used four pairs of configurations to measure the effect of each of the four content components; each pair mainly differs in one component, with the others kept as similar as possible:

- *rules*: E_rules_v2 vs A_bare
- *document skeleton*: H4_sop_only vs E_rules_v2
- *detailed content*: G_template_rules vs H3_skeleton
- *worked examples*: H2_keep_examples vs G_template_rules

The effect of each component (denoted Δ) is the difference between the two configurations' mean scores; Δ is expressed on the raw 0–5 scale, without standardisation, and its 95% CI was obtained by bootstrap (Table 3). We deliberately used this direct pairwise contrast rather than a more elaborate statistical model because it is the easiest to interpret.

#### 2.4.3 Inter-rater agreement

Inter-rater agreement was reported using three complementary measures: Pearson correlation (captures linear association while tolerating systematic shifts between raters), Spearman correlation (captures rank-order agreement without assuming linearity), and intraclass correlation coefficients (ICCs, following the Shrout–Fleiss framework [13]). Four ICC variants were used:

- **ICC(2,1)**: single-rater absolute agreement, two-way random effects;
- **ICC(3,1)**: single-rater consistency, two-way mixed effects;
- **ICC(2,k)**: k-rater averaged absolute agreement;
- **ICC(3,k)**: k-rater averaged consistency.

Pairwise comparisons (e.g., expert mean vs each LLM judge, and pairwise comparisons within the expert panel) used the single-rater variants ICC(2,1) and ICC(3,1); the overall reliability of the three-expert panel was characterised with the averaged variants ICC(2,k) and ICC(3,k) (k = 3). The reasoning is as follows: for panel reliability, the question is whether the three experts' average score is dependable, hence the averaged variants; for judge–expert comparisons, the question is whether a single judge can reproduce the experts' ranking, hence the single-rater consistency variant ICC(3,1). The consistency form tolerates a wholesale offset between the two sets of scores, and that offset—the LLM judges' systematic overestimation—is reported separately in §3.5, so it is not concealed by this choice. All ICCs were computed with the `pingouin` Python library.

#### 2.4.4 Self-preference bias

For each model M (Claude or GPT) acting as judge, the self-preference bias was computed following the classical convention of Panickssery et al. [12]: the same judge rates documents generated by its own family and by the other model.

bias_M = mean(judge = M, generator = M) − mean(judge = M, generator = M′),

where M′ is the other model. Positive values mean judge M scores its own documents higher; negative values mean the opposite. As a sensitivity check, we recomputed the bias using an alternative formulation (same generator, different judges), obtaining +0.464 (Claude) and −0.472 (GPT); the sign and direction agree with the classical estimates (+0.294 and −0.301) reported in §3.4.

#### 2.4.5 Note on the experimental design

The nine configurations are not a Taguchi L9 orthogonal array but a structured subset of the four-dimensional configuration space: rules and document skeleton each take three levels (absent / partial / full), and detailed content and worked examples each take two (absent / present). The configurations were selected to isolate each dimension through the pairwise contrasts described in §2.4.2, not to satisfy orthogonal-balance criteria; the Δ estimates therefore correspond only to the specific pairs listed in §2.4.2.

---

## 3. Results

### 3.1 Configuration ranking under the combined automated and LLM-judge evaluation

We ranked the nine configurations across the 405 Claude Opus 4.6–generated documents using a composite score that combined the Tier 1 automated scorer mean and the Tier 2 LLM-judge mean (averaged across the Claude and GPT judges), each min-max normalised to [0, 1] across the nine configurations and then averaged with equal weight (Table 2).

**Table 2.** Composite ranking of the nine configurations. The composite score combines the Tier 1 automated mean and the Tier 2 LLM-judge mean (averaged across the Claude and GPT judges), each min-max normalised to [0, 1] across the nine configurations and then averaged with equal weight.

| Configuration | System-prompt size | Composite score |
|---|---|---|
| H4_sop_only | ~2,000 tokens | 0.994 |
| H3_skeleton | ~5,000 tokens | 0.869 |
| G_template_rules | ~16,000 tokens | 0.851 |
| H2_keep_examples | ~25,000 tokens | 0.759 |
| E_rules_v2 | ~1,200 tokens | 0.729 |
| C_full | ~56,000 tokens | 0.493 |
| F_template | ~15,000 tokens | 0.345 |
| B_simple | ~300 tokens | 0.227 |
| A_bare | 0 tokens | 0.000 |

H4_sop_only achieved the highest composite score at only ~2,000 tokens, well below the template-anchored configurations (G_template_rules ~16,000 tokens; H2_keep_examples ~25,000 tokens) and the full-context C_full (~56,000 tokens); as §3.5 shows, however, this ranking does not survive expert evaluation.

### 3.2 Four-component substitution-contrast ablation

The ablation effects of the four components are summarised in Table 3.

**Table 3.** Ablation effects of the four prompt components (Tier 2b GPT-judge ratings; the two configurations in each contrast are given in §2.4.2). The three right-hand columns give Δ stratified by task class (n = 15 per cell: 5 tasks × 3 replicates). These stratified Δ values, and the by-dimension Δ decomposition in §3.2, are descriptive point estimates without CIs or significance tests; CIs and adjusted p-values for the main effects are given in the left-hand columns.

| Component | Δ (all tasks) | 95% CI | BH-adjusted p | Δ_A Authoring | Δ_B Operation | Δ_C Audit |
|---|---|---|---|---|---|---|
| rules | +0.511 | [+0.28, +0.75] | <0.001 | +0.507 | +0.613 | +0.413 |
| document skeleton | +0.213 | [+0.05, +0.39] | 0.11 | +0.347 | +0.187 | +0.107 |
| detailed content | −0.031 | [−0.19, +0.12] | 0.79 | +0.107 | +0.053 | −0.253 |
| worked examples | −0.053 | [−0.21, +0.11] | 0.61 | −0.080 | −0.173 | +0.093 |

Of the four components, only rules remained significant after multiplicity correction (BH-adjusted p < 0.001) and was the only clearly effective component. The document-skeleton effect was directionally positive and its bootstrap CI excluded zero, but the rank-based test was not significant (BH-adjusted p = 0.11), so we treat it as suggestive evidence requiring further validation; neither detailed content nor worked examples had a detectable effect. A supplementary contrast further showed that H4_sop_only (a single SOP skeleton) and H3_skeleton (the full module skeleton) performed comparably (Δ = −0.009). Stratified by task class (the three right-hand columns of Table 3; n = 15 per cell), the rules effect was consistent in direction and comparable in magnitude across all three classes (+0.41 to +0.61) and did not reverse with task class; the other three components fluctuated across classes and were far smaller in magnitude than rules.

The rules effect can also be decomposed by scoring dimension (GPT judge; n = 45 per configuration): operability +0.867, professional depth +0.644, clause coverage +0.400, PDCA closure +0.333, and internal consistency +0.311. The two largest gains fall on operability and professional depth rather than on the format- and structure-oriented dimensions, indicating that a rules constraint does not merely regularise the outward form of a document but also increases the amount of laboratory-specific technical detail written into it. This decomposition is by scoring dimension, however, not by document type. "Professional depth" is only a proxy for technical specificity (Table 1). A genuine stratification by document type—comparing generic management documents against laboratory-specific technical documents—cannot be performed here, because the task set contains no technical documents at all (§4.6, Limitation xviii).

These results apply only to the LLM-judge tier (the Tier 2b GPT judge); the expert-tier comparisons appear in §3.5.

### 3.3 2 × 2 symmetric cross-model validation

Figure 2 shows the results of the 2 × 2 symmetric design: each of the two models (Claude, GPT) generated documents that were then scored by each of the two judges, across the 9 configurations × three tasks (A1, B1, C1) × three replicates per cell. Both models were run on the same three tasks, so this cross-model comparison is task-matched and configuration effects are not confounded with task effects; generalisation to other tasks nevertheless remains limited (see §4.6, Limitation v). The most striking finding is that C_full (~56,000 tokens) dropped sharply in compliance when generated by GPT-5.4: for GPT-generated documents, the Claude judge gave 1.40 and the GPT judge 1.84 (0–5 scale), whereas the same C_full configuration generated by Claude scored between 3.22 and 4.56 across the two judges. This indicates that the ~56,000-token full-context configuration is specific to Claude and cannot be transferred to GPT-5.4 within the parameters tested here.

We inspected the GPT-generated C_full outputs document by document and found three recurrent problems: (i) declining instruction-following—constraints stated at the start of the system prompt were no longer applied in the later part of the output; (ii) structural breakdown—disordered sections, missing required headings, or numbering errors; and (iii) clause-citation confusion—incorrect, mismatched, or even fabricated ISO 15189:2022 clause identifiers. None of these problems appeared in the corresponding Claude outputs.

### 3.4 Self-preference bias of LLM judges

The self-preference biases computed with the Panickssery formula (§2.4.4) are shown in Table 4. The two values have opposite signs but point to the same thing: both judges actually rated Claude-generated documents higher (by about 0.3 points). Moreover, once C_full is excluded both biases collapse toward zero—so this gap is driven mainly by C_full, the configuration where GPT broke down under long context (§3.3).

**Table 4.** Self-preference bias of the two judges (0–5 scale; positive = scoring its own family's documents higher).

| Judge | All nine configurations | Excluding C_full |
|---|---|---|
| Claude | +0.294 | −0.064 |
| GPT | −0.301 | −0.167 |

This opposite-signed pattern does not match classical self-preference (each judge favouring its own family), which would produce same-signed positive biases for both. The observed pattern is compatible with two non-exclusive explanations: (a) a genuine difference in generation quality between Claude and GPT (consistent with GPT's C_full breakdown in §3.3); and (b) a shared preference of both judges for Claude's phrasing or formatting. Because the expert sample (n = 10) consisted entirely of Claude-generated documents (§2.3.3), this study cannot distinguish the two; this is a key direction for follow-up validation (§4.6, Limitation i).

A judge may score its own family's documents too highly. To remove this effect, we re-ranked the configurations using only cross-model scores (the Claude judge on GPT-generated documents, and the GPT judge on Claude-generated documents). Under this ranking, the top four (G_template_rules, H3_skeleton, E_rules_v2, H4_sop_only) lay within 0.11 points of one another and were statistically indistinguishable, whereas C_full fell from sixth in the §3.1 composite ranking to ninth (last). This indicates that C_full's relatively high LLM-judge score in §3.1 rested on two things: the Claude judge over-rating its own output, and GPT being unable to produce usable output at the ~56,000-token configuration (§3.3).

### 3.5 Expert-tier validation

Inter-rater agreement among the three experts was excellent: ICC(2,k) = 0.982 (95% CI [0.95, 1.00]), and all three pairwise comparisons were above 0.92 ("excellent" by the Cicchetti benchmark [14]). This indicates that the five-dimensional rubric (Table 1) was highly reproducible across raters; however, because all three were from the same institution, this agreement may be higher than would be achieved across institutions (see §4.6, Limitation ii).

Agreement between the experts and the two LLM judges was markedly lower (Figure 3): ICC(3,1) = 0.548 (95% CI [−0.08, 0.86], p = 0.04) for the Claude judge and only 0.217 (95% CI [−0.44, 0.72], p = 0.26) for the GPT judge. Both intervals cross zero and n is only 10, so these two agreement coefficients can serve only as directional indications and do not support firm statistical conclusions. Both judges also systematically scored compliance higher than the experts—by 0.905 points (Claude) and 0.525 points (GPT). Claude–expert agreement was therefore moderate, and GPT–expert agreement poor.

The ranking of the seven configurations is given in Table 5, and is almost the reverse of the LLM-judge tier.

**Table 5.** Scores for the seven sampled configurations (0–5 scale; sorted by expert mean; 1–2 documents per configuration).

| Configuration | Expert mean | Claude judge | GPT judge | n |
|---|---|---|---|---|
| F_template | 4.24 | 4.60 | 4.00 | 1 |
| H2_keep_examples | 4.07 | 4.40 | 4.00 | 1 |
| G_template_rules | 4.06 | 4.80 | 4.50 | 2 |
| C_full | 3.45 | 4.90 | 4.00 | 2 |
| H4_sop_only | 3.20 | 4.30 | 4.20 | 2 |
| E_rules_v2 | 3.19 | 4.00 | 4.00 | 1 |
| A_bare | 3.04 | 4.00 | 3.80 | 1 |

The top three are all template-anchored configurations (F_template, H2_keep_examples, G_template_rules), whereas H4_sop_only (~2,000 tokens)—ranked first at the LLM-judge tier—fell to fifth under expert review, only 0.16 points above the no-prompt baseline A_bare. The most overestimated were C_full and H4_sop_only (about 1 point above the experts): both comply in document structure and terminology but lack the practical, clinically grounded operational detail that only experts can identify. The token-efficient, high-scoring advantage that skeleton configurations show at the LLM-judge tier is therefore not borne out under expert evaluation. With only 1–2 documents per configuration, this ranking is preliminary and requires confirmation with a larger expert sample.

### 3.6 Token size and compliance scores: divergent relationships across evaluation tiers

Figure 4 plots the compliance scores of all three evaluators (experts, Claude judge, GPT judge) against system-prompt token size, all based on the same n = 10 expert-blinded subset. The three curves diverge: both LLM judges scored the low-token configurations and C_full highly, whereas the experts scored highest only in the mid-range template configurations (~15,000–16,000 tokens; F_template, G_template_rules), with both ends of the curve declining markedly.

The expert–judge divergence therefore follows a descriptive U-shaped pattern (no test of non-linearity was performed, given the sample size): at the low-token end (A_bare, E_rules_v2, H4_sop_only) and the high-token end (C_full) the gap reaches 0.8–1.1 points, whereas in the mid-range template region the two converge (gap ≤ 0.6). This indicates that token efficiency and clinical usability correspond to two different optimisation objectives—relative to the expert-validated compliance, the LLM-judge tier overestimated both the low-token configurations and C_full.

Framed in terms of efficiency, the answer to research question (ii) turns not on the absolute token count but on the compliance return per unit of added tokens. §3.2 showed that only the rules component produced a definite gain, and the rules themselves take only ~1,000 tokens (E_rules_v2); the per-token return is therefore highest when rules are added and falls off quickly thereafter. The expert tier presents a different trade-off: the template-anchored configurations (~15,000–16,000 tokens) yield a lower per-token return, yet reach a higher absolute score that rules alone cannot, whereas C_full (~56,000 tokens) has the lowest return of all. The "minimum tokens required" thus depends on the use case—for rapid LLM-judged drafting, ~1,000 tokens of rules suffice; for documents that must pass expert review, ~15,000–16,000 tokens buy a higher quality ceiling. (With only 1–2 expert-scored documents per configuration, this comparison is qualitative.)

---

## 4. Discussion

### 4.1 Prompt minimisation holds at the LLM-judge tier but not at the expert tier

At the LLM-judge tier, the four-component ablation gives a clear account: the rules component was necessary (BH-adjusted p < 0.001), the document-skeleton component was directionally positive but not significant (p = 0.11), and neither detailed content nor worked examples produced a detectable improvement (§3.2). This aligns with the lost-in-the-middle phenomenon reported by Liu et al. [15] (adding too much context to a long prompt can dilute model attention and degrade output quality) and with the prompt-engineering literature more broadly [8].

The expert-tier results qualify this account (§3.5). The template-anchored F_template and G_template_rules earned markedly higher expert scores, whereas the skeleton-only H4_sop_only was about one point lower (per-configuration samples are very small and these are exploratory observations; see §3.5). A plausible explanation is that the model's own knowledge does not reliably cover the clinical-practice details required by ISO 15189:2022 and CNAS-CL02:2023—in our task set, emergency-sample handling, acceptance of patient-self-collected specimens, qualification requirements for sample-courier personnel, and detailed sample-rejection criteria. When these are not stated explicitly in the system prompt, the model tends to fall back on generic procedural language: such language meets structural and terminological compliance (the two dimensions most readily detected by automated and LLM-based scoring, §3.6) but lacks the practical operability required of documents intended for accreditation submission. Prompt minimisation is therefore appropriate for rapid drafting that is judged only by an LLM; but when a document must pass expert review for a formal accreditation submission, a template-anchored prompt is required.

### 4.2 The full-context trap is model-dependent

Although template-anchored configurations improve expert scores (§4.1), simply lengthening the prompt can be counterproductive when a model lacks stable long-context handling. C_full (~56,000 tokens) appears to be the safest choice—it includes all potentially relevant material and matches the intuition that "more context is more reliable." But our data show this intuition did not hold across the two models: for the same C_full, Claude scored 3.22–4.56 on average whereas GPT-5.4 scored only 1.40–1.84, accompanied by the three failure modes recorded in §3.3 (declining instruction-following, structural breakdown, and clause-citation confusion). A plausible explanation—consistent with the lost-in-the-middle phenomenon of Liu et al. [15] and with the long-context benchmarks in both vendors' technical documentation [3, 4]—is that within this length range Claude maintained more stable attention, whereas GPT-5.4, under the parameters tested, did not consistently respect the system-prompt constraints in such a long prompt.

This carries a methodological implication: any claim that "configuration X works" must be validated across multiple generation models. Evaluating on a single model conflates the effect of the configuration itself with the model's intrinsic properties (long-context capacity, instruction-following stability, and how well its training data matches the target regulatory domain), and cannot be generalised to other models. We therefore recommend validating any long-context QMS prompt (e.g., approaching or exceeding ~50,000 tokens) on the specific model and version before deployment. This is because long-context behaviour can vary substantially, both between models and between adjacent versions of the same model.

### 4.3 Bias profile and appropriate use of LLM-as-judge

This study quantified two distinct types of rating bias. The first is a cross-judge directional bias: both judges rated Claude-generated documents about 0.3 points higher than GPT-generated ones (§3.4), an effect driven mainly by C_full. As explained in §3.4, this pattern does not match classical self-preference (a judge favouring its own model's outputs), and more likely reflects either a genuine difference in generation quality between Claude and GPT or a shared preference of both judges for Claude's writing style. The second is a systematic LLM–expert offset: both judges overestimated the expert-determined compliance scores by 0.52–0.90 points (§3.5).

The practical guidance from these two biases is as follows. The Claude judge's moderate agreement with the expert ranking [ICC(3,1) = 0.548] suggests it could serve as a first-pass filter in large-scale generation, screening out clearly low-quality outputs before expert review; however, the 95% CI of this coefficient crosses zero (n = 10; see §3.5), so this use requires confirmation in a larger sample. The GPT judge's poorer and non-significant agreement [ICC(3,1) = 0.217, p = 0.26] makes it unsuitable as a substitute for expert scoring. For documents intended for accreditation submission, formal QMS adoption, or operational use, expert final review remains indispensable. The configuration-level implications of these biases are summarised in §4.4 (Table 6).

### 4.4 Configuration recommendations stratified by use scenario

Synthesising the evidence from the three evaluation tiers, we summarise configuration recommendations for the principal use scenarios in Table 6. There is a key trade-off (see §3.5 and §3.6): the configurations that score highest at the LLM-judge tier (H4_sop_only, E_rules_v2) are the most token-efficient but lack the practical, clinically grounded detail needed to meet formal submission requirements, whereas the template-anchored configurations (F_template, G_template_rules) score lower at the LLM-judge tier yet receive the highest expert ratings.

**Table 6.** Configuration recommendations stratified by use scenario.

| Use scenario | Recommended configuration | Tokens | Rationale | Trade-off |
|---|---|---|---|---|
| Rapid first-draft generation; internal iteration | H4_sop_only or E_rules_v2 | ~1,000–2,000 | Near-optimal at the LLM-judge tier; highest token efficiency | Requires manual supplementation of clinical detail |
| Batch drafting of multiple SOPs | H4_sop_only or H3_skeleton | ~2,000–5,000 | Task-specific skeleton plus rules | Requires manual supplementation of clinical detail |
| Formal documents for CNAS submission | G_template_rules | ~16,000 | Top-three expert compliance; cross-model robust | Higher token cost |
| Complete quality manual | F_template or G_template_rules | ~15,000–16,000 | Highest expert scores | Higher token cost |
| Not recommended | C_full | ~56,000 | Collapses under GPT-5.4 generation; ranks last after debiasing | — |
| Not recommended | A_bare, B_simple | 0–~300 | Insufficient prompt constraint; below the practical compliance baseline | — |

A practical workflow emerging from these data is to: (i) generate a rapid first draft with H4_sop_only; (ii) supplement the practical clinical detail through manual review or targeted re-prompting; and (iii) regenerate or refine the final document for accreditation submission using G_template_rules. It should be emphasised that every configuration in Table 6 produces only a reference draft: all require revision by laboratory staff and final expert review before use for accreditation, and the configurations differ only in the completeness of that draft, not in whether expert review is needed. The amount of manual rework each configuration requires was not quantified in this study and is a direction for future work.

### 4.5 LLM assistance within the personnel-competence requirements of ISO 15189

The drafting of QMS documents is not merely a clerical output; it is also the process through which laboratory staff build their sense of responsibility and risk awareness. If this work is delegated entirely to an LLM, staff gradually lose writing practice and struggle to develop a deep understanding of the ISO 15189 process as a whole. We therefore regard human supervision as a constraint on the use of LLMs in this setting. ISO 15189:2022 requires competent personnel and a complete examination process, not merely well-formatted documents; our data show precisely why LLM generation cannot replace this competence: the LLM judges overestimated expert-determined compliance by 0.52–0.90 points. A model that cannot even reliably evaluate compliance certainly should not be entrusted with final authorship. This position aligns with the recently emerging consensus that, in healthcare quality management, LLMs should be confined to clerical tasks that are grounded in historical data and performed under mandatory human verification, with autonomous operation regarded as premature [16]. We therefore position LLM assistance as an efficiency tool: the final authoring, review, and approval remain the responsibility of qualified personnel, while the time it saves at the drafting stage can be redirected toward the higher-order review, validation, and continual-improvement activities that ISO 15189 prioritises.

### 4.6 Limitations

The present study has the following limitations.

**(i) Limited expert sample, all from Claude-generated documents.** The expert tier comprised three raters scoring 10 documents (per-stratum n = 1 or 2; see §3.5), all drawn from the Claude-generation pool, with no expert evaluation of any GPT-generated document. The expert tier therefore supports only directional ranking for Claude-generated documents and is insufficient for strict statistical inference; the two explanations in §3.4—(a) a genuine generation-quality gap between Claude and GPT, and (b) a shared judge preference for Claude's style—also cannot be distinguished within this study. Furthermore, the cross-judge bias in §3.4 is driven mainly by the single C_full configuration (which contributes the largest single-configuration bias of +3.156 to the Claude judge and the largest negative bias of −1.378 to the GPT judge), so future replication should report bias distributions per configuration. All 10 documents were Class A procedure documents; generalisation to Class B and Class C still requires validation. A key direction for future work is multi-centre validation: three to five raters scoring 30–50 documents per institution, including matched GPT-generated samples and Class B/C tasks.

**(ii) Same-institution agreement may overestimate generalisability.** The very high agreement among the three experts [ICC(2,k) = 0.982] supports the validity of the five-dimensional rubric but may also stem from shared professional culture, training background, and clause-interpretation habits within a single institution; the observed reliability may therefore be higher than what holds across institutions.

**(iii) Dual role of the first author.** The first author was both Rater 1 and the study designer. To reduce self-influence, Raters 2 and 3 scored independently without knowledge of Rater 1's ratings; each rater's data are openly released for independent audit.

**(iv) Expert and LLM tiers used the same rubric.** The five-dimensional rubric was used identically by the LLM judges and the experts, creating a risk of shared-measurement bias. Future work should add expert-specific dimensions (e.g., practical implementability under departmental workflow constraints) that an LLM is unlikely to have learned from training data. It should also be noted that all three raters were internal auditors. An internal auditor is trained to check whether a document fully covers the standard's clauses and is properly formatted; a bench-level examiner is concerned with a different question—whether the steps a document describes can actually be carried out on the department's existing instruments and information systems. A document can be beyond reproach in clause coverage and formatting, and receive a high score from an internal auditor, yet not be executable at the bench. The implementability dimension noted above should therefore be rated by bench-level technologists or section leaders, rather than (or not only) by internal auditors. A further dimension worth adding is "fillability": whether a document leaves the content that the laboratory must supply as blank slots—empty tables, formulas awaiting values, parameter ranges to be determined—rather than having the model invent plausible-looking numbers. This dimension bears on whether a document can be used safely: if the model supplies concrete figures for quality-control limits or reference intervals, users may not be able to tell that those figures were fabricated, and the risk of copying them across is far greater than that of poor formatting.

**(v) Limited GPT-5.4 task coverage.** Only the A1, B1, and C1 tasks were generated by GPT-5.4 (81 documents). Both models were run on the same three tasks, so the cross-model comparison in §3.3 is task-matched; three tasks are nevertheless too few to exclude task specificity—for example, these three tasks may happen to be particularly unfavourable for GPT-5.4's long-context handling. The model dependence of the full-context trap is therefore a preliminary observation: its evidential strength does not match that of the Claude-side conclusions, which rest on 405 documents, and it requires validation on a larger set of tasks. In addition, the blinded expert review covered no GPT-generated document, so this conclusion is supported only by Tiers 1 and 2 and has not been independently confirmed at the expert tier.

**(vi) Domain specificity.** The findings are limited to ISO 15189 medical-laboratory QMS documents; transfer to adjacent regulatory frameworks (e.g., ISO 17025 for testing and calibration laboratories, or ISO 9001 for general quality management) requires separate validation.

**(vii) Limited set of judge models.** Only Claude Opus 4.6 and GPT-5.4 served as judges; whether the observed cross-judge directional bias and expert-overestimation pattern generalise to other models (e.g., Gemini, open-weight models) is unclear.

**(viii) Single language only.** All QMS documents were generated and evaluated in Chinese; the configuration effects and bias behaviour in English or other languages have not been verified.

**(ix) Model temporality.** The conclusions rest on the specific model versions and parameters tested between 2 and 14 April 2026; as LLMs continue to iterate, periodic re-validation may be needed.

**(x) Some raw ratings were kept only as group means.** For two subsets (Claude judge × GPT-generated, and Claude judge × H-group × Claude-generated), we stored only the mean across that group's documents, not each document's individual rating (i.e., no per-document JSON files). The full 2 × 2 self-preference matrix therefore cannot be independently recomputed at the individual-document level. However, the per-document raw Claude-judge ratings for the six core configurations (A/B/C/E/F/G; 270 ratings) and all 486 per-document GPT-judge ratings are openly released.

**(xi) Intra-judge reliability not assessed.** Each LLM judge scored each document only once; judges were not asked to re-score documents to quantify their own variability. Agreement between raters was obtained indirectly, via the 2 × 2 cross-comparison between the Claude and GPT judges and the three-expert ICC analysis.

**(xii) No pre-scoring calibration session.** The three raters scored independently from the published rubric and the ISO 15189:2022 / CNAS-CL02:2023 standards, without a prior calibration session (in which a few example documents would first be scored jointly to align interpretation). The very high agreement among the raters indicates that, within this single institution, their understanding of the rating scale was already closely aligned; but in a multi-centre study, holding a calibration session beforehand would further improve reproducibility.

**(xiii) Claude was accessed through the Claude Code tool.** We ran Claude (both generation and judging) through the Claude Code tool rather than by calling Anthropic's API directly. This tool prepends a fixed block of its own instructions (tool definitions and file-system guidance) before our prompt, so the prompt the model actually receives is somewhat longer than the per-configuration token counts reported in §2.1. Because this added block is identical across all 9 configurations and all judging calls, it does not affect comparisons between configurations or the judge-versus-expert conclusions; it matters only if one wants to reproduce the exact absolute scores, which requires the same Claude Code version. Calling the API directly with the same configurations may yield slightly different absolute scores.

**(xiv) AIHubMix routing not independently audited.** GPT-5.4 was accessed via the AIHubMix proxy, which claims transparent forwarding to the upstream OpenAI API. We did not independently verify that its responses are exactly equivalent to direct OpenAI calls; subtle routing-level differences (request batching, header handling, regional routing) cannot be fully ruled out, although the GPT-5.4 model identifier was consistent throughout the call chain.

**(xv) Temperature setting and generation variability.** Generation was stochastic for both models: GPT-5.4 used temperature = 0.7, while Claude was run through the Claude Code Agent with no temperature set explicitly. No temperature sensitivity analysis was performed, and no low-temperature condition (e.g., 0.3–0.5) was compared. Random variation was mitigated by three replicates per combination: among the Claude judge's ratings of the six core configurations × 15 tasks, the standard deviation across the three replicates of the same configuration–task combination had a median of 0.231 points (0–5 scale), and 74.4% of combinations fell below 0.5 points, indicating limited replicate-to-replicate variability. Strict bit-level reproducibility was nevertheless not achieved; studies seeking deterministic comparison should set temperature = 0 for both models.

**(xvi) Interaction effects between components were not estimated.** Each of the four comparisons in §2.4.2 replaced one component at a time, but against different backgrounds: rules were measured with no document skeleton present, whereas detailed content was measured with rules and a skeleton already in place. Each Δ therefore reflects the effect of a component at a specific background, not an independent effect that can be added across backgrounds. In other words, this study cannot tell whether components act synergistically—the effect of adding two components together need not equal the sum of their separate effects. Separating such interaction terms requires a full-factorial or orthogonal design, which we leave to future work.

**(xvii) Generation and judging parameters differed between the two models.** As described in §2.2 and §2.3.2, GPT-5.4 generation used temperature = 0.7 and max_completion_tokens = 16,000, whereas Claude was run through the Claude Code Agent with neither parameter set explicitly; the judging side was likewise asymmetric, with the GPT judge using temperature = 0 and max_completion_tokens = 2,000 and the Claude judge running as an Agent sub-agent with parameters not set explicitly. The cross-model comparison (§3.3) and the self-preference decomposition (§3.4) are therefore confounded by this parameter mismatch, and differences between the two models cannot be attributed to the models alone. We note that the direction of this confound is conservative: GPT-5.4 received both a lower temperature and a larger output budget—settings that should favour instruction-following and compliance—yet still degraded sharply under C_full, so the model dependence of the full-context trap is unlikely to be an artefact of a parameter disadvantage. Future work should nevertheless harmonise generation and judging parameters across models.

**(xviii) The task set contains no technical documents.** The 15 tasks cover system-level documents concerned with document control, internal audit, pre-assessment self-inspection, and management review (Supplementary Table S1), including corrective action and CAPA closure (B5, C5) and system-wide reviews spanning dozens of clauses (B3, C3). The set contains no technical documents, however: no method validation or verification reports, no measurement-uncertainty procedures, no critical-value reporting and clinical-communication records, and no procedures for handling external quality assessment results. Writing such documents requires the laboratory's own analytical performance data—precision, trueness, reportable range, interfering substances—together with the rationale for its internal quality-control rules and its clinical decision thresholds. What these documents really test is whether a laboratory holds genuine validation data and hands-on operating experience, and system-level documents are far less demanding in this respect. Whether "rules is the only definitely effective component" generalises to technical documents is therefore a question this study cannot answer. The blinded expert review is narrower still, covering only Class A documents (§2.3.3). Extending the task set to technical documents is an important direction for future work. In on-site accreditation assessments, nonconformities cluster in three document types in particular: method performance validation reports; records verifying or establishing biological reference intervals; and procedures for evaluating measurement uncertainty. All three must incorporate the laboratory's own examination data. It is precisely for that reason that they stand to benefit most from LLM-assisted drafting, and that the usability of any resulting draft is hardest to judge. Future work should cover them first.

**(xix) Subspecialty heterogeneity was not covered.** All 15 tasks in this study are documents written for the laboratory department as a whole—for example, a personnel-training and competence-evaluation procedure (A1), an equipment-management procedure (A2), and a sample-collection-and-handling SOP (A3)—none of which targets a specific clinical subspecialty. SOPs across subspecialties differ greatly in complexity and degree of standardisation: clinical chemistry is the most process-driven; clinical microbiology involves extensive manual interpretation and is less standardised; and molecular diagnostics has exacting contamination-control requirements. The 10 expert-reviewed documents were all drawn from Class A tasks (§2.3.3) and therefore likewise cover no subspecialty. Consequently, the finding that template-anchored configurations perform best under expert review is at present supported only for department-level generic documents. Whether template-anchored prompts can produce acceptable documents in judgement-intensive fields such as microbiology and molecular diagnostics is not answered here: such documents must incorporate the laboratory's own subspecialty content—organism-identification workflows, contamination-control provisions—that a template may not supply.

**(xx) Coverage of the pre-examination, examination, and post-examination phases is unbalanced.** Classified by the process phases of ISO 15189:2022, the 15 tasks break down as follows: one pre-examination task (A3, a sample-collection-and-handling SOP); four examination tasks (B2, C1, C2, C4, all concerning internal quality control and analyser operation); no post-examination task; and ten management-level or system-wide tasks (Supplementary Table S1). Post-examination documents—result reporting and review, critical-value notification and records, sample retention and disposal—are absent from the task set entirely. Pre- and post-examination documents typically involve hand-offs with clinical departments and nursing units and depend on the actual interfaces and communication conventions of the hospital's LIS/HIS; where the system prompt supplies none of this, such content is correspondingly harder for an LLM to generate. Because there were no post-examination tasks and only one pre-examination task, this study cannot compare generation quality across the three phases. Balancing coverage across the three phases is a gap that future work should close.

**(xxi) Patient-safety risk was not assessed.** None of the three evaluation tiers contains an item directed specifically at patient safety: Tier 1 examines formatting, clause citation, and terminology, while the five dimensions of Table 1 examine clause coverage, operability, internal consistency, PDCA closure, and professional depth. None of these dimensions directly answers the question of whether a document contains a substantive error or omission that could endanger patients—an incomplete critical-value list, an inappropriately set trigger for repeat testing, or a gap in the reporting and confidentiality workflow for communicable-disease results. Compliant formatting and complete clause coverage do not amount to the absence of patient-safety risk. Moreover, as noted in (xx), post-examination documents such as critical-value reporting procedures were absent from the task set, so risks of this kind had no opportunity to surface in this study. Future work should include a separate "patient-safety risk" item on the expert rating form, screened document by document, rather than leaving it implicit within "operability" or "professional depth".

---

## 5. Conclusions

The optimal prompt configuration for LLM-assisted ISO 15189 QMS document generation varies with the evaluation tier. At the LLM-judge tier, H4_sop_only (~2,000 tokens) achieved the highest composite score; under expert evaluation, however, the top three were the template-anchored F_template, H2_keep_examples, and G_template_rules (expert mean 4.06–4.24), whereas H4_sop_only fell to fifth, only 0.16 points above the no-prompt baseline A_bare. Both types of configuration, therefore, produce only a reference draft: laboratory staff must in every case revise and supplement it according to their own department's circumstances, and an expert must finalise it; neither can be submitted for accreditation directly. The two differ only in their starting point—minimal prompts (H4_sop_only or E_rules_v2; ~1,000–2,000 tokens) provide a brief outline suitable for a quick start, whereas the template-anchored configurations (G_template_rules or F_template; ~15,000–16,000 tokens) provide a more complete draft, closer to submission form, suitable as the drafting document for documents bound for formal accreditation. More precisely, the value of a template-anchored configuration lies in producing a reliable document skeleton: the section structure, the fields that must be completed, and the elements that must be addressed. The content that actually determines whether a document can be used for accreditation—the laboratory's own quality-control data, its patient data distributions, and its historical proficiency-testing and interlaboratory-comparison results—must be entered by laboratory staff and interpreted by competent personnel. An LLM does not hold these data and therefore cannot generate them. C_full (~56,000 tokens) should be used with caution in the present setting, particularly when generation is performed by GPT-5.4 (see the long-context failure modes documented in §3.3); it should be noted that these failure modes are supported only by the automated and LLM-judge tiers, as the blinded expert review did not cover any GPT-generated document. LLM-as-judge can be used to pre-screen generated outputs: in large-scale generation, the Claude judge can first filter out clearly low-quality outputs; the remaining documents still require revision by laboratory staff before being passed to experts. The Claude judge's moderate agreement with the expert ranking [ICC(3,1) = 0.548] may make it adequate for this screening role, but the 95% CI of this coefficient crosses zero (n = 10) and requires confirmation in a larger sample; the GPT-5.4 judge [ICC(3,1) = 0.217] is unsuitable for it. For any document intended for accreditation submission, formal QMS adoption, or operational use, expert final review remains indispensable.

To our knowledge, this is the first systematic comparison of prompt-content effects on ISO 15189–compliant QMS document generation across two state-of-the-art LLMs and a three-tier evaluation framework; the findings provide an empirical basis for prompt-design guidance in laboratory accreditation workflows.

---

## Declarations

**Research funding**: The study received no external research funding.

**Author contributions**: Sidi Liu was responsible for the conceptualisation and design of the study, the conduct of all experiments, the data analysis, and the drafting and revision of the manuscript. Dongdong Li was responsible for study supervision and critical revision of the manuscript and, as the corresponding author, takes responsibility for the content of the article. Both authors have read and approved the final manuscript.

**Competing interests**: The authors declare no competing interests.

**Informed consent**: Written informed consent was obtained from Raters 2 and 3 prior to their participation in the blinded expert review. The consent form described the study purpose, the intended use of the ratings, the data-handling and de-identification procedures, and the right to withdraw at any time.

**Ethical approval**: This study did not require formal ethical approval, because it did not involve patient data, biological samples, or human intervention. The QMS documents generated and evaluated used fictitious placeholder names (e.g., "Dr Li", "Dr Zhang") and contained no identifiable personal information. The inter-rater dataset was collected as methodological research from informed-consent volunteers; rater-level identifying data are stored under coded labels (Rater 1 / Rater 2 / Rater 3) in the released dataset.

**Data availability**: The 486 generated documents, 864 LLM-as-judge ratings, 30 blinded expert ratings, and all analysis code are openly available on GitHub (https://github.com/stttttte/iso15189-llm-config-experiment) under a dual licence: MIT for code and CC BY 4.0 for data. A versioned snapshot has been archived on Zenodo (DOI: [10.5281/zenodo.20091464](https://doi.org/10.5281/zenodo.20091464)).

---

## Acknowledgements

The author thanks the two colleagues who participated in the blinded expert review (Raters 2 and 3) for providing an independent expert perspective with full informed consent.

---

## Figure Legends

**Figure 1.** The nine prompt configurations evaluated in the study. Left panel: inclusion of each configuration across the four prompt-content dimensions (rules, document skeleton, detailed content, worked examples); ✓ = full inclusion, ◐ = partial inclusion, — = absent. Right panel: total system-prompt size of each configuration, expressed in thousands of tokens (cl100k_base tokenizer). The two panels are not proportional: the left-panel marks index the presence of *distilled, structured* prompt components, whereas the right-panel size reflects the total volume of loaded text. C_full reaches the largest token count by loading the full raw reference corpus (the complete ISO 15189 and CNAS standard texts plus an existing document library), yet its rules dimension is only partial (◐), because explicit rules are embedded within that raw text rather than supplied as a distilled rule set. A shorter configuration such as H2_keep_examples (~25K tokens) can therefore show full inclusion (✓) across all four structured dimensions while containing far fewer tokens than C_full.

**Figure 2.** Heatmap of the 2 × 2 cross-model symmetric design. Cells show the mean compliance score (0–5 Likert scale) across the three tasks (A1, B1, C1) for each of the nine configurations (rows) crossed with the four generator–judge combinations (columns). C_full exhibits a marked drop in the two GPT-generated columns (1.40 and 1.84, indicated by black-bordered cells), in sharp contrast with the two Claude-generated columns (Claude-judge × Claude-generated = 4.56; GPT-judge × Claude-generated = 3.22).

**Figure 3.** Systematic overestimation of compliance scores by the LLM judges relative to the three-rater expert panel (n = 10 documents × 3 raters). Horizontal axis: mean rating of the three experts. Vertical axis: LLM-judge rating. Left: Claude Opus 4.6 as judge [ICC(3,1) = 0.548, 95% CI −0.08 to 0.86; Pearson r = 0.573; mean difference (expert − Claude) = −0.905]. Right: GPT-5.4 as judge [ICC(3,1) = 0.217, 95% CI −0.44 to 0.72; Pearson r = 0.259; mean difference (expert − GPT) = −0.525]. Dashed line: 1:1 perfect agreement. Markers are colour-coded by configuration (legend inset).

**Figure 4.** Compliance score (0–5 Likert) versus system-prompt token size, computed on the n = 10 expert-blinded subset (seven configurations; per-stratum n = 1 or 2). Horizontal axis: token count on a symmetric-logarithmic scale (cl100k_base tokenizer). All three curves are based on the same matched samples: solid green line with squares, three-rater expert mean; solid red line with circles, Claude Opus 4.6 judge applied to Claude-generated outputs; solid blue line with triangles, GPT-5.4 judge applied to Claude-generated outputs. Orange-shaded band: the token-efficient optimum identified by the LLM-judge tier (E_rules_v2 / H4_sop_only). Green-shaded band: the clinical-usability optimum identified by expert evaluation (F_template / G_template_rules). Error bars are omitted because per-stratum n = 1 or 2; the corresponding LLM-versus-expert calibration scatter is shown in Figure 3.

---

## References

1. ISO 15189:2022. Medical laboratories — Requirements for quality and competence. Geneva: International Organization for Standardization; 2022.

2. Yang S, Zhou Y, Wang C, Luo M. The 'Double Helix' model of quality monitoring: risk mapping of quality management system during initial ISO 15189 implementation in a medical laboratory. PLoS One 2026;21:e0342129.

3. Anthropic. Claude Opus 4.6 System Card. San Francisco (CA): Anthropic; 2026. Available at: https://www.anthropic.com/claude-opus-4-6-system-card. [Accessed 9 May 2026].

4. OpenAI. GPT-5 System Card. San Francisco (CA): OpenAI; 2025. Available at: https://openai.com/index/gpt-5-system-card/. [Accessed 9 May 2026].

5. Boiko DA, MacKnight R, Kline B, Gomes G. Autonomous chemical research with large language models. Nature 2023;624:570–8.

6. Jin D, Pan E, Oufattole N, Weng WH, Fang H, Szolovits P. What disease does this patient have? A large-scale open domain question answering dataset from medical exams. Appl Sci 2021;11:6421.

7. Zhao WX, Zhou K, Li J, Tang T, Wang X, Hou Y, et al. A survey of large language models. arXiv preprint 2023; arXiv:2303.18223.

8. Schulhoff S, Ilie M, Balepur N, Kahadze K, Liu A, Si C, et al. The prompt report: a systematic survey of prompting techniques. arXiv preprint 2024; arXiv:2406.06608.

9. Zheng L, Chiang WL, Sheng Y, Zhuang S, Wu Z, Zhuang Y, et al. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In: Advances in Neural Information Processing Systems 36 (NeurIPS 2023) Datasets and Benchmarks Track. 2023.

10. Tan H, Guo Z, Shi Z, Xu L, Liu Z, Feng Y, et al. ProxyQA: an alternative framework for evaluating long-form text generation with large language models. In: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers); 2024 Aug 11–16; Bangkok, Thailand. Stroudsburg (PA): Association for Computational Linguistics; 2024. p. 6806–27.

11. Chiang WL, Zheng L, Sheng Y, Angelopoulos AN, Li T, Li D, et al. Chatbot Arena: an open platform for evaluating LLMs by human preference. arXiv preprint 2024; arXiv:2403.04132.

12. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. arXiv preprint 2024; arXiv:2404.13076.

13. Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. Psychol Bull 1979;86:420–8.

14. Cicchetti DV. Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments in psychology. Psychol Assess 1994;6:284–90.

15. Liu NF, Lin K, Hewitt J, Paranjape A, Bevilacqua M, Petroni F, et al. Lost in the middle: how language models use long contexts. Trans Assoc Comput Linguist 2024;12:157–73.

16. Knott M, Krebs M, Kerscher A. Large language models in healthcare quality management: a European perspective on process automation and compliance. Front Digit Health 2026;8:1761641.

---

**Word count (main text including references)**: ~6000 words
**Tables**: 6
**Figures**: 4
**References**: 16
