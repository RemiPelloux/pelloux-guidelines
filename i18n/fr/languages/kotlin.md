# Kotlin

Profil pour `.kt` et `.kts`, pour Android, Compose et la JVM. S'applique en plus des règles
communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier, écran | ≤ 300 lignes | 400 |
| Module d'entrée : ViewModel, repository, service, controller | ≤ 200 lignes | 200 |
| Fonction, `@Composable` | ≤ 25 lignes | 25 |
| Paramètres | ≤ 3 | 3, puis une data class |

Les fonctions `@Composable` prennent souvent un `modifier` et des callbacks. Regrouper les
callbacks dans une data class `Actions` ou une interface plutôt que de passer cinq lambdas.

## Idiomes qui gardent le code dans les limites

- Des data classes pour tout ce qui dépasse trois valeurs. Des arguments nommés à l'appel.
- `sealed interface` pour l'état de l'UI : `Loading`, `Content`, `Error`. Un seul `when`, pas de
  flags booléens.
- Coroutines et `Flow`. Pas de `GlobalScope`. Rattacher le travail à `viewModelScope` ou à un scope
  structuré.
- Des expression bodies (`fun total() = items.sumOf { it.price }`) pour les one-liners.
- `?.let`, `?:` et `return` anticipé plutôt que des null checks imbriqués. Pas de `!!` hors des
  tests.
- Les chaînes viennent de `strings.xml` (`stringResource`), jamais en dur dans un Composable.

## Ne jamais committer

`println(`, `printStackTrace()`, `Log.d(` ajoutés pendant le debug, `!!` sur du code livré,
`@Suppress` sans justification.

## Faire respecter avec vos propres outils

`detekt.yml` :

```yaml
complexity:
  LongMethod:
    active: true
    threshold: 25
  LongParameterList:
    active: true
    functionThreshold: 4
    constructorThreshold: 8
    ignoreDefaultParameters: false
  LargeClass:
    active: true
    threshold: 400
  NestedBlockDepth:
    active: true
    threshold: 4
style:
  MagicNumber:
    active: true
  ForbiddenMethodCall:
    active: true
    methods:
      - "kotlin.io.println"
      - "kotlin.io.print"
```

Selon l'outil, un seuil est inclusif ou non. L'audit Pelloux fait référence pour les chiffres
exacts.

## Vérifier avant de committer

```sh
./gradlew ktlintCheck detekt
./gradlew testDebugUnitTest      # or: ./gradlew test
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`src/test/`, `src/androidTest/`, `build/`, sources générées (`build/generated/`), scripts de build
`*.gradle.kts`.
