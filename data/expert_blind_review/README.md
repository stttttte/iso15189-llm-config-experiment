# 专家盲评归档与复现

这里保存已完成的探索性专家评估：3 位同单位共同作者，对 10 篇 Claude 生成的 A 类文件（A1/A2/A3，来自 7 组配置）各评 5 个维度，合计 30 份评分表、150 个维度分数。评分范围为 0–5，允许小数。这是内部专家验证，不能视为独立外部验证。

## 文件清单

- `papers/paper_01.md` 至 `paper_10.md`：评分时隐藏配置标签的 10 篇文件。
- `rating_sheet_rater1_filled.md`、`rating_sheet_rater2_filled.md`、`rating_sheet_rater3_filled.md`：三位专家的原始评分记录。
- `blind_key.json`：`blind_id/group/task/rep` 映射，来自此前已公开的三专家分析结果，供离线复现使用。
- `icc_results_3raters.json`：历史三专家结果，包含逐篇评分、映射和组均值。
- `icc_results.json`：保留的单专家历史分析，不代表当前主分析。旧说明提及的 `rating_sheet_filled.md` 未以该文件名收录，请使用上述三份具名评分文件。

## 离线复现

在仓库根目录安装 `requirements.txt` 后运行：

```bash
python3 code/compute_icc_3raters.py
```

不需要 API。默认输出到 `reproduced/icc_results_3raters.json`，不会覆盖归档评分。可使用 `--output-dir DIR` 指定其他结果目录。

预期结果：专家间 ICC(2,k)=0.982；专家均值与 Claude/GPT 的 ICC(3,1) 分别为 0.548/0.217；Claude/GPT 相对专家均值平均高估 0.90/0.52 分。JSON 中 `diff` 为“专家减评审模型”，因此符号相反。H4 专家组均值为 3.20，在覆盖的七组中排第五。各组样本量很小且不等，不能据此确立最优配置。

## 盲法与新评审

原评分时配置标签被隐藏，但源文件映射已经能从已公开结果恢复，不能将当前工作包当作对未来评审者仍保密的盲评包。新的独立评审应另行创建盲化材料并在评分完成前单独保存映射。`code/prepare_blind_review.py` 保留历史路径假设，使用前需要适配。

Claude 文件级原始评审目前有 273 条（270 条主组记录加 3 条 H 组补充记录，均针对 Claude 生成文件），GPT 有 486 条；其他历史 Claude 汇总均值无法全部恢复到文件级记录和分母。详见 [数据字典](../../docs/DATA_DICTIONARY.md) 和 [复现说明](../../docs/REPRODUCIBILITY.md)。

当前目录说明属于未发布的一致性修订副本。历史评分文件保持原样。
