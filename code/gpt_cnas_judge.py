"""
GPT CNAS Judge — 用 GPT 以 CNAS 主任评审员视角评估 LLM 生成的 ISO 15189 文件。

用法：
  # 单任务：
  python3 gpt_cnas_judge.py --task A1 --model gpt-5.4
  # 全量 15 任务：
  python3 gpt_cnas_judge.py --all --model gpt-5.4
  # 仅某组：
  python3 gpt_cnas_judge.py --all --group G_template_rules --model gpt-5.4
  # 并发（加速）：
  python3 gpt_cnas_judge.py --all --model gpt-5.4 --concurrency 5

环境变量：
  GPT_API_KEY        必填
  OPENAI_BASE_URL    默认 https://aihubmix.com/v1

输出：
  gpt_judge_scores/{group}/{group}-{task}-{rep}.json   单篇评分
  gpt_judge_summary.json                                汇总
"""

import os
import re
import json
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
SCORES_DIR = BASE_DIR / "gpt_judge_scores"
SUMMARY_FILE = BASE_DIR / "gpt_judge_summary.json"

GPT_API_KEY = os.environ.get("GPT_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://aihubmix.com/v1")

GROUPS = ["A_bare", "B_simple", "C_full", "E_rules_v2", "F_template", "G_template_rules",
          "H2_keep_examples", "H3_skeleton", "H4_sop_only",
          # GPT-5.4 生成的组（P0-2 多模型验证）
          "gpt4o_A_bare", "gpt4o_B_simple", "gpt4o_C_full", "gpt4o_E_rules_v2",
          "gpt4o_F_template", "gpt4o_G_template_rules",
          "gpt4o_H2_keep_examples", "gpt4o_H3_skeleton", "gpt4o_H4_sop_only"]
TASKS = ["A1","A2","A3","A4","A5","B1","B2","B3","B4","B5","C1","C2","C3","C4","C5"]
REPS = [1, 2, 3]

# 任务上下文（用于 prompt 中告诉 judge 评估的是什么类型的文件）
TASK_CONTEXT = {
    "A1": ("人员培训与能力评估控制程序", "ISO 15189:2022 §6.2"),
    "A2": ("设备管理控制程序", "ISO 15189:2022 §6.4"),
    "A3": ("样本采集与处理 SOP", "ISO 15189:2022 §5.4/7.2"),
    "A4": ("管理评审修订（质量手册章节）", "ISO 15189:2022 §8.9"),
    "A5": ("设备校准记录表（修订）", "ISO 15189:2022 §6.5"),
    "B1": ("年度内审检查表", "ISO 15189:2022 §5-8 全章"),
    "B2": ("检验过程质量控制专项内审检查表", "ISO 15189:2022 §7.3"),
    "B3": ("迎检自查报告", "ISO 15189:2022 全章"),
    "B4": ("管理评审输入材料", "ISO 15189:2022 §8.9"),
    "B5": ("评审后整改计划及验证方案", "ISO 15189:2022 §8.7/8.8"),
    "C1": ("内部质控程序文件审查报告", "CNAS 主任评审员视角"),
    "C2": ("生化分析仪 SOP 审查报告", "CNAS 主任评审员视角"),
    "C3": ("体系级覆盖完整性审查报告", "CNAS 主任评审员视角"),
    "C4": ("审核驱动修改——文件更新", "ISO 15189:2022 各条款"),
    "C5": ("整改闭环——纠正措施报告", "ISO 15189:2022 §8.7/8.8"),
}


JUDGE_PROMPT_TEMPLATE = """你是一位资深 CNAS 主任评审员，专门评审医学实验室 ISO 15189:2022 质量管理体系文件。

请以真实评审视角审查以下文件，按 5 个维度打分（每维度 0-5 分，整数），并给出简短理由（每条不超过 40 字）。

**文件类型**：{task_name}
**对应标准**：{standard}

**评分维度**：

1. **条款满足度**（SHALL 要求是否被实质性满足，而非仅仅引用）
   - 5分：对应条款所有 SHALL 要求均有具体落地措施
   - 3分：覆盖主要条款但有遗漏或浮于表面
   - 1分：大量条款仅引用未落实，或严重遗漏

2. **可操作性**（一线人员能否直接按此文件执行）
   - 5分：每步有具体责任人（岗位名）、量化时限、明确输出（表单编号）
   - 3分：大部分步骤可操作，少量模糊
   - 1分：大量"及时""相关人员""定期"等无法执行的表述

3. **内部一致性**（交叉引用是否闭环、职责分配无矛盾）
   - 5分：引用的文件/表单全部在相关章节列出，职责分配清晰
   - 3分：少量悬空引用或表述矛盾
   - 1分：大量悬空引用或职责冲突

4. **PDCA 闭环**（计划→执行→检查→改进是否完整）
   - 5分：明确有计划、执行记录、效果评估、不合格处理→改进的完整链条
   - 3分：有 P-D-C 但缺少 A（改进/反馈机制）
   - 1分：仅描述执行步骤，无检查和改进

5. **专业深度**（是否体现对检验科实际工作的理解）
   - 5分：包含检验科专业细节（如 Westgard 规则、测量不确定度、Sigma 度量、HIL 指数、盲样测试、PCR 分区、冷链等）
   - 3分：有一定专业性但偏通用
   - 1分：内容泛泛，可套用于任何实验室

---

**待审查文件内容**：

{content}

---

**输出要求**：严格按以下 JSON 格式输出，不要添加任何解释性文字，不要用 markdown 代码块包裹：

{{
  "条款满足度": {{"score": <0-5整数>, "reason": "<一句话理由>"}},
  "可操作性": {{"score": <0-5整数>, "reason": "<一句话理由>"}},
  "内部一致性": {{"score": <0-5整数>, "reason": "<一句话理由>"}},
  "PDCA闭环": {{"score": <0-5整数>, "reason": "<一句话理由>"}},
  "专业深度": {{"score": <0-5整数>, "reason": "<一句话理由>"}}
}}"""


def call_gpt(prompt: str, model: str, max_tokens: int = 2000, retries: int = 3) -> str:
    """调用 GPT API，含重试"""
    from openai import OpenAI
    client = OpenAI(api_key=GPT_API_KEY, base_url=OPENAI_BASE_URL)
    last_err = None
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0,
                max_completion_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            last_err = e
            wait = 2 ** attempt
            print(f"  [WARN] API 调用失败 (尝试 {attempt+1}/{retries}): {e}，{wait}s 后重试")
            time.sleep(wait)
    raise RuntimeError(f"调用 GPT 失败: {last_err}")


def extract_json(text: str) -> dict | None:
    """从 GPT 响应中提取 JSON"""
    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", text.strip())
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", cleaned)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


def judge_one_file(group: str, task: str, rep: int, model: str, force: bool = False) -> dict:
    """评审单个文件"""
    filename = f"{group}-{task}-{rep}.md"
    input_path = OUTPUTS_DIR / group / filename
    output_path = SCORES_DIR / group / f"{filename}.json"

    if not input_path.exists():
        return {"status": "skip", "reason": "file_not_found", "filename": filename}

    if output_path.exists() and not force:
        return {"status": "skip", "reason": "already_scored", "filename": filename}

    # 读取文件内容
    with open(input_path, encoding="utf-8") as f:
        content = f.read()

    # 构建 prompt
    task_name, standard = TASK_CONTEXT.get(task, ("QMS 文件", "ISO 15189:2022"))
    prompt = JUDGE_PROMPT_TEMPLATE.format(
        task_name=task_name, standard=standard, content=content
    )

    # 调用 GPT
    try:
        raw = call_gpt(prompt, model=model)
    except Exception as e:
        return {"status": "error", "reason": str(e), "filename": filename}

    parsed = extract_json(raw)
    if not parsed:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path.with_suffix(".raw.txt"), "w", encoding="utf-8") as f:
            f.write(raw)
        return {"status": "parse_error", "filename": filename, "raw": raw[:200]}

    # 保存
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "group": group, "task": task, "rep": rep, "file": filename,
        "model": model, "scores": parsed,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    scores = {k: v["score"] for k, v in parsed.items()}
    mean = sum(scores.values()) / len(scores)
    return {"status": "ok", "filename": filename, "mean": mean, "scores": scores}


def run_batch(targets: list, model: str, concurrency: int, force: bool):
    """并发执行"""
    print(f"共 {len(targets)} 篇待评，并发 {concurrency}，模型 {model}")
    results = []
    with ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = {
            ex.submit(judge_one_file, g, t, r, model, force): (g, t, r)
            for (g, t, r) in targets
        }
        for i, fut in enumerate(as_completed(futures), 1):
            g, t, r = futures[fut]
            try:
                result = fut.result()
            except Exception as e:
                result = {"status": "exception", "filename": f"{g}-{t}-{r}", "error": str(e)}
            results.append(result)
            status = result.get("status", "?")
            icon = {"ok": "✅", "skip": "⏭", "error": "❌", "parse_error": "⚠️", "exception": "💥"}.get(status, "?")
            extra = f"mean={result['mean']:.2f}" if status == "ok" else result.get("reason", "")
            print(f"  [{i}/{len(targets)}] {icon} {result['filename']}  {extra}")
    return results


def summarize():
    """汇总所有已评分的结果"""
    all_scores = []
    for json_file in SCORES_DIR.rglob("*.json"):
        if json_file.name == "gpt_judge_summary.json":
            continue
        try:
            with open(json_file, encoding="utf-8") as f:
                d = json.load(f)
            scores = {k: v["score"] for k, v in d["scores"].items()}
            all_scores.append({
                "group": d["group"], "task": d["task"], "rep": d["rep"],
                "file": d["file"], **scores,
                "mean": sum(scores.values()) / len(scores),
            })
        except Exception as e:
            print(f"  [WARN] 解析 {json_file} 失败: {e}")

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        json.dump(all_scores, f, ensure_ascii=False, indent=2)
    print(f"\n汇总完成：{len(all_scores)} 条 → {SUMMARY_FILE}")

    # 按组统计
    from collections import defaultdict
    import statistics
    by_group = defaultdict(list)
    for s in all_scores:
        by_group[s["group"]].append(s["mean"])
    print(f"\n{'组':<22} {'n':>4} {'均值':>6}")
    print("-" * 40)
    for g in GROUPS:
        if g in by_group:
            vals = by_group[g]
            print(f"{g:<22} {len(vals):>4} {statistics.mean(vals):>6.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", help="任务 ID 或逗号分隔列表（如 A1 或 A1,B1,C1）")
    ap.add_argument("--group", help="仅评估单个组")
    ap.add_argument("--rep", type=int, help="仅评估单个重复（1/2/3）")
    ap.add_argument("--all", action="store_true", help="全量 15 任务 × 6 组 × 3 重复")
    ap.add_argument("--model", default="gpt-5.4", help="模型名称（默认 gpt-5.4）")
    ap.add_argument("--concurrency", type=int, default=5, help="并发数（默认 5）")
    ap.add_argument("--force", action="store_true", help="强制重跑已有评分")
    ap.add_argument("--summarize", action="store_true", help="仅汇总现有结果")
    args = ap.parse_args()

    if args.summarize:
        summarize()
        return

    if not GPT_API_KEY:
        print("ERROR: 请设置环境变量 GPT_API_KEY")
        return

    # 构建任务列表
    tasks_to_run = [t.strip() for t in args.task.split(",")] if args.task else TASKS
    groups_to_run = [args.group] if args.group else GROUPS
    reps_to_run = [args.rep] if args.rep else REPS

    if not args.all and not args.task:
        print("提示：使用 --all 评估全量，或 --task <任务ID> 评估单任务")
        return

    targets = [(g, t, r) for g in groups_to_run for t in tasks_to_run for r in reps_to_run]
    run_batch(targets, model=args.model, concurrency=args.concurrency, force=args.force)

    print("\n正在生成汇总...")
    summarize()


if __name__ == "__main__":
    main()
