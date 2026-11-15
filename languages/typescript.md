# TypeScript and JavaScript

Profile for `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs` and `.cjs`. Applies on top of the core guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| File, component, page | ≤ 300 lines | 400 |
| Hook (`hooks/`), service (`services/`), route handler (`routes/`, `api/`) | ≤ 200 lines | 200 |
| Function, component body, callback | ≤ 25 lines | 25 |
| Parameters | ≤ 3 | 3, then one typed options object |

A React component is a function: its body counts against the 25 lines. Split by extracting child
components and hooks, not by moving JSX into helper functions in the same file.

## Idioms that keep code inside the limits

- One options object instead of a fourth parameter: `createUser({ email, role, invitedBy })`.
- `type Props` next to the component, destructured in the signature.
- Data fetching lives in a hook or a query function, never inline in a component.
- One HTTP client for the whole app. No raw `fetch` or `axios` calls scattered in components.
- Narrow with type guards and `satisfies`, not with casts.
- Early `return` for loading, empty and error states before the main JSX.
- Every user-visible string goes through the i18n layer. No ternaries on the locale.
- Imports start at the project root through a `@/` alias (`paths` in `tsconfig.json`, `resolve.alias` in Vite). Two `../` at most.

## Never commit

`console.log`, `console.debug`, `debugger`, `it.only`, `describe.only`, `test.only`, `as any`,
`@ts-ignore`, `@ts-expect-error` used to silence a real error, `// eslint-disable` without a reason
on the same line.

## Enforce it with your own tools

`eslint.config.js`, with `typescript-eslint` loaded:

```js
export default [
  {
    files: ["**/*.{ts,tsx,js,jsx}"],
    ignores: ["**/*.test.*", "**/*.spec.*", "**/locales/**", "**/*.d.ts", "dist/**"],
    rules: {
      "max-lines": ["error", { max: 400, skipBlankLines: true, skipComments: true }],
      "max-lines-per-function": ["error", { max: 25, skipBlankLines: true, skipComments: true }],
      "max-params": ["error", 3],
      "max-depth": ["error", 3],
      "no-magic-numbers": ["warn", { ignore: [-1, 0, 1, 2], ignoreArrayIndexes: true }],
      "no-console": ["error", { allow: ["warn", "error"] }],
      "no-debugger": "error",
      "no-restricted-imports": ["error", { patterns: [{ group: ["../../../*"], message: "Import from @/ instead" }] }],
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/ban-ts-comment": "error",
    },
  },
];
```

On a legacy codebase, start these at `warn` and use ESLint bulk suppressions
(`eslint --suppress-all`, then `--prune-suppressions` as files shrink) so the count only goes down.

## Verify before commit

```sh
npx tsc --noEmit
npx eslint --max-warnings 0 $(git diff --cached --name-only --diff-filter=ACMR -- '*.ts' '*.tsx')
npx vitest run --changed     # or: npx jest --onlyChanged
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`*.test.*`, `*.spec.*`, `__tests__/`, `*.d.ts`, `locales/`, `i18n/`, generated clients, `dist/`,
`build/`, `.next/`, `node_modules/`.
