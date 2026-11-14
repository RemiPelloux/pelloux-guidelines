# Swift

Profile for `.swift`, for SwiftUI, UIKit and server-side Swift. Applies on top of the core
guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| File, view | ≤ 300 lines | 400 |
| Entry module: view model, service, store | ≤ 200 lines | 200 |
| Function, method, `body` | ≤ 25 lines | 25 |
| Parameters | ≤ 3 | 3, then a struct |

## Idioms that keep code inside the limits

- A long SwiftUI `body` becomes small `View` structs, not computed properties in the same file.
- `guard let` and early `return` instead of nested `if let`.
- `struct` and `enum` by default, `class` only for identity or reference semantics.
- `async`/`await` and structured concurrency. No completion-handler pyramids in new code.
- One networking client. Views never build a `URLRequest`.
- Strings from `Localizable.xcstrings` (`String(localized:)`). Colors and fonts from the asset
  catalog or the design system.
- No force unwrap (`!`) or `try!` outside tests and documented invariants.

## Never commit

`print(`, `debugPrint(`, `dump(`, `fatalError("TODO")` on a shipped path, `// swiftlint:disable`
without a reason.

## Enforce it with your own tools

`.swiftlint.yml`:

```yaml
file_length:
  warning: 300
  error: 400
type_body_length:
  warning: 200
  error: 300
function_body_length:
  warning: 25
  error: 30
function_parameter_count:
  warning: 3
  error: 4
cyclomatic_complexity:
  warning: 8
  error: 12
nesting:
  type_level: 2
  function_level: 3
force_unwrapping: error
custom_rules:
  no_debug_print:
    regex: '^\s*(print|debugPrint|dump)\('
    message: "Remove debug output before committing"
    severity: error
opt_in_rules:
  - force_unwrapping
```

## Verify before commit

```sh
swiftlint --strict
swift build && swift test        # or: xcodebuild test -scheme <Scheme>
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`*Tests/`, `*UITests/`, `Generated/`, `*.generated.swift`, `Pods/`, `.build/`, `DerivedData/`.
