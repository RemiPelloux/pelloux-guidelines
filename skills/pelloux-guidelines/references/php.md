# PHP

Profile for `.php`, for Laravel, Symfony and plain PHP. Applies on top of the core guidelines.

## Limits

| Scope | Target | Hard limit |
|---|---|---|
| Class file | ≤ 300 lines | 400 |
| Controller (`Http/Controllers/`, `Controller/`) | ≤ 200 lines | 200 |
| Method | ≤ 25 lines | 25 |
| Parameters | ≤ 4 | 4, then a Form Request, a DTO or an options array with a shape |

Constructors with promoted, injected dependencies are exempt from the parameter limit.

## Idioms that keep code inside the limits

- Thin controllers: validate with a Form Request, delegate to an action or a service, return a
  resource. No queries in controllers.
- One invokable action class per use case when a service grows past 200 lines.
- `readonly` DTOs instead of associative arrays passed around.
- `declare(strict_types=1);` at the top of every new file. Native types on every parameter,
  property and return.
- Eloquent: eager-load with `with()`, never query inside a loop.
- Translations through `__()` / `trans()`. No user-visible string in a controller.
- Imports one per line, grouped, formatted by Pint or PHP-CS-Fixer.

## Never commit

`dd(`, `dump(`, `var_dump(`, `print_r(`, `ray(`, `Log::debug(` added for a debugging session,
`exit;` in application code, `@` error suppression.

## Enforce it with your own tools

PHPStan at the highest level your codebase can hold, with a baseline for the rest:

```neon
# phpstan.neon
parameters:
  level: max
  paths: [app, src]
includes:
  - phpstan-baseline.neon
```

PHPMD for size and parameters (`phpmd.xml`):

```xml
<ruleset name="pelloux">
  <rule ref="rulesets/codesize.xml/ExcessiveMethodLength">
    <properties><property name="minimum" value="26"/><property name="ignore-whitespace" value="true"/></properties>
  </rule>
  <rule ref="rulesets/codesize.xml/ExcessiveParameterList">
    <properties><property name="minimum" value="5"/></properties>
  </rule>
  <rule ref="rulesets/codesize.xml/ExcessiveClassLength">
    <properties><property name="minimum" value="401"/></properties>
  </rule>
</ruleset>
```

## Verify before commit

```sh
php artisan test --filter=<YourTest>     # or: vendor/bin/phpunit --filter <YourTest>
vendor/bin/phpstan analyse
vendor/bin/pint --dirty                   # or: vendor/bin/php-cs-fixer fix
python3 .pelloux/pelloux.py audit --staged
```

## Exempt

`tests/`, `database/migrations/`, `database/seeders/`, `database/factories/`, `lang/`,
`resources/lang/`, `config/`, `vendor/`, `storage/`, `bootstrap/cache/`.
