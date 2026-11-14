import unittest

from helpers import body, functions


class Detection(unittest.TestCase):
    def test_typescript_shapes(self):
        code = (
            "export function plain(a: number, b: number) {\n  return a + b;\n}\n"
            "const arrow = async (a, b, c, d) => {\n" + body(3) + "\n};\n"
            "const expr = (a: string) => a.trim();\n"
            "class A {\n  async method(opts: { a: 1, b: 2 }): Promise<void> {\n    run();\n  }\n}\n"
            "useEffect(() => {\n  go();\n}, []);\n"
            "if (ready) {\n  start();\n}\n"
        )
        found = functions(code, "typescript")
        self.assertEqual(set(found), {"plain", "arrow", "expr", "method"})
        self.assertEqual(found["arrow"].params, 4)
        self.assertEqual(found["arrow"].length, 5)
        self.assertIsNone(found["expr"].length)
        self.assertEqual(found["method"].params, 1)

    def test_python_skips_docstring_and_self(self):
        code = ('class A:\n    def run(self, a, b, *, c, d=1):\n        """Doc.\n\n        More.\n'
                '        """\n        # comment\n        x = a\n        return x\n\n\ndef top():\n    pass\n')
        found = functions(code, "python")
        self.assertEqual(found["run"].params, 4)
        self.assertEqual(found["run"].length, 3)
        self.assertEqual(found["top"].length, 2)

    def test_rust_receiver_generics_and_char_braces(self):
        code = ("impl A {\n    pub fn new(a: u8) -> Self { Self { a } }\n"
                "    fn go<'a, T: Into<String>>(&'a mut self, x: T, y: HashMap<u8, u8>) {\n"
                "        let c = '{';\n        let d = \"}\";\n    }\n"
                "    fn declared(&self, a: u8);\n}\n")
        found = functions(code, "rust")
        self.assertEqual(found["go"].params, 2)
        self.assertEqual(found["go"].length, 4)
        self.assertNotIn("declared", found)

    def test_go_receiver_and_grouped_names(self):
        code = "func (s *Server) Handle(ctx context.Context, a, b int, c string) error {\n\treturn nil\n}\n"
        found = functions(code, "go")
        self.assertEqual(found["Handle"].params, 4)

    def test_php_constructor_is_flagged_as_constructor(self):
        code = ("<?php\nclass A {\n  public function __construct(private A $a, private B $b,"
                " private C $c, private D $d, private E $e) {}\n"
                "  public function store(Request $r): Response {\n    return x();\n  }\n}\n")
        found = functions(code, "php")
        self.assertTrue(found["__construct"].is_constructor)
        self.assertEqual(found["store"].length, 3)

    def test_dart_named_group_counts_once(self):
        code = ("class W {\n  Widget build(BuildContext context, {required int a, String? b}) {\n"
                "    return Text('}');\n  }\n  int get total => 1;\n"
                "  void tap(int a, int b) => print(a);\n}\n")
        found = functions(code, "dart")
        self.assertEqual(found["build"].params, 2)
        self.assertEqual(found["build"].length, 3)
        self.assertIsNone(found["tap"].length)

    def test_kotlin_expression_and_block(self):
        code = ("fun <T> List<T>.second(): T = this[1]\n"
                "fun render(a: Int, b: Int, c: Int, d: Int) {\n    println(a)\n}\n")
        found = functions(code, "kotlin")
        self.assertIsNone(found["second"].length)
        self.assertEqual(found["render"].params, 4)

    def test_swift_init_and_func(self):
        code = ("struct A {\n  init(a: Int) {\n    self.a = a\n  }\n"
                "  func load(_ id: Int, force: Bool) async throws -> Data {\n    try await x()\n  }\n}\n")
        found = functions(code, "swift")
        self.assertTrue(found["init"].is_constructor)
        self.assertEqual(found["load"].params, 2)

    def test_cpp_methods_and_prototypes(self):
        code = ("int add(int a, int b);\n"
                "int add(int a, int b) {\n  return a + b;\n}\n"
                "std::vector<int> Foo::bar(const Opts& o) const {\n  if (o.x) {\n    return {};\n  }\n"
                "  return {1};\n}\n")
        found = functions(code, "cpp")
        self.assertEqual(found["add"].length, 3)
        self.assertEqual(found["Foo::bar"].length, 6)

    def test_ignore_marker(self):
        code = "// pelloux-ignore: generated table\nfunction big(a, b, c, d) {\n}\n"
        self.assertEqual(functions(code, "typescript"), {})


if __name__ == "__main__":
    unittest.main()
