# C and C++

Profile for `.c`, `.h`, `.cc`, `.cpp`, `.cxx`, `.hpp` and `.hh`. Applies on top of the core
guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| Source or header file | ≤ 300 lines | 400 |
| Entry module: request handler, command, subsystem facade | ≤ 200 lines | 200 |
| Function | ≤ 25 lines | 25 |
| Parameters | ≤ 4 | 4, then a struct passed by `const&` or pointer |

## Idioms that keep code inside the limits

- One header, one responsibility. Include what you use, forward-declare the rest.
- RAII for every resource in C++: `std::unique_ptr`, `std::lock_guard`, scope guards. No naked
  `new` and `delete`.
- In C, one cleanup label per function (`goto out;`) instead of nested `if` ladders.
- A config struct with designated initializers (`(struct opts){ .retries = 3 }`) beats a fifth
  argument.
- `constexpr` and `enum class` instead of `#define` constants.
- `std::span`, `std::string_view` for non-owning views. Bounds-checked access in new code.
- Warnings are errors: `-Wall -Wextra -Wpedantic -Werror`.

## Never commit

`printf("DEBUG`, `fprintf(stderr, …)` added while debugging, `#if 0` blocks (commented-out code),
`// NOLINT` without a check name and a reason.

## Enforce it with your own tools

`.clang-tidy`:

```yaml
Checks: >
  bugprone-*, modernize-*, performance-*, readability-function-size,
  readability-magic-numbers, cppcoreguidelines-owning-memory
WarningsAsErrors: "*"
CheckOptions:
  - key: readability-function-size.LineThreshold
    value: 25
  - key: readability-function-size.ParameterThreshold
    value: 4
  - key: readability-function-size.NestingThreshold
    value: 3
```

Run tests under sanitizers at least in CI: `-fsanitize=address,undefined`.

## Verify before commit

```sh
clang-format --dry-run --Werror $(git diff --cached --name-only -- '*.c' '*.cpp' '*.h' '*.hpp')
clang-tidy -p build $(git diff --cached --name-only -- '*.c' '*.cpp')
cmake --build build && ctest --test-dir build
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`test/`, `tests/`, `third_party/`, `vendor/`, `external/`, generated headers, `build/`.
