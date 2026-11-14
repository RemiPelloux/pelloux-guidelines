# Go

Profile for `.go`. Applies on top of the core guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| File | ≤ 300 lines | 400 |
| Entry module: HTTP handler, gRPC service, command | ≤ 200 lines | 200 |
| Function or method | ≤ 25 lines | 25 |
| Parameters (excluding the receiver; `ctx` counts) | ≤ 4 | 4, then an options struct |

## Idioms that keep code inside the limits

- `ctx context.Context` first, then at most three values. Beyond that, a `Params` or `Options`
  struct.
- Return early on `err != nil`. Wrap with `fmt.Errorf("doing x: %w", err)`, once per layer.
- Small interfaces defined where they are used, not where they are implemented.
- One package per concern. A file per type once a file passes 300 lines.
- Table-driven tests with `t.Run`.
- `log/slog` for structured logs. No `fmt.Println` in services.

## Never commit

`println(` and `print(` built-ins, `spew.Dump(`, `fmt.Printf("DEBUG`, `//nolint` without a linter
name and a reason, ignored errors (`_ = f()`) without a comment.

## Enforce it with your own tools

`.golangci.yml` (golangci-lint v2):

```yaml
version: "2"
linters:
  enable: [funlen, gocyclo, mnd, forbidigo, revive]
  settings:
    funlen:
      lines: 25
      statements: -1
      ignore-comments: true
    gocyclo:
      min-complexity: 10
    forbidigo:
      forbid:
        - pattern: ^print(ln)?$
        - pattern: ^spew\.
    revive:
      rules:
        - name: argument-limit
          arguments: [4]
        - name: file-length-limit
          arguments: [{ max: 400, skipComments: true, skipBlankLines: true }]
```

## Verify before commit

```sh
gofmt -l . && go vet ./...
golangci-lint run
go test ./...
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`*_test.go`, `*.pb.go`, `*_gen.go`, `zz_generated.*`, `mock_*.go`, `vendor/`, `testdata/`.
