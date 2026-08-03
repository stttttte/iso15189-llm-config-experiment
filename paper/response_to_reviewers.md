# Response to Reviewers — CCLM.2026.0735 (Resubmission)

> 随稿上传件（File Designation: Author's Response to Reviewer/Editor Critique，须排在上传文件第一位）。
> 引号内楷体段落均为修订稿原文，可供审稿人直接核对。

---

## Response to Reviewers

**Manuscript CCLM.2026.0735 – resubmission**

**Evaluating LLM-Assisted Drafting of ISO 15189 Quality Management Documents: Prompt Configuration, LLM-as-Judge Bias, and Exploratory Expert Validation**

We thank both reviewers for their careful reading and constructive criticism. The manuscript has been revised extensively in response. Because the revision touches nearly every part of the paper – a new title, a condensed and restructured text (main text shortened by approximately 27%, from about 7,500 to about 5,500 words), a compressed abstract, four redesigned figures, a rewritten Limitations section, and corrected methodological reporting – a change-highlighted copy would mark almost the entire document; we therefore provide the detailed point-by-point mapping below and can supply a highlighted copy on request.

Two changes of record accompany the revision. First, the title has been changed to reflect the study's actual scope. Second, the author list has been expanded from one to five: Lan Yang and Xinying Chen (Raters 2 and 3 of the blinded expert panel) and Dan Wu (data curation) have been added as co-authors, and Dongdong Li joins as supervising and corresponding author; individual roles are specified in the Author Contributions statement, and all authors have read and approved the resubmitted manuscript.

---

### Reviewer 1

**Comment (summarized).** ISO 15189 documentation is not a bureaucratic exercise but tangible evidence that the laboratory operates in a controlled, competent, and verifiable manner. Drafting procedures is an integral part of staff training, responsibility and accountability, competence development, and risk awareness. If AI replaces personnel in this task, the laboratory loses active participation, process understanding, and quality culture; ISO 15189 requires competent professionals, not merely well-written documents. Proposing such tools for drafting procedures would ultimately reduce the value of accreditation itself.

**Response.** We agree with every element of this assessment, and we have revised the manuscript so that this position is now explicit and structural rather than incidental. We would also note that our findings speak directly to this concern: they quantify how far polished-looking LLM output stands from genuine compliance, and show that only expert review detects the gap.

Specifically:

1. **Human supervision is now framed as a binding constraint, in the reviewer's own terms (Section 4.5).** The revised manuscript states: *"The drafting of QMS documents is not merely a clerical output; it is also the process through which laboratory staff build their sense of responsibility and risk awareness. If this work is delegated entirely to an LLM, staff gradually lose writing practice and struggle to develop a deep understanding of the ISO 15189 process as a whole. We therefore regard human supervision as a constraint on the use of LLMs in this setting. ISO 15189:2022 requires competent personnel and a complete examination process, not merely well-formatted documents."* This aligns with the published consensus that LLMs in healthcare quality management should be confined to clerical tasks under mandatory human verification (reference [14]).

2. **The Conclusions have been rewritten around this position.** They now close: *"Ultimately, ISO 15189 documentation is the process by which laboratory staff learn processes and risks, take responsibility, and demonstrate competence; an LLM can take over only its routine textual work – expert final review remains indispensable."*

3. **Every configuration is now described as producing only a reference draft.** The Conclusions state that no configuration's output can be submitted directly, and that the content that actually determines accreditation readiness – the laboratory's own quality-control data, patient data distributions, and proficiency-testing history – must be entered and interpreted by competent personnel, because an LLM does not hold these data. Section 4.4 was retitled "Provisional configuration guidance," and every scenario in Table 5 requires revision by laboratory staff and expert final review.

4. **Our data quantify the risk the reviewer describes.** Both LLM judges overestimated expert-rated compliance by 0.52–0.90 points; the configuration ranked first by LLM judges fell to fifth under expert review, only 0.16 points above the no-prompt baseline; and the documents most overestimated were precisely those that comply in structure and terminology but lack clinically grounded operational detail (Section 3.5). We do not propose replacing personnel; the study's purpose is to locate the boundary of safe use, and the data show that boundary is far more restrictive than LLM-based evaluation alone would suggest.

---

### Reviewer 2

**Comment 2.1.** The paper is overly complex and difficult to read; the text feels "inhuman" in its delivery, dense and flat, with interpretive sentences scattered among technical details. Shorten the text to focus on essentials and emphasize key points.

**Response.** We have condensed and rewritten the text throughout:

- The main text was shortened by approximately 27% (from about 7,500 to about 5,500 words), with the Methods section reduced by more than 40%; implementation detail was moved to the Supplementary Material rather than deleted, and every methodological statement retained in the main text.
- The Conclusions were rewritten from 444 to approximately 220 words as a single connected argument (finding → practical implications → closing position), with interpretive topic sentences carrying the thread (e.g., *"Nor is more context safer"*; *"Evaluation, too, cannot be delegated"*).
- The Limitations section was rewritten from an enumerated list into six plain prose paragraphs.
- Redundant cross-references and parenthetical statistics were pruned; all remaining statistics follow one uniform bracket format [estimate, 95% CI (…); adjusted p].
- A small self-preference table was merged into a single sentence of text, and the per-dimension and per-task-class effect decompositions were consolidated into Table 3 rather than scattered through prose.

**Comment 2.2.** In the abstract, it is not immediately clear what C_full is; the explanation appears later in the text.

**Response.** Corrected. The abstract now glosses the configuration at first mention – *"the full-context C_full (~56,000 tokens)"* – with the full definition retained in Section 2.1.

**Comment 2.3.** References at the beginning of the Introduction are misnumbered (first reference is number 7, the second number 14).

**Response.** Corrected. The reference list was renumbered completely; the Introduction now opens with references [1] and [2], and the final list contains 14 sequentially numbered references in order of first citation.

**Comment 2.4.** Figure 1 should be clarified: C_full, despite being longer, seems to contain less material.

**Response.** Figure 1 was redesigned to remove exactly this ambiguity. It now shows a component-presence matrix (included ✓ / partial ◑ / absent —) alongside a separate bar encoding of total system-prompt size, and the caption states explicitly that the two encodings are not proportional: the component marks index the presence of distilled, structured prompt content, whereas bar length reflects the total volume of loaded text. C_full reaches the largest token count by loading the full raw reference corpus, yet its rules mark is only partial, because explicit rules are embedded in that raw text rather than supplied as a distilled rule set.

**Comment 2.5.** Figure 3 has 7 colors in the legend, 9 dots in the left panel, 10 dots in the right panel; some colors are duplicated and some are missing.

**Response.** The original scatter plot has been replaced by a Bland–Altman agreement analysis (new Figure 3). Each panel now shows exactly the n = 10 expert-reviewed documents, colored by a consistent four-category configuration-family scheme (with an open circle for the no-prompt baseline) that matches the legend exactly. All four figures were redesigned with a single colorblind-safe palette applied consistently across the manuscript.

**Comment 2.6.** Avoid deep vertical technical detail unless functional; gather numerical data into tables rather than scattering them in parentheses.

**Response.** Done as part of the condensation described under 2.1: stratified and per-dimension effect estimates now sit in Table 3; document counts, parameters, and rating tallies are stated once in Methods rather than repeated; and parenthetical numbers in the Discussion were removed except where a specific claim depends on them.

---

### Additional changes made during revision

- Methodological reporting was corrected against the released code: the generation and judging parameters of both models are now stated exactly (Section 2.2 and Section 2.3.2), the Claude-judge coverage (378 document-level ratings, 77.8%) is explained (batch execution; some batches retained only group-level means), the non-independence of replicates sharing tasks is acknowledged in Section 2.4.1, and the provenance of the automated-scorer weights is stated in Section 2.3.1.
- An "Acknowledgment of AI tool use" section (De Gruyter Brill AI Policy for Authors) is embedded in the manuscript, covering AI as research objects, AI as evaluators, AI-assisted drafting, figure integrity, and accountability.
- The public repository and archive were updated to match the resubmission (GitHub, Zenodo v1.1.0; the manuscript now cites the version-independent concept DOI 10.5281/zenodo.20091463).

We thank the reviewers again; the manuscript is substantially clearer and more honest about its limits as a result of their comments.
