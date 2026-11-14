# Rust

Profile for `.rs`. Applies on top of the core guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| Module file | ≤ 300 lines | 400 |
| Entry module: HTTP handler, command, service | ≤ 200 lines | 200 |
| Function or method | ≤ 25 lines | 25 |
| Parameters (excluding `self`) | ≤ 4 | 4, then a config or builder struct |

## Idioms that keep code inside the limits

- Split a growing module into a directory: `mod.rs` re-exports, one file per concern.
- `?` and early returns instead of nested `match` on `Result`.
- `thiserror` for library errors, `anyhow` at the binary edge. No `unwrap()` or `expect()` outside
  tests, `main` setup and invariants you document in the message.
- Newtypes over primitive arguments (`UserId(u64)`, not `u64`) so four parameters stay readable.
- A builder or a `Config` struct with `Default` when a constructor needs more than four values.
- `#![forbid(unsafe_code)]` in crates that do not need `unsafe`. Where you need it, one
  `// SAFETY:` comment per block.
- Borrow by default (`&str`, `&[T]`), own only when you store.

## Never commit

`dbg!(`, `todo!()` and `unimplemented!()` on a shipped path, `println!` used for debugging in a
library, `#[allow(...)]` without a reason comment.

## Enforce it with your own tools

`clippy.toml`:

```toml
too-many-arguments-threshold = 4
too-many-lines-threshold = 25
cognitive-complexity-threshold = 15
```

Then turn on the lints that are off by default:

```sh
cargo clippy --all-targets -- -D warnings \
  -W clippy::too_many_lines -W clippy::dbg_macro -W clippy::todo \
  -W clippy::unwrap_used -W clippy::print_stdout
```

## Verify before commit

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`tests/`, `benches/`, `examples/`, `#[cfg(test)]` modules (keep them in `tests.rs` beside the
module), `build.rs` output, `target/`.
