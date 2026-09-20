20 September 2026

Dear Editor-in-Chief,

We are pleased to submit our original research manuscript entitled "Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation" for consideration for publication in Clinica Chimica Acta.

Medical laboratories seeking ISO 15189 accreditation must prepare extensive controlled quality management system (QMS) documentation. Based on the first author's laboratory quality-management experience, this can involve approximately 100–300 documents and several months of drafting. Large language models (LLMs) may assist this work, but evidence on input configuration and the reliability of LLM-based evaluation in this setting remains limited. Our study addresses both questions.

We generated 486 QMS documents across nine input configurations using Claude Opus 4.6 and GPT-5.4, and evaluated them through an automated scorer, two LLM judges, and blinded review of 10 Claude-generated documents by three qualified ISO 15189 internal auditors from the same institution. The retained evaluation materials include 759 document-level LLM-judge records and additional aggregate means. Three findings may be of practical interest to your readership:

1. The "best" configuration depends on the evaluation endpoint. H4_sop_only ranked first under the automated/GPT composite but fifth among the seven expert-reviewed configurations, whereas template-anchored configurations achieved the highest expert means. These exploratory rankings do not establish a minimum token requirement or accreditation readiness.

2. LLM judges overestimated expert-rated compliance by 0.52–0.90 points in the reviewed subset and showed model-dependent preference patterns that did not match classical self-preference. They may support preliminary screening, but cannot substitute for expert review of documents intended for accreditation.

3. More context was not consistently associated with better scores. The full-context configuration, whose archived text contains approximately 56,000 tokens, performed markedly worse with GPT-5.4 than with Claude in the three shared tasks. This finding is specific to the tested models and runtime settings and was not validated at the expert tier for GPT-generated documents.

The contribution is the comparison of two generation models and nine input configurations for long-form ISO 15189 QMS drafting, together with evaluation across automated, LLM, and exploratory expert endpoints. The findings offer provisional guidance for laboratory document development under mandatory human verification, rather than an autonomous route to accreditation-ready documents.

Study materials, including generated documents, available document-level judge ratings, retained aggregate scores, expert ratings, and analysis code, are available on GitHub (https://github.com/stttttte/iso15189-llm-config-experiment). Release v1.2.0, including the reporting and reproducibility corrections, is archived on Zenodo (DOI: 10.5281/zenodo.22855972). The manuscript explicitly distinguishes archived configuration-text sizes from unverified historical Claude input usage and describes the limitations of aggregate-only judge records.

The study involved no patient data. Written informed consent was obtained from the two participating raters other than the first author, who are co-authors. The authors declare no competing interests or relationships with LLM providers. The manuscript is original, has not been published previously, and is not under consideration by any other journal. All authors have read and approved the manuscript and its submission to Clinica Chimica Acta.

Thank you for considering our manuscript.

Sincerely,
Dongdong Li, on behalf of all authors
Department of Laboratory Medicine, West China Hospital, Sichuan University
Sichuan Clinical Research Center for Laboratory Medicine
Chengdu, Sichuan, PR China
Email: jiangxili1219@163.com
ORCID: 0000-0002-0290-6485
