# Kotlin

Profile for `.kt` and `.kts`, for Android, Compose and the JVM. Applies on top of the core
guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| File, screen | ≤ 300 lines | 400 |
| Entry module: ViewModel, repository, service, controller | ≤ 200 lines | 200 |
| Function, `@Composable` | ≤ 25 lines | 25 |
| Parameters | ≤ 3 | 3, then a data class |

`@Composable` functions often take a `modifier` and callbacks. Group the callbacks into one
`Actions` data class or an interface instead of passing five lambdas.

## Idioms that keep code inside the limits

- Data classes for anything with more than three values. Named arguments at call sites.
- `sealed interface` for UI state: `Loading`, `Content`, `Error`. One `when`, no boolean flags.
- Coroutines and `Flow`. No `GlobalScope`. Scope work to `viewModelScope` or a structured scope.
- Expression bodies (`fun total() = items.sumOf { it.price }`) for one-liners.
- `?.let`, `?:` and early `return` instead of nested null checks. No `!!` outside tests.
- Strings from `strings.xml` (`stringResource`), never hard-coded in a Composable.

## Never commit

`println(`, `printStackTrace()`, `Log.d(` added while debugging, `!!` on shipped paths,
`@Suppress` without a reason.

## Enforce it with your own tools

`detekt.yml`:

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

Tools differ on whether a threshold is inclusive. The Pelloux audit is the reference for the exact
numbers.

## Verify before commit

```sh
./gradlew ktlintCheck detekt
./gradlew testDebugUnitTest      # or: ./gradlew test
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`src/test/`, `src/androidTest/`, `build/`, generated sources (`build/generated/`), `*.gradle.kts`
build scripts.
