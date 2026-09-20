"""Offline regression checks against the released, independently audited data."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def data_hashes():
    return {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((ROOT / "data").rglob("*")) if path.is_file()
    }


def load_icc_module():
    spec = importlib.util.spec_from_file_location(
        "compute_icc_3raters", ROOT / "code" / "compute_icc_3raters.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleasedDataReproductionTests(unittest.TestCase):
    def run_script(self, script, output_dir):
        return subprocess.run(
            [sys.executable, str(ROOT / "code" / script), "--output-dir", str(output_dir)],
            cwd=output_dir,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_icc_cli_recomputes_from_public_inputs_without_changing_data(self):
        before = data_hashes()
        with tempfile.TemporaryDirectory() as output_dir:
            run = self.run_script("compute_icc_3raters.py", output_dir)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            output = Path(output_dir) / "icc_results_3raters.json"
            self.assertTrue(output.is_file(), run.stdout + run.stderr)
            result = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(data_hashes(), before)
        self.assertEqual(result["n_papers"], 10)
        self.assertAlmostEqual(result["icc"]["expert_panel"]["ICC_2_k"], 0.9817874724257523, places=12)
        self.assertAlmostEqual(result["icc"]["expert_vs_claude"]["ICC31"], 0.5484063917443198, places=12)
        self.assertAlmostEqual(result["icc"]["expert_vs_gpt"]["ICC31"], 0.21713298545493243, places=12)
        # Existing JSON uses expert minus judge; positive judge bias is its negative.
        self.assertAlmostEqual(result["icc"]["expert_vs_claude"]["diff"], -0.9046666666666667, places=12)
        self.assertAlmostEqual(result["icc"]["expert_vs_gpt"]["diff"], -0.5246666666666668, places=12)

    def test_table1_cli_uses_45_claude_outputs_per_configuration(self):
        expected = [
            ("H4_sop_only", 0.9939393939393937),
            ("H3_skeleton", 0.8691159586681976),
            ("G_template_rules", 0.8506305883171552),
            ("H2_keep_examples", 0.758583829106217),
            ("E_rules_v2", 0.728794837003792),
            ("C_full", 0.4933966530981456),
            ("F_template", 0.34520752878961825),
            ("B_simple", 0.2274623386563687),
            ("A_bare", 0.0),
        ]
        before = data_hashes()
        with tempfile.TemporaryDirectory() as output_dir:
            run = self.run_script("reproduce_ranking.py", output_dir)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            result = json.loads((Path(output_dir) / "table1_ranking.json").read_text(encoding="utf-8"))
        self.assertEqual(data_hashes(), before)
        self.assertEqual(result["n_outputs"], 405)
        self.assertEqual([row["group"] for row in result["ranking"]], [row[0] for row in expected])
        for actual, (group, composite) in zip(result["ranking"], expected):
            with self.subTest(group=group):
                self.assertEqual(actual["n_auto"], 45)
                self.assertEqual(actual["n_gpt_judge"], 45)
                self.assertAlmostEqual(actual["composite"], composite, places=12)
        self.assertAlmostEqual(result["ranking"][0]["auto_mean"], 2.0246666666666666, places=12)
        self.assertAlmostEqual(result["ranking"][0]["gpt_judge_mean"], 4.022222222222222, places=12)

    def test_scripts_reject_outputs_inside_released_data(self):
        before = data_hashes()
        for script in ["compute_icc_3raters.py", "reproduce_ranking.py"]:
            with self.subTest(script=script):
                run = self.run_script(script, ROOT / "data" / "expert_blind_review")
                self.assertNotEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(data_hashes(), before)

    def test_icc_supports_legacy_and_modern_pingouin_type_labels(self):
        module = load_icc_module()
        recorded = json.loads((ROOT / "data" / "expert_blind_review" / "icc_results_3raters.json").read_text(encoding="utf-8"))
        df = pd.DataFrame(recorded["per_paper"])
        # Derive expert means from unrounded rater means, as the analysis does.
        raters = ["rater1_mean", "rater2_mean", "rater3_mean"]
        df["expert_mean"] = df[raters].mean(axis=1)
        actual_intraclass_corr = module.pg.intraclass_corr
        modern = {"ICC1": "ICC(1,1)", "ICC2": "ICC(A,1)", "ICC3": "ICC(C,1)",
                  "ICC1k": "ICC(1,k)", "ICC2k": "ICC(A,k)", "ICC3k": "ICC(C,k)"}
        for labels in [modern, {v: k for k, v in modern.items()}]:
            def with_labels(**kwargs):
                result = actual_intraclass_corr(**kwargs)
                result["Type"] = result["Type"].replace(labels)
                return result

            with self.subTest(labels=list(labels.values())), patch.object(module.pg, "intraclass_corr", with_labels), contextlib.redirect_stdout(io.StringIO()):
                pair = module.compute_icc_pair(df, "expert_mean", "claude_mean", "expert vs Claude")
                panel = module.compute_icc_multi(df, raters, "expert panel")
                self.assertAlmostEqual(pair["ICC31"], 0.5484063917443198, places=12)
                self.assertAlmostEqual(panel["ICC_2_k"], 0.9817874724257523, places=12)


if __name__ == "__main__":
    unittest.main()
