"""Regression checks for the final CCLM figures using only released inputs."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np


ROOT = Path(__file__).resolve().parents[1]


class FinalFiguresTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.work = tempfile.TemporaryDirectory(prefix="cclm-figure-test-")
        cls.root = Path(cls.work.name) / "repository"
        (cls.root / "code").mkdir(parents=True)
        shutil.copy2(ROOT / "code/make_figures.py", cls.root / "code/make_figures.py")
        (cls.root / "data").symlink_to(ROOT / "data", target_is_directory=True)
        os.environ["MPLBACKEND"] = "Agg"
        spec = importlib.util.spec_from_file_location("final_figure_test_module", cls.root / "code/make_figures.py")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    @classmethod
    def tearDownClass(cls):
        cls.work.cleanup()

    def test_public_inputs_preserve_all_cross_judge_scores(self):
        order, matrix = self.module.load_fig2()
        source = json.loads((ROOT / "data/analysis/2x2_symmetric_complete.json").read_text())["matrix"]
        for group, row in zip(order, matrix):
            key = "E_rules_v2" if group == "E_rules" else group
            np.testing.assert_allclose(row, [source[key][q] for q in ("CC", "CG", "GC", "GG")])

    def test_token_coordinates_and_subset_ranking_are_explicit(self):
        by = self.module.load_fig4().set_index("group")
        self.assertAlmostEqual(by.loc["F_template", "tokens"], 23.090, places=3)
        self.assertAlmostEqual(by.loc["G_template_rules", "tokens"], 24.235, places=3)
        rank = self.module.load_composite_ranking(set(by.index))
        self.assertEqual(rank, ["H4_sop_only", "G_template_rules", "H2_keep_examples", "E_rules_v2", "C_full", "F_template", "A_bare"])
        expert_rank = list(by.sort_values("expert", ascending=False).index)
        self.assertEqual(expert_rank.index("H4_sop_only") + 1, 5)
        self.assertEqual(expert_rank.index("F_template") + 1, 1)
        expected = json.loads((ROOT / "data/expert_blind_review/icc_results_3raters.json").read_text())["per_paper"]
        for group in by.index:
            papers = [p for p in expected if p["group"] == group]
            for key in ("expert", "claude", "gpt"):
                self.assertAlmostEqual(by.loc[group, key], sum(p[f"{key}_mean"] for p in papers) / len(papers))

    def test_renders_final_four_figures_from_any_working_directory(self):
        output = Path(self.work.name) / "rendered"
        env = dict(os.environ, MPLBACKEND="Agg", MPLCONFIGDIR=str(Path(self.work.name) / "mplconfig"))
        result = subprocess.run([sys.executable, str(self.root / "code/make_figures.py"), "--output-dir", str(output)],
                                cwd=self.work.name, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name for p in output.glob("*.png")}, {f"Figure{i}.png" for i in range(1, 5)})
        for number in range(1, 5):
            self.assertGreater((output / f"Figure{number}.png").stat().st_size, 20_000)
            self.assertTrue((output / f"Figure{number}.svg").exists())
        self.assertFalse((self.root / "code/figures").exists())
        self.assertFalse((self.root / "figures").exists())
        fig1 = (output / "Figure1.svg").read_text()
        fig4 = (output / "Figure4.svg").read_text()
        self.assertNotIn("V3 one panel", fig1)
        self.assertIn("Archived configuration size", fig1)
        self.assertIn("cl100k_base", fig1)
        self.assertIn("Automated/GPT", fig4)
        self.assertIn("composite", fig4)
        self.assertNotIn("token-efficient", fig4)
        self.assertNotIn("expert-optimal", fig4)

    def test_bland_altman_uses_unchanged_document_scores(self):
        papers = json.loads((ROOT / "data/expert_blind_review/icc_results_3raters.json").read_text())["per_paper"]
        figures = []
        with mock.patch.object(self.module, "save", side_effect=lambda figure, name: figures.append(figure)):
            self.module.figure3()
        figure = figures[0]
        for axis, judge in zip(figure.axes, ("claude_mean", "gpt_mean")):
            expected = np.array([[(p["expert_mean"] + p[judge]) / 2, p[judge] - p["expert_mean"]] for p in papers])
            plotted = np.concatenate([points.get_offsets() for points in axis.collections])
            np.testing.assert_allclose(plotted, expected)
            difference = expected[:, 1]
            bias, sd = difference.mean(), difference.std(ddof=1)
            np.testing.assert_allclose([line.get_ydata()[0] for line in axis.lines], [0, bias, bias + 1.96 * sd, bias - 1.96 * sd])
        self.module.plt.close(figure)


if __name__ == "__main__":
    unittest.main()
