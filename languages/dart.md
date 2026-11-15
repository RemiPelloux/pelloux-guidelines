# Dart and Flutter

Profile for `.dart`. Applies on top of the core guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| File, screen, widget | ≤ 300 lines | 400 |
| Entry module: repository, service, controller, notifier | ≤ 200 lines | 200 |
| Function, method, `build()` | ≤ 25 lines | 25 |
| Positional parameters | ≤ 3 | 3, then named parameters in one `{}` group |

A group of named parameters `{required this.a, this.b}` counts as one parameter, the way an options
object does in TypeScript. Keep the group short anyway: more than six named values is a missing
model class.

## Idioms that keep code inside the limits

- A long `build()` becomes small `StatelessWidget` classes, not `_buildHeader()` helper methods:
  widgets rebuild independently and can be `const`.
- `const` constructors everywhere they compile.
- One API client for the whole app. No raw `http` calls in widgets.
- Colors, spacing and type from the design system (`AppDesign`, `ThemeData`). No raw `Color(0x…)`.
- Every string from `context.l10n`. The ARB files stay in parity across locales.
- State in one place per feature (Riverpod, Bloc or `ChangeNotifier`). Widgets read it, they do
  not own business logic.
- `package:` imports (`package:app/widgets/x.dart`) instead of `../../../`.

## Never commit

`print(`, `debugPrint(` left from a debugging session, `debugger()`, mock data in shipped screens,
`// ignore:` without a reason.

## Enforce it with your own tools

`analysis_options.yaml`:

```yaml
include: package:flutter_lints/flutter.yaml
analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
linter:
  rules:
    avoid_print: true
    prefer_const_constructors: true
    prefer_final_locals: true
    always_declare_return_types: true
    avoid_dynamic_calls: true
    always_use_package_imports: true
```

The Dart analyzer has no size rules: the Pelloux audit covers files, functions and parameters.

## Verify before commit

```sh
dart format --output=none --set-exit-if-changed lib test
flutter analyze --fatal-infos
flutter test
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`test/`, `integration_test/`, `*.g.dart`, `*.freezed.dart`, `*.gr.dart`, `l10n/` generated code,
`build/`, `.dart_tool/`.
