# A Compliance Study of LLM-Generated Medical Laboratory QMS Documents Under Different Configurations

**Author**: Sidi Liu¹

**Affiliation**: ¹ Department of Laboratory Medicine, West China Hospital Xiamen, Sichuan University, Xiamen, Fujian 361024, China

**Corresponding author**: Sidi Liu, lllsssddd@icloud.com, ORCID: 0009-0006-1695-5372

**Short title**: LLM configuration for ISO 15189 document compliance

**Keywords**: ISO 15189; medical laboratory; quality management system; large language model; prompt engineering; LLM-as-Judge; expert validation

---

## Abstract

**Objectives**: This study aimed to systematically compare the compliance of large language model (LLM)-generated ISO 15189:2022 medical laboratory quality management system (QMS) documents under different configuration strategies, to identify the optimal configuration range, and to expose systematic biases in current evaluation methods through a multi-tier evaluation framework.

**Methods**: An asymmetric two-model design produced 486 QMS documents in total: Claude Opus 4.6 × 9 configurations × 15 tasks × 3 replicates (405 documents), and, for cross-model validation, GPT-5.4 × 9 configurations × 3 tasks (A1/B1/C1) × 3 replicates (81 documents). The nine configurations were obtained by orthogonally combining four dimensions—rules, skeleton, detailed content, and examples—with token sizes ranging from 0 to 71 K. Three evaluation tiers were applied: (1) a Python automated compliance scorer; (2) dual LLM-as-Judge review by Claude and GPT-5.4 (864 ratings = 378 Claude-judge + 486 GPT-judge, including a 2 × 2 symmetric cross-model design); and (3) independent scoring by three ISO 15189-qualified experts on 10 stratified-randomly sampled, blinded documents. Inter-rater agreement was assessed by Pearson correlation, Spearman correlation, and intraclass correlation coefficients [ICC(2,1) and ICC(3,1)].

**Results**: (1) Four-factor orthogonal ablation showed that the rules layer (Δ = +0.511, p < 0.001) and the skeleton layer (Δ = +0.213, p = 0.055) contributed significantly or near-significantly at the LLM-judge tier; detailed content (Δ = −0.031, p = 0.79) and examples (Δ = −0.053, p = 0.46) contributed nothing or were mildly harmful. (2) The full-context configuration C_full (71 K) yielded cross-evaluated scores of 3.22–4.56 under Claude generation but dropped to 1.40–1.84 under GPT-5.4 generation, indicating that long-context exploitation in this scenario is model-specific to Claude Opus. (3) Claude-as-judge exhibited a self-preference bias of approximately +0.46, whereas GPT-as-judge showed an inverse bias of approximately −0.47. (4) Inter-rater agreement among the three experts reached ICC(2,k) = 0.982; expert mean versus Claude-as-judge gave ICC(3,1) = 0.548 (p = 0.04), versus GPT-as-judge ICC(3,1) = 0.217 (p = 0.26); both LLM judges systematically overestimated by 0.52–0.90 points. (5) The configuration ranked first by LLM judges, H4_sop_only (6 K skeleton), ranked second-to-last under expert evaluation (3.20, n = 2), whereas template-based configurations F_template (35 K), H2_keep_examples (61 K), and G_template_rules (38 K) ranked highest under expert evaluation (4.06–4.24).

**Conclusions**: The "optimal configuration" for LLM-assisted QMS document generation depends on the evaluation perspective. Scenarios prioritizing token efficiency and cost control should adopt H4_sop_only (6 K) or E_rules (3 K); scenarios involving formal submission and CNAS accreditation application should adopt G_template_rules (38 K) or F_template (35 K). C_full (71 K) should be avoided under current GPT-class models given the instability of their long-context capability. LLM-as-Judge can serve as a first-pass screening tool but cannot replace expert final review; Claude-as-judge ranks moderately consistently with experts and may serve as a coarse proxy, whereas GPT-as-judge is unsuitable for this purpose.

---

## 1. Introduction

ISO 15189:2022 *Medical laboratories — Requirements for quality and competence* is the international standard for medical laboratory accreditation, and its recognition in China has been steadily increasing. CNAS-CL02:2023, the corresponding implementation document issued by the China National Accreditation Service for Conformity Assessment, was released in parallel. Such standards prescribe what laboratories *should do* but not *how to do it*, requiring each laboratory to construct, on its own, a complete documentation system covering the quality manual, procedure documents, and standard operating instructions. In a typical tertiary-level hospital clinical laboratory, such a system contains 100 to 300 controlled documents and constitutes a systems-engineering effort spanning structural organization, clause mapping, form numbering, and responsibility assignment; manual drafting by the quality team typically takes several months, after which several rounds of internal audit are required before the system can be finalized. Laboratories pursuing CNAS accreditation generally require technical experts and trainers to guide them through this process.

The advancement of large language models (LLMs) has opened the possibility of automating this process. New-generation models such as Claude Opus 4.6 and GPT-5.4 have approached professional-level performance in long-document generation, structured output, and domain terminology use [1, 2]. However, one question that has not been systematically studied is what kind of system prompt should be supplied to an LLM in order to produce a compliant and usable QMS document. Two extreme strategies are observed in practice: the "full-context hypothesis," which loads all potentially relevant material (the ISO standard text, CNAS criteria, the existing document library, and examples) into the system prompt, with token counts often reaching 50–100 K; and the "minimal hypothesis," which provides only rule constraints and section skeletons and relies on the model's internalized knowledge to generate content, with token counts of only a few thousand. Empirical evidence for either strategy remains limited because existing studies of LLM configuration [3, 4] have focused on prompt engineering for general tasks and have not systematically compared specialized document scenarios such as QMS.

The bias inherent in evaluation methods is another deeper problem. LLM-generated quality is currently most often evaluated using the LLM-as-Judge approach (i.e., another LLM acts as the rater) [5]. Prior work has documented that LLM judges exhibit a self-preference bias (preferring text generated by their own model family) [6], but the manifestation of such bias in specialized domains—such as medical laboratory QMS—and its effect on configuration-comparison conclusions has not been empirically characterized.

Against this background, the present study was designed to use 486 generated documents, 864 LLM judge ratings, and 30 expert blind ratings to address the following research questions: (i) Which components of a system-prompt configuration (rules, skeleton, detailed content, examples) contribute to the quality of LLM-generated QMS documents? (ii) What is the minimum effective token budget? (iii) Does the optimal configuration generalize across generation models (Claude vs. GPT)? (iv) What is the magnitude of LLM judge self-preference bias? (v) Under cross-comparison of multi-tier evaluation (automated scoring, LLM judges, expert ratings), which configuration is the most robust?

---

## 2. Materials and methods

### 2.1 Configuration design

Nine controlled configurations were designed by orthogonally combining four dimensions: rules, skeleton, detailed content, and examples (Figure 1). Among them, A_bare (0 K) and B_simple (0.4 K) served as baselines; C_full (71 K) represented the full-context input strategy; E_rules (3.1 K) contained only the rules layer; F_template (35 K) contained the complete template without rules; G_template_rules (38 K) combined rules and template; H2_keep_examples (61 K) retained examples in addition to G; H3_skeleton (13 K) preserved the module skeleton while removing detailed content; and H4_sop_only (6 K) preserved only the single SOP skeleton most relevant to the task.

The rules layer was based on rules.md (3.1 K) and revised through domain-expert review: three incorrect terminology mappings were removed (instrument → equipment, calibrator product → calibrator, inter-laboratory comparison → proficiency testing); three target terms were corrected (specimen → sample, test item → measurand, linear range → reportable range); and 10 verified mappings together with 7 categories of vague-expression prohibitions were retained. The skeleton layer was extracted from the template library by the strip_to_skeleton algorithm, which preserved section headings, the introductory paragraph of each section, and form numbering lists, while removing verbatim clause excerpts, detailed table content, examples, detailed step lists, and code blocks.

### 2.2 Generation models and tasks

The main experiment used Claude Opus 4.6 (Anthropic) × 9 configurations × 15 tasks × 3 replicates, producing 405 documents. The 15 tasks were grouped according to CNAS audit scenarios into Class A (document drafting; e.g., personnel training and competence-evaluation control procedures), Class B (system operation; e.g., annual internal-audit checklists), and Class C (audit simulation; e.g., review reports for internal quality-control procedure documents), with 5 tasks each. Cross-model validation used GPT-5.4 (OpenAI, accessed via the AIHubMix proxy) × 9 configurations × 3 tasks (A1/B1/C1) × 3 replicates, producing 81 documents. Both models were configured with temperature = 1.0 and max_tokens = 12 000, and they used identical system-prompt configurations.

### 2.3 Three-tier evaluation framework

**Tier 1**: A Python automated compliance scorer (auto_scorer.py, openly released) rated all 486 documents on five dimensions (0–5 integer scale).
- **Format**: required section headings matched per task class (Class A procedure documents: 8 sections; Class B checklists/reports: 6 sections; Class C audit reports: 7 sections; synonyms accepted), combined with numbering-depth and empty-section checks; ≥3 missing sections scored 1, 1 missing section scored 3.
- **Clause coverage**: regular-expression matching of ISO 15189:2022 chapter 4–8 clause identifiers (e.g., 5.4.1), filtered by a ±40-character context window to suppress spurious matches; ≥10 unique clauses with at least one CNAS-CL02 reference scored 5, no reference scored 1.
- **Terminology compliance**: a 14-term mapping table aligned with ISO 15189:2022 / CNAS-CL02:2023 (e.g., 分析前过程 → 检验前过程, 标本 → 样品, 不确定度 → 测量不确定度), with context-exclusion rules to avoid false positives (e.g., 不确定度 inside 测量不确定度 is not flagged).
- **Vague expressions**: detection of expressions such as 及时, 相关人员, 定期, dual-filtered by a compound-word whitelist and a 30-character trailing window for frequency quantifiers (e.g., "weekly" or "annually" suppresses the flag).
- **Composite score**: a weighted aggregate (auto_weighted) of the five dimensions; the exact weights are defined in the WEIGHTS dictionary of auto_scorer.py.

**Tier 2a**: Claude Opus 4.6 was used as judge under a "CNAS chief assessor" role prompt (the JUDGE_PROMPT_TEMPLATE in gpt_cnas_judge.py, identical to that used in Tier 2b), scoring each document on five dimensions on a 0–5 scale (rubric below). Model parameters: temperature = 1.0, max_tokens = 4 096; one rating per document, single API call. A total of 378 Claude-judge ratings were generated: 270 covered the six core configuration groups (A/B/C/E/F/G) × 15 tasks × 3 replicates (Claude-gen, per-paper raw fully released); 81 covered 9 configurations × A1/B1/C1 × 3 replicates (GPT-gen, archived only as aggregated means; see §4.5 limitation x); and 27 covered the H groups (H2/H3/H4) × A1/B1/C1 × 3 replicates (Claude-gen, archived only as aggregated means).

**Tier 2b**: GPT-5.4 (OpenAI, accessed through the AIHubMix API proxy) served as judge using exactly the same prompt, rubric, and 0–5 scale as Tier 2a. Model parameters: temperature = 1.0, max_tokens = 4 096. All 486 generated documents were rated (405 Claude-gen + 81 GPT-gen), one rating per document; per-paper raw JSON files are fully retained and openly released. Combined, Tiers 2a and 2b yielded **864 LLM-judge ratings** (= 378 from Claude-judge + 486 from GPT-judge); the asymmetry reflects that Claude-judge was not run on H-group × full-15-task or on the complete GPT-gen set (see §4.5 limitation x). Tiers 2a and 2b together formed a 2 × 2 symmetric design (Claude-gen × Claude-judge, Claude-gen × GPT-judge, GPT-gen × Claude-judge, GPT-gen × GPT-judge), enabling orthogonal decomposition of self-preference bias.

**Scoring scale.** Each of the five dimensions was scored on a 0–5 integer scale: **5 = fully compliant** (5-point anchor below); **4 = mostly compliant** (between the 5- and 3-point anchors, with minor issues only); **3 = partially compliant** (3-point anchor); **2 = noticeably non-compliant** (between the 3- and 1-point anchors); **1 = severely non-compliant** (1-point anchor); **0 = the dimension cannot be evaluated** because the document is essentially absent or non-substantive (e.g., the model returned only a planning enquiry rather than the requested document). The 5/3/1 anchor descriptors below were specified to all judges (LLM and expert) in identical wording; intermediate scores (2, 4) were assigned when the document fell between two adjacent anchors.

**Five-dimensional rating rubric** (shared by Tiers 2a/2b and Tier 3):

| Dimension | Anchor at 5 | Anchor at 3 | Anchor at 1 |
|-----------|-------------|-------------|-------------|
| Clause coverage | All SHALL requirements of the relevant clauses are operationalised with concrete measures | Major clauses covered but with omissions or surface-level treatment | Most clauses merely cited without implementation, or major omissions |
| Operability | Every step has a named role (job title), quantified deadline, and explicit output (form ID) | Most steps actionable, a few vague | Pervasive use of "in a timely manner", "relevant personnel", "periodically" without operational detail |
| Internal consistency | All referenced documents and forms appear in the corresponding sections; responsibilities cleanly assigned | A few dangling references or minor textual contradictions | Many dangling references or conflicting responsibility assignments |
| PDCA closure | Explicit Plan–Do–Check–Act chain with execution records, effectiveness evaluation, non-conformity handling, and improvement | P-D-C present but A (improvement/feedback) missing | Execution steps only; no check or improvement |
| Professional depth | Contains laboratory-specific detail (e.g., Westgard rules, measurement uncertainty, Sigma metrics, HIL indices, blind testing, PCR zoning, cold chain) | Some professional flavour but largely generic | Generic content applicable to any laboratory |

**Tier 3**: Three ISO 15189-qualified experts independently scored 10 blinded, stratified-randomly sampled documents. Rater 1 was the first author, with ISO 15189 accreditation-assessment experience; Raters 2 and 3 were qualified ISO 15189 internal auditors from the same institution. The sampling strategy used a fixed random seed (seed = 42) to draw 10 of the 486 documents stratified across 7 core configuration groups × Class A procedure tasks (A1/A2/A3), with 1 to 2 documents per group. The three experts scored independently without inspecting each other's ratings or discussing them; Raters 2 and 3 completed their scoring without knowledge of Rater 1's ratings, and only thereafter were the three sets of ratings merged. Written informed consent was obtained from Raters 2 and 3 before scoring. The experts used exactly the same five-dimensional rubric as the LLM judges (see table above) and were free to consult the full text of ISO 15189:2022 and CNAS-CL02:2023 and their annexes during scoring.

**Blinding procedure.** Blinding was implemented at four levels (script: `prepare_blind_review.py`):
- *File renaming.* Each sampled document was copied from its original path `outputs/{group}/{group}-{task}-{rep}.md` to a flat series `paper_01.md … paper_10.md`; group and replicate identifiers were thereby removed from the filename and the directory structure presented to experts.
- *Content sanitisation.* An automated text scan of all 10 blinded files confirmed zero occurrences of any model identifier ("Claude", "GPT", "Opus") or configuration-group token ("H4", "C_full", "G_template", "F_template", "H2_keep", "E_rules", "A_bare", "H3_skeleton") in the document body, so the model/configuration source could not be inferred from the text.
- *Order randomisation.* The assignment of (group, task, rep) triples to paper_01–paper_10 was shuffled with a fixed Python random seed (seed = 42). The resulting order was identical for all three experts; only the task category (e.g., "Personnel training and competence-evaluation control procedure") was disclosed in the rating sheet, because this is intrinsic to the document and necessary for assessment, while the underlying configuration group remained hidden.
- *Key isolation.* The (paper_id → group, task, rep) mapping (`blind_review/key.json`) was sealed before scoring began and was opened only after all three rater sheets had been submitted.

### 2.4 Statistical analysis

Pairwise between-group comparisons used the two-sided Mann–Whitney U test (scipy.stats.mannwhitneyu) on per-paper GPT-judge scores (n = 45 per group: 15 tasks × 3 replicates), with Bonferroni correction applied for multiple comparisons within the four-factor ablation. The four configuration-component effects were quantified under an orthogonal substitution scheme using targeted configuration contrasts: rules = E_rules_v2 vs A_bare; skeleton = H4_sop_only vs E_rules_v2; detailed content = G_template_rules vs H3_skeleton; examples = H2_keep_examples vs G_template_rules. Each effect Δ was defined as a *simple arithmetic mean difference*, Δ = mean(group_B) − mean(group_A), where each group mean is the unweighted average of the 45 per-paper GPT-judge scores in that configuration; no covariates, random effects, weighting, or shrinkage were applied. The same 45-per-group sample served as input to the corresponding Mann–Whitney U test reported alongside each Δ. No L9 orthogonal-array decomposition, least-squares-means estimation, or mixed-effects modelling was used. Inter-rater agreement was assessed by Pearson correlation, Spearman correlation, and the ICC(2,1) (absolute agreement) and ICC(3,1) (consistency in ranking) defined by Shrout and Fleiss [13]. ICC computation used the pingouin 0.5 Python library. Self-preference bias was quantified by cross-model differencing as bias = (mean own-own) − (mean cross-own).

---

## 3. Results

### 3.1 Nine-group ranking at the LLM-judge tier

Across the 405 Claude-generated documents, the composite three-track score (automated scoring + Claude judge + GPT judge) ranked the configurations as follows: H4_sop_only (6 K) first (0.994), H3_skeleton (13 K) second, G_template_rules (38 K) third, H2_keep_examples (61 K) fourth, E_rules (3.1 K) fifth, C_full (71 K) sixth, F_template (35 K) seventh, B_simple eighth, and A_bare ninth. At the LLM-judge tier, H4 reached the highest composite score with the smallest token budget.

### 3.2 Four-factor orthogonal ablation

The main effect of the rules layer was +0.511 (p < 0.001) and that of the skeleton layer was +0.213 (p = 0.055), both contributing positively (significantly or near-significantly) at the LLM-judge tier. Detailed content showed no contribution (G vs. H3: Δ = −0.031, p = 0.79), and examples showed a directional harm (H2 vs. G: Δ = −0.053, p = 0.46). H4 and H3 did not differ significantly (Δ = −0.009, p = 0.80), suggesting that the task-specific SOP skeleton (6 K) and the full module skeleton (13 K) are functionally equivalent. This ablation result holds only at the LLM-judge tier; expert-tier analysis is reported in Section 3.5.

### 3.3 2 × 2 symmetric cross-model validation

Figure 2 presents the 2 × 2 symmetric matrix (n = 9 configurations × 4 quadrants). C_full exhibited a marked drop in performance under GPT generation (GPT-gen × Claude-judge mean 1.40; GPT-gen × GPT-judge mean 1.84), whereas the same C_full under Claude generation produced cross-evaluated scores of 3.22–4.56. This indicates that the apparent usability of the 71 K full-context configuration under Claude Opus is model-specific rather than a general result. GPT-5.4 under the 71 K configuration exhibited failure modes including instruction forgetting, structural breakdown, and clause confusion.

### 3.4 Self-preference bias of LLM judges

Computed as bias = (own-own) − (cross-own), the mean bias of the Claude judge was +0.464 (positive in 8 of 9 groups; the maximum, +1.33, occurred at C_full), and that of the GPT judge was −0.472 (negative in 8 of 9 groups, i.e., GPT preferred Claude-generated text). The two biases formed a symmetric, opposite-signed pattern of comparable magnitude, indicating that the bias originates at the judge end as a systematic phenomenon rather than from any genuine quality difference at the generation end. Skeleton-type configurations (E, H3, H4) showed the smallest bias (< 0.15).

After removing self-preference bias (by retaining only the cross-evaluation mean, i.e., the average of Claude-judge → GPT-gen and GPT-judge → Claude-gen), the nine groups ranked as follows: G_template_rules first (4.211), H3_skeleton second (4.167), E_rules third (4.133), H4_sop_only fourth (4.100). The four configurations G, H3, E, and H4 became statistically equivalent after debiasing (Δ < 0.11). C_full dropped to ninth (2.310) under this ranking.

### 3.5 Expert-tier validation

Inter-rater agreement among the three experts was excellent: ICC(2,k) = 0.982 (95% CI [0.95, 1.00]); ICC(3,k) = 0.981; pairwise ICC(2,1) values were 0.948 (R1–R2), 0.928 (R1–R3), and 0.969 (R2–R3), all reaching the excellent range (> 0.90). This indicates that the five-dimensional rubric is highly objective in design while also suggesting that consensus among same-institution experts may overestimate cross-institution agreement (see Section 5).

The expert mean compared with the Claude judge gave ICC(3,1) = 0.548 (p = 0.04), Pearson r = 0.573, Spearman ρ = 0.509, mean difference −0.905; the expert mean compared with the GPT judge gave ICC(3,1) = 0.217 (p = 0.26), Pearson r = 0.259, mean difference −0.525 (Figure 3). Both LLM judges systematically overestimated by 0.52–0.90 points; Claude versus expert ranking agreement was at a moderate level, whereas GPT versus expert agreement was poor.

The expert mean by configuration ranked as follows: F_template 4.24 (n = 1) first, H2_keep_examples 4.07 (n = 1) second, G_template_rules 4.06 (n = 2) third, C_full 3.45 (n = 2) fourth, H4_sop_only 3.20 (n = 2) fifth, E_rules 3.19 (n = 1) sixth, A_bare 3.04 (n = 1) seventh. The first-ranked configuration at the LLM-judge tier (H4_sop_only, 6 K) ranked second-to-last under expert evaluation (only 0.16 above A_bare). Overestimation by the LLM judges was largest for C_full and H4 (Δ = expert − LLM-judges mean = −1.00 and −1.05, respectively), suggesting that although these two configurations exhibit structural completeness and terminological compliance, their insufficient depth in clinical practice is detectable to experts.

### 3.6 Token size versus quality: a dual-perspective relationship

Figure 4 shows the relationship between token size and quality scores from two perspectives. The Claude-judge curve increases monotonically with token size, remaining at 4.90 even at C_full; the GPT-judge curve peaks near H4 (6 K) and then descends, collapsing at C_full; the expert curve peaks at the F/G template region (35–38 K) at 4.24 but reaches only 3.20 at H4 (6 K). The three curves diverge most prominently in the 6–13 K interval: the LLM judges already consider this region near peak, whereas experts judge it as still substantially below the optimum. This result indicates that token-efficiency-oriented configuration optimization and clinical-usability-oriented configuration optimization correspond to two different objective functions in the QMS generation scenario.

---

## 4. Discussion

### 4.1 Configuration minimization holds at the LLM tier but not at the expert tier

Four-factor ablation at the LLM-judge tier yields a parsimonious conclusion: rules and skeleton are necessary, while detailed content and examples contribute nothing or are even harmful. This conclusion is consistent with the lost-in-the-middle theory [3] and with prompt-minimization practice [12]. However, expert-tier analysis overturns this simplification: detailed content (the full template in F and G) substantially improves clinical usability (F 4.24 vs. H4 3.20, a difference of 1.04), because the LLM's internalized knowledge does not cover all sub-scenarios of clinical practice—including emergency-sample handling, patient-self-collected specimens, courier-personnel qualification, and rejection criteria. Such information must be explicitly supplied through the system prompt.

### 4.2 The full-context trap is model-dependent

C_full (71 K) is a typical "looks-safe" configuration option: it includes all potentially relevant material and aligns with the "more is safer" intuition. Yet under GPT-5.4 generation (cross-evaluated scores 1.40–1.84), it failed completely. A possible explanation is that Claude Opus has been more thoroughly trained for long-context attention and is able to extract effective signal from 71 K of context, whereas GPT-5.4 exhibits instruction forgetting under such long configurations. The methodological lesson is that any conclusion that "configuration X is acceptable" must be validated across generation models; single-model results are entangled with model characteristics and should not be extrapolated.

### 4.3 Limitations and appropriate use of LLM-as-Judge

The present study quantified two important categories of bias: cross-LLM bias (Claude overestimates its own family by +0.46; GPT shows the inverse −0.47) and machine-versus-expert bias (both LLM judges overestimate by 0.52–0.90 points). The Claude-judge ranking was moderately consistent with the three-expert mean (ICC = 0.548) and may serve as a coarse proxy: in large-scale generation scenarios, Claude judging can first filter out clearly low-quality outputs, sparing expert time. The GPT judge's ranking agreement with experts was only ICC = 0.217 and is unsuitable as a proxy. Critical documents (those for submission, formal system files, and operational deployment) must undergo expert final review.

### 4.4 Configuration recommendations stratified by scenario

Synthesizing evidence from all three tiers, configuration recommendations for different use scenarios are summarized below (Table 6):

| Use scenario | Recommended configuration | Tokens | Rationale | Trade-off |
|--------------|---------------------------|--------|-----------|-----------|
| Rapid first-draft generation; internal iteration | H4_sop_only or E_rules | 3–6 K | Near-optimal at LLM tier; highest efficiency | Requires manual supplementation of clinical detail |
| Multiple SOP drafting | H4 or H3 | 6–13 K | Task-specific skeleton plus rules | Same as above |
| Formal documents for CNAS submission | G_template_rules | 38 K | Highest expert acceptance; cross-model robust | Higher token cost |
| Complete quality manual | F_template or G | 35–38 K | Highest expert scores | Same as above |
| Not recommended | C_full (71 K) | — | Collapses under GPT generation; lowest cross-evaluation rank | — |
| Not recommended | A_bare, B_simple | — | Baseline too low; lacks compliance | — |

The recommended practical workflow is to generate the first draft with H4, supplement clinical detail by manual review, and finally regenerate or refine critical documents with G.

### 4.5 Limitations

The present study has the following limitations. (i) Limited expert sample size: n = 3 raters × 10 documents, with only 1 to 2 documents per group, supporting only directional ranking conclusions and not strict statistical inference. Multi-center validation with 3–5 experts × 30–50 documents across institutions is a key direction for future work. (ii) Two-edged effect of same-institution agreement: the very high agreement among the three experts [ICC(2,k) = 0.982] is both evidence of the validity of the five-dimensional rubric and a possible reflection of shared professional culture, training lineage, and clause-interpretation habits within the same institution, which may overestimate cross-institution generalizability. (iii) Dual role of the first author: the first author acted both as Rater 1 and as study designer. Raters 2 and 3 completed their scoring without knowledge of Rater 1's ratings, and the data of all raters are fully released. (iv) Shared rubric between experts and LLM judges: there is a risk of shared-measurement bias; future work should add expert-native dimensions such as clinical usability. (v) Limited GPT-5.4 task coverage: only A1/B1/C1 (81 documents) were generated. (vi) Domain specificity: results are restricted to ISO 15189 medical laboratories, and transferability to other standards such as ISO 17025 or ISO 9001 remains to be validated. (vii) Absence of third-party LLM judges: only Claude and GPT were used as judges. (viii) Language scope: all QMS documents were in Chinese; the effects in English or other languages have not been verified. (ix) Model temporality: the quality of generated documents depends on the model used, and the conclusions of the present study may need to be re-validated as LLMs continue to iterate. (x) Raw-data retention for cross-judge cells: per-paper raw scores for the Claude-judge × GPT-gen quadrant and for the Claude-judge × H-group Claude-gen subset were archived only as aggregated means; the per-paper JSON files were not retained. The 2 × 2 self-preference matrix therefore cannot be independently recomputed from the lowest-level data, although per-paper raw Claude-judge ratings for the six core configuration groups (A/B/C/E/F/G; 270 ratings) and all 486 GPT-judge per-paper ratings are fully released. (xi) Intra-judge reliability not assessed: each LLM judge scored each document exactly once; judges were not asked to re-score documents to quantify intra-judge variance. Inter-judge reliability is captured via the 2 × 2 cross-comparison between Claude and GPT judges and via the three-expert ICC analysis.

---

## 5. Conclusions

The optimal configuration for LLM-assisted ISO 15189 QMS document generation depends on the evaluation perspective. At the LLM-judge tier, H4_sop_only (6 K) achieves the highest composite score; under expert evaluation, F_template (35 K), H2_keep_examples (61 K), and G_template_rules (38 K) tie at the top (mean 4.06–4.24), with H4 ranked second-to-last. Scenarios prioritizing token efficiency and cost control should adopt H4 or E_rules (3–6 K); scenarios requiring formal submission and CNAS accreditation application should adopt G or F (35–38 K); C_full (71 K) should be avoided. LLM-as-Judge can serve as a first-pass screening proxy (Claude is more effective than GPT), but critical documents must undergo expert final review.

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

## Figure Legends

**Figure 1.** Nine configurations tested for LLM-assisted ISO 15189 QMS generation. Left: inclusion of each configuration along the four dimensions of rules, skeleton, detailed content, and examples (✓ included, half-circle partial, — absent); right: the system-prompt size of each configuration (K tokens).

**Figure 2.** Heatmap of the 2 × 2 cross-model symmetric design. Mean score (across tasks A1/B1/C1, 0–5 scale) for nine configurations (rows) × four generator–judge combinations (columns). C_full collapses markedly in the two GPT-generated columns (1.40 and 1.84, black-bordered cells), in sharp contrast with the two Claude-generated columns (4.56 and 3.22).

**Figure 3.** Systematic overestimation of LLM judges relative to a three-rater expert panel (n = 10 papers × 3 raters). Horizontal axis: mean rating of the three experts. Vertical axis: LLM-judge rating. Left: vs Claude Opus 4.6 [ICC(3,1) = 0.548; Pearson r = 0.573; mean diff = −0.90]. Right: vs GPT-5.4 [ICC(3,1) = 0.217; Pearson r = 0.259; mean diff = −0.52]. Dashed line: 1:1 perfect agreement; configurations colour-coded.

**Figure 4.** Token size versus quality score — LLM judges peak at 6–13 K while experts prefer 35–61 K. Horizontal axis: system-prompt size (symlog scale). Vertical axis: quality score (0–5). Solid green line (squares): three-rater expert mean. Solid red line (circles): Claude Opus 4.6 judge. Solid blue line (triangles): GPT-5.4 judge. Orange-shaded band marks the token-efficient optimum (H4 / H3); green-shaded band marks the expert-judged clinical-usability optimum (F / G).

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

---

**Word count (main text including references)**: ~5400 words
**Tables**: 1 (Table 6 — configuration recommendations stratified by scenario)
**Figures**: 4
**References**: 13
