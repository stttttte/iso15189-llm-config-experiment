# v1.2.0 Reporting and reproducibility corrections

Author-approved correction release dated 20 September 2026, prepared alongside the manuscript revision for Clinica Chimica Acta. This is not a journal publication or submission.

## Corrections

- Distinguish 759 recoverable document-level judge records (486 GPT and 273 Claude) from additional aggregate-only Claude results. Do not equate historical coverage totals with fully retained individual records.
- Identify the Table 1 composite as equally weighted, separately normalized automated and GPT-judge means. Its nine numerical results and ranking are unchanged.
- Recount archived configuration text with cl100k_base and distinguish task-specific files from fixed F/G references. These counts do not reconstruct historical Claude requests or establish a minimum token requirement.
- Preserve missing-record and input-equivalence limitations in the manuscript, README, and data/reproduction guides.
- Correct the skeleton-effect confidence interval upper bound from 0.39 to 0.38 using the released analysis; retain the original expert scores, main ICC estimates, and judge-expert bias results.
- Repair public ICC/ranking/figure reproduction, add the already-public blind-review mapping in machine-readable form, and add eight reproduction tests.
- Include the CCA consistency-revised manuscript, cover letter, Highlights, and four figures. Earlier CCLM/JMIR files and figures remain historical artifacts.

## Verification

Eight reproduction tests passed immediately before release. The 486 generated files, 492 score files, and 96 configuration files are byte-identical to the pre-correction repository. No missing observations were fabricated and no new model calls were performed. Original expert rating sheets are unchanged.

## Archive and citation status

The connected GitHub-to-Zenodo integration will archive this release. The version-specific DOI is not known until Zenodo processes the release. Manuscript and cover-letter archive citations in this snapshot describe the previously verified v1.1.0 archive; after the new DOI is verified, a citation-only follow-up on the main branch and local submission copies will point to this v1.2.0 archive. This publication-metadata update will not change the release's research data, analyses, or scientific results.

Historical v1.1.0 DOI: https://doi.org/10.5281/zenodo.21769007

All-version Zenodo DOI: https://doi.org/10.5281/zenodo.20091463
