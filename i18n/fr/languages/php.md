# PHP

Profil pour `.php`, pour Laravel, Symfony et PHP natif. S'applique en plus des règles communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier de classe | ≤ 300 lignes | 400 |
| Controller (`Http/Controllers/`, `Controller/`) | ≤ 200 lignes | 200 |
| Méthode | ≤ 25 lignes | 25 |
| Paramètres | ≤ 4 | 4, puis une Form Request, un DTO ou un tableau d'options typé (shape) |

Les constructeurs avec des dépendances injectées en propriétés promues échappent à la limite de
paramètres.

## Idiomes qui gardent le code dans les limites

- Des controllers minces : valider avec une Form Request, déléguer à une action ou à un service,
  retourner une resource. Pas de requêtes dans les controllers.
- Une classe d'action invokable par cas d'usage quand un service dépasse 200 lignes.
- Des DTO `readonly` plutôt que des tableaux associatifs qui circulent partout.
- `declare(strict_types=1);` en tête de chaque nouveau fichier. Des types natifs sur chaque
  paramètre, propriété et retour.
- Eloquent : eager-load avec `with()`, jamais de requête dans une boucle.
- Les traductions passent par `__()` / `trans()`. Aucune chaîne visible par l'utilisateur dans un
  controller.
- Un import par ligne, groupés, formatés par Pint ou PHP-CS-Fixer.

## Ne jamais committer

`dd(`, `dump(`, `var_dump(`, `print_r(`, `ray(`, `Log::debug(` ajoutés pour une session de debug,
`exit;` dans le code applicatif, la suppression d'erreurs avec `@`.

## Faire respecter avec vos propres outils

PHPStan au niveau le plus élevé que la base de code peut tenir, avec une baseline pour le reste :

```neon
# phpstan.neon
parameters:
  level: max
  paths: [app, src]
includes:
  - phpstan-baseline.neon
```

PHPMD pour la taille et les paramètres (`phpmd.xml`) :

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

## Vérifier avant de committer

```sh
php artisan test --filter=<YourTest>     # or: vendor/bin/phpunit --filter <YourTest>
vendor/bin/phpstan analyse
vendor/bin/pint --dirty                   # or: vendor/bin/php-cs-fixer fix
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`tests/`, `database/migrations/`, `database/seeders/`, `database/factories/`, `lang/`,
`resources/lang/`, `config/`, `vendor/`, `storage/`, `bootstrap/cache/`.
