# Go

Profil pour `.go`. S'applique en plus des règles communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier | ≤ 300 lignes | 400 |
| Module d'entrée : handler HTTP, service gRPC, commande | ≤ 200 lignes | 200 |
| Fonction ou méthode | ≤ 25 lignes | 25 |
| Paramètres (hors receveur ; `ctx` compte) | ≤ 4 | 4, puis une struct d'options |

## Idiomes qui gardent le code dans les limites

- `ctx context.Context` en premier, puis trois valeurs au maximum. Au-delà, une struct `Params` ou
  `Options`.
- Retourner tôt sur `err != nil`. Wrapper avec `fmt.Errorf("doing x: %w", err)`, une fois par
  couche.
- De petites interfaces définies là où elles sont utilisées, pas là où elles sont implémentées.
- Un package par responsabilité. Un fichier par type dès qu'un fichier dépasse 300 lignes.
- Des tests table-driven avec `t.Run`.
- `log/slog` pour les logs structurés. Pas de `fmt.Println` dans les services.

## Ne jamais committer

Les built-ins `println(` et `print(`, `spew.Dump(`, `fmt.Printf("DEBUG`, `//nolint` sans nom de
linter ni justification, des erreurs ignorées (`_ = f()`) sans commentaire.

## Faire respecter avec vos propres outils

`.golangci.yml` (golangci-lint v2) :

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

## Vérifier avant de committer

```sh
gofmt -l . && go vet ./...
golangci-lint run
go test ./...
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`*_test.go`, `*.pb.go`, `*_gen.go`, `zz_generated.*`, `mock_*.go`, `vendor/`, `testdata/`.
