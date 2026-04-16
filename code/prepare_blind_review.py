"""
生成 P0-1 专家盲评材料。
- 10 篇固定采样 → 种子 42 打乱 paper_01..10
- 不改写正文；复制时去除可能的组名标识（当前已确认内容无泄漏）
- 产出：blind_review/paper_NN.md + key.json + rating_sheet.md
"""

import json
import random
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
OUTPUTS = BASE / "outputs"
BLIND = BASE / "blind_review"

SAMPLES = [
    ("H4_sop_only",      "A1", 2),
    ("H4_sop_only",      "A3", 1),
    ("C_full",           "A1", 1),
    ("C_full",           "A2", 2),
    ("G_template_rules", "A1", 1),
    ("G_template_rules", "A2", 3),
    ("H2_keep_examples", "A1", 3),
    ("E_rules_v2",       "A3", 2),
    ("A_bare",           "A2", 1),
    ("F_template",       "A1", 2),
]

TASK_NAME = {
    "A1": "人员培训与能力评估控制程序",
    "A2": "设备管理控制程序",
    "A3": "样本采集与处理 SOP",
}


def main():
    BLIND.mkdir(exist_ok=True)

    # 打乱分配盲评编号（种子 42 可复现）
    rnd = random.Random(42)
    shuffled = SAMPLES[:]
    rnd.shuffle(shuffled)

    key_rows = []
    for blind_id, (group, task, rep) in enumerate(shuffled, start=1):
        src = OUTPUTS / group / f"{group}-{task}-{rep}.md"
        dst = BLIND / f"paper_{blind_id:02d}.md"
        shutil.copy(src, dst)
        key_rows.append({
            "blind_id": f"paper_{blind_id:02d}",
            "group": group,
            "task": task,
            "rep": rep,
            "source_file": f"{group}/{group}-{task}-{rep}.md",
            "task_name": TASK_NAME.get(task, task),
        })

    # key.json（评分完成后再打开）
    with open(BLIND / "key.json", "w", encoding="utf-8") as f:
        json.dump(key_rows, f, ensure_ascii=False, indent=2)

    # 评分表（只暴露 task_name，不暴露组）
    sheet = ["# P0-1 专家盲评评分表", "",
             "> 每篇按 5 维度打分，每维度 **0-5 整数**。5=完全符合，3=部分符合，1=严重不符，0=完全缺失。",
             "> 评分维度定义与 CNAS 主任评审员 judge prompt 完全一致。",
             "",
             "## 评分维度（参考 judge prompt）", "",
             "| # | 维度 | 5 分锚定 | 1 分锚定 |",
             "|---|------|---------|---------|",
             "| 1 | **条款满足度** | 对应条款所有 SHALL 要求均有具体落地措施 | 大量条款仅引用未落实，或严重遗漏 |",
             '| 2 | **可操作性** | 每步有具体责任人（岗位名）、量化时限、明确输出（表单编号） | 大量"及时/相关人员/定期"等无法执行的表述 |',
             "| 3 | **内部一致性** | 引用的文件/表单全部在相关章节列出，职责分配清晰 | 大量悬空引用或职责冲突 |",
             "| 4 | **PDCA 闭环** | 明确有 P-D-C-A 完整链条 | 仅描述执行步骤，无检查和改进 |",
             "| 5 | **专业深度** | 含检验科专业细节（Westgard/HIL/PCR 分区/测量不确定度等） | 内容泛泛，可套用于任何实验室 |",
             "",
             "---", ""]

    for row in key_rows:
        sheet += [
            f"## {row['blind_id']} — {row['task_name']}",
            "",
            "| 维度 | 分数 (0-5) | 简要理由（可选，≤40 字）|",
            "|------|-----------|------------------------|",
            "| 1. 条款满足度 |  |  |",
            "| 2. 可操作性   |  |  |",
            "| 3. 内部一致性 |  |  |",
            "| 4. PDCA 闭环  |  |  |",
            "| 5. 专业深度   |  |  |",
            "",
            "**总体印象**（可选，≤60 字）：",
            "",
            "---", ""
        ]

    with open(BLIND / "rating_sheet.md", "w", encoding="utf-8") as f:
        f.write("\n".join(sheet))

    # README 给人看的说明
    readme = f"""# P0-1 专家盲评工作包

## 文件清单
- `paper_01.md` ~ `paper_10.md`：10 篇待盲评文件（已随机打乱，组信息不可见）
- `rating_sheet.md`：评分表，**请在此文件打分**
- `key.json`：组映射（**评分完成前请勿打开**）
- `compute_icc.py`：评分完成后跑一下，得到 ICC

## 评分流程
1. 依次打开 `paper_01.md` ~ `paper_10.md`，粗读 5-10 分钟
2. 在 `rating_sheet.md` 对应段落填分（0-5 整数，5 维度）
3. 理由可选（省略也行，只要数字）
4. 评分全部完成后告诉 Claude，跑 `python3 compute_icc.py`

## 预计工作量
- 每篇 ~15 分钟，合计 2-3 小时
- 可以分多次完成（不会污染评分）

## 统计对比
评分完成后，ICC 会对比：
- 你 vs Claude judge
- 你 vs GPT judge
- 你 vs 两 judge 均值
- ICC(2,1) 和 ICC(3,1) 双口径
"""
    with open(BLIND / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"✅ 生成 {len(shuffled)} 篇盲评材料 → {BLIND}")
    print(f"   评分表：{BLIND / 'rating_sheet.md'}")
    print(f"   key.json 已保存（评分后再开）")


if __name__ == "__main__":
    main()
