import unittest

import helpers  # noqa: F401  (puts tools/ on sys.path)
from pelloux_audit import config
from pelloux_audit.checks import Unit, check_file
from pelloux_audit.languages import BY_NAME
from pelloux_audit.mask import mask
from pelloux_audit.smells import deep_imports


def hits(code: str, lang: str, depth: int = 2) -> list:
    language = BY_NAME[lang]
    return deep_imports(code, mask(code, language), language, depth)


class DeepImports(unittest.TestCase):
    def test_typescript_import_export_require_and_dynamic(self):
        code = ("import a from '../../lib/a';\n"
                "import { b } from '../../../lib/b';\n"
                "export * from \"../../../../c\";\n"
                "const d = require('../../../d');\n"
                "const e = await import(`../../../e`);\n"
                "import f from '@/lib/f';\n")
        self.assertEqual(hits(code, "typescript"), [(2, 3), (3, 4), (4, 3), (5, 3)])

    def test_strings_and_comments_are_not_imports(self):
        code = ("// import x from '../../../x';\n"
                "const s = \"from '../../../y'\";\n"
                "/* require('../../../z') */\n")
        self.assertEqual(hits(code, "typescript"), [])

    def test_python_counts_dots_minus_one(self):
        code = "from .. import a\nfrom ... import b\nfrom ....models import c\nfrom app.x import d\n"
        self.assertEqual(hits(code, "python"), [(3, 3)])

    def test_dart_php_cpp_rust(self):
        self.assertEqual(hits("import '../../../widgets/x.dart';\n", "dart"), [(1, 3)])
        php = "<?php\nrequire_once __DIR__ . '/../../../vendor/autoload.php';\ninclude '../a.php';\n"
        self.assertEqual(hits(php, "php"), [(2, 3)])
        self.assertEqual(hits('#include "../../../core/a.h"\n#include <vector>\n', "cpp"), [(1, 3)])
        self.assertEqual(hits("use super::super::super::db;\nuse super::x;\n", "rust"), [(1, 3)])

    def test_depth_is_configurable_and_null_turns_it_off(self):
        code = "import a from '../../a';\n"
        self.assertEqual(hits(code, "typescript", depth=1), [(1, 2)])
        self.assertEqual(hits(code, "typescript", depth=None), [])

    def test_finding_is_ratcheted_per_file_with_advice(self):
        cfg = config.Config(root=None)
        code = "import a from '../../../a';\nimport b from '../../../../b';\n"
        found = [f for f in check_file(Unit("src/x.ts", code, BY_NAME["typescript"]), cfg)
                 if f.rule == "deep-import"]
        self.assertEqual((found[0].key, found[0].value, found[0].line), ("deep-import::src/x.ts", 2, 1))
        self.assertIn("@/", found[0].message)

    def test_languages_without_relative_imports_are_skipped(self):
        self.assertEqual(hits('import "../../../pkg"\n', "go"), [])


if __name__ == "__main__":
    unittest.main()
