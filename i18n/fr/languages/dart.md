# Dart et Flutter

Profil pour `.dart`. S'applique en plus des règles communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier, écran, widget | ≤ 300 lignes | 400 |
| Module d'entrée : repository, service, controller, notifier | ≤ 200 lignes | 200 |
| Fonction, méthode, `build()` | ≤ 25 lignes | 25 |
| Paramètres positionnels | ≤ 3 | 3, puis des paramètres nommés dans un seul groupe `{}` |

Un groupe de paramètres nommés `{required this.a, this.b}` compte comme un seul paramètre, comme un
objet d'options en TypeScript. Garder quand même le groupe court : au-delà de six valeurs nommées,
il manque une classe de modèle.

## Idiomes qui gardent le code dans les limites

- Un `build()` trop long se découpe en petites classes `StatelessWidget`, pas en méthodes helper
  `_buildHeader()` : les widgets se reconstruisent indépendamment et peuvent être `const`.
- Des constructeurs `const` partout où ça compile.
- Un seul client API pour toute l'app. Pas d'appels `http` bruts dans les widgets.
- Couleurs, espacements et typographie issus du design system (`AppDesign`, `ThemeData`). Pas de
  `Color(0x…)` en dur.
- Chaque chaîne vient de `context.l10n`. Les fichiers ARB restent alignés entre toutes les locales.
- L'état à un seul endroit par fonctionnalité (Riverpod, Bloc ou `ChangeNotifier`). Les widgets le
  lisent, ils ne portent pas de logique métier.
- Des imports `package:` (`package:app/widgets/x.dart`) plutôt que `../../../`.

## Ne jamais committer

`print(`, `debugPrint(` oubliés après une session de debug, `debugger()`, des données mockées dans
les écrans livrés, `// ignore:` sans justification.

## Faire respecter avec vos propres outils

`analysis_options.yaml` :

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

L'analyzer Dart n'a pas de règles de taille : l'audit Pelloux couvre les fichiers, les fonctions et
les paramètres.

## Vérifier avant de committer

```sh
dart format --output=none --set-exit-if-changed lib test
flutter analyze --fatal-infos
flutter test
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`test/`, `integration_test/`, `*.g.dart`, `*.freezed.dart`, `*.gr.dart`, code généré dans `l10n/`,
`build/`, `.dart_tool/`.
