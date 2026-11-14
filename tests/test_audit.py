import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import helpers  # noqa: F401  (puts tools/ on sys.path)
from pelloux_audit import baseline, config
from pelloux_audit.audit import Request, run
from pelloux_audit.checks import Unit, check_file
from pelloux_audit.languages import BY_NAME
from pelloux_audit.mask import mask

TOOL = Path(__file__).resolve().parent.parent / "tools" / "pelloux.py"


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def long_ts(name: str, lines: int) -> str:
    return f"export function {name}() {{\n" + "  step();\n" * lines + "}\n"


class Rules(unittest.TestCase):
    def setUp(self):
        self.cfg = config.Config(root=Path("."))

    def test_tolerance_rounds_down(self):
        self.assertEqual([self.cfg.hard(n) for n in (400, 200, 25)], [440, 220, 27])

    def test_file_size_target_and_limit(self):
        unit = Unit("src/big.ts", "x;\n" * 450, BY_NAME["typescript"])
        rules = {(f.rule, f.severity) for f in check_file(unit, self.cfg)}
        self.assertIn(("file-size", "error"), rules)

    def test_entry_module_has_its_own_limit(self):
        unit = Unit("src/services/api.ts", "x;\n" * 230, BY_NAME["typescript"])
        found = check_file(unit, self.cfg)
        self.assertEqual(found[0].rule, "module-size")
        self.assertEqual(found[0].severity, "error")

    def test_tests_are_size_exempt_but_not_debug_exempt(self):
        text = long_ts("t", 60) + "it.only('x', () => {});\n"
        found = check_file(Unit("src/a.test.ts", text, BY_NAME["typescript"]), self.cfg)
        self.assertEqual([f.rule for f in found], ["debug"])

    def test_debug_inside_strings_and_comments_is_ignored(self):
        text = "const s = 'console.log(x)';\n// console.log(y)\nconsole.log(z);\n"
        found = check_file(Unit("a.ts", text, BY_NAME["typescript"]), self.cfg)
        self.assertEqual(found[0].value, 1)
        self.assertEqual(found[0].line, 3)

    def test_debug_count_is_ratcheted_per_file(self):
        text = "dd($a);\n$b = 1;\ndd($b);\n"
        found = check_file(Unit("a.php", text, BY_NAME["php"]), self.cfg)
        self.assertEqual((found[0].key, found[0].value), ("debug::a.php", 2))

    def test_mask_keeps_positions(self):
        code = 'a = "x{y}" # c\nb\n'
        masked = mask(code, BY_NAME["python"])
        self.assertEqual(len(masked), len(code))
        self.assertNotIn("{", masked)

    def test_glob_without_slash_matches_any_depth(self):
        self.assertTrue(config.glob_regex("*.spec.*").match("a/b/c.spec.ts"))
        self.assertTrue(config.glob_regex("**/tests/**").match("tests/a.py"))
        self.assertFalse(config.glob_regex("vendor/**").match("src/vendor.ts"))


class Ratchet(unittest.TestCase):
    def test_seed_then_shrink_holds_and_growth_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root, "src/a.ts", long_ts("a", 40))
            cfg = config.load(root)
            first = run(cfg, Request())
            self.assertFalse(first.ok)
            baseline.write(cfg.baseline_path(), first.findings)
            self.assertTrue(run(cfg, Request()).ok)
            write(root, "src/a.ts", long_ts("a", 35))
            shrunk = run(cfg, Request())
            self.assertTrue(shrunk.ok)
            write(root, "src/a.ts", long_ts("a", 45))
            grown = run(cfg, Request())
            self.assertIn("grew past its baseline", grown.result.errors[0].message)

    def test_legacy_baseline_format_is_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "pelloux-baseline.json"
            path.write_text(json.dumps({"oversized_files": [{"path": "a.ts", "lines": 500}]}))
            self.assertEqual(baseline.load(path), {"file-size::a.ts": 500})

    def test_config_overrides_are_additive_for_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root, "pelloux.json", json.dumps({"function": {"limit": 40},
                                                    "exclude": ["legacy/**"]}))
            cfg = config.load(root)
            self.assertEqual(cfg.function_limit, 40)
            self.assertTrue(cfg.is_excluded("legacy/x.ts"))
            self.assertTrue(cfg.is_excluded("a/node_modules/b.js"))


class Cli(unittest.TestCase):
    def test_hook_reports_to_the_agent_with_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "big.ts"
            target.write_text(long_ts("big", 40))
            payload = json.dumps({"tool_input": {"file_path": str(target)}})
            done = subprocess.run([sys.executable, str(TOOL), "hook"], input=payload,
                                  capture_output=True, text=True)
            self.assertEqual(done.returncode, 2)
            self.assertIn("big() has 42 lines", done.stderr)

    def test_hook_never_fails_on_bad_input(self):
        done = subprocess.run([sys.executable, str(TOOL), "hook"], input="not json",
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0)


if __name__ == "__main__":
    unittest.main()
