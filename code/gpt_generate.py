"""
P0-2 多模型验证：用 GPT-4o 生成文件，验证"H4 最优"结论是否模型无关。

用法：
  python3 gpt_generate.py --tasks A1,B1,C1 --model gpt-4o --concurrency 3

  # 仅跑单任务：
  python3 gpt_generate.py --tasks A1 --groups G_template_rules,H4_sop_only

  # 全量（不推荐，成本高）：
  python3 gpt_generate.py --all

环境变量：
  GPT_API_KEY        必填
  OPENAI_BASE_URL    默认 https://aihubmix.com/v1

输出：
  outputs/gpt4o_{group_name}/gpt4o_{group_name}-{task}-{rep}.md
"""

import os
import json
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
CONFIGS_DIR = BASE_DIR / "configs"
TASK_MSG_DIR = BASE_DIR / "task_messages"

GPT_API_KEY = os.environ.get("GPT_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://aihubmix.com/v1")

# 9 组配置映射：group_name → (config_getter, description)
# config_getter(task) returns the system prompt string
def load_simple_prompt():
    return """你是一名 ISO 15189:2022 医学实验室质量管理体系文件专家。你的职责是协助实验医学科编写、修订和审查质量管理体系文件。

请按以下基本要求工作：

1. 语言：使用中文编写，专业术语保留英文原文并附中文（如 ISO 15189:2022）。
2. 文件结构：程序文件应包含以下八个部分——目的、适用范围、职责、定义与缩略语、程序内容、相关文件、记录表格、变更历史。
3. 标准引用：内容应引用 ISO 15189:2022 和 CNAS-CL02:2023 的对应条款。
4. 术语规范：使用 2022 版标准术语，如"检验前过程"而非"分析前过程"，"样品"而非"标本"，"生物参考区间"而非"正常值范围"。
5. 表述方式：操作步骤使用祈使句（"应""必须""shall"），避免模糊表述和口语化表达。
6. 编号格式：标题层级使用"1""1.1""1.1.1"格式。"""


def load_full_config():
    with open(BASE_DIR / "full_config.txt", encoding="utf-8") as f:
        return f.read()


def load_rules():
    with open(BASE_DIR / "config_restructured" / "rules.md", encoding="utf-8") as f:
        return f.read()


def load_config_file(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


GROUP_CONFIGS = {
    "A_bare": lambda task: "",
    "B_simple": lambda task: load_simple_prompt(),
    "C_full": lambda task: load_full_config(),
    "E_rules_v2": lambda task: load_rules(),
    "F_template": lambda task: load_config_file(CONFIGS_DIR / f"F_{task}.txt"),
    "G_template_rules": lambda task: load_config_file(CONFIGS_DIR / f"G_{task}.txt"),
    "H2_keep_examples": lambda task: load_config_file(CONFIGS_DIR / f"H2_{task}.txt"),
    "H3_skeleton": lambda task: load_config_file(CONFIGS_DIR / f"H3_{task}.txt"),
    "H4_sop_only": lambda task: load_config_file(CONFIGS_DIR / f"H4_{task}.txt"),
}

# GPT-4o 生成组输出到独立目录（前缀 gpt4o_）
# 文件名格式：gpt4o_{group}-{task}-{rep}.md


def call_gpt_generate(system_prompt: str, user_message: str, model: str,
                     max_tokens: int = 16000, retries: int = 3) -> str:
    """调用 GPT API 生成"""
    from openai import OpenAI
    client = OpenAI(api_key=GPT_API_KEY, base_url=OPENAI_BASE_URL)
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_message})

    last_err = None
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0.7,  # 与 Claude 生成的温度保持一致（有一定多样性）
                max_completion_tokens=max_tokens,
                messages=messages,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            last_err = e
            wait = 2 ** attempt
            print(f"  [WARN] API 失败 (尝试 {attempt+1}/{retries}): {e}, {wait}s 后重试")
            time.sleep(wait)
    raise RuntimeError(f"GPT 调用失败: {last_err}")


def generate_one(group: str, task: str, rep: int, model: str, force: bool = False) -> dict:
    """生成单篇"""
    model_short = model.replace(".", "").replace("-", "")
    output_dir = OUTPUTS_DIR / f"gpt4o_{group}"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"gpt4o_{group}-{task}-{rep}.md"

    if output_path.exists() and not force:
        return {"status": "skip", "filename": output_path.name}

    # 加载配置
    try:
        sys_prompt = GROUP_CONFIGS[group](task)
    except Exception as e:
        return {"status": "error", "filename": output_path.name, "reason": f"config_load: {e}"}

    # 加载任务
    task_path = TASK_MSG_DIR / f"{task}.txt"
    if not task_path.exists():
        return {"status": "error", "filename": output_path.name, "reason": "task_msg_not_found"}
    with open(task_path, encoding="utf-8") as f:
        user_msg = f.read()

    # 调用 GPT
    try:
        content = call_gpt_generate(sys_prompt, user_msg, model=model)
    except Exception as e:
        return {"status": "error", "filename": output_path.name, "reason": str(e)}

    if not content.strip():
        return {"status": "empty", "filename": output_path.name}

    # 写入
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return {"status": "ok", "filename": output_path.name, "bytes": len(content.encode("utf-8"))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="A1,B1,C1", help="任务 ID 列表（逗号分隔）")
    ap.add_argument("--groups", default=",".join(GROUP_CONFIGS.keys()), help="组名列表（逗号分隔）")
    ap.add_argument("--reps", default="1,2,3", help="重复编号")
    ap.add_argument("--model", default="gpt-5.4")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--all", action="store_true", help="全部 15 任务（成本高，不推荐）")
    args = ap.parse_args()

    if not GPT_API_KEY:
        print("ERROR: 请设置环境变量 GPT_API_KEY")
        return

    if args.all:
        tasks = ["A1","A2","A3","A4","A5","B1","B2","B3","B4","B5","C1","C2","C3","C4","C5"]
    else:
        tasks = [t.strip() for t in args.tasks.split(",")]
    groups = [g.strip() for g in args.groups.split(",")]
    reps = [int(r) for r in args.reps.split(",")]

    targets = [(g, t, r) for g in groups for t in tasks for r in reps]
    print(f"共 {len(targets)} 篇待生成（{len(groups)} 组 × {len(tasks)} 任务 × {len(reps)} 重复）")
    print(f"模型: {args.model}  并发: {args.concurrency}")

    # 估算成本
    estimated_cost = len(targets) * 0.6  # GPT-5.4 单篇约 $0.5-0.7
    print(f"预估成本: ~${estimated_cost:.0f}\n")

    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = {
            ex.submit(generate_one, g, t, r, args.model, args.force): (g, t, r)
            for (g, t, r) in targets
        }
        for i, fut in enumerate(as_completed(futures), 1):
            g, t, r = futures[fut]
            try:
                result = fut.result()
            except Exception as e:
                result = {"status": "exception", "filename": f"gpt4o_{g}-{t}-{r}", "error": str(e)}
            results.append(result)
            status = result.get("status", "?")
            icon = {"ok": "✅", "skip": "⏭", "error": "❌", "empty": "⚠️"}.get(status, "?")
            extra = f"({result.get('bytes',0)//1024}K)" if status == "ok" else result.get("reason", "")
            print(f"  [{i}/{len(targets)}] {icon} {result['filename']} {extra}")

    # 汇总
    ok = sum(1 for r in results if r["status"] == "ok")
    skip = sum(1 for r in results if r["status"] == "skip")
    errors = sum(1 for r in results if r["status"] in ["error", "empty", "exception"])
    print(f"\n完成: {ok} 成功, {skip} 跳过, {errors} 失败")


if __name__ == "__main__":
    main()
