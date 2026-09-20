Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation

Authors: Sidi Liu1, Lan Yang1, Xinying Chen1, Dan Wu1, Dongdong Li2,3,*

Affiliations: ¹ Department of Laboratory Medicine, West China Hospital Xiamen, Sichuan University, Xiamen, Fujian 361024, China; ² Department of Laboratory Medicine, West China Hospital, Sichuan University, Chengdu, Sichuan 610041, China; ³ Sichuan Clinical Research Center for Laboratory Medicine, Chengdu 610041, Sichuan, PR China

Corresponding author: * Dongdong Li, Department of Laboratory Medicine, West China Hospital, Sichuan University, and Sichuan Clinical Research Center for Laboratory Medicine, Chengdu, Sichuan, PR China; email jiangxili1219@163.com; ORCID https://orcid.org/0000-0002-0290-6485

ORCID: Sidi Liu 0009-0006-1695-5372; Dongdong Li 0000-0002-0290-6485

Short title: Prompt configuration and LLM-as-judge bias in ISO 15189 drafting

Abstract

Objectives: To evaluate the ISO 15189:2022 compliance of quality management system (QMS) documents drafted with large language model (LLM) assistance.

Methods: We generated 486 QMS documents with Claude Opus 4.6 (405) and GPT-5.4 (81) across nine prompt configurations varying rules, document skeleton, detailed content, and worked examples. Evaluation combined an automated scorer, two LLM judges (759 archived document-level ratings plus additional aggregate records), and blinded review of 10 sampled Claude-generated documents by three ISO 15189 internal auditors.

Results: Only the rules component significantly improved compliance at the LLM-judge tier [Δ = 0.511, bootstrap 95% CI (0.28, 0.75); Benjamini–Hochberg-adjusted p < 0.001]. The full-context C_full (archived configuration text: ~56,000 tokens) scored 3.22–4.56 for Claude-generated documents but only 1.40–1.84 for GPT-5.4-generated documents. Within-institution expert agreement was excellent [ICC(2,k) = 0.982]; judge–expert agreement was at best moderate [ICC(3,1) = 0.548 vs 0.217], with wide confidence intervals crossing zero, and both judges overestimated expert scores by 0.52–0.90 points. H4_sop_only, favored by the automated/GPT composite, fell to fifth of seven under expert review, whereas template-anchored configurations ranked highest (4.06–4.24).

Conclusions: The optimal configuration varied with the evaluation tier: minimal prompts may suit exploratory drafts requiring subsequent human review; template-anchored prompts tended to perform best under exploratory expert review; and C_full performed markedly worse with GPT-5.4 under the tested settings. These findings do not establish a minimum token requirement. LLM-as-judge can support first-pass screening, but expert final review remains indispensable.

Keywords: ISO 15189; large language models; LLM-as-judge; medical laboratory accreditation; prompt engineering; quality management system

1. Introduction

ISO 15189:2022 Medical laboratories — Requirements for quality and competence [1] is the international standard for medical laboratory accreditation. In China, its adoption by medical laboratories continues to expand [2]. The corresponding national implementation document is CNAS-CL02:2023, issued by the China National Accreditation Service for Conformity Assessment (CNAS). These standards define what laboratories must achieve but do not prescribe in detail how each laboratory should implement the required processes. As a result, each laboratory must establish its own quality management system (QMS) documentation, including a quality manual, procedure documents, standard operating procedures, and associated records and forms. Based on the first author's experience as an ISO 15189 internal auditor, such a system in a tertiary hospital clinical laboratory contains on the order of 100–300 controlled documents and spans structural organization, clause-to-document mapping, form numbering, and responsibility assignment; drafting by an in-house quality team typically takes several months, followed by multiple rounds of internal audit before finalization. Laboratories pursuing CNAS accreditation typically engage external technical experts or trainers to guide this process.

Large language models (LLMs) have the potential to reduce this workload by generating structured first drafts of quality management documents. State-of-the-art models such as Claude Opus 4.6 and GPT-5.4 have shown increasing competence in long-document generation, structured output, and the use of domain-specific terminology [3, 4]. However, the optimal prompt design for generating compliant and operationally usable ISO 15189 quality management documents remains unclear. In practice, two broad prompting strategies are commonly used. The first is a full-context strategy, in which all potentially relevant materials, such as ISO and CNAS standards, existing standard operating procedures, templates, and worked examples, are loaded into the system prompt. This approach may result in prompts exceeding 50,000 to 100,000 tokens. The second is a minimal-prompt strategy, in which only distilled rules, formatting constraints, or document skeletons are provided, leaving the model to generate most content from its pretrained knowledge. Empirical evidence supporting either approach remains limited, as existing surveys of LLM behavior and prompting [5, 6] have largely addressed general-purpose tasks and have not specifically examined specialized regulatory-document scenarios such as QMS authoring.

A second methodological challenge concerns evaluation. LLM-generated outputs are currently most often assessed by the LLM-as-judge approach, in which a separate LLM assigns the scores [7]. In addition, methods for assessing long-form generation quality [8] and preference benchmarks built from large-scale human voting [9] are two other principal approaches. Studies have found that LLM judges tend to favor outputs from models in their own family (self-preference bias) [10]. However, whether and how this bias arises in specialized, regulated settings such as medical-laboratory QMS, and how it affects comparisons between configurations, has not been empirically characterized.

To address these gaps, the present study generated 486 QMS documents, analyzed 759 archived document-level LLM-judge ratings and additional retained group means, and obtained 30 blinded expert ratings, addressing the following five questions: (i) Which of the four prompt components – rules, document skeleton, detailed content, and worked examples – contributes most to compliance? (ii) How does archived configuration-text size relate descriptively to the evaluation results? (iii) Is the optimal configuration consistent between Claude Opus 4.6 and GPT-5.4? (iv) How large is the LLM-judge self-preference bias in this domain? (v) Which configuration performs robustly across all three tiers – automated scoring, LLM judges, and expert ratings? This study treats LLMs as drafting and screening tools rather than autonomous authors of controlled quality management documents. ISO 15189 documentation must reflect the laboratory's validated processes, instruments, responsibilities, workflows, and records, and must be reviewed and approved by competent personnel. An LLM-generated document may provide a useful first draft, but it is not itself a controlled document. It has no institutional accountability, has not been verified against local practice, and cannot replace expert review. Accordingly, our analysis focuses not on whether LLMs can independently produce accreditation-ready documents, but on how different prompt configurations affect the quality of drafts and how reliably LLM-based evaluation reflects expert judgment.

2. Materials and methods

2.1 Configuration design

We designed nine system-prompt configurations differing in four content categories: rules, document skeleton, detailed content, and worked examples. The composition and archived configuration-text size of each configuration are given in Figure 1. The substitution contrasts target specific content categories (Section 2.4.2), but the design does not independently manipulate content composition and token quantity. The letter D was skipped in the numbering: the early D_rules variant was discarded after expert review during configuration development identified terminology errors and was replaced by E_rules_v2.

The rules component is a rules.md file (~1,200 tokens) retaining, after domain-expert review, 10 terminology mappings (e.g., normalizing "specimen" to "sample" and "inter-laboratory comparison" to "proficiency testing"; English glosses shown here for presentation, as the deployed rules file was written in Chinese) and seven categories of prohibited vague expressions. The document skeleton was extracted from institutional templates by a custom script (strip_to_skeleton), keeping section headings, each section's introductory paragraph, and form numbers. Archived configuration files were recounted with cl100k_base (OpenAI tiktoken), excluding task messages, agent wrappers, and tool definitions. For F, G, H2, H3, and H4, reported sizes are means across the 15 archived task-specific files: 23,090 (range 12,160–42,885), 24,235 (13,305–44,030), 25,052 (13,397–44,345), 5,375 (4,262–6,916), and 2,373 (1,939–3,937) tokens, respectively. The separate fixed F/G reference files contain 14,947/16,138 tokens and are not the basis of these means. Fixed B, E, and C files contain 348, 1,236, and 56,151 tokens; A contains no experimental configuration text. These sizes describe archived artifacts, not verified historical Claude request sizes.

2.2 Generation models and tasks

The primary experiment used Claude Opus 4.6 (Anthropic, San Francisco, CA, USA) through the Claude Code Agent in text-only mode, with no tool calls during generation, although the framework's built-in tool definitions remain in the system prompt (Section 4.6). Nine configurations × 15 tasks × 3 replicates yielded 405 documents. The 15 tasks were grouped by CNAS audit scenario into three classes of five: Class A, document drafting; Class B, system operation; and Class C, audit simulation. The full task list with the corresponding ISO 15189:2022 clauses is given in Supplementary Table S1 and the original prompts in the GitHub repository. These tasks cover system-level documents concerned with document control, internal audit, and management review; they include no technical documents such as method validation reports or measurement-uncertainty procedures (Section 4.6).

For cross-model validation, GPT-5.4 (OpenAI, San Francisco, CA, USA) was accessed through the official openai Python SDK (v2.30.0), with the base URL pointed to the AIHubMix endpoint because direct access to the OpenAI API was unavailable from the authors' region. To limit API cost, GPT-5.4 generation covered only the first task of each class (A1, B1, and C1; these were not randomly sampled), run on the same nine configurations with three replicates, yielding 81 documents.

Both models were assigned the same nine configuration definitions, but the released GPT script loads task-specific F/G/H configurations, whereas complete Claude per-call input logs are unavailable. Exact input equivalence therefore cannot be retrospectively verified. Generation parameters also differed. Claude ran through the Claude Code Agent, which does not expose temperature or max_tokens, so neither was set explicitly; GPT-5.4 was called with temperature = 0.7 and max_completion_tokens = 16,000. Both settings are stochastic, hence the three replicates per combination; the consequences of this mismatch for cross-model comparison are discussed in Section 4.6. All API calls were made between 2 and 14 April 2026.

2.3 Three-tier evaluation framework

Compliance was evaluated with three complementary tiers, all scoring on a common 0–5 integer scale: an automated rule-based scorer (Tier 1), two LLM judges (Tiers 2a and 2b), and an independent blinded expert review (Tier 3). Tier 1 covered only structural features that code can detect objectively; Tiers 2 and 3 shared a five-dimensional rubric (Supplementary Table S2) – clause coverage, operability, internal consistency, PDCA closure, and professional depth.

2.3.1 Tier 1 – Automated scoring of structural compliance

The auto-scorer (auto_scorer.py, open source) rated all 486 documents on three dimensions: format (whether the document includes the section headings, numbering depth, and non-empty content required by its task class), clause coverage (regex matching of ISO 15189:2022 chapters 4–8 and CNAS-CL02:2023 clause identifiers), and terminology compliance (non-preferred terms flagged against an ISO 15189/CNAS-validated vocabulary table, together with detection of vague expressions such as "in a timely manner" and "relevant personnel"). These were combined into a weighted composite (auto_weighted; format 0.18, clause coverage 0.22, terminology 0.13), on which the Tier 1 rankings in Section 3 are based. These three weights are the corresponding entries of a seven-dimension a priori weighting scheme (summing to 1) defined in the released scorer, of which only the three rule-checkable dimensions are computed at this tier; because the composite is min-max normalized and used only for relative ranking (Section 3.1), the retained weight sum of 0.53 does not affect any result.

This tier measures structural compliance only. Clause coverage in particular records how many clauses a document cites, not whether those clauses are implemented: a document stating merely that "internal quality control shall be performed in accordance with 7.3.1", without specifying an actual QC scheme, still counts as covering that clause. Tiers 2 and 3 fill this gap – the clause-coverage dimension of the rubric assigns a score of 1 when many clauses are cited but left unimplemented – so a high Tier 1 score does not mean a document is ready to be submitted for accreditation.

2.3.2 Tier 2 – LLM-as-judge

The two judges (Claude and GPT) evaluated outputs from both generation models in a 2 × 2 design. Claude Opus 4.6, in the role of a "CNAS chief assessor", used the shared five-dimensional rubric through Claude Code Agent sub-agents, with temperature and max_tokens not explicitly set. Claude judging ran in successive batches. The archive contains 273 identifiable document-level Claude evaluations: 270 core evaluations (six configurations × 15 tasks × three replicates) and three supplemental H-group evaluations, all of Claude-generated documents. Additional historical Claude judgments survive only as aggregate means; their document-level scores and some cell denominators cannot be reconstructed. GPT-5.4 used the same rubric and 0–5 scale to rate all 486 documents once (405 Claude-generated + 81 GPT-generated), with temperature = 0 and max_completion_tokens = 2,000; all 486 JSON outputs parsed successfully and are released. Thus 759 document-level judge–document records are available, in addition to the retained aggregates. The cross-model analysis uses the archived group means, whereas analyses requiring individual observations use the available document-level records (Section 4.6). Supplementary Table S2 defines the 5-, 3-, and 1-point anchors (fully, partially, and severely non-compliant); scores 4 and 2 fall between adjacent anchors, and 0 means the dimension could not be evaluated. These anchor descriptions were identical for both judges and the experts.

2.3.3 Tier 3 – Expert review

Three qualified ISO 15189 internal auditors independently scored 10 blinded, stratified-randomly sampled documents on the same five dimensions. All three raters are authors of this paper and work at the same institution: Rater 1 was the first author, Rater 2 was Lan Yang, and Rater 3 was Xinying Chen. They scored independently, without communicating and without seeing one another's ratings; to avoid self-influence, Rater 1 viewed the Tier 1/2 scores only after all three rater sheets had been submitted. Written informed consent was obtained from Raters 2 and 3 before scoring, and during scoring the experts could freely consult ISO 15189:2022 and CNAS-CL02:2023. No formal pre-scoring calibration session was held (Section 4.6).

The 10 documents were drawn from the 486-document pool by stratified random sampling with a fixed seed (seed = 42), stratified across seven configurations × the three Class A tasks (A1–A3), with one or two documents per realized stratum. Only Class A was sampled, as it is the most stable and representative document type in CNAS audits (Section 4.6); the seven configurations evaluated here are listed in Section 3.5. Blinding was performed with the open-source script prepare_blind_review.py: each document was renamed to an anonymous identifier, all model and configuration markers were removed from the text and verified, and the presentation order was randomized, identical for all three experts. The key linking documents to configurations was sealed until all rater sheets had been submitted.

2.4 Statistical analysis

2.4.1 Pairwise group comparisons and multiplicity correction

Pairwise comparisons between configurations used two-sided Mann–Whitney U tests on the GPT-judge scores for each document (n = 45 per configuration; 15 tasks × 3 replicates). Observations within a configuration share the 15 underlying tasks and are therefore not fully independent; the tests treat replicates as independent, a simplification. The task-class-stratified estimates (Table 2), in which the rules effect is consistent in direction across all three classes, argue against a task-driven artifact. Because the four component contrasts share configurations and are therefore not independent, multiplicity was controlled with the Benjamini–Hochberg FDR procedure (α = 0.05) rather than the more conservative Bonferroni, retaining more power while controlling the false-discovery rate. A 95% confidence interval for each effect estimate (Δ) was obtained by bootstrap (nonparametric percentile method, fixed seed, B = 10,000 resamples).

2.4.2 Quantification of configuration-component effects

Four pairs of configurations measured the four content components, each pair differing mainly in one component: rules (E_rules_v2 vs A_bare), document skeleton (H4_sop_only vs E_rules_v2), detailed content (G_template_rules vs H3_skeleton), and worked examples (H2_keep_examples vs G_template_rules). The effect of each component (Δ) is the difference between the two configurations' mean scores, expressed on the raw 0–5 scale without standardization, with a bootstrap 95% CI (Table 2). We deliberately used this direct pairwise contrast rather than a more elaborate statistical model because it is the easiest to interpret. The nine configurations are not a Taguchi L9 orthogonal array but a structured subset of the four-dimensional configuration space, selected to isolate each dimension through these contrasts rather than to satisfy orthogonal-balance criteria; the Δ estimates therefore correspond only to those specific pairs.

2.4.3 Inter-rater agreement

Inter-rater agreement was reported using Pearson correlation, Spearman correlation, and intraclass correlation coefficients (ICCs, following the Shrout–Fleiss framework [11]), all computed with the pingouin Python library. Pairwise comparisons (expert mean vs each LLM judge, and comparisons within the expert panel) used the single-rater variants ICC(2,1) and ICC(3,1), whereas the overall reliability of the three-expert panel used the averaged variants ICC(2,k) and ICC(3,k) (k = 3). The reasoning is that panel reliability asks whether the three experts' average score is dependable, hence the averaged variants, whereas judge–expert comparison asks whether a single judge can reproduce the experts' ranking, hence the single-rater consistency variant ICC(3,1). The consistency form tolerates a wholesale offset between the two sets of scores, and that offset – the LLM judges' systematic overestimation – is reported separately in Section 3.5.

2.4.4 Self-preference bias

For each model M (Claude or GPT) acting as judge, self-preference bias was computed following Panickssery et al. [10]:

bias_M = mean(judge = M, generator = M) − mean(judge = M, generator = M′),

where M′ is the other model; positive values mean judge M scores its own documents higher. As a sensitivity check, we recomputed the bias using an alternative formulation (same generator, different judges), obtaining +0.464 (Claude) and −0.472 (GPT), which agree in sign and direction with the classical estimates (+0.294 and −0.301) reported in Section 3.4.

3. Results

3.1 Configuration ranking under the combined automated and GPT-judge evaluation

We ranked the nine configurations across the 405 Claude-generated documents using a composite score (Table 1). The composite combines the Tier 1 automated mean and the Tier 2b GPT-judge mean (45 documents per configuration), each min-max normalized to [0, 1] across the nine configurations and then averaged with equal weight. Claude-judge scores are not included in this composite. H4_sop_only achieved the highest composite score and has relatively small archived configuration files (mean 2,373 tokens), compared with the template-based configurations and C_full; as Section 3.5 shows, however, this ranking does not survive expert evaluation.

Table 1. Composite ranking of the nine configurations (automated/GPT composite).

| Configuration | Archived size (tokens) | Composite score |
| --- | --- | --- |
| H4_sop_only | 2,373 | 0.994 |
| H3_skeleton | 5,375 | 0.869 |
| G_template_rules | 24,235 | 0.851 |
| H2_keep_examples | 25,052 | 0.759 |
| E_rules_v2 | 1,236 | 0.729 |
| C_full | 56,151 | 0.493 |
| F_template | 23,090 | 0.345 |
| B_simple | 348 | 0.227 |
| A_bare | 0 | 0.000 |

Archived configuration-text size is the mean across 15 task-specific files for F/G/H2/H3/H4 and the fixed-file count for A/B/E/C (Section 2.1); it is not a verified per-call input count.

3.2 Four-component substitution-contrast ablation

The ablation effects of the four components are summarized in Table 2.

Table 2. Ablation effects of the four prompt components (Tier 2b GPT-judge ratings; the two configurations in each contrast are given in Section 2.4.2).

| Component | Δ (all tasks) | 95% CI | BH-adjusted p | Δ_A Authoring | Δ_B Operation | Δ_C Audit |
| --- | --- | --- | --- | --- | --- | --- |
| rules | +0.511 | (+0.28, +0.75) | <0.001 | +0.507 | +0.613 | +0.413 |
| document skeleton | +0.213 | (+0.05, +0.38) | 0.11 | +0.347 | +0.187 | +0.107 |
| detailed content | −0.031 | (−0.19, +0.12) | 0.79 | +0.107 | +0.053 | −0.253 |
| worked examples | −0.053 | (−0.21, +0.11) | 0.61 | −0.080 | −0.173 | +0.093 |

The three right-hand columns give Δ stratified by task class (n = 15 per cell: 5 tasks × 3 replicates). These stratified Δ values, and the by-dimension Δ decomposition in Section 3.2, are descriptive point estimates without CIs or significance tests; CIs and adjusted p-values for the main effects are given in the left-hand columns.

Only rules remained significant after multiplicity correction [BH-adjusted p < 0.001]. The document-skeleton effect was directionally positive with a bootstrap CI excluding zero, but the rank-based test was not significant [BH-adjusted p = 0.11], so we treat it as suggestive only; neither detailed content nor worked examples had a detectable effect. A supplementary contrast showed that H4_sop_only (a single SOP skeleton) and H3_skeleton (the full module skeleton) performed comparably [Δ = −0.009]. Stratified by task class (Table 2, right-hand columns), the rules effect was consistent in direction and magnitude across all three classes (+0.41 to +0.61) and did not reverse, whereas the other components fluctuated and were far smaller.

Decomposed by scoring dimension (GPT judge; n = 45 per configuration), the rules effect was largest for operability (+0.867) and professional depth (+0.644), and smaller for clause coverage (+0.400), PDCA closure (+0.333), and internal consistency (+0.311). The two largest gains thus fall on operability and professional depth rather than on the format- and structure-oriented dimensions, indicating that a rules constraint does not merely regularize a document's outward form but also increases the laboratory-specific technical detail written into it. This decomposition is by scoring dimension, not by document type: "professional depth" is only a proxy for technical specificity (Supplementary Table S2), and a genuine stratification by document type cannot be performed here because the task set contains no technical documents (Section 4.6). These results apply only to the LLM-judge tier; the expert-tier comparisons appear in Section 3.5.

3.3 2 × 2 symmetric cross-model validation

Figure 2 summarizes the archived 2 × 2 generator–judge means for the intended cross-model subset of tasks A1, B1, and C1. GPT-judge means can be reconstructed from nine documents per configuration and generator (three tasks × three replicates). Some Claude-judge cells are supported only by retained aggregate records, so their underlying document counts cannot all be independently verified (Section 4.6). C_full has an archived configuration size of 56,151 tokens: its GPT-generated outputs scored 1.40 with the Claude judge and 1.84 with the GPT judge, compared with 3.22–4.56 for Claude-generated outputs. This is a descriptive model- and runtime-dependent contrast, not evidence that this configuration is generally suitable for one model family and unsuitable for another.

We inspected the GPT-generated C_full outputs document by document and found three recurrent problems: (i) declining instruction-following – constraints stated at the start of the system prompt were no longer applied in the later part of the output; (ii) structural breakdown – disordered sections, missing required headings, or numbering errors; and (iii) clause-citation confusion – incorrect, mismatched, or even fabricated ISO 15189:2022 clause identifiers. None of these problems appeared in the corresponding Claude outputs.

3.4 Apparent self-preference of LLM judges

The self-preference biases (Section 2.4.4) had opposite signs but pointed to the same thing: across all nine configurations the Claude judge scored +0.294 and the GPT judge −0.301, meaning both judges rated Claude-generated documents about 0.3 points higher. Excluding C_full, both biases collapsed toward zero (Claude −0.064; GPT −0.167), so the gap is driven mainly by C_full – the configuration where GPT broke down under long context (Section 3.3).

This opposite-signed pattern does not match classical self-preference, which would produce positive biases for both judges. Two non-exclusive explanations are compatible with it: (a) a genuine generation-quality difference between Claude and GPT (consistent with GPT's C_full breakdown); and (b) a shared preference of both judges for Claude's phrasing or formatting. Because the expert sample (n = 10) was entirely Claude-generated, this study cannot distinguish the two (Section 4.6).

As a descriptive sensitivity analysis, we re-ranked configurations using only cross-model group means (each judge scoring the other model's documents). The top four (G_template_rules, H3_skeleton, E_rules_v2, H4_sop_only) lay within 0.11 points, whereas C_full ranked ninth (last), compared with sixth in Table 1. This comparison uses different evaluation summaries and does not establish that bias has been removed. Because some Claude-judge cells are available only as means, no document-level significance test is claimed for this re-ranking.

3.5 Expert-tier validation

Inter-rater agreement among the three experts was excellent: ICC(2,k) = 0.982 [95% CI (0.95, 1.00)], with all pairwise comparisons above 0.92 ("excellent" by the Cicchetti benchmark [12]). The five-dimensional rubric was therefore highly reproducible across raters, although all three came from the same institution, so this agreement may exceed what holds across institutions (Section 4.6).

Agreement between the experts and the two LLM judges was markedly lower (Figure 3): ICC(3,1) = 0.548 [95% CI (−0.08, 0.86), p = 0.04] for the Claude judge and only 0.217 [95% CI (−0.44, 0.72), p = 0.26] for the GPT judge. Both intervals cross zero and n is only 10, so these two agreement coefficients can serve only as directional indications and do not support firm statistical conclusions. Both judges also systematically scored compliance higher than the experts – by 0.905 points (Claude) and 0.525 points (GPT). Claude–expert agreement was therefore moderate, and GPT–expert agreement poor.

The ranking of the seven configurations is given in Table 3, and is almost the reverse of the automated/GPT composite ranking (Figure 4b).

Table 3. Scores for the seven sampled configurations (0–5 scale; sorted by expert mean; 1–2 documents per configuration).

| Configuration | Expert mean | Claude judge | GPT judge | n |
| --- | --- | --- | --- | --- |
| F_template | 4.24 | 4.60 | 4.00 | 1 |
| H2_keep_examples | 4.07 | 4.40 | 4.00 | 1 |
| G_template_rules | 4.06 | 4.80 | 4.50 | 2 |
| C_full | 3.45 | 4.90 | 4.00 | 2 |
| H4_sop_only | 3.20 | 4.30 | 4.20 | 2 |
| E_rules_v2 | 3.19 | 4.00 | 4.00 | 1 |
| A_bare | 3.04 | 4.00 | 3.80 | 1 |

The top three are all template-anchored (F_template, H2_keep_examples, G_template_rules; expert means 4.06–4.24), whereas H4_sop_only – ranked first by the automated/GPT composite – fell to fifth, only 0.16 points above the no-prompt baseline A_bare. The most overestimated were C_full and H4_sop_only (about 1 point above the experts): both comply in structure and terminology but lack the clinically grounded operational detail that only experts detect. The favorable automated/GPT composite ranking of skeleton configurations is therefore not borne out under expert evaluation. With only 1–2 documents per configuration, this ranking is preliminary.

3.6 Archived configuration size and compliance scores across evaluation tiers

Figure 4a plots the mean scores of all three evaluators (experts, Claude judge, GPT judge) for the same n = 10 expert-reviewed documents against the archived configuration-text sizes defined in Section 2.1. The horizontal positions for task-specific configurations use the 15-file means, not reconstructed inputs for those 10 historical Claude calls. Both LLM judges scored the smaller configurations and C_full highly, whereas the expert panel scored the template-anchored F_template, G_template_rules, and H2_keep_examples configurations highest. Their archived mean sizes are approximately 23,000–25,000 tokens.

The expert–judge divergence is descriptive: the gaps are larger for A_bare, E_rules_v2, H4_sop_only, and C_full than for F_template, G_template_rules, and H2_keep_examples. No non-linearity test was performed, and the archived size axis cannot establish a causal token–quality relationship. The observed differences concern evaluation endpoints and configuration families, not a validated token-efficiency optimum.

For research question (ii), the retained rules file is small (1,236 tokens) and its addition improved GPT-judge scores in the specified contrast (Section 3.2). Template-anchored configurations obtained higher expert means in the small reviewed subset. However, content composition and text quantity were not independently manipulated, complete Claude input logs are unavailable, and expert samples contain only one or two documents per configuration. The study therefore does not establish a minimum token requirement or a per-token return; the practical comparison remains qualitative.

4. Discussion

This study evaluated LLM-assisted drafting of ISO 15189 quality management system documentation across nine prompt configurations, two generation models, two LLM judges, and a small blinded expert-reviewed subset. The main finding is that the best-performing prompt configuration depended on the evaluation tier. Minimal rule- or skeleton-based prompts were favored by automated and LLM-based scoring, whereas template-anchored prompts achieved higher mean scores in the expert-reviewed subset. In addition, the full-context configuration showed marked model- and runtime-dependent instability, and both LLM judges systematically overestimated expert ratings. Together, these findings suggest that LLMs can support drafting and preliminary screening of QMS documentation, but cannot replace expert review or local validation by competent laboratory personnel.

4.1 Prompt minimization holds at the LLM-judge tier but not at the expert tier

At the LLM-judge tier, the four-component ablation gives a clear account: adding the rules component improved scores in the specified contrast [BH-adjusted p < 0.001], the document-skeleton component was directionally positive but not significant [p = 0.11], and neither detailed content nor worked examples produced a detectable improvement (Section 3.2). This aligns with the lost-in-the-middle phenomenon reported by Liu et al. [13] (adding too much context to a long prompt can dilute model attention and degrade output quality) and with the prompt-engineering literature more broadly [6].

The expert-tier results qualify this account (Section 3.5). The template-anchored F_template and G_template_rules earned markedly higher expert scores, whereas the skeleton-only H4_sop_only was about one point lower (per-configuration samples are very small and these are exploratory observations). A plausible explanation is that the model's own knowledge does not reliably cover the clinical-practice details required by ISO 15189:2022 and CNAS-CL02:2023 – in our task set, emergency-sample handling, acceptance of patient-self-collected specimens, qualification requirements for sample-courier personnel, and detailed sample-rejection criteria. When these are not stated explicitly in the system prompt, the model tends to fall back on generic procedural language: such language meets structural and terminological compliance (the two dimensions most readily detected by automated and LLM-based scoring, Section 3.6) but lacks the practical operability required of documents intended for accreditation submission. These exploratory observations favor considering template-anchored prompts when expert-reviewed drafts are needed; they do not establish a required prompt configuration or token threshold for accreditation submission.

4.2 The full-context trap is model-dependent

Although template-anchored configurations improve expert scores (Section 4.1), simply lengthening the prompt can be counterproductive when a model lacks stable long-context handling. C_full (archived configuration text: ~56,000 tokens) appears to be the safest choice – it includes all potentially relevant material and matches the intuition that "more context is more reliable." But our data show this intuition did not hold across the two models: for outputs labeled C_full, Claude scored 3.22–4.56 on average whereas GPT-5.4 scored only 1.40–1.84, accompanied by the three failure modes recorded in Section 3.3 (declining instruction-following, structural breakdown, and clause-citation confusion). Long-context degradation is one possible explanation [3, 4, 13], but exact historical input equivalence is unverified and attention was not measured; input and runtime differences cannot be excluded.

This carries a methodological implication: any claim that "configuration X works" must be validated across multiple generation models. Evaluating on a single model conflates the effect of the configuration itself with the model's intrinsic properties (long-context capacity, instruction-following stability, and how well its training data matches the target regulatory domain), and cannot be generalized to other models. We therefore recommend validating any long-context QMS prompt (e.g., approaching or exceeding ~50,000 tokens) on the specific model and version before deployment. This is because long-context behavior can vary substantially, both between models and between adjacent versions of the same model.

4.3 Bias profile and appropriate use of LLM-as-judge

This study quantified two distinct rating biases. The first is a cross-judge directional bias: both judges rated Claude-generated documents about 0.3 points higher, driven mainly by C_full (Section 3.4). As noted above, this does not match classical self-preference and more likely reflects either a genuine quality difference between the two models or a shared preference for Claude's writing style. The second is a systematic LLM–expert offset: both judges overestimated expert-determined compliance by 0.52–0.90 points (Section 3.5).

The practical guidance from these two biases is as follows. The Claude judge's moderate agreement with the expert ranking [ICC(3,1) = 0.548] suggests it could serve as a first-pass filter in large-scale generation, screening out clearly low-quality outputs before expert review; however, the 95% CI of this coefficient crosses zero (n = 10; see Section 3.5), so this use requires confirmation in a larger sample. The GPT judge's poorer and non-significant agreement [ICC(3,1) = 0.217, p = 0.26] makes it unsuitable as a substitute for expert scoring. For documents intended for accreditation submission, formal QMS adoption, or operational use, expert final review remains indispensable. The configuration-level implications of these biases are summarized in Section 4.4 (Table 4).

4.4 Provisional configuration guidance by use scenario

Synthesizing the three tiers, Table 4 summarizes provisional configuration guidance. Smaller rule- and skeleton-based configurations performed favorably on the automated/GPT composite, whereas template-anchored configurations received the highest expert means in the reviewed subset. The token column describes archived configuration files rather than verified historical request sizes or a validated minimum input requirement.

Table 4. Provisional configuration guidance by use scenario.

| Use scenario | Provisional configuration | Archived tokens | Rationale | Trade-off |
| --- | --- | --- | --- | --- |
| Rapid first-draft generation; internal iteration | H4_sop_only or E_rules_v2 | 1,236–2,373 | Favorable automated/GPT composite ranking | Requires manual supplementation of clinical detail |
| Batch drafting of multiple SOPs | H4_sop_only or H3_skeleton | 2,373–5,375 | Task-specific skeleton + rules | Requires manual supplementation of clinical detail |
| Formal documents for CNAS submission | G_template_rules | 24,235 | Top-three expert mean in the small reviewed subset | Larger archived configuration; input equivalence unverified |
| Complete quality manual | F_template or G_template_rules | 23,090–24,235 | Highest expert scores | Larger archived configuration; input equivalence unverified |
| Use with caution under the tested settings | C_full | 56,151 | Low scores for GPT-generated outputs; last by cross-model group means | — |
| Not recommended | A_bare, B_simple | 0–348 | Insufficient prompt constraint; below the practical compliance baseline | — |

A practical workflow emerging from these data is to: (i) generate a rapid first draft with H4_sop_only; (ii) supplement the practical clinical detail through manual review or targeted re-prompting; and (iii) regenerate or refine the final document for accreditation submission using G_template_rules. It should be emphasized that every configuration in Table 4 produces only a reference draft: all require revision by laboratory staff and final expert review before use for accreditation, and the configurations differ only in the completeness of that draft, not in whether expert review is needed. The amount of manual rework each configuration requires was not quantified in this study and is a direction for future work.

4.5 LLM assistance within the personnel-competence requirements of ISO 15189

The drafting of QMS documents is not merely a clerical output; it is also the process through which laboratory staff build their sense of responsibility and risk awareness. If this work is delegated entirely to an LLM, staff gradually lose writing practice and struggle to develop a deep understanding of the ISO 15189 process as a whole. We therefore regard human supervision as a constraint on the use of LLMs in this setting. ISO 15189:2022 requires competent personnel and a complete examination process, not merely well-formatted documents, and our data show how far LLM output stands from that requirement: the LLM judges overestimated expert-determined compliance by 0.52–0.90 points. This position aligns with the emerging consensus that, in healthcare quality management, LLMs should be confined to clerical tasks grounded in historical data and performed under mandatory human verification, with autonomous operation regarded as premature [14]. We therefore position LLM assistance as an efficiency tool: the final authoring, review, and approval remain the responsibility of qualified personnel, while the time it saves at the drafting stage can be redirected toward the higher-order review, validation, and continual-improvement activities that ISO 15189 prioritizes.

4.6 Limitations

This study has several limitations. First, the expert-reviewed subset was small: three internal auditors evaluated only 10 documents, with one or two documents per configuration. All expert-reviewed documents were Claude-generated Class A procedure documents, and no GPT-generated, Class B, or Class C documents were included. The expert-tier findings therefore provide exploratory calibration rather than statistically stable configuration rankings.

Second, all three expert raters came from the same institution, and all three are authors of this paper. Although blinding and independent scoring were used, the high inter-rater agreement may overestimate reproducibility across institutions.

Third, the cross-model comparison was limited. GPT-5.4 generation covered only three tasks, and the two models were accessed through different runtime environments with non-identical generation and judging parameters. The observed full-context degradation should therefore be interpreted as model- and runtime-dependent rather than as a general property of either model family. In addition, both fixed and task-specific F/G configuration files were retained, but complete Claude per-call input logs were not archived. Exact input equivalence across the two models cannot be verified, and archived configuration sizes must not be interpreted as measured Claude input usage or causal token thresholds.

Fourth, only 273 Claude-judge document-level records can be reconstructed, comprising 270 core and three supplemental evaluations; additional historical batches survive as aggregate means. Earlier coverage totals are not counts of fully retained individual records. For the aggregate-only cells, neither individual scores nor all denominators can be independently verified. The cross-model means and bias decomposition are therefore descriptive, while the expert comparison and GPT-based component contrasts use recoverable individual records.

Fifth, the task set focused on system-level QMS documents and did not include technically demanding documents such as method validation or verification reports, measurement-uncertainty procedures, biological reference interval verification, or critical-value reporting. Generalization to such documents requires separate validation. All documents were also generated and evaluated in Chinese; the configuration effects and bias patterns reported here therefore remain unverified in English or other languages.

Finally, the evaluation rubric did not directly assess patient-safety risk, local implementability by bench-level staff, or the risk of fabricated laboratory-specific parameters. Future work should use larger multi-center expert panels, include matched GPT-generated samples, cover technical and post-examination documents, harmonize model parameters, and assess revision burden and patient-safety implications.

5. Conclusions

The optimal prompt configuration for LLM-assisted ISO 15189 QMS document generation varies with the evaluation tier: H4_sop_only, favored by the automated/GPT composite, fell to fifth under expert review, whereas the template-anchored F_template, H2_keep_examples, and G_template_rules ranked highest (Table 3). Either way, the output is only a reference draft and cannot be submitted directly. Minimal prompts may give a quick-start outline; template-anchored configurations give a working draft closer to submission form, whose value lies in a reliable document skeleton – the content that actually determines accreditation readiness (the laboratory's own quality-control data, patient data distributions, and proficiency-testing history) must be entered and interpreted by competent personnel, because an LLM does not hold these data. Nor is more context safer: C_full (archived configuration text: ~56,000 tokens), which loads the full reference corpus, should instead be used with caution, particularly when generation is performed by GPT-5.4 (its failure modes were observed only at the automated and LLM-judge tiers). Evaluation, too, cannot be delegated: LLM-as-judge is suitable only for pre-screening large numbers of drafts before expert review – the Claude judge is tentatively adequate for this role [ICC(3,1) = 0.548, 95% CI crossing zero, n = 10], whereas the GPT-5.4 judge is not [ICC(3,1) = 0.217]. Ultimately, ISO 15189 documentation is the process by which laboratory staff learn processes and risks, take responsibility, and demonstrate competence; an LLM can take over only its routine textual work – expert final review remains indispensable.

Declarations

Research funding: The study received no external research funding.

Author contributions: Sidi Liu was responsible for the conceptualization and design of the study, the conduct of all experiments, the data analysis, and the drafting and revision of the manuscript. Dongdong Li was responsible for study supervision and critical revision of the manuscript and, as the corresponding author, takes responsibility for the content of the article. Lan Yang and Xinying Chen served as independent raters in the blinded expert review (Raters 2 and 3, respectively). Dan Wu assisted with data curation. All authors have read and approved the final manuscript.

Competing interests: The authors declare no competing interests. None of the three expert raters had any commercial, research, or consulting relationship with Anthropic, OpenAI, or other LLM providers, and none received funding or in-kind support from these entities.

Informed consent: This study involved no patients or human subjects. Written informed consent was obtained from Raters 2 and 3 (Lan Yang and Xinying Chen, now co-authors) prior to their participation in the blinded expert review. The consent form described the study purpose, the intended use of the ratings, the data-handling and de-identification procedures, and the right to withdraw at any time.

Ethical approval: This study did not require formal ethical approval, because it did not involve patient data, biological samples, or human intervention. The QMS documents generated and evaluated used fictitious placeholder names (e.g., "Dr Li", "Dr Zhang") and contained no identifiable personal information. The inter-rater dataset was collected as methodological research from informed-consent volunteers; rater-level identifying data are stored under coded labels (Rater 1 / Rater 2 / Rater 3) in the released dataset.

Data availability: The public repository (https://github.com/stttttte/iso15189-llm-config-experiment) contains 486 generated documents, 486 GPT-judge document-level evaluations, 273 Claude-judge document-level evaluations, additional retained Claude group means, and 30 blinded expert ratings. Code is licensed under MIT and data under CC BY 4.0. The existing v1.1.0 archive is available on Zenodo (DOI: 10.5281/zenodo.21769007; https://doi.org/10.5281/zenodo.21769007). Complete document-level records for the aggregate-only Claude batches and complete historical Claude input logs are not available. The existing archive predates the present reporting and reproducibility corrections.

Acknowledgments

Acknowledgment of AI tool use. The authors disclose the following use of generative artificial intelligence (AI) tools in this work.

(1) AI as research objects. Claude Opus 4.6 (Anthropic, San Francisco, CA, USA) and GPT-5.4 (OpenAI, San Francisco, CA, USA, accessed via the AIHubMix API proxy) were used to generate the 486 ISO 15189:2022 QMS documents that constitute the primary dataset of this study; these documents are the experimental objects under investigation, are not fabricated clinical data, and were not used in real patient care.

(2) AI as evaluators. The same two models served as LLM judges. Available document-level records comprise 486 GPT-judge and 273 Claude-judge evaluations; additional Claude results were retained only as group means (Sections 2.3.2 and 4.6). The repository provides the retained prompts, parameter descriptions, score files, and aggregate summaries. These materials do not constitute complete per-call logs for every historical Claude evaluation.

(3) AI-assisted manuscript drafting. The first author used Claude Code (Claude Opus 4.6, Anthropic) to assist with manuscript outlining, generation of initial draft material, table preparation, and data-visualization code generation. The initial draft material was subsequently substantially rewritten by the authors. All AI-suggested content, wording, and analytical code were critically reviewed, revised, and verified by the authors, who take full responsibility for the final manuscript, including all claims, interpretations, and conclusions.

(4) No AI-generated images or manipulated data. Figures 1–4 were plotted with Python and matplotlib from retained numerical records and recounted configuration-text sizes. No image-generation models were used, and generative AI was not used to modify the numerical data.

(5) Accountability. The authors accept full responsibility for all content of this submission, in accordance with the ICMJE authorship criteria.

Figure Legends

Figure 1. The nine prompt configurations evaluated in the study.

For each configuration (rows, ordered by archived configuration size), the four left columns show whether each prompt component is included (✓, dark), partially included (◑, light), or absent (—, pale); the right column shows archived configuration-text size in thousands of cl100k_base tokens: the mean across 15 task-specific files for F/G/H2/H3/H4 and the fixed-file count for A/B/E/C (Section 2.1). The two encodings are not proportional: the component marks index the presence of distilled, structured prompt content, whereas bar length describes the retained configuration text, not verified historical per-call input usage. C_full reaches the largest token count by loading the full raw reference corpus (the complete ISO 15189 and CNAS standard texts plus an existing document library), yet its rules component is only partial (◑), because explicit rules are embedded within that raw text rather than supplied as a distilled rule set.

Figure 2. Cross-model validation across the four generator–judge combinations.

For each configuration (rows), the two horizontal segments span the scores assigned by the Claude judge (circles) and the GPT judge (triangles) to Claude-generated documents (blue) and GPT-generated documents (orange); scores are the archived means for the intended A1/B1/C1 cross-model subset (0–5 scale). GPT-judge values are reconstructable from individual records; some Claude-judge cells are retained only as means with unverified denominators (Section 4.6). All combinations lie in the 3.1–4.7 range except GPT-generated C_full, which collapses to 1.40 (Claude judge) and 1.84 (GPT judge), whereas the same configuration generated by Claude scores 3.22–4.56.

Figure 3. Bland–Altman analysis of agreement between each LLM judge and the expert panel (n = 10 documents).

Each point is one document; the horizontal axis shows the mean of the expert-panel and judge scores, and the vertical axis their difference (judge − expert). The solid line marks the mean bias (+0.90 for the Claude judge, panel a; +0.52 for the GPT judge, panel b) and the dashed lines the 95% limits of agreement (mean ± 1.96 SD). Points are colored by configuration family; the open circle is the no-prompt baseline. The black line at zero indicates perfect agreement; nearly all points lie above it, showing systematic overestimation by both judges.

Figure 4. Archived configuration size, quality, and ranking differences between evaluation endpoints.

(a) Mean scores for the expert panel (green squares), Claude judge (orange circles), and GPT judge (blue triangles) on the n = 10 expert-reviewed subset, plotted against archived configuration-text size (symlog scale). Task-specific configurations use their 15-file mean sizes, not reconstructed inputs to those 10 Claude calls; no optimal token interval is inferred. (b) Rankings among the seven expert-reviewed configurations, comparing the automated/GPT composite (Table 1, restricted to these seven configurations) with the expert panel (Table 3). H4_sop_only moves from first to fifth and F_template from sixth to first; the two rankings use different document sample sizes.

References

1. ISO 15189:2022. Medical laboratories — Requirements for quality and competence. Geneva: International Organization for Standardization; 2022.

2. Yang S, Zhou Y, Wang C, Luo M. The 'Double Helix' model of quality monitoring: risk mapping of quality management system during initial ISO 15189 implementation in a medical laboratory. PLoS One 2026;21:e0342129.

3. Anthropic. Claude Opus 4.6 System Card. San Francisco (CA): Anthropic; 2026. Available at: https://www.anthropic.com/claude-opus-4-6-system-card. [Accessed 9 May 2026].

4. OpenAI. GPT-5 System Card. San Francisco (CA): OpenAI; 2025. Available at: https://openai.com/index/gpt-5-system-card/. [Accessed 9 May 2026].

5. Zhao WX, Zhou K, Li J, Tang T, Wang X, Hou Y, et al. A survey of large language models. arXiv preprint 2023; arXiv:2303.18223.

6. Schulhoff S, Ilie M, Balepur N, Kahadze K, Liu A, Si C, et al. The prompt report: a systematic survey of prompting techniques. arXiv preprint 2024; arXiv:2406.06608.

7. Zheng L, Chiang WL, Sheng Y, Zhuang S, Wu Z, Zhuang Y, et al. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In: Advances in Neural Information Processing Systems 36 (NeurIPS 2023) Datasets and Benchmarks Track. 2023.

8. Tan H, Guo Z, Shi Z, Xu L, Liu Z, Feng Y, et al. ProxyQA: an alternative framework for evaluating long-form text generation with large language models. In: Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers); 2024 Aug 11–16; Bangkok, Thailand. Stroudsburg (PA): Association for Computational Linguistics; 2024. p. 6806–27.

9. Chiang WL, Zheng L, Sheng Y, Angelopoulos AN, Li T, Li D, et al. Chatbot Arena: an open platform for evaluating LLMs by human preference. arXiv preprint 2024; arXiv:2403.04132.

10. Panickssery A, Bowman SR, Feng S. LLM evaluators recognize and favor their own generations. arXiv preprint 2024; arXiv:2404.13076.

11. Shrout PE, Fleiss JL. Intraclass correlations: uses in assessing rater reliability. Psychol Bull 1979;86:420–8.

12. Cicchetti DV. Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments in psychology. Psychol Assess 1994;6:284–90.

13. Liu NF, Lin K, Hewitt J, Paranjape A, Bevilacqua M, Petroni F, et al. Lost in the middle: how language models use long contexts. Trans Assoc Comput Linguist 2024;12:157–73.

14. Knott M, Krebs M, Kerscher A. Large language models in healthcare quality management: a European perspective on process automation and compliance. Front Digit Health 2026;8:1761641.

Word count (main text, excluding title page, abstract, tables, figures, and references): approximately 5,700 words

Tables: 4

Figures: 4

References: 14

