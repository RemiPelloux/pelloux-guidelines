# Rust

Profil pour `.rs`. S'applique en plus des règles communes.

## Limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier de module | ≤ 300 lignes | 400 |
| Module d'entrée : handler HTTP, commande, service | ≤ 200 lignes | 200 |
| Fonction ou méthode | ≤ 25 lignes | 25 |
| Paramètres (hors `self`) | ≤ 4 | 4, puis une struct de config ou un builder |

## Idiomes qui gardent le code dans les limites

- Découper un module qui grossit en répertoire : `mod.rs` réexporte, un fichier par responsabilité.
- `?` et retours anticipés plutôt que des `match` imbriqués sur `Result`.
- `thiserror` pour les erreurs de bibliothèque, `anyhow` en bordure du binaire. Pas de `unwrap()` ni
  de `expect()` hors des tests, du setup de `main` et des invariants documentés dans le message.
- Des newtypes plutôt que des arguments primitifs (`UserId(u64)`, pas `u64`) pour que quatre
  paramètres restent lisibles.
- Un builder ou une struct `Config` avec `Default` quand un constructeur a besoin de plus de quatre
  valeurs.
- `#![forbid(unsafe_code)]` dans les crates qui n'ont pas besoin d'`unsafe`. Là où c'est nécessaire,
  un commentaire `// SAFETY:` par bloc.
- Emprunter par défaut (`&str`, `&[T]`), ne posséder que pour stocker.

## Ne jamais committer

`dbg!(`, `todo!()` et `unimplemented!()` sur du code livré, `println!` utilisé pour débugger dans
une bibliothèque, `#[allow(...)]` sans commentaire de justification.

## Faire respecter avec vos propres outils

`clippy.toml` :

```toml
too-many-arguments-threshold = 4
too-many-lines-threshold = 25
cognitive-complexity-threshold = 15
```

Puis activer les lints désactivés par défaut :

```sh
cargo clippy --all-targets -- -D warnings \
  -W clippy::too_many_lines -W clippy::dbg_macro -W clippy::todo \
  -W clippy::unwrap_used -W clippy::print_stdout
```

## Vérifier avant de committer

```sh
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
python3 .pelloux/pelloux.py audit --staged
```

## Exemptés

`tests/`, `benches/`, `examples/`, modules `#[cfg(test)]` (les garder dans un `tests.rs` à côté du
module), sortie de `build.rs`, `target/`.
