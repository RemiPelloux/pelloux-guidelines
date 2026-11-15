# C et C++

Profil pour `.c`, `.h`, `.cc`, `.cpp`, `.cxx`, `.hpp` et `.hh`. S'applique en plus des règles
communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier source ou header | ≤ 300 lignes | 400 |
| Module d'entrée : request handler, commande, façade de sous-système | ≤ 200 lignes | 200 |
| Fonction | ≤ 25 lignes | 25 |
| Paramètres | ≤ 4 | 4, puis une struct passée par `const&` ou par pointeur |

## Idiomes qui gardent le code dans les limites

- Un header, une responsabilité. Inclure ce qu'on utilise, déclarer le reste en forward declaration.
- RAII pour chaque ressource en C++ : `std::unique_ptr`, `std::lock_guard`, scope guards. Pas de
  `new` ni de `delete` nus.
- En C, un seul label de nettoyage par fonction (`goto out;`) au lieu d'une cascade de `if`
  imbriqués.
- Une struct de config avec des designated initializers (`(struct opts){ .retries = 3 }`) vaut
  mieux qu'un cinquième argument.
- `constexpr` et `enum class` plutôt que des constantes en `#define`.
- `std::span`, `std::string_view` pour les vues non propriétaires. Accès avec contrôle des bornes
  dans le nouveau code.
- Les warnings sont des erreurs : `-Wall -Wextra -Wpedantic -Werror`.
- Les racines du code dans le chemin d'include (`target_include_directories`) plutôt que `#include "../../../x.h"`.

## Ne jamais committer

`printf("DEBUG`, `fprintf(stderr, …)` ajouté pendant le debug, blocs `#if 0` (code commenté),
`// NOLINT` sans nom de check ni justification.

## Faire respecter avec vos propres outils

`.clang-tidy` :

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

Lancer les tests sous sanitizers, au minimum en CI : `-fsanitize=address,undefined`.

## Vérifier avant de committer

```sh
clang-format --dry-run --Werror $(git diff --cached --name-only -- '*.c' '*.cpp' '*.h' '*.hpp')
clang-tidy -p build $(git diff --cached --name-only -- '*.c' '*.cpp')
cmake --build build && ctest --test-dir build
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`test/`, `tests/`, `third_party/`, `vendor/`, `external/`, headers générés, `build/`.
