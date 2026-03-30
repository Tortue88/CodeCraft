"""
CodeCraft MVP - Jeu de programmation
=====================================
Guidez Steve (carre bleu) jusqu'au coffre (C).

Commandes disponibles dans l'editeur :
  avancer(n)        - avance de n cases
  reculer(n)        - recule de n cases
  tourner_droite()  - tourne a droite (90 degres)
  tourner_gauche()  - tourne a gauche (90 degres)
  demi_tour()       - fait demi-tour (180 degres)

Raccourcis :
  F5  = Executer
  F11 = Plein ecran / Fenetre

Installation : pip install pygame
Lancement    : python codecraft_mvp.py
"""

import pygame
import sys

pygame.init()

# ─── COULEURS ───────────────────────────────────────────────
NOIR    = (  0,   0,   0)
BLANC   = (255, 255, 255)
GRIS    = (180, 180, 180)
BLEU    = ( 50, 100, 200)
VERT    = ( 60, 140,  60)
EAU     = ( 60, 120, 220)
ROUGE   = (200,  50,  50)
JAUNE   = (240, 200,   0)
FOND    = ( 30,  30,  30)
OR      = (220, 160,  20)

# ─── DIRECTIONS ─────────────────────────────────────────────
NORD, EST, SUD, OUEST = 0, 1, 2, 3
NOM_DIR = {NORD: "Nord", EST: "Est", SUD: "Sud", OUEST: "Ouest"}
DX = {NORD:  0, EST: +1, SUD:  0, OUEST: -1}
DY = {NORD: -1, EST:  0, SUD: +1, OUEST:  0}

# ─── NIVEAUX ────────────────────────────────────────────────
NIVEAUX = [

    # Niveau 1 : Ligne droite — solution : avancer(9)
    {
        "titre": "Niveau 1  -  Ligne droite",
        "hint":  "Hint : avancer(n) avance de n cases",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A.........CA",
            "A..........A",
            "A..........A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 5, "sdir": EST,
        "code": [
            "# Niveau 1 : Le coffre est droit devant !",
            "# Utilisez avancer(n) pour avancer de n cases.",
            "",
            "avancer(?)",
        ],
    },

    # Niveau 2 : Premier virage — solution : avancer(6), tourner_droite(), avancer(6)
    {
        "titre": "Niveau 2  -  Premier virage",
        "hint":  "Hint : avancer -> tourner -> avancer",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A......C...A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 1, "sdir": EST,
        "code": [
            "# Niveau 2 : Le coffre est en bas a droite.",
            "# Allez a droite, puis tournez vers le bas.",
            "",
            "avancer(?)",
            "tourner_droite()",
            "avancer(?)",
        ],
    },

    # Niveau 3 : Detour aquatique
    # Solution : avancer(2), tourner_droite(), avancer(6), tourner_gauche(), avancer(5)
    {
        "titre": "Niveau 3  -  Detour aquatique",
        "hint":  "L'eau bloque ! Descendez d'abord.",
        "carte": [
            "AAAAAAAAAAAA",
            "A...~~~~...A",
            "A...~~~~...A",
            "A...~~~~...A",
            "A...~~~~...A",
            "A...~~~~...A",
            "A...~~~~...A",
            "A.......C..A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 1, "sdir": EST,
        "code": [
            "# Niveau 3 : L'eau bloque le chemin direct !",
            "# Contournez par le bas, puis repartez a l'Est.",
            "",
            "avancer(?)",
            "tourner_droite()",
            "avancer(?)",
            "tourner_gauche()",
            "avancer(?)",
        ],
    },

    # Niveau 4 : Le couloir — Steve face au NORD en bas
    # Solution : avancer(7), tourner_droite(), avancer(4),
    #            tourner_droite(), avancer(4), tourner_gauche(), avancer(5)
    {
        "titre": "Niveau 4  -  Le couloir",
        "hint":  "Steve regarde au Nord. Zigzaguez !",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A.........CA",
            "A.~~~~.....A",
            "A.~~~~.....A",
            "A.~~~~~~~~~A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 8, "sdir": NORD,
        "code": [
            "# Niveau 4 : Steve est en bas, face au Nord.",
            "# La flaque bloque l'Est. Montez d'abord !",
            "# Puis zigzaguez en 3 virages jusqu'au coffre.",
            "",
            "avancer(?)",
            "tourner_droite()",
            "avancer(?)",
            "tourner_droite()",
            "avancer(?)",
            "tourner_gauche()",
            "avancer(?)",
        ],
    },

    # Niveau 5 : Grand parcours — Steve face a l'OUEST en haut a droite
    # Solution : avancer(8), tourner_droite(), avancer(6),
    #            demi_tour(), avancer(4), tourner_gauche(),
    #            avancer(7), tourner_gauche(), avancer(4),
    #            tourner_gauche(), avancer(8)
    {
        "titre": "Niveau 5  -  Grand parcours",
        "hint":  "Vous aurez besoin de demi_tour() !",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A....~~~...A",
            "A....~~~...A",
            "A..........A",
            "A.........CA",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 9, "sy": 1, "sdir": OUEST,
        "code": [
            "# Niveau 5 : Le grand parcours final !",
            "# Steve est en haut a droite, face a l'Ouest.",
            "# Hint : demi_tour() fait un 180 degres.",
            "# C'est a vous de trouver le chemin !",
            "",
        ],
    },
    # Niveau 6 : Abattage — solution : avancer(3), briser(), avancer(6)
    {
        "titre": "Niveau 6  -  Abattage",
        "hint":  "briser() detruit la tuile devant Steve",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A....A....CA",
            "A..........A",
            "A..........A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 5, "sdir": EST,
        "code": [
            "# Niveau 6 : Un arbre bloque la route !",
            "# Avancez jusqu'a l'arbre, brisez-le, continuez.",
            "",
            "avancer(3)",
            "briser()",
            "avancer(?)",
        ],
    },

    # Niveau 7 : La foret — solution : avancer(1), briser(), avancer(2), briser(), avancer(3)
    {
        "titre": "Niveau 7  -  La foret",
        "hint":  "Brisez les arbres un par un",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..A..A...CA",
            "A..........A",
            "A..........A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 5, "sdir": EST,
        "code": [
            "# Niveau 7 : Deux arbres bloquent la route !",
            "# Brisez-les un par un.",
            "",
            "avancer(1)",
            "briser()",
            "avancer(3)",
            "briser()",
            "avancer(?)",
        ],
    },

    # Niveau 8 : Poser l'etabli
    # Solution : briser(), avancer(1), briser(), placer_etabli(), avancer(7)
    {
        "titre": "Niveau 8  -  Poser l'etabli",
        "hint":  "Abattez 2 arbres, posez l'etabli, puis avancez",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A.AA......CA",
            "A..........A",
            "A..........A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 5, "sdir": EST,
        "code": [
            "# Niveau 8 : Collectez du bois et posez un etabli !",
            "# briser() sur un arbre donne 2 bois.",
            "# Il faut 4 bois pour placer_etabli().",
            "# Posez l'etabli derriere vous avec demi_tour() !",
            "",
            "briser()",
            "avancer(1)",
            "briser()",
            "avancer(1)",
            "demi_tour()",
            "placer_etabli()",
            "demi_tour()",
            "avancer(?)",
        ],
        "condition": lambda: any(CARTE[l][c] == 'T' for l in range(NB_LIG) for c in range(NB_COL)),
    },

    # Niveau 9 : La pioche
    # 5 arbres = 10 bois. Besoin : 4 (etabli) + 2 (batons) + 3 (pioche) = 9 bois + 2 batons
    # Solution : avancer(2), briser(), avancer(1), briser(), avancer(1), briser(),
    #            avancer(1), briser(), avancer(1), briser(), placer_etabli(),
    #            ouvrir_etabli(), crafter_batons(), ouvrir_etabli(), crafter_pioche_bois(),
    #            avancer(1), briser(), avancer(1)
    {
        "titre": "Niveau 9  -  La pioche",
        "hint":  "Abattez 5 arbres -> etabli -> crafter -> pioche -> pierre",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A..AAAAA#.CA",
            "A..........A",
            "A..........A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 5, "sdir": EST,
        "code": [
            "# Niveau 9 : Fabriquez une pioche pour briser la pierre !",
            "# 1. Abattez les arbres (briser) - 5 arbres = 10 bois",
            "# 2. Posez un etabli (placer_etabli) - cout : 4 bois",
            "# 3. Ouvrez-le (ouvrir_etabli)",
            "# 4. Craftez des batons (crafter_batons) - cout : 2 bois",
            "# 5. Ouvrez l'etabli a nouveau, craftez pioche",
            "# 6. Brisez la pierre (briser)",
            "",
            "avancer(2)",
            "briser()",
            "avancer(?)",
        ],
    },

    # Niveau 10 : Le grand craft
    # 5 arbres ligne 2, pierre col 8 ligne 6, coffre col 9 ligne 6
    {
        "titre": "Niveau 10  -  Le grand craft",
        "hint":  "5 arbres = 10 bois. Etabli=4, Batons=2, Pioche=3+2b. Bonne chance !",
        "carte": [
            "AAAAAAAAAAAA",
            "A..........A",
            "A...AAAAA..A",
            "A..........A",
            "A..........A",
            "A..........A",
            "A.......#C.A",
            "A..........A",
            "A..........A",
            "AAAAAAAAAAAA",
        ],
        "sx": 1, "sy": 1, "sdir": EST,
        "code": [
            "# Niveau 10 : Le grand craft final !",
            "# Vous avez besoin d'au moins 9 bois (5 arbres).",
            "# Sequence : abattre -> etabli -> batons",
            "#            -> pioche -> briser pierre -> coffre",
            "",
            "# Etape 1 : Naviguer vers les arbres et les abattre",
            "avancer(?)",
            "briser()",
            "# ... continuez !",
        ],
    },
]

# ─── TUILES ─────────────────────────────────────────────────
TUILE_COULEUR = {
    '.': VERT,
    '~': EAU,
    'A': (30, 80, 20),
    '#': (110,110,110),
    's': (200,185, 80),
    'C': (160, 100, 30),
    'T': (180, 120, 40),
    'B': (140, 90, 30),
    'R': (160, 160, 160),
}
IMPASSABLE = {'~', 'A', '#', 'T'}

# ─── CARTE ACTIVE ───────────────────────────────────────────
CARTE  = []
NB_COL = 0
NB_LIG = 0

# ─── DIMENSIONS DYNAMIQUES ──────────────────────────────────
# Ces variables sont recalculees par recalculer_layout()
# a chaque changement de taille de fenetre.
STAT_H  = 30          # barre de statut (hauteur fixe)
CELL    = 46          # taille d'une tuile (recalculee)
MAP_W   = 552         # largeur de la carte en pixels
MAP_H   = 460         # hauteur de la carte en pixels
PANEL_W = 380         # largeur du panneau droit
WIN_W   = 932
WIN_H   = 460
LH      = 16          # hauteur d'une ligne editeur
VIS     = 10          # lignes visibles dans l'editeur

# Zones et boutons (recalcules par recalculer_layout)
ZONE_NIVEAU     = None
ZONE_INVENTAIRE = None
ZONE_TITRE_ED   = None
ZONE_EDIT     = None
ZONE_BTNS     = None
ZONE_AIDE     = None
ZONE_CON      = None
r_exec  = None
r_reset = None
r_clear = None

# ─── ECRAN ──────────────────────────────────────────────────
screen      = pygame.display.set_mode((932, 490), pygame.RESIZABLE)
plein_ecran = False
pygame.display.set_caption("CodeCraft  |  F11 = plein ecran")
clock = pygame.time.Clock()

# ─── POLICES (independantes du layout) ──────────────────────
POLICE    = pygame.font.SysFont("Courier New", 13)
POLICE_UI = pygame.font.SysFont("Arial", 12)
POLICE_B  = pygame.font.SysFont("Arial", 12, bold=True)

# ─── ETAT DU JEU ────────────────────────────────────────────
niveau_actuel = 0
steve = {"x": 1, "y": 1, "dir": EST}

# ─── EDITEUR DE CODE ────────────────────────────────────────
lignes  = []
cur_lig = 0
cur_col = 0
scroll  = 0

# ─── EXECUTION ──────────────────────────────────────────────
en_exec   = False
etapes    = []
etape_idx = 0
timer     = 0
DELAI_MS  = 230

# ─── INVENTAIRE ET CRAFT ────────────────────────────────────
inventaire = {}
etabli_ouvert = False

# ─── CONSOLE ────────────────────────────────────────────────
messages = []

def log(texte, couleur=GRIS):
    messages.append((texte, couleur))
    if len(messages) > 60:
        messages.pop(0)

# ═══════════════════════════════════════════════════
#  LAYOUT DYNAMIQUE
# ═══════════════════════════════════════════════════
def recalculer_layout():
    """
    Recalcule toutes les dimensions a partir de la taille
    actuelle de la fenetre. Appelee au demarrage et a chaque
    redimensionnement ou bascule plein ecran.
    """
    global CELL, MAP_W, MAP_H, PANEL_W, WIN_W, WIN_H
    global ZONE_NIVEAU, ZONE_INVENTAIRE, ZONE_TITRE_ED, ZONE_EDIT
    global ZONE_BTNS, ZONE_AIDE, ZONE_CON
    global LH, VIS, r_exec, r_reset, r_clear

    W, H = screen.get_size()
    WIN_W = W
    WIN_H = H - STAT_H

    # Le panneau occupe 1/3 de la largeur (min 340, max 440)
    PANEL_W = max(340, min(440, W // 3))

    # La carte remplit le reste, CELL est le plus grand entier
    # tel que 12*CELL <= espace_carte_w et 10*CELL <= espace_carte_h
    espace_w = W - PANEL_W
    espace_h = WIN_H
    CELL = min(espace_w // 12, espace_h // 10)
    CELL = max(CELL, 20)    # minimum raisonnable

    MAP_W = 12 * CELL
    MAP_H = 10 * CELL

    # x de debut du panneau (juste apres la carte)
    PX = MAP_W + 4
    PW = PANEL_W - 8        # largeur utile du panneau

    # Zones verticales du panneau
    # Le panneau est divise en : titre-niveau / titre-editeur / editeur /
    #                            boutons / aide / console / statut
    AIDE_H = 170            # hauteur fixe du bloc aide (10 commandes)
    CON_H  = max(80, WIN_H // 6)   # console : 1/6 de la hauteur
    BTN_H  = 30
    TITH   = 18             # hauteur d'une barre de titre

    # Hauteur de l'inventaire (variable)
    lh_inv = POLICE_UI.get_height() + 2
    nb_inv = len(inventaire)
    INV_H  = (nb_inv * lh_inv + 22) if nb_inv > 0 else 0

    # On calcule de bas en haut
    y_con   = WIN_H - CON_H
    y_btns  = y_con - AIDE_H - TITH - BTN_H - 4
    y_inv   = TITH + 4
    y_edit  = y_inv + INV_H + TITH     # apres inventaire + titre editeur
    edit_h  = y_btns - y_edit - 4

    ZONE_NIVEAU     = pygame.Rect(PX, 2,      PW, TITH)
    ZONE_INVENTAIRE = pygame.Rect(PX, y_inv, PW, INV_H) if nb_inv > 0 else None
    ZONE_TITRE_ED   = pygame.Rect(PX, y_inv + INV_H, PW, TITH)
    ZONE_EDIT       = pygame.Rect(PX, y_edit, PW, max(edit_h, 40))
    ZONE_BTNS     = pygame.Rect(PX, y_btns, PW, BTN_H)
    ZONE_AIDE     = pygame.Rect(PX, y_btns + BTN_H + 4,          PW, AIDE_H)
    ZONE_CON      = pygame.Rect(PX, y_btns + BTN_H + AIDE_H + TITH + 8, PW, CON_H)

    LH  = POLICE.get_height() + 2
    VIS = ZONE_EDIT.height // LH

    BTN_W  = PW // 3
    r_exec  = pygame.Rect(ZONE_BTNS.x,            ZONE_BTNS.y, BTN_W, BTN_H)
    r_reset = pygame.Rect(ZONE_BTNS.x + BTN_W + 2, ZONE_BTNS.y, BTN_W, BTN_H)
    r_clear = pygame.Rect(ZONE_BTNS.x + BTN_W*2+4, ZONE_BTNS.y, BTN_W, BTN_H)

def toggle_plein_ecran():
    """Bascule plein ecran / fenetre redimensionnable."""
    global screen, plein_ecran
    plein_ecran = not plein_ecran
    if plein_ecran:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((932, 490), pygame.RESIZABLE)
    recalculer_layout()

# ═══════════════════════════════════════════════════
#  CHARGEMENT DE NIVEAU
# ═══════════════════════════════════════════════════
def charger_niveau(n):
    global CARTE, NB_COL, NB_LIG, niveau_actuel
    global lignes, cur_lig, cur_col, scroll

    niveau_actuel = n
    niv    = NIVEAUX[n]
    CARTE  = [list(r) for r in niv["carte"]]
    NB_COL = len(CARTE[0])
    NB_LIG = len(CARTE)

    steve["x"]   = niv["sx"]
    steve["y"]   = niv["sy"]
    steve["dir"] = niv["sdir"]

    lignes  = niv["code"][:]
    cur_lig = len(lignes) - 1
    cur_col = len(lignes[cur_lig])
    scroll  = 0

# ═══════════════════════════════════════════════════
#  PARSEUR / COMPILATEUR
# ═══════════════════════════════════════════════════
def compiler(code):
    etapes_loc, erreurs = [], []
    for num, ligne in enumerate(code, 1):
        s = ligne.strip()
        if not s or s.startswith('#'):
            continue
        if s.startswith('avancer(') and s.endswith(')'):
            try:
                n = int(s[8:-1])
                for _ in range(n): etapes_loc.append(('pas', +1))
            except ValueError:
                erreurs.append("Ligne " + str(num) + " : avancer(?) — entier attendu")
        elif s.startswith('reculer(') and s.endswith(')'):
            try:
                n = int(s[8:-1])
                for _ in range(n): etapes_loc.append(('pas', -1))
            except ValueError:
                erreurs.append("Ligne " + str(num) + " : reculer(?) — entier attendu")
        elif s == 'tourner_droite()':
            etapes_loc.append(('tourner', +1))
        elif s == 'tourner_gauche()':
            etapes_loc.append(('tourner', -1))
        elif s == 'demi_tour()':
            etapes_loc.append(('tourner', +2))
        elif s == 'briser()':
            etapes_loc.append(('action', 'briser'))
        elif s == 'placer_etabli()':
            etapes_loc.append(('action', 'placer_etabli'))
        elif s == 'ouvrir_etabli()':
            etapes_loc.append(('action', 'ouvrir_etabli'))
        elif s == 'crafter_batons()':
            etapes_loc.append(('action', 'crafter_batons'))
        elif s == 'crafter_pioche_bois()':
            etapes_loc.append(('action', 'crafter_pioche_bois'))
        else:
            erreurs.append("Ligne " + str(num) + " inconnue : " + s)
    return etapes_loc, erreurs

# ═══════════════════════════════════════════════════
#  ACTIONS DU JEU
# ═══════════════════════════════════════════════════
def executer():
    global en_exec, etapes, etape_idx, timer
    if en_exec: return
    reinitialiser()
    messages.clear()
    es, erreurs = compiler(lignes)
    if erreurs:
        for e in erreurs: log("ERREUR: " + e, ROUGE)
        return
    if not es:
        log("Aucune commande a executer.", JAUNE)
        return
    log("Execution : " + str(len(es)) + " etape(s)...", (100, 200, 255))
    etapes, etape_idx, timer = es, 0, 0
    en_exec = True

def reinitialiser():
    global en_exec, etapes, etape_idx, CARTE, etabli_ouvert, inventaire
    niv = NIVEAUX[niveau_actuel]
    steve["x"], steve["y"], steve["dir"] = niv["sx"], niv["sy"], niv["sdir"]
    CARTE = [list(r) for r in niv["carte"]]
    inventaire = {}
    etabli_ouvert = False
    en_exec, etapes, etape_idx = False, [], 0

def niveau_suivant():
    global en_exec
    en_exec = False
    suivant = niveau_actuel + 1
    if suivant < len(NIVEAUX):
        messages.clear()
        charger_niveau(suivant)
        log("Niveau " + str(suivant+1) + " / " + str(len(NIVEAUX)), (100, 200, 255))
        log(NIVEAUX[suivant]["hint"], (160, 200, 140))
    else:
        log("", BLANC)
        log("***  FELICITATIONS  ***", JAUNE)
        log("Vous avez termine tous les niveaux !", OR)
        log("Vous etes un vrai programmeur !", (200, 255, 200))

# ─── HELPERS INVENTAIRE ET ACTIONS ──────────────────────────
def tuile_devant():
    fx = steve["x"] + DX[steve["dir"]]
    fy = steve["y"] + DY[steve["dir"]]
    if 0 <= fx < NB_COL and 0 <= fy < NB_LIG:
        return fx, fy, CARTE[fy][fx]
    return fx, fy, None

def inv_ajouter(item, n):
    inventaire[item] = inventaire.get(item, 0) + n

def inv_retirer(item, n):
    inventaire[item] = inventaire.get(item, 0) - n
    if inventaire[item] <= 0:
        del inventaire[item]

def inv_a(item, n):
    return inventaire.get(item, 0) >= n

def action_briser():
    global etabli_ouvert
    fx, fy, t = tuile_devant()
    if t == 'A':
        CARTE[fy][fx] = 'B'
        inv_ajouter("bois", 2)
        log("Arbre brise ! +2 bois", (100, 200, 100))
        return True
    elif t == '#' and inv_a("pioche_bois", 1):
        CARTE[fy][fx] = 'R'
        inv_retirer("pioche_bois", 1)
        log("Pierre brisee ! La pioche en bois est usee.", (100, 200, 100))
        return True
    else:
        if t == '#':
            log("Il faut une pioche pour briser la pierre !", ROUGE)
        else:
            log("Rien a briser devant Steve !", ROUGE)
        return False

def action_placer_etabli():
    fx, fy, t = tuile_devant()
    if not inv_a("bois", 4):
        log("Pas assez de bois pour l'etabli (4 requis) !", ROUGE)
        return False
    if t not in ('.', 'B'):
        log("Impossible de poser l'etabli ici !", ROUGE)
        return False
    CARTE[fy][fx] = 'T'
    inv_retirer("bois", 4)
    log("Etabli pose ! (-4 bois)", (100, 200, 100))
    return True

def action_ouvrir_etabli():
    global etabli_ouvert
    fx, fy, t = tuile_devant()
    if t != 'T':
        log("Pas d'etabli devant Steve !", ROUGE)
        return False
    etabli_ouvert = True
    log("Etabli ouvert.", (100, 200, 100))
    return True

def action_crafter_batons():
    global etabli_ouvert
    if not etabli_ouvert:
        log("Ouvrez d'abord un etabli !", ROUGE)
        return False
    if not inv_a("bois", 2):
        log("Pas assez de bois (2 requis) !", ROUGE)
        return False
    inv_retirer("bois", 2)
    inv_ajouter("baton", 4)
    etabli_ouvert = False
    log("Crafte : 4 batons ! (-2 bois)", (100, 200, 100))
    return True

def action_crafter_pioche_bois():
    global etabli_ouvert
    if not etabli_ouvert:
        log("Ouvrez d'abord un etabli !", ROUGE)
        return False
    if not inv_a("bois", 3) or not inv_a("baton", 2):
        log("Il faut 3 bois et 2 batons !", ROUGE)
        return False
    inv_retirer("bois", 3)
    inv_retirer("baton", 2)
    inv_ajouter("pioche_bois", 1)
    etabli_ouvert = False
    log("Crafte : pioche en bois ! (-3 bois, -2 batons)", (100, 200, 100))
    return True

ACTIONS = {
    'briser': action_briser,
    'placer_etabli': action_placer_etabli,
    'ouvrir_etabli': action_ouvrir_etabli,
    'crafter_batons': action_crafter_batons,
    'crafter_pioche_bois': action_crafter_pioche_bois,
}

def jouer_prochaine_etape():
    global en_exec, etape_idx
    if etape_idx >= len(etapes):
        en_exec = False
        if CARTE[steve["y"]][steve["x"]] == 'C':
            niv = NIVEAUX[niveau_actuel]
            condition = niv.get("condition", None)
            if condition is None or condition():
                log("BRAVO ! Steve a trouve le coffre !", JAUNE)
                niveau_suivant()
            else:
                log("Objectif non rempli ! Relisez les instructions.", ROUGE)
        else:
            log("Termine en (" + str(steve['x']) + "," + str(steve['y']) + "). Pas encore au coffre.", GRIS)
            log("Reessayez !", (220, 160, 60))
        return
    type_e, val = etapes[etape_idx]
    etape_idx += 1
    if type_e == 'tourner':
        steve["dir"] = (steve["dir"] + val) % 4
        sens = "droite" if val==1 else ("gauche" if val==-1 else "demi-tour")
        log("  -> Tourne " + sens + " -> " + NOM_DIR[steve['dir']], (150, 200, 255))
    elif type_e == 'pas':
        nx = steve["x"] + DX[steve["dir"]] * val
        ny = steve["y"] + DY[steve["dir"]] * val
        if not (0 <= nx < NB_COL and 0 <= ny < NB_LIG):
            log("  BLOQUE : bord de carte !", ROUGE)
            en_exec = False
        elif CARTE[ny][nx] in IMPASSABLE:
            log("  BLOQUE par '" + CARTE[ny][nx] + "' en (" + str(nx) + "," + str(ny) + ") !", ROUGE)
            en_exec = False
        else:
            steve["x"], steve["y"] = nx, ny
    elif type_e == 'action':
        fn = ACTIONS.get(val)
        if fn and not fn():
            en_exec = False

# ═══════════════════════════════════════════════════
#  DESSIN
# ═══════════════════════════════════════════════════
def dessiner_carte():
    for lig in range(NB_LIG):
        for col in range(NB_COL):
            t = CARTE[lig][col]
            r = pygame.Rect(col*CELL, lig*CELL, CELL, CELL)
            pygame.draw.rect(screen, TUILE_COULEUR[t], r)
            pygame.draw.rect(screen, NOIR, r, 1)
            if t == 'C':
                etoile = POLICE_B.render("*", True, JAUNE)
                screen.blit(etoile, (col*CELL + CELL//2 - etoile.get_width()//2,
                                     lig*CELL + CELL//2 - etoile.get_height()//2))
            elif t not in ('.', 'A', '~'):
                label = POLICE_UI.render(t, True, BLANC)
                screen.blit(label, (col*CELL + 3, lig*CELL + 3))

def dessiner_steve():
    x = steve["x"] * CELL + CELL // 2
    y = steve["y"] * CELL + CELL // 2
    taille = max(8, CELL // 5)
    pygame.draw.rect(screen, BLEU,        pygame.Rect(x-taille, y-taille, taille*2, taille*2))
    pygame.draw.rect(screen, (20,60,150), pygame.Rect(x-taille, y-taille, taille*2, taille*2), 2)
    dist = taille + 6
    fleche = {NORD:(x, y-dist), EST:(x+dist, y), SUD:(x, y+dist), OUEST:(x-dist, y)}
    pygame.draw.circle(screen, ROUGE, fleche[steve["dir"]], max(3, taille//2))

def dessiner_bouton(rect, texte, actif=True):
    couleur = GRIS if actif else (110, 110, 110)
    pygame.draw.rect(screen, couleur, rect)
    pygame.draw.rect(screen, NOIR, rect, 1)
    t = POLICE_UI.render(texte, True, NOIR if actif else (160,160,160))
    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))

def dessiner_editeur():
    global scroll
    pygame.draw.rect(screen, (20, 20, 35), ZONE_EDIT)
    pygame.draw.rect(screen, GRIS, ZONE_EDIT, 1)

    if cur_lig < scroll:
        scroll = cur_lig
    elif cur_lig >= scroll + VIS:
        scroll = cur_lig - VIS + 1

    for i in range(VIS):
        idx = scroll + i
        if idx >= len(lignes): break
        ligne = lignes[idx]
        y = ZONE_EDIT.y + i * LH + 2

        if idx == cur_lig:
            pygame.draw.rect(screen, (40, 45, 70),
                             pygame.Rect(ZONE_EDIT.x+1, y, ZONE_EDIT.w-2, LH))

        s = ligne.strip()
        if s.startswith('#'):
            col = (100, 160,  80)
        elif any(c in s for c in ('avancer','reculer','tourner','demi_tour','briser','placer_etabli','ouvrir_etabli','crafter')):
            col = (220, 220, 140)
        else:
            col = (200, 200, 215)

        num = POLICE_UI.render(str(idx+1), True, (80, 80, 110))
        screen.blit(num, (ZONE_EDIT.x + 2, y + 1))
        t = POLICE.render(ligne, True, col)
        screen.blit(t, (ZONE_EDIT.x + 22, y))

        if idx == cur_lig and not en_exec:
            cx = ZONE_EDIT.x + 22 + POLICE.size(ligne[:cur_col])[0]
            pygame.draw.line(screen, BLANC, (cx, y), (cx, y + LH - 2), 1)

AIDE_CMDS = [
    ("avancer(n)",       "avance de n cases en avant"),
    ("reculer(n)",       "recule de n cases en arriere"),
    ("tourner_droite()", "pivote 90 degres a droite"),
    ("tourner_gauche()", "pivote 90 degres a gauche"),
    ("demi_tour()",      "fait volte-face (180 degres)"),
    ("briser()",             "brise tuile devant Steve"),
    ("placer_etabli()",      "pose un etabli (4 bois)"),
    ("ouvrir_etabli()",      "ouvre l'etabli devant Steve"),
    ("crafter_batons()",     "2 bois -> 4 batons"),
    ("crafter_pioche_bois()","3 bois+2 batons -> pioche"),
]

def dessiner_aide():
    r_titre = pygame.Rect(ZONE_AIDE.x, ZONE_AIDE.y, ZONE_AIDE.w, 18)
    pygame.draw.rect(screen, (0, 0, 128), r_titre)
    screen.blit(POLICE_UI.render("Commandes disponibles", True, BLANC),
                (r_titre.x + 4, r_titre.y + 2))
    r_corps = pygame.Rect(ZONE_AIDE.x, ZONE_AIDE.y+18, ZONE_AIDE.w, ZONE_AIDE.h-18)
    pygame.draw.rect(screen, (20, 20, 35), r_corps)
    pygame.draw.rect(screen, GRIS, r_corps, 1)
    lh = POLICE.get_height() + 2
    for i, (cmd, desc) in enumerate(AIDE_CMDS):
        y = r_corps.y + 3 + i * lh
        t_cmd  = POLICE.render(cmd, True, (220, 220, 140))
        t_desc = POLICE_UI.render(desc, True, (140, 140, 160))
        screen.blit(t_cmd,  (r_corps.x + 4, y))
        screen.blit(t_desc, (r_corps.x + 4 + t_cmd.get_width() + 6, y + 1))

def dessiner_console():
    r_tit = pygame.Rect(ZONE_CON.x, ZONE_CON.y-18, ZONE_CON.w, 18)
    pygame.draw.rect(screen, (0, 0, 128), r_tit)
    screen.blit(POLICE_UI.render("Console", True, BLANC), (r_tit.x + 4, r_tit.y + 2))
    pygame.draw.rect(screen, (10, 10, 15), ZONE_CON)
    pygame.draw.rect(screen, GRIS, ZONE_CON, 1)
    h_lig = POLICE_UI.get_height() + 2
    nb_vis = ZONE_CON.height // h_lig
    debut  = max(0, len(messages) - nb_vis)
    for i, (txt, col) in enumerate(messages[debut:]):
        t = POLICE_UI.render(txt, True, col)
        screen.blit(t, (ZONE_CON.x + 4, ZONE_CON.y + 3 + i * h_lig))

def dessiner_interface():
    niv = NIVEAUX[niveau_actuel]

    # Fond du panneau (toute la hauteur a droite de la carte)
    pygame.draw.rect(screen, (200, 200, 200),
                     pygame.Rect(MAP_W, 0, WIN_W - MAP_W, WIN_H + STAT_H))

    # Bandeau niveau (couleur progresse avec la difficulte)
    teintes = [
        (  0,   0, 128),
        (  0,  80, 160),
        (  0, 120, 100),
        (  0, 140,  60),
        ( 80, 130,   0),
        ( 40, 100,  80),
        ( 60,  80, 120),
        (100,  60,  40),
        (120,  40,  60),
        (140,  20,  20),
    ]
    pygame.draw.rect(screen, teintes[niveau_actuel], ZONE_NIVEAU)
    t_niv = POLICE_B.render(niv["titre"], True, BLANC)
    screen.blit(t_niv, (ZONE_NIVEAU.x + 4, ZONE_NIVEAU.y + 2))
    t_idx = POLICE_B.render(str(niveau_actuel+1) + " / " + str(len(NIVEAUX)), True, JAUNE)
    screen.blit(t_idx, (ZONE_NIVEAU.right - t_idx.get_width() - 6, ZONE_NIVEAU.y + 2))

    # Inventaire
    if ZONE_INVENTAIRE is not None:
        r_inv_titre = pygame.Rect(ZONE_INVENTAIRE.x, ZONE_INVENTAIRE.y, ZONE_INVENTAIRE.w, 18)
        pygame.draw.rect(screen, (100, 60, 20), r_inv_titre)
        screen.blit(POLICE_UI.render("Inventaire", True, BLANC),
                    (r_inv_titre.x + 4, r_inv_titre.y + 2))
        r_inv_corps = pygame.Rect(ZONE_INVENTAIRE.x, ZONE_INVENTAIRE.y + 18,
                                  ZONE_INVENTAIRE.w, ZONE_INVENTAIRE.h - 18)
        pygame.draw.rect(screen, (40, 30, 20), r_inv_corps)
        pygame.draw.rect(screen, GRIS, r_inv_corps, 1)
        lh_inv = POLICE_UI.get_height() + 2
        for i, (item, qty) in enumerate(inventaire.items()):
            y_item = r_inv_corps.y + 2 + i * lh_inv
            t_item = POLICE_UI.render(item + " x" + str(qty), True, (220, 200, 140))
            screen.blit(t_item, (r_inv_corps.x + 6, y_item))

    # Titre editeur
    pygame.draw.rect(screen, (0, 0, 128), ZONE_TITRE_ED)
    screen.blit(POLICE_UI.render("Editeur de code", True, BLANC),
                (ZONE_TITRE_ED.x + 4, ZONE_TITRE_ED.y + 2))

    dessiner_editeur()
    dessiner_bouton(r_exec,  "Executer", not en_exec)
    dessiner_bouton(r_reset, "Reinit.",  not en_exec)
    dessiner_bouton(r_clear, "Effacer",  not en_exec)
    dessiner_aide()
    dessiner_console()

    # Barre de statut (bas de la fenetre, pleine largeur)
    r_stat = pygame.Rect(0, WIN_H, WIN_W, STAT_H)
    pygame.draw.rect(screen, GRIS, r_stat)
    pygame.draw.line(screen, NOIR, (0, WIN_H), (WIN_W, WIN_H), 1)
    etat = ("Steve : (" + str(steve['x']) + ", " + str(steve['y']) + ")  "
            "Dir : " + NOM_DIR[steve['dir']])
    if en_exec: etat += "   [En cours...]"
    screen.blit(POLICE_UI.render(etat, True, NOIR), (8, WIN_H + 7))
    hint_t = POLICE_UI.render(niv["hint"], True, (80, 80, 80))
    screen.blit(hint_t, (WIN_W - hint_t.get_width() - 8, WIN_H + 7))

    # Separateur vertical carte / panneau
    pygame.draw.line(screen, (120,120,120), (MAP_W, 0), (MAP_W, WIN_H), 2)

# ═══════════════════════════════════════════════════
#  GESTION CLAVIER
# ═══════════════════════════════════════════════════
def gerer_clavier(event):
    global cur_lig, cur_col
    if en_exec: return

    k = event.key

    if k == pygame.K_RETURN:
        reste = lignes[cur_lig][cur_col:]
        lignes[cur_lig] = lignes[cur_lig][:cur_col]
        lignes.insert(cur_lig + 1, reste)
        cur_lig += 1; cur_col = 0

    elif k == pygame.K_BACKSPACE:
        if cur_col > 0:
            l = lignes[cur_lig]
            lignes[cur_lig] = l[:cur_col-1] + l[cur_col:]
            cur_col -= 1
        elif cur_lig > 0:
            cur_col = len(lignes[cur_lig - 1])
            lignes[cur_lig - 1] += lignes[cur_lig]
            lignes.pop(cur_lig)
            cur_lig -= 1

    elif k == pygame.K_UP and cur_lig > 0:
        cur_lig -= 1; cur_col = min(cur_col, len(lignes[cur_lig]))
    elif k == pygame.K_DOWN and cur_lig < len(lignes) - 1:
        cur_lig += 1; cur_col = min(cur_col, len(lignes[cur_lig]))
    elif k == pygame.K_LEFT and cur_col > 0:
        cur_col -= 1
    elif k == pygame.K_RIGHT and cur_col < len(lignes[cur_lig]):
        cur_col += 1
    elif k == pygame.K_HOME:
        cur_col = 0
    elif k == pygame.K_END:
        cur_col = len(lignes[cur_lig])
    elif k == pygame.K_F5:
        executer()
    elif k == pygame.K_F11:
        toggle_plein_ecran()
    elif event.unicode and event.unicode.isprintable():
        l = lignes[cur_lig]
        lignes[cur_lig] = l[:cur_col] + event.unicode + l[cur_col:]
        cur_col += 1

# ═══════════════════════════════════════════════════
#  DEMARRAGE
# ═══════════════════════════════════════════════════
recalculer_layout()
charger_niveau(0)
log("Bienvenue dans CodeCraft !", (100, 200, 255))
log("Niveau 1 / " + str(len(NIVEAUX)) + "  -  Ligne droite", (180, 255, 180))
log(NIVEAUX[0]["hint"], (160, 200, 140))
log("F5 = executer  |  F11 = plein ecran", (120, 160, 120))

# ═══════════════════════════════════════════════════
#  BOUCLE PRINCIPALE
# ═══════════════════════════════════════════════════
while True:
    dt = clock.tick(60)

    if en_exec:
        timer += dt
        if timer >= DELAI_MS:
            timer = 0
            jouer_prochaine_etape()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        elif event.type == pygame.KEYDOWN:
            gerer_clavier(event)

        elif event.type == pygame.VIDEORESIZE:
            # L'utilisateur a redimensionne la fenetre manuellement
            recalculer_layout()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if not en_exec:
                if r_exec.collidepoint(pos):
                    executer()
                elif r_reset.collidepoint(pos):
                    reinitialiser(); messages.clear()
                    log("Reinitialise.", (100, 200, 255))
                elif r_clear.collidepoint(pos):
                    lignes[:] = [""]; cur_lig, cur_col = 0, 0
                elif ZONE_EDIT.collidepoint(pos):
                    cur_lig = min((pos[1] - ZONE_EDIT.y) // LH + scroll,
                                  len(lignes) - 1)
                    cur_col = 0
                    for c in range(len(lignes[cur_lig]) + 1):
                        if ZONE_EDIT.x + 22 + POLICE.size(lignes[cur_lig][:c])[0] >= pos[0]:
                            break
                        cur_col = c

    screen.fill(FOND)
    dessiner_carte()
    dessiner_steve()
    dessiner_interface()
    pygame.display.flip()
