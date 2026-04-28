# LLM 在不同配置下生成医学实验室 QMS 文件的合规性研究

**作者**：刘斯迪（Sidi Liu）¹

**单位**：¹ 四川大学华西厦门医院检验科，福建厦门 361024，中国

**通讯作者**：刘斯迪，lllsssddd@icloud.com，ORCID: 0009-0006-1695-5372

**Short title**：LLM configuration for ISO 15189 document compliance

**关键词**：ISO 15189；医学实验室；质量管理体系；大语言模型；prompt engineering；LLM-as-Judge；专家验证

---

## 摘要

**Objectives**：本研究旨在系统比较不同配置策略下大语言模型（large language model, LLM）生成 ISO 15189:2022 医学实验室质量管理体系（quality management system, QMS）文件的合规性，识别最优配置区间，并通过多层次评估揭示现有评估方法的系统性偏差。

**Methods**：采用非对称双模型设计，共生成 486 份 QMS 文件：Claude Opus 4.6 × 9 组配置 × 15 任务 × 3 重复（405 份）；GPT-5.4 × 9 组 × 3 任务（A1/B1/C1）× 3 重复（81 份，用于跨模型验证）。9 组配置按规则、骨架、详细内容、示例 4 个维度正交组合，token 规模从 0 覆盖至 71 K。评估采用三层框架：(1) Python 自动合规评分器；(2) Claude 与 GPT-5.4 双 LLM 评审（共 864 次评分，含 2×2 对称跨模型验证）；(3) 3 位 ISO 15189 资格专家对 10 份分层随机抽样的盲化文件独立评分。一致性采用 Pearson 相关系数、Spearman 相关系数以及组内相关系数 [ICC(2,1) 与 ICC(3,1)] 评价。

**Results**：(1) 四因子正交消融显示，规则层（Δ=+0.511，p<0.001）与骨架层（Δ=+0.213，p=0.055）在 LLM 评估层显著有效；详细内容（Δ=−0.031，p=0.79）与示例（Δ=−0.053，p=0.46）无贡献或轻微有害。(2) 全量配置 C_full（71 K）在 Claude 生成下的跨评分为 3.22–4.56，在 GPT-5.4 生成下降至 1.40–1.84，提示 Claude Opus 的长上下文能力在此场景中具有模型特异性。(3) Claude 评审存在 +0.464 的自评偏差，GPT 评审呈 −0.472 的反向偏差。(4) 3 位专家之间 ICC(2,k)=0.982，而专家均值与 Claude 评审的 ICC(3,1)=0.548（p=0.04）、与 GPT 评审的 ICC(3,1)=0.217（p=0.26）；两种 LLM 评审均系统性高估 0.52–0.90 分。(5) LLM 评估层的最优配置 H4_sop_only（6 K 骨架）在专家视角下排名倒数第二（3.20 分，n=2），而模板类配置 F_template（35 K）与 G_template_rules（38 K）在专家视角下最优（4.06–4.24 分）。

**Conclusions**：LLM 辅助 QMS 文件生成的"最优配置"取决于评估视角。追求 token 效率与成本控制的场景建议采用 H4_sop_only（6 K）或 E_rules（3 K）；正式送审与 CNAS 认可申请场景建议采用 G_template_rules（38 K）或 F_template（35 K）。C_full（71 K）在现阶段 GPT 类模型长上下文能力不稳定的情况下应避免使用。LLM 评审可作为初筛工具，但不可替代专家终审；Claude 评审与专家排序呈中等一致性，可作为粗筛代理，GPT 评审则不适合此用途。

---

## 1. Introduction

ISO 15189:2022《医学实验室——质量和能力的要求》作为医学实验室认证的国际标准，在国内的认可度日益提升，CNAS-CL02:2023 作为中国合格评定国家认可委员会对应的实施文本同步推出。该类标准明确规定实验室"应做什么"但不规定"如何做"，因此实验室须自行构建覆盖质量手册、程序文件与作业指导书的完整文件体系。此类体系在典型三级甲等医院检验科中通常包含 100 至 300 份受控文件，涉及结构组织、条款映射、表单编号与职责分配的系统工程，依靠质量小组手工编写需时数月，且体系建立后仍需经过多轮内审方可定型。寻求 CNAS 认可的实验室通常需要技术专家与培训师协助方能完成此过程。

大语言模型（LLM）的发展为这一过程提供了自动化的可能性。Claude Opus 4.6 与 GPT-5.4 等新一代模型在长文档生成、结构化输出和专业术语使用方面已接近专业人员的水平 [1,2]。然而，一个尚未被系统研究的问题是：应当向 LLM 提供何种 system prompt，才能使其产出合规且可用的 QMS 文件。实践中存在两种极端策略：其一为"全量假设"，即将所有相关资料（ISO 原文、CNAS 准则、既有文件库、示例）一并载入 system prompt，token 数通常达 50–100 K 级别；其二为"极简假设"，即仅提供规则约束与章节骨架，依赖模型内化知识生成内容，token 数仅数千。两种假设的实证证据均有限，因为现有 LLM 配置研究 [3,4] 多关注通用任务的 prompt engineering，缺乏针对 QMS 这类专业文档场景的系统比较。

评估方法的偏差是另一个深层问题。目前 LLM 生成质量的评估多依赖 LLM-as-Judge 方法（即使用另一 LLM 作为评分者）[5]。已有研究发现 LLM 评审存在 self-preference bias（偏爱自家模型生成的文本）[6]，但这种偏差在专业领域（如医学实验室 QMS）中的具体表现及其对配置比较结论的影响尚缺乏实证数据。

基于上述背景，本研究拟通过 486 份生成文件、864 次 LLM 评审评分与 30 次专家盲评评分，回答以下研究问题：(i) 配置文件中的哪些成分（规则、骨架、详细内容、示例）对 LLM 生成 QMS 文件的质量有贡献；(ii) 最精简的有效配置所需 token 数；(iii) 跨生成模型（Claude 与 GPT）下最优配置是否一致；(iv) LLM 评审的自评偏差规模；(v) 在多层次评估（自动评分、LLM 评审、专家评分）交叉对比下，哪种配置最稳健。

---

## 2. Materials and methods

### 2.1 配置组设计

依据规则、骨架、详细内容、示例 4 个维度进行正交组合，设计 9 组对照配置（Figure 1）。其中 A_bare（0 K）与 B_simple（0.4 K）为基线；C_full（71 K）代表全量输入策略；E_rules（3.1 K）仅含规则层；F_template（35 K）为无规则的完整模板；G_template_rules（38 K）为规则与模板的组合；H2_keep_examples（61 K）在 G 基础上额外保留示例；H3_skeleton（13 K）保留模块骨架但删除详细内容；H4_sop_only（6 K）仅保留任务最相关的单个 SOP 骨架。

![Figure 1](figures/fig1_config_composition.png)

**Figure 1.** 用于 LLM 辅助 ISO 15189 QMS 文件生成的 9 组配置。左：各配置在规则、骨架、详细内容、示例 4 个维度的纳入情况（✓ 完整、半圆 部分、— 缺失）；右：各配置的 system-prompt 大小（千 token）。

规则层基于 rules.md（3.1 K），经领域专家校验修正：删除 3 条错误术语映射（仪器→设备、校准品→校准物、室间质评→能力验证），修正 3 条目标术语（标本→样品、检验项目→检测项目、线性范围→可报告范围），保留 10 条正确映射与 7 类模糊表述禁令。骨架层由 strip_to_skeleton 算法从模板库中提取，保留章节标题、各章节首段说明与表单编号列表，删除条款原文摘录、详细表格内容、示例、详细步骤列表与代码块。

### 2.2 生成模型与任务

主实验采用 Claude Opus 4.6（Anthropic）× 9 组配置 × 15 任务 × 3 重复，共生成 405 份文件。15 项任务按 CNAS 评审场景分为 A 类（文件编写，例如人员培训与能力评估控制程序）、B 类（体系运行，例如年度内审检查表）与 C 类（审核模拟，例如内部质控程序文件审查报告），每类 5 项。跨模型验证采用 GPT-5.4（OpenAI，通过 AIHubMix 代理接入）× 9 组 × 3 任务（A1/B1/C1）× 3 重复，共生成 81 份文件。两种模型均设定 temperature=1.0，max_tokens=12 000，使用相同的 system prompt 配置。

### 2.3 三层评估框架

**层 1**：Python 自动合规评分器对全部 486 份文件评分，输出格式、条款、术语、违规和模糊 5 项指标。

**层 2a**：Claude Opus 4.6 作为评审员，以 CNAS 主任评审员视角按 5 个维度（条款满足度、可操作性、内部一致性、PDCA 闭环、专业深度）进行 0–5 分评分，共评 378 份。

**层 2b**：GPT-5.4 评审员使用相同 prompt 覆盖全部 486 份文件。层 2a 与 2b 构成 2×2 对称设计（Claude-gen × Claude-judge、Claude-gen × GPT-judge、GPT-gen × Claude-judge、GPT-gen × GPT-judge），用于正交分解自评偏差。

**层 3**：3 位 ISO 15189 资格专家对 10 份分层随机抽样的盲化文件独立评分。Rater 1 为第一作者，具有 ISO 15189 认可评审经验；Rater 2 与 Rater 3 为同单位合格 ISO 15189 内审员。抽样策略采用固定随机种子（seed=42），从 486 份文件中分层抽取 10 份，覆盖 7 个核心配置组 × A 类程序任务（A1/A2/A3），每组 1 至 2 份。随机打乱 paper_01 至 paper_10 编号并去除组名标识。三位专家独立评分，不互相查看评分或讨论；Rater 2 与 Rater 3 在不知晓 Rater 1 评分的前提下完成评分后方与之汇总。评分前获得 Rater 2 与 Rater 3 的书面知情同意。专家使用与 LLM 评审员完全相同的 5 维度评分量规。

### 2.4 统计方法

组间比较采用 Kruskal-Wallis 检验与 Mann-Whitney U 检验，多重比较采用 Bonferroni 校正。四因子效应量采用双因子方差分析。评分者间一致性采用 Pearson 相关系数、Spearman 相关系数以及 Shrout 与 Fleiss [13] 定义的 ICC(2,1)（绝对一致）与 ICC(3,1)（排序一致）评价。ICC 计算采用 pingouin 0.5 Python 库。自评偏差采用跨模型差分定量，即 bias = (own-own 均值) − (cross-own 均值)。

---

## 3. Results

### 3.1 LLM 评估层的 9 组排名

在 Claude 生成的 405 份文件中，综合三轨（自动评分、Claude 评审、GPT 评审）综合分排序为：H4_sop_only（6 K）第 1 名（0.994），H3_skeleton（13 K）第 2 名，G_template_rules（38 K）第 3 名，H2_keep_examples（61 K）第 4 名，E_rules（3.1 K）第 5 名，C_full（71 K）第 6 名，F_template（35 K）第 7 名，B_simple 第 8 名，A_bare 第 9 名。LLM 评估层下 H4 以最少 token 达到最高综合分。

### 3.2 四因子正交消融

规则层主效应为 +0.511（p<0.001），骨架层主效应为 +0.213（p=0.055），在 LLM 层均有显著或接近显著的正向贡献。详细内容无贡献（G vs H3：Δ=−0.031，p=0.79），示例呈方向性有害（H2 vs G：Δ=−0.053，p=0.46）。H4 与 H3 差异不显著（Δ=−0.009，p=0.80），提示任务特定 SOP 骨架（6 K）与完整模块骨架（13 K）效果等效。此消融结果仅在 LLM 层成立，专家层分析见 3.5 节。

### 3.3 2×2 跨模型对称验证

Figure 2 展示 2×2 对称矩阵（n=9 配置 × 4 象限）。C_full 在 GPT 生成条件下出现显著性能下降（GPT-gen × Claude-judge 平均 1.40；GPT-gen × GPT-judge 平均 1.84），而同一 C_full 在 Claude 生成条件下的跨评分为 3.22–4.56。这提示 71 K 全量配置在 Claude Opus 下仍能产出合格文件的现象具有模型特异性，并非通用结论。GPT-5.4 在 71 K 超长配置下出现指令遗忘、结构错乱与条款混搭等失败模式。

![Figure 2](figures/fig2_2x2_symmetric.png)

**Figure 2.** 2 × 2 跨模型对称评分热力图。9 个配置（行）× 4 个生成-评审组合（列）的平均得分（A1/B1/C1 均值，0–5 分）。C_full 在 GPT-生成两列出现显著塌陷（1.40 与 1.84，黑框标注），与 Claude-生成两列（4.56 与 3.22）形成强对比。

### 3.4 LLM 评审的自评偏差

依 bias = (own-own) − (cross-own) 公式计算，Claude 评审均值偏差为 +0.464（9 组中 8 组正向，C_full 最大为 +1.33），GPT 评审均值偏差为 −0.472（9 组中 8 组负向，即 GPT 偏好 Claude 生成的文本）。两者呈方向相反、幅度相当的对称偏差模式，提示该偏差系 judge 端的系统性现象，而非生成端的质量差异。骨架型配置（E、H3、H4）偏差最小（<0.15）。

规避自评偏差后（仅采用跨评均值，即 Claude-judge→GPT-gen 与 GPT-judge→Claude-gen 的均值），9 组排序为：G_template_rules 第 1 名（4.211），H3_skeleton 第 2 名（4.167），E_rules 第 3 名（4.133），H4_sop_only 第 4 名（4.100）。G、H3、E、H4 四组在去除自评偏差后统计等价（Δ<0.11）。C_full 在此排序下降至第 9 名（2.310）。

### 3.5 专家层校验

3 位专家之间的一致性极高：ICC(2,k)=0.982（95% CI [0.95, 1.00]），ICC(3,k)=0.981；两两比较的 ICC(2,1) 分别为 0.948（R1-R2）、0.928（R1-R3）、0.969（R2-R3），均达到优秀等级（>0.90）。此结果提示 5 维度评分量规设计具有高度客观性，同时亦表明同单位专家的共识可能高估了跨单位一致性（详见 5 节）。

专家均值与 Claude 评审的 ICC(3,1)=0.548（p=0.04），Pearson r=0.573，Spearman ρ=0.509，均值差为 −0.905；专家均值与 GPT 评审的 ICC(3,1)=0.217（p=0.26），Pearson r=0.259，均值差为 −0.525（Figure 3）。两种 LLM 评审均系统性高估 0.52–0.90 分；Claude 与专家的排序一致性处于中等水平，GPT 则为差。

![Figure 3](figures/fig3_expert_vs_llm.png)

**Figure 3.** LLM 评审相对 3 位专家的系统性高估（n = 10 文档 × 3 评分员）。横轴为 3 位专家均值，纵轴为 LLM 评审。左：vs Claude Opus 4.6 [ICC(3,1) = 0.548；Pearson r = 0.573；mean diff = −0.90]；右：vs GPT-5.4 [ICC(3,1) = 0.217；Pearson r = 0.259；mean diff = −0.52]。虚线为 1:1 完全一致线，配置组按颜色编码。

按配置组的专家均值排序为：F_template 4.24（n=1）第 1 名，H2_keep_examples 4.07（n=1）第 2 名，G_template_rules 4.06（n=2）第 3 名，C_full 3.45（n=2）第 4 名，H4_sop_only 3.20（n=2）第 5 名，E_rules 3.19（n=1）第 6 名，A_bare 3.04（n=1）第 7 名。LLM 评估层的第 1 名（H4_sop_only，6 K）在专家视角下排名倒数第二（仅高于 A_bare 0.16 分）。LLM 评审对 C_full 与 H4 的高估最严重（Δ 分别为 −1.27 与 −1.05），提示这两种配置虽呈现结构完整性与术语合规性，但专家可识别其临床实操深度不足。

### 3.6 token 规模与质量的双视角关系

Figure 4 以双视角呈现 token 规模与质量评分的关系。Claude 评审曲线随 token 规模单调上升，至 C_full 仍保持 4.90；GPT 评审曲线在 H4（6 K）附近达到峰值后下降，在 C_full 处出现崩溃；专家评审曲线在 F 与 G 模板区（35–38 K）达到峰值 4.24，而在 H4（6 K）仅 3.20。三条曲线在 6–13 K 区间的分歧最为显著：LLM 评审认为已接近峰值，而专家判断仍显著低于最优。这一结果揭示 token 效率导向的配置优化与临床可用性导向的配置优化在 QMS 生成场景中对应两个不同的目标函数。

![Figure 4](figures/fig4_token_vs_quality.png)

**Figure 4.** token 规模与质量评分关系——LLM 评审在 6–13 K 达峰，专家偏好 35–61 K。横轴为 system-prompt 大小（symlog 刻度），纵轴为 0–5 质量评分。绿色实线（方块）为 3 位专家均值，红色实线（圆点）为 Claude Opus 4.6 评审，蓝色实线（三角）为 GPT-5.4 评审。橙色阴影区为 token 效率最优区（H4 / H3），绿色阴影区为专家临床可用性最优区（F / G）。

---

## 4. Discussion

### 4.1 配置精简化在 LLM 层成立但在专家层不成立

LLM 评审层的四因子消融得出一个简洁结论：规则与骨架必需，详细内容与示例无贡献甚至有害。此结论与 lost-in-the-middle 理论 [3] 及 prompt 精简化实践 [12] 一致。然而专家层分析推翻了这一简化：详细内容（F 与 G 的完整模板）显著提升临床可用性（F 4.24 vs H3 3.28，差距达 0.96），原因在于 LLM 的内化知识不足以覆盖临床实操的所有子场景，包括急诊样本处理、患者自采送检、运送人员资格认证与拒收标准等。此类信息必须通过 system prompt 显式提供。

### 4.2 全量输入陷阱的模型依赖性

C_full（71 K）是一个典型的看起来安全的配置选项：其包含所有可能相关的资料，符合宁多勿少的直觉。但在 GPT-5.4 生成条件下（跨评分 1.40–1.84），其表现彻底失败。可能的解释为：Claude Opus 的 long-context attention 训练更充分，能在 71 K 中筛选有效信号；GPT-5.4 在超长配置下出现指令遗忘。方法学启示：任何关于某配置尚可用的结论必须经跨生成模型验证，单模型结论与模型特性绑定，不应外推。

### 4.3 LLM 评审的局限与合理使用范围

本研究量化了两类重要偏差：跨 LLM 偏差（Claude 高估自家 +0.46，GPT 反向 −0.47）与跨机器-专家偏差（两种 LLM 高估 0.52–0.90 分）。Claude 评审的排序与 3 位专家均值呈中等一致性（ICC=0.548），可作为粗筛代理——在大规模文件生成场景下，先以 Claude 评审筛除明显低质量输出可节省专家时间。GPT 评审与专家排序的相关性仅 ICC=0.217，不适合作为代理。关键文件（送审、体系文件、上线执行）必须由专家终审。

### 4.4 配置推荐的场景分层

综合三层评估证据，针对不同使用场景的配置推荐如下（Table 6）：

| 使用场景 | 推荐配置 | Token | 依据 | 权衡 |
|---------|---------|-------|------|------|
| 快速生成初稿、内部迭代 | H4_sop_only 或 E_rules | 3–6 K | LLM 评估层近最优，效率最高 | 需人工补充临床细节 |
| 多 SOP 编写 | H4 或 H3 | 6–13 K | 任务特定骨架加规则 | 同上 |
| 正式文件、CNAS 送审 | G_template_rules | 38 K | 专家层认可度最高，跨模型稳健 | token 成本较高 |
| 完整质量手册 | F_template 或 G | 35–38 K | 专家层评分最优 | 同上 |
| 不推荐 | C_full（71 K） | — | GPT 生成下崩溃，跨评排名最低 | — |
| 不推荐 | A_bare、B_simple | — | 基线过低，缺合规性 | — |

推荐的实际工作流为：先以 H4 生成初稿，再由人工校对补充临床细节，关键文件最后采用 G 重新生成或精修。

### 4.5 局限性

本研究存在以下局限。(i) 专家样本规模有限：n=3 rater × 10 文件，组均值仅 1 至 2 份，仅支持排序方向性结论而非严格统计推断。跨单位 3 至 5 位专家 × 30 至 50 份文件的多中心验证是关键的未来工作。(ii) 同单位专家一致性的双刃剑：3 位专家间 ICC(2,k)=0.982 的极高一致性既是 5 维度评分量规有效的证据，亦可能反映同单位共享的专业文化、培训谱系与对模糊条款的解读习惯，从而高估了跨单位可推广性。(iii) 第一作者的双重角色：第一作者同时担任 Rater 1 与研究设计者。Rater 2 与 Rater 3 在不知晓 Rater 1 评分的前提下独立完成评分；各 rater 数据完整公开。(iv) 专家与 LLM 评审共享 5 维度量规：存在 shared-measurement bias 风险，未来应加入临床可用性等专家原生维度。(v) GPT-5.4 生成任务覆盖受限：仅覆盖 A1/B1/C1（81 份）。(vi) 领域特异性：结果限定于 ISO 15189 医学实验室，对 ISO 17025、ISO 9001 等其他标准的迁移性待验证。(vii) 第三方 LLM 评审缺失：仅采用 Claude 与 GPT 两类评审。(viii) 语言限定：全部为中文 QMS 文件，英语或其他语言场景下的效果未验证。(ix) 模型时效性：生成文件的质量受所用模型影响，随着大模型持续迭代，本研究结论可能需要重新验证。

---

## 5. Conclusions

LLM 辅助 ISO 15189 QMS 文件生成的最优配置取决于评估视角。LLM 评估层下 H4_sop_only（6 K）综合最优；专家视角下 F_template（35 K）、H2_keep_examples（61 K）与 G_template_rules（38 K）并列最优（均值 4.06–4.24 分），H4 位列倒数第二。追求 token 效率与成本控制的场景推荐采用 H4 或 E_rules（3–6 K），正式送审与 CNAS 认可申请场景推荐采用 G 或 F（35–38 K），C_full（71 K）应避免使用。LLM 评审可作为初筛代理（Claude 评审效果优于 GPT），但关键文件必须经专家终审。

---

## 申报声明

**Research funding**：本研究未接受外部研究资助。

**Author contributions**：刘斯迪独立完成研究设计、实验实施、数据分析、论文撰写与最终定稿，并对全文内容承担责任。

**Competing interests**：作者声明无利益冲突。

**Informed consent**：Rater 2 与 Rater 3 在参与专家盲评前已获得书面知情同意。知情同意表说明了研究目的、评分用途、匿名保障及随时退出的权利。

**Ethical approval**：本研究不涉及患者数据、生物样本或人体干预。生成与评估的 QMS 文件均采用虚构占位符（如"李某"、"张医生"）并未包含任何可识别的个人信息。评分者间的数据属于方法学研究范畴，已获得知情同意。

**Data availability**：486 份生成文件、864 次 LLM 评审数据、30 次专家盲评数据及全部分析脚本已公开于 GitHub（https://github.com/stttttte/iso15189-llm-config-experiment），遵循 MIT（代码）与 CC BY 4.0（数据）双许可。

---

## 致谢

感谢两位参与盲评的同事（Rater 2 与 Rater 3）在知情同意的前提下为研究提供独立的专家视角。

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

**Word count (正文含参考文献)**：约 6200 字  
**Tables**：6（含推荐配置表 Table 6）  
**Figures**：4  
**References**：13
