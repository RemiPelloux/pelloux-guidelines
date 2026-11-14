# TypeScript et JavaScript

Profil pour `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs` et `.cjs`. S'applique en plus des règles communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier, composant, page | ≤ 300 lignes | 400 |
| Hook (`hooks/`), service (`services/`), route handler (`routes/`, `api/`) | ≤ 200 lignes | 200 |
| Fonction, corps de composant, callback | ≤ 25 lignes | 25 |
| Paramètres | ≤ 3 | 3, puis un seul objet d'options typé |

Un composant React est une fonction : son corps compte dans les 25 lignes. Le découper en extrayant
des composants enfants et des hooks, pas en déplaçant du JSX dans des fonctions helper du même
fichier.

## Idiomes qui gardent le code dans les limites

- Un objet d'options plutôt qu'un quatrième paramètre : `createUser({ email, role, invitedBy })`.
- `type Props` à côté du composant, déstructuré dans la signature.
- Le data fetching vit dans un hook ou une fonction de query, jamais inline dans un composant.
- Un seul client HTTP pour toute l'app. Pas d'appels `fetch` ou `axios` bruts éparpillés dans les
  composants.
- Affiner les types avec des type guards et `satisfies`, pas avec des casts.
- `return` anticipé pour les états de chargement, vide et erreur, avant le JSX principal.
- Chaque chaîne visible par l'utilisateur passe par la couche i18n. Pas de ternaires sur la locale.

## Ne jamais committer

`console.log`, `console.debug`, `debugger`, `it.only`, `describe.only`, `test.only`, `as any`,
`@ts-ignore`, `@ts-expect-error` utilisé pour faire taire une vraie erreur, `// eslint-disable` sans
justification sur la même ligne.

## Faire respecter avec vos propres outils

`eslint.config.js`, avec `typescript-eslint` chargé :

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
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/ban-ts-comment": "error",
    },
  },
];
```

Sur une base de code legacy, démarrer ces règles en `warn` et utiliser les bulk suppressions
d'ESLint (`eslint --suppress-all`, puis `--prune-suppressions` au fur et à mesure que les fichiers
rétrécissent) pour que le compteur ne fasse que baisser.

## Vérifier avant de committer

```sh
npx tsc --noEmit
npx eslint --max-warnings 0 $(git diff --cached --name-only --diff-filter=ACMR -- '*.ts' '*.tsx')
npx vitest run --changed     # or: npx jest --onlyChanged
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`*.test.*`, `*.spec.*`, `__tests__/`, `*.d.ts`, `locales/`, `i18n/`, clients générés, `dist/`,
`build/`, `.next/`, `node_modules/`.
