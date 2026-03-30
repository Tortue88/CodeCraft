# Instructions pour Claude Code — CodeCraft MVP : Niveaux 6 à 10

## Contexte

Le fichier `codecraft_mvp.py` est un jeu de programmation en pygame.
Le joueur écrit du code dans un éditeur intégré pour déplacer Steve (carré bleu)
jusqu'à un coffre (C) sur une grille 12×10.

Les niveaux 1 à 5 existent déjà et couvrent les commandes de déplacement de base.
Tu dois ajouter les niveaux 6 à 10 avec un système de craft inspiré de Minecraft.

---

## Architecture existante à comprendre avant de modifier

### Structure d'un niveau (dans la liste `NIVEAUX`)
```python
{
    "titre": "Niveau N  -  Nom",
    "hint":  "Texte d'aide affiché dans la barre de statut",
    "carte": [
        "AAAAAAAAAAAA",   # 12 colonnes
        "A..........A",   # 10 lignes
        ...
        "AAAAAAAAAAAA",
    ],
    "sx": 1, "sy": 1, "sdir": EST,   # position/direction de départ de Steve
    "code": [                          # code pré-rempli dans l'éditeur
        "# Commentaire",
        "avancer(?)",
    ],
}
```

### Tuiles existantes
```
'.' = herbe       (passable)
'~' = eau         (impassable)
'A' = arbre       (impassable)
'#' = pierre      (impassable)
's' = sable       (passable)
'C' = coffre      (objectif — déclenche la victoire)
```

### Commandes existantes (dans `compiler()`)
- `avancer(n)` → n pas en avant
- `reculer(n)` → n pas en arrière
- `tourner_droite()` → +90°
- `tourner_gauche()` → -90°
- `demi_tour()` → 180°

### Inventaire
Il n'existe pas encore. Tu dois le créer.

### Fonctions clés
- `compiler(code)` → parse les lignes, retourne `(etapes, erreurs)`
- `jouer_prochaine_etape()` → exécute une étape de la file
- `log(texte, couleur)` → affiche un message dans la console
- `charger_niveau(n)` → charge le niveau n
- `recalculer_layout()` → recalcule toutes les zones d'UI

---

## Ce que tu dois implémenter

### 1. Inventaire global

Ajoute un dictionnaire global `inventaire` :
```python
inventaire = {}   # ex: {"bois": 2, "baton": 4, ...}
```

Réinitialise-le dans `reinitialiser()` à chaque niveau.

Affiche l'inventaire dans le panneau entre la carte et l'éditeur
(une zone `ZONE_INVENTAIRE`) — une ligne par ressource possédée,
format : `bois x2`, `baton x4`, etc.
N'afficher la zone que si l'inventaire n'est pas vide.

---

### 2. Nouvelles tuiles

Ajoute ces caractères dans `TUILE_COULEUR` et `IMPASSABLE` :

| Char | Nom          | Passable | Couleur suggérée    | Notes                        |
|------|--------------|----------|---------------------|------------------------------|
| `T`  | Etabli       | non      | (180, 120, 40)      | crafting table               |
| `B`  | Arbre abattu | oui      | (140, 90, 30)       | après avoir brisé un arbre   |
| `R`  | Pierre brisée| oui      | (160, 160, 160)     | après avoir brisé de la pierre|

Les tuiles `A` et `#` restent impassables jusqu'à être brisées.

---

### 3. Nouvelles commandes

Ajoute ces commandes dans `compiler()` ET dans `AIDE_CMDS` (helper visuel).

#### `briser()`
- Steve brise la tuile **devant** lui (dans sa direction).
- Si la tuile devant est `'A'` (arbre) :
  - La tuile devient `'B'` (arbre abattu, passable).
  - Ajoute 2 `bois` à l'inventaire.
  - Log : `"Arbre brisé ! +2 bois"`
- Si la tuile devant est `'#'` (pierre) et Steve a une `pioche_bois` dans l'inventaire :
  - La tuile devient `'R'` (pierre brisée, passable).
  - Log : `"Pierre brisée ! La pioche en bois est usée."`
  - Retire la `pioche_bois` de l'inventaire.
- Sinon : log une erreur et arrête l'exécution.

#### `placer_etabli()`
- Steve place un établi sur la tuile **devant** lui.
- Condition : avoir au moins 4 `bois` dans l'inventaire.
- La tuile devant doit être `'.'` (herbe) ou `'B'`.
- La tuile devient `'T'`.
- Retire 4 `bois` de l'inventaire.
- Log : `"Etabli posé ! (-4 bois)"`
- Sinon : log une erreur et arrête.

#### `ouvrir_etabli()`
- Steve ouvre l'établi sur la tuile **devant** lui.
- Condition : la tuile devant est `'T'`.
- Ne fait que valider l'état — active un flag `etabli_ouvert = True`.
- Log : `"Etabli ouvert."`
- Sinon : log une erreur et arrête.

#### `crafter_batons()`
- Condition : `etabli_ouvert` est True ET avoir au moins 2 `bois`.
- Retire 2 `bois`, ajoute 4 `baton`.
- Remet `etabli_ouvert = False`.
- Log : `"Crafté : 4 bâtons ! (-2 bois)"`

#### `crafter_pioche_bois()`
- Condition : `etabli_ouvert` est True ET avoir au moins 3 `bois` ET 2 `baton`.
- Retire 3 `bois` et 2 `baton`, ajoute 1 `pioche_bois`.
- Remet `etabli_ouvert = False`.
- Log : `"Crafté : pioche en bois ! (-3 bois, -2 bâtons)"`

---

### 4. Niveaux 6 à 10

Ajoute ces 5 niveaux à la fin de la liste `NIVEAUX`.

---

#### Niveau 6 — "Abattage"

**Objectif** : Un arbre bloque le chemin direct. Steve doit le briser.

**Carte** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..........A
A....A....CA    ← arbre en col 5, coffre en col 10
A..........A
A..........A
A..........A
AAAAAAAAAAAA
```
Steve démarre en (1, 5), face EST.

**Code starter** :
```python
# Niveau 6 : Un arbre bloque la route !
# Avancez jusqu'a l'arbre, brisez-le, continuez.

avancer(3)
briser()
avancer(?)
```

**Hint** : `"briser() detruit la tuile devant Steve"`

**Solution** : `avancer(3), briser(), avancer(6)`

---

#### Niveau 7 — "La forêt"

**Objectif** : Deux arbres bloquent le chemin. Steve doit en abattre deux.

**Carte** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..........A
A..A..A...CA    ← arbres en col 3 et col 6
A..........A
A..........A
A..........A
AAAAAAAAAAAA
```
Steve démarre en (1, 5), face EST.

**Code starter** :
```python
# Niveau 7 : Deux arbres bloquent la route !
# Brisez-les un par un.

avancer(1)
briser()
avancer(?)
briser()
avancer(?)
```

**Hint** : `"Brisez les arbres un par un"`

**Solution** : `avancer(1), briser(), avancer(2), briser(), avancer(3)`

---

#### Niveau 8 — "Poser l'établi"

**Objectif** : Le coffre est bloqué par de la pierre. Steve doit abattre un arbre,
collecter du bois, poser un établi sur l'herbe libre devant lui.
(Ce niveau ne demande PAS encore de briser la pierre — juste de poser l'établi.)

**Carte** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..A.......A    ← arbre en col 3
A.........#A    ← pierre en col 10 (devant le coffre, mais le coffre n'est pas visible)
A.........CA    ← coffre en col 10, ligne 6
A..........A
A..........A
AAAAAAAAAAAA
```

Attends — simplifie : le coffre est accessible directement ici,
mais Steve doit D'ABORD poser un établi (condition de victoire étendue :
vérifier que `'T'` existe quelque part sur la carte en plus d'atteindre `'C'`).

**Alternative plus simple** : La carte a un arbre en col 3 ligne 5, et le coffre
est en col 10 ligne 5. Pour atteindre le coffre, il faut passer par col 3 (arbre).
De plus, une zone herbe en col 5 ligne 5 doit avoir un établi posé
avant que Steve puisse continuer (validation : vérifier `etabli_ouvert` a été utilisé).

**Implémentation recommandée** — utilise une "condition de victoire spéciale" :

Ajoute un champ optionnel `"condition"` dans le dictionnaire de niveau :
```python
"condition": lambda: 'T' in [CARTE[l][c] for l in range(NB_LIG) for c in range(NB_COL)]
```
Si ce champ existe, la victoire requiert aussi que cette condition soit vraie.

**Carte finale** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..........A
A..A......CA    ← arbre col 3, coffre col 10
A..........A
A..........A
A..........A
AAAAAAAAAAAA
```
Steve démarre en (1, 5), face EST.

**Code starter** :
```python
# Niveau 8 : Collectez du bois et posez un etabli !
# briser() sur un arbre donne 2 bois.
# Il faut 4 bois pour placer_etabli().

avancer(1)
briser()
avancer(1)
briser()
placer_etabli()
avancer(?)
```

**Hint** : `"Abattez 2 arbres, posez l'etabli, puis avancez"`

**Solution** :
```
avancer(1), briser(),   # +2 bois (total: 2)
avancer(1), briser(),   # impossible, 1 seul arbre en col 3
```

**Révise la carte pour avoir 2 arbres** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..........A
A.AA......CA    ← arbres col 2 et col 3, coffre col 10
A..........A
A..........A
A..........A
AAAAAAAAAAAA
```
Solution : `avancer(0), briser(), avancer(0), briser(), placer_etabli(), avancer(6)`

Ajuste les positions de départ et le nombre d'avancer() pour que ça soit cohérent.

---

#### Niveau 9 — "La pioche"

**Objectif** : La pierre bloque le chemin. Steve doit collecter du bois,
poser un établi, ouvrir l'établi, crafter des bâtons, crafter une pioche,
puis briser la pierre.

**Carte** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..........A
AAAA...#..CA    ← mur d'arbres abattables col 1-3, pierre col 7, coffre col 10
A..........A
A..........A
A..........A
AAAAAAAAAAAA
```

Steve démarre en (4, 5), face EST (déjà passé les arbres, on commence propre).
Il y a 3 arbres en col 1, 2, 3 (mais Steve part de col 4 — pas d'arbres à abattre ici).

**Simplifie** : Mets 3 arbres en cols 5, 6, 7 et Pierre en col 8.
Steve part de (1,5) face EST, doit avancer jusqu'aux arbres, les abattre (6 bois),
poser l'établi, crafter bâtons + pioche, puis briser la pierre.

**Carte finale** :
```
AAAAAAAAAAAA
A..........A
A..........A
A..........A
A..........A
A...AAA#..CA    ← arbres col 4,5,6 ; pierre col 7 ; coffre col 10
A..........A
A..........A
A..........A
AAAAAAAAAAAA
```
Steve démarre en (1, 5), face EST.

**Code starter** :
```python
# Niveau 9 : Fabriquez une pioche pour briser la pierre !
# 1. Abattez les arbres (briser)
# 2. Posez un etabli (placer_etabli) — cout : 4 bois
# 3. Ouvrez-le (ouvrir_etabli)
# 4. Craftez des batons (crafter_batons) — cout : 2 bois
# 5. Craftez une pioche (crafter_pioche_bois) — cout : 3 bois + 2 batons
# 6. Brisez la pierre (briser)

avancer(2)
briser()
avancer(?)
briser()
avancer(?)
briser()
placer_etabli()
ouvrir_etabli()
crafter_batons()
crafter_pioche_bois()
avancer(?)
briser()
avancer(?)
```

**Hint** : `"Abattez 3 arbres -> etabli -> crafter -> pioche -> pierre"`

---

#### Niveau 10 — "Le grand craft"

**Objectif** : Niveau final. Steve part loin du coffre.
Il doit naviguer sur une carte complexe, abattre des arbres,
construire un établi, crafter tous les ingrédients,
briser de la pierre, et atteindre le coffre.
Le coffre est entouré de pierre de tous côtés sauf un, et la seule
entrée est bloquée par un arbre.

**Carte** :
```
AAAAAAAAAAAA
A..........A
A...AAA....A    ← forêt ligne 2 cols 4,5,6
A..........A
A..........A
A.......###A    ← mur de pierre ligne 5 cols 8,9,10
A.......#C#A    ← coffre entouré de pierre
A.......###A    ← mur de pierre ligne 7 cols 8,9,10
A..........A
AAAAAAAAAAAA
```

Attends — le coffre doit être accessible. Mets une entrée à briser :
```
AAAAAAAAAAAA
A..........A
A...AAA....A    ← arbres à abattre cols 4,5,6 ligne 2
A..........A
A..........A
A.......#.#A
A.......#C#A    ← col 9 libre (entrée), coffre col 9,6
A.......###A
A..........A
AAAAAAAAAAAA
```

**Implémentation recommandée pour le niveau 10** :

Mets une pierre en col 8 ligne 6 (devant l'entrée du coffre).
Steve doit abattre les arbres pour avoir du bois,
construire l'établi, crafter la pioche, traverser vers la pierre, la briser,
puis entrer dans la pièce du coffre.

**Carte finale propre** :
```
AAAAAAAAAAAA
A..........A
A...A.A....A    ← 2 arbres en col 4 et col 6
A..........A
A..........A
A........#.A    ← pierre col 9
A........CAA    ← coffre col 9... non, le coffre doit être atteignable
A..........A
A..........A
AAAAAAAAAAAA
```

**Prends le temps de vérifier que chaque niveau est mathématiquement solvable**
avant de l'implémenter. Calcule le bois disponible vs le bois requis pour le craft.

Bois requis pour une pioche : 4 (établi) + 2 (bâtons) + 3 (pioche) = **9 bois total**
= **5 arbres minimum** (5 × 2 = 10 bois, suffisant).

Pour le niveau 10, mets **5 arbres accessibles** sur la carte.

**Code starter niveau 10** :
```python
# Niveau 10 : Le grand craft final !
# Vous avez besoin d'au moins 9 bois (5 arbres).
# Sequence : abattre -> etabli -> batons -> pioche -> briser pierre -> coffre

# Etape 1 : Naviguer vers les arbres et les abattre
avancer(?)
briser()
# ... continuez !
```

**Hint** : `"5 arbres = 10 bois. Etabli=4, Batons=2, Pioche=3+2b. Bonne chance !"`

---

## Détails d'implémentation

### Etapes de type 'action'

Les nouvelles commandes ne sont pas des déplacements.
Ajoute un nouveau type d'étape dans le compilateur :

```python
# Dans compiler(), nouvelles étapes :
etapes_loc.append(('action', 'briser'))
etapes_loc.append(('action', 'placer_etabli'))
etapes_loc.append(('action', 'ouvrir_etabli'))
etapes_loc.append(('action', 'crafter_batons'))
etapes_loc.append(('action', 'crafter_pioche_bois'))
```

Dans `jouer_prochaine_etape()`, ajoute un bloc `elif type_e == 'action':`
qui dispatche vers des fonctions `action_briser()`, `action_placer_etabli()`, etc.

### Flag `etabli_ouvert`

Ajoute un global :
```python
etabli_ouvert = False
```
Réinitialise à `False` dans `reinitialiser()`.

### Affichage de l'inventaire

Dans `dessiner_interface()`, après le dessin de la carte et avant (ou dans) le panneau,
ajoute une zone `ZONE_INVENTAIRE` entre `ZONE_NIVEAU` et `ZONE_TITRE_ED`.

Hauteur suggérée : `max(0, len(inventaire)) * (POLICE_UI.get_height() + 2) + 22`
(titre + lignes). Si l'inventaire est vide, hauteur = 0 (zone invisible).

Pense à recalculer `ZONE_TITRE_ED` et `ZONE_EDIT` en tenant compte
de la hauteur variable de `ZONE_INVENTAIRE` dans `recalculer_layout()`.

### Validation de victoire

Modifie `jouer_prochaine_etape()` pour vérifier la condition optionnelle :

```python
if CARTE[steve["y"]][steve["x"]] == 'C':
    niv = NIVEAUX[niveau_actuel]
    condition = niv.get("condition", None)
    if condition is None or condition():
        log("BRAVO !", JAUNE)
        niveau_suivant()
    else:
        log("Objectif non rempli ! Relisez les instructions.", ROUGE)
        en_exec = False
```

---

## Checklist finale

- [ ] `inventaire` global créé et réinitialisé dans `reinitialiser()`
- [ ] `etabli_ouvert` global créé et réinitialisé
- [ ] Tuiles `T`, `B`, `R` ajoutées dans `TUILE_COULEUR` (et retirées de `IMPASSABLE` pour B et R)
- [ ] 5 nouvelles commandes dans `compiler()`
- [ ] 5 nouvelles commandes dans `AIDE_CMDS`
- [ ] Logique de chaque action dans `jouer_prochaine_etape()`
- [ ] `ZONE_INVENTAIRE` affichée dans le panneau
- [ ] `recalculer_layout()` tient compte de la hauteur de l'inventaire
- [ ] Les 5 niveaux ajoutés dans `NIVEAUX`, solvables mathématiquement
- [ ] Condition de victoire optionnelle (`"condition"`) vérifiée
- [ ] Syntaxe Python valide (tester avec `python3 -c "import ast; ast.parse(open('codecraft_mvp.py').read())"`)
ENDOFFILE