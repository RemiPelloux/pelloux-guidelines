# Swift

Profil pour `.swift`, pour SwiftUI, UIKit et Swift côté serveur. S'applique en plus des règles
communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier, vue | ≤ 300 lignes | 400 |
| Module d'entrée : view model, service, store | ≤ 200 lignes | 200 |
| Fonction, méthode, `body` | ≤ 25 lignes | 25 |
| Paramètres | ≤ 3 | 3, puis une struct |

## Idiomes qui gardent le code dans les limites

- Un `body` SwiftUI trop long se découpe en petites structs `View`, pas en computed properties dans
  le même fichier.
- `guard let` et `return` anticipé plutôt que des `if let` imbriqués.
- `struct` et `enum` par défaut, `class` uniquement pour l'identité ou la sémantique de référence.
- `async`/`await` et concurrence structurée. Pas de pyramides de completion handlers dans le
  nouveau code.
- Un seul client réseau. Les vues ne construisent jamais de `URLRequest`.
- Les chaînes viennent de `Localizable.xcstrings` (`String(localized:)`). Couleurs et polices
  issues de l'asset catalog ou du design system.
- Pas de force unwrap (`!`) ni de `try!` hors des tests et des invariants documentés.

## Ne jamais committer

`print(`, `debugPrint(`, `dump(`, `fatalError("TODO")` sur du code livré, `// swiftlint:disable`
sans justification.

## Faire respecter avec vos propres outils

`.swiftlint.yml` :

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

## Vérifier avant de committer

```sh
swiftlint --strict
swift build && swift test        # or: xcodebuild test -scheme <Scheme>
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`*Tests/`, `*UITests/`, `Generated/`, `*.generated.swift`, `Pods/`, `.build/`, `DerivedData/`.
