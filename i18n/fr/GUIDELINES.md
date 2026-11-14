# Pelloux Guidelines

Une discipline de code pour les humains et les agents IA qui travaillent sur la même base de code.
Dix règles, quelques chiffres non négociables, et une machine qui les vérifie avant chaque commit.

Les profils de langage dans `languages/` ajoutent des limites, des idiomes et des réglages de
linter propres à chaque stack. Quand un profil donne un autre chiffre pour son langage, le profil
l'emporte. Tout le reste s'applique à tous les langages.

---

## 1. Terminer le travail

Exécuter la tâche de A à Z. Un plan, une modification partielle ou une liste d'étapes laissée à
l'utilisateur, ce n'est pas terminé.

- Si la commande peut être lancée, le fichier modifié, la config branchée ou le test exécuté, le
  faire soi-même.
- Pas de phrase de fin qui renvoie la balle, du type « vous pouvez maintenant… » ou « ensuite,
  lancez… », quand l'étape fait partie de la tâche et que l'accès est là pour la faire.
- Terminé veut dire que le résultat demandé fonctionne et qu'il est vérifié : tests, vérification
  des types et build passent sur ce qui a été touché.
- S'arrêter avant la fin uniquement en cas de vrai blocage : un secret manquant, une action
  destructive qui demande une validation, ou un choix produit que seul un humain peut faire. Dans
  ce cas, dire ce qui bloque, ce qui est terminé, et la plus petite information nécessaire pour
  continuer.

## 2. Réfléchir avant de coder

- Énoncer ses hypothèses. En cas de doute, demander.
- Quand une demande peut se lire de plusieurs façons, lister les lectures possibles. Ne pas en
  choisir une en silence.
- S'il existe une approche plus simple, le dire, et la défendre quand c'est justifié.
- Si quelque chose n'est pas clair, s'arrêter et poser la question avant d'écrire du code.

## 3. Choisir la correction la plus simple

Pour tout changement non trivial, nommer au moins trois approches avant d'écrire du code (une
ligne chacune) :

1. **Corriger au point de défaillance :** élargir une validation, changer une ligne de config,
   corriger l'hypothèse fausse.
2. **Contourner ailleurs :** une transformation côté appelant, un flag de plus, un adaptateur.
3. **Ajouter un nouveau pipeline ou une abstraction :** un nouveau module, un service ou un helper
   partagé.

Par défaut, (1). Si le choix se porte sur (2) ou (3), écrire une phrase qui explique pourquoi (1)
ne suffit pas. Ne pas ajouter de complexité côté client quand une allowlist côté serveur ou un
changement de config suffit.

## 4. Faire court

- Le minimum de code qui résout le problème. Rien de spéculatif.
- Pas d'abstraction pour du code utilisé une seule fois.
- Pas de flexibilité, d'option ou de configuration que personne n'a demandée.
- Pas de gestion d'erreur pour des cas qui ne peuvent pas arriver.
- Préférer la bibliothèque standard. Chaque nouvelle dépendance doit mériter sa place : écrire
  pourquoi.
- 200 lignes qui pourraient en faire 50 ? Les réécrire.

## 5. Ne changer que ce qui est demandé

- Ne toucher qu'à ce que la tâche exige. Chaque ligne modifiée doit se rattacher à la demande.
- Ne pas « améliorer » le code, les commentaires ou la mise en forme d'à côté.
- Suivre les patterns déjà en place dans la base de code, même si on l'aurait écrit autrement.
- Ne jamais lancer un formatter sur tout l'arbre en effet de bord. Formater les fichiers modifiés.
- Code mort déjà présent : le signaler, le laisser. Code rendu inutile par le changement : le
  supprimer.

## 6. Prouver

Découper la tâche en étapes vérifiables avant de modifier quoi que ce soit :

```
1. <step> → verify: <check>
2. <step> → verify: <check>
```

- Correction de bug : la reproduire d'abord avec un test ou une commande qui échoue, puis montrer
  qu'il passe.
- Changement de comportement : un test pour le cas nominal et un pour le cas d'échec.
- **Ne jamais mocker la fonctionnalité qu'on livre.** Mocker le réseau, l'horloge et les services
  tiers, pas le code testé. Un test qui passe alors que la fonctionnalité a été supprimée ne prouve
  rien.
- Ne jamais ignorer, désactiver ou assouplir un test qui échoue pour passer au vert. Corriger le
  code ou signaler l'échec.

## 7. Rester dans les limites

| Périmètre | Cible | Limite stricte |
|---|---|---|
| Fichier source | ≤ 300 lignes | 400 lignes |
| Module d'entrée : controller, route handler, hook, service | ≤ 200 lignes | 200 lignes |
| Fonction ou méthode | ≤ 25 lignes | 25 lignes |
| Paramètres | ≤ 3 | 3 (4 en PHP, Python, Go, Rust, C et C++) |
| Profondeur d'imbrication | ≤ 3 | 3 |

- La longueur d'une fonction compte les lignes non vides et hors commentaires, de la signature à la
  ligne de fermeture.
- Les paramètres n'incluent pas le receveur (`self`, `this`, `&self`). Au-delà de la limite, passer
  un objet d'options, une struct, une dataclass ou un objet de requête.
- Les constructeurs qui injectent des dépendances échappent à la limite de paramètres. Une longue
  liste à cet endroit veut dire que la classe en fait trop, et la limite de fichier le détectera.
- Pas de nombres magiques : utiliser des constantes nommées ou la config.
- Préférer les early returns aux conditions imbriquées.
- L'audit tolère 10 % de dépassement avant d'échouer (440 lignes pour un fichier, 220 pour un
  module d'entrée, 27 pour une fonction). La tolérance est pour la machine. La limite reste la
  cible à viser en écrivant.

**Exemptés :** tests, migrations, seeders, fichiers de traduction, code généré, code vendorisé et
données statiques. Les fichiers legacy qui dépassent la limite vont dans `pelloux-baseline.json`
(voir règle 10).

## 8. Ne laisser aucune trace de debug

- Aucune sortie de debug dans un commit : `console.log`, `print`, `dd`, `dump`, `var_dump`, `dbg!`,
  `breakpoint()`, `debugger`. Chaque profil liste les tokens propres à son langage.
- Pas de code commenté. Git s'en souvient.
- Pas de tests focalisés (`it.only`, `describe.only`) ni de marqueurs de conflit de merge.
- Pas de `as any`, `@ts-ignore`, `# type: ignore` ou `@SuppressWarnings` pour faire taire une vraie
  erreur.
- Aucun secret dans les fichiers. Utiliser un `.env` ignoré par git et tenir `.env.example` à jour.
- Supprimer les imports, fonctions et variables rendus inutiles par le changement.

## 9. Committer en bon coéquipier

- Conventional Commits : `<type>(<scope>): <imperative subject ≤ 72 chars>`. Types : `feat`, `fix`,
  `docs`, `test`, `refactor`, `perf`, `build`, `chore`.
- Un seul changement logique par commit.
- Stager par chemin explicite. Jamais `git add -A` ni `git add .` : un autre agent ou une autre
  personne peut partager le même working tree.
- Préserver le travail fait en parallèle. Merger, ne jamais écraser. Ne jamais force-push une
  branche partagée.
- Ne jamais contourner un hook en échec avec `--no-verify` sur un commit destiné à être déployé.
- Ne jamais pousser sur une branche de production, sauf si le dépôt indique que c'est le workflow.
- Les agents en parallèle travaillent dans des worktrees git séparés, une tâche chacun.

## 10. Laisser la machine vérifier

Une règle que personne ne vérifie finit par dériver. Chaque dépôt branche les limites à trois
endroits :

| Couche | Vérification |
|---|---|
| Boucle de l'agent | Le hook Claude Code prévient l'agent dès qu'un fichier qu'il modifie dépasse une limite stricte |
| Pre-commit | `pelloux audit --staged` sur les fichiers en cours de commit |
| CI | `pelloux audit` sur tout l'arbre, plus les linters natifs du profil de langage |

Le code legacy n'est jamais une raison de s'arrêter. `pelloux seed` enregistre toutes les
violations actuelles dans `pelloux-baseline.json`. Ensuite, l'effet cliquet s'applique : un fichier
ou une fonction de la liste peut rétrécir, jamais grossir, et rien de nouveau ne peut y entrer. Ne
relancer le seed que volontairement, dans un commit dédié.
