import pygame, math
from settings import *

# ── Map layout (22 cols × 29 rows) ────────────────────────────────────────────
#
#  Row 0     : top wall
#  Row 1-3   : exterior (grass, sakura, path)
#  Row 4     : school front wall (entrance door cols 10-11)
#  Row 5-6   : entrance hall  [principal at (11,6)]
#  Row 7     : inner wall — door to CP at col 3, corridor at cols 10-11,
#                            door to CE1 at col 18
#  Row 8-11  : CP classroom (cols 1-9) | corridor (10-11) | CE1 (cols 12-20)
#  Row 12    : board/window wall at classroom ends — corridor continues
#  Row 13    : wall + corridor
#  Row 14    : *** LOCKED GATE *** (cols 10-11, needs grades 1+2)
#  Row 15    : corridor
#  Row 16    : wall — door to CE2 at col 3, corridor 10-11, door to CM1 col 18
#  Row 17-20 : CE2 classroom (cols 1-9) | corridor | CM1 (cols 12-20)
#  Row 21    : board/window wall — corridor continues
#  Row 22    : wall + corridor
#  Row 23    : *** LOCKED GATE *** (cols 10-11, needs grades 3+4)
#  Row 24-26 : CM2 classroom (full width)
#  Row 27    : CM2 board wall
#  Row 28    : bottom wall

F  = FLOOR;      W = WALL;     D = DESK;      B = BOARD
O  = DOOR_OPEN;  X = WINDOW;   L = LOCKER
P  = PATH;       G = GRASS;    SK= SAKURA
LK = LOCKED_DOOR

_MAP = [
# col: 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],  # 0
    [W, G, G,SK, G, G, G, G, G, G, G, G, G, G, G, G,SK, G, G, G, G, W],  # 1
    [W, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, W],  # 2
    [W, G, G, G, G, G, P, P, P, P, P, P, P, P, P, P, G, G, G, G, G, W],  # 3
    [W, W, W, W, W, W, W, W, W, W, O, O, W, W, W, W, W, W, W, W, W, W],  # 4 entrance wall
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 5 entrance hall
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 6 principal NPC here
    [W, W, W, O, W, W, W, W, W, W, F, F, W, W, W, W, W, W, O, W, W, W],  # 7 CP door(3) | corridor | CE1 door(18)
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 8 classroom floor
    [W, F, D, F, D, F, F, F, F, F, F, F, F, F, F, F, D, F, D, F, F, W],  # 9 desks
    [W, F, F, F, F, F, F, D, F, F, F, F, F, D, F, F, F, F, F, F, F, W],  # 10 desks
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 11 teacher row
    [W, W, B, B, B, B, W, X, W, W, F, F, W, W, X, W, B, B, B, B, W, W],  # 12 board wall (bottom CP/CE1) + corridor
    [W, W, W, W, W, W, W, W, W, W, F, F, W, W, W, W, W, W, W, W, W, W],  # 13 wall + corridor
    [W, W, W, W, W, W, W, W, W, W,LK,LK, W, W, W, W, W, W, W, W, W, W],  # 14 LOCKED GATE (grades 1+2)
    [W, W, W, W, W, W, W, W, W, W, F, F, W, W, W, W, W, W, W, W, W, W],  # 15 corridor
    [W, W, W, O, W, W, W, W, W, W, F, F, W, W, W, W, W, W, O, W, W, W],  # 16 CE2 door(3) | corridor | CM1 door(18)
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 17 classroom floor
    [W, F, D, F, D, F, F, F, F, F, F, F, F, F, F, F, D, F, D, F, F, W],  # 18 desks
    [W, F, F, F, F, F, F, D, F, F, F, F, F, D, F, F, F, F, F, F, F, W],  # 19 desks
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 20 teacher row
    [W, W, B, B, B, B, W, X, W, W, F, F, W, W, X, W, B, B, B, B, W, W],  # 21 board wall (bottom CE2/CM1) + corridor
    [W, W, W, W, W, W, W, W, W, W, F, F, W, W, W, W, W, W, W, W, W, W],  # 22 wall + corridor
    [W, W, W, W, W, W, W, W, W, W,LK,LK, W, W, W, W, W, W, W, W, W, W],  # 23 LOCKED GATE (grades 3+4)
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 24 CM2 entry floor
    [W, F, D, F, D, F, F, F, F, F, F, F, F, F, F, D, F, D, F, F, F, W],  # 25 CM2 desks
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 26 CM2 floor (teacher row)
    [W, W, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W, W],  # 27 CM2 board wall
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],  # 28 bottom wall
]

# ── NPC data (ALL positions verified as FLOOR tiles in _MAP) ──────────────────
NPC_DATA = [
    # ── Entrance hall ─────────────────────────────────────────────────────────
    (11, 6, 0, "tutorial",
     "Welcome to Sakura Elementary!\nArrow keys to walk, SPACE to talk.\nComplete each grade to unlock the next!",
     "Bienvenue a l'Ecole Sakura !\nFleches pour marcher, ESPACE pour parler.\nComplete chaque niveau pour avancer !", 0),

    # ── CP classroom (cols 1-9, rows 8-11) ────────────────────────────────────
    (5, 11, 1, "greetings",
     "Good morning! Ohayou gozaimasu!\nLet's learn Japanese greetings!",
     "Bonjour ! Ohayou gozaimasu !\nApprenons les salutations japonaises !", 0),
    (3, 9, 1, "hiragana_vowels",
     "A-I-U-E-O! The 5 vowels!\nThe very foundation of Japanese.",
     "A-I-U-E-O ! Les 5 voyelles !\nLa base absolue du japonais.", 0),
    (7, 10, 1, "numbers_1_10",
     "Ichi, ni, san! Let's count to 10!",
     "Ichi, ni, san ! Comptons jusqu'a 10 !", 0),
    (1, 8, 1, "colors",
     "Aka is red, ao is blue!\nLearn all the Japanese colors!",
     "Aka c'est rouge, ao c'est bleu !\nApprends toutes les couleurs !", 0),

    # ── CE1 classroom (cols 12-20, rows 8-11) ─────────────────────────────────
    (16, 11, 2, "hiragana_ta",
     "TA, NA, HA rows! Let's continue\nlearning hiragana together!",
     "Les lignes TA, NA, HA ! Continuons\nles hiragana ensemble !", 0),
    (14, 9, 2, "school_items",
     "Enpitsu, hon, kaban...\nDo you know your school supplies?",
     "Enpitsu, hon, kaban...\nTu connais tes fournitures scolaires ?", 0),
    (19, 10, 2, "days_of_week",
     "Getsuyoubi, kayoubi...\nLearn the days of the week!",
     "Getsuyoubi, kayoubi...\nApprends les jours de la semaine !", 0),

    # ── CE2 classroom (cols 1-9, rows 17-20) ──────────────────────────────────
    (5, 20, 3, "katakana_basic",
     "Katakana! Used for foreign words.\nLet's learn: ア、イ、ウ、エ、オ!",
     "Les katakana ! Pour les mots etrangers.\nApprenons : ア、イ、ウ、エ、オ !", 0),
    (3, 18, 3, "food",
     "Gohan, sushi, ramen!\nLearn delicious Japanese food!",
     "Gohan, sushi, ramen !\nApprenons la delicieuse cuisine japonaise !", 0),
    (7, 19, 3, "telling_time",
     "Ima nanji desu ka?\nWhat time is it? Let's practice!",
     "Ima nanji desu ka ?\nQuelle heure est-il ? Pratiquons !", 0),

    # ── CM1 classroom (cols 12-20, rows 17-20) ────────────────────────────────
    (16, 20, 4, "katakana_loanwords",
     "Terebi, sumaho, konpyuuta!\nKatakana for loanwords!",
     "Terebi, sumaho, konpyuuta !\nKatakana pour les mots empruntes !", 0),
    (19, 18, 4, "adjectives",
     "Ookii! Chiisai! Yasashii!\nAdjectives make your Japanese vivid!",
     "Ookii ! Chiisai ! Yasashii !\nLes adjectifs donnent vie au japonais !", 0),
    (13, 19, 4, "verbs_basic",
     "Tabemasu, ikimasu, mimasu!\nTime for basic Japanese verbs!",
     "Tabemasu, ikimasu, mimasu !\nLes verbes de base en japonais !", 0),

    # ── CM2 classroom (cols 1-20, rows 24-26) ─────────────────────────────────
    (11, 26, 5, "kanji_n5_numbers",
     "Kanji! The ultimate challenge!\nStart with: 一、二、三、四、五!",
     "Les Kanji ! Le defi ultime !\nCommençons par : 一、二、三、四、五 !", 0),
    (5, 25, 5, "sentences_basic",
     "~ wa nan desu ka?\nBasic Japanese sentence patterns!",
     "~ wa nan desu ka ?\nPatterns de phrases japonaises de base !", 0),
    (14, 25, 6, "kanji_n5_nature",
     "Yama, kawa, ki, mori...\nNature kanji from JLPT N5!",
     "Yama, kawa, ki, mori...\nKanji de la nature au JLPT N5 !", 0),
    (17, 24, 6, "grammar_te_form",
     "Tabete kudasai! Mite imasu!\nThe te-form — master Japanese grammar!",
     "Tabete kudasai ! Mite imasu !\nLa forme te — maitrisez la grammaire !", 0),
]

# ── Signs ─────────────────────────────────────────────────────────────────────
SIGNS_DATA = [
    (11, 5,  "SAKURA ELEMENTARY",      "ECOLE PRIMAIRE SAKURA"),
    (3,  6,  "CP  Grade 1",            "CP  1ere annee"),
    (18, 6,  "CE1  Grade 2",           "CE1  2eme annee"),
    (3,  15, "CE2  Grade 3",           "CE2  3eme annee"),
    (18, 15, "CM1  Grade 4",           "CM1  4eme annee"),
    (11, 23, "CM2  Grades 5-6",        "CM2  5-6eme annee"),
]

# ── Locks: (tx, ty, required_grades) ─────────────────────────────────────────
LOCK_DATA = [
    (10, 14, frozenset({1, 2})),
    (11, 14, frozenset({1, 2})),
    (10, 23, frozenset({3, 4})),
    (11, 23, frozenset({3, 4})),
]


class Tilemap:
    def __init__(self):
        self.data   = [row[:] for row in _MAP]
        self.height = len(self.data)
        self.width  = len(self.data[0])

    def get(self, tx, ty):
        if 0 <= ty < self.height and 0 <= tx < self.width:
            return self.data[ty][tx]
        return WALL

    def is_passable(self, tx, ty, grade_progress=None):
        tile = self.get(tx, ty)
        if tile == LOCKED_DOOR:
            if grade_progress is None:
                return False
            for lx, ly, required in LOCK_DATA:
                if tx == lx and ty == ly:
                    return required.issubset(grade_progress)
            return False
        return tile in PASSABLE

    def unlock_visually(self, tx, ty):
        if self.get(tx, ty) == LOCKED_DOOR:
            self.data[ty][tx] = DOOR_OPEN

    def draw(self, surf, cam_x, cam_y, sw, sh):
        stx = max(0, cam_x // TILE)
        sty = max(0, cam_y // TILE)
        etx = min(self.width,  stx + sw // TILE + 2)
        ety = min(self.height, sty + sh // TILE + 2)
        for ty in range(sty, ety):
            for tx in range(stx, etx):
                self._draw_tile(surf, self.data[ty][tx],
                                tx * TILE - cam_x, ty * TILE - cam_y)

    def _draw_tile(self, surf, tile, sx, sy):
        T = TILE
        if tile == GRASS:
            col = C["grass"] if (sx // T + sy // T) % 2 == 0 else C["grass2"]
            pygame.draw.rect(surf, col, (sx, sy, T, T))

        elif tile == SAKURA:
            pygame.draw.rect(surf, C["grass"], (sx, sy, T, T))
            pygame.draw.rect(surf, (160,120,80), (sx+T//2-2, sy+T//2, 4, T//2))
            pygame.draw.circle(surf, C["sakura"],      (sx+T//2,   sy+T//2-2), 10)
            pygame.draw.circle(surf, C["sakura_light"],(sx+T//2-4, sy+T//2-5),  6)
            pygame.draw.circle(surf, C["sakura_dark"], (sx+T//2+4, sy+T//2),    5)

        elif tile == PATH:
            pygame.draw.rect(surf, C["path"], (sx, sy, T, T))
            pygame.draw.rect(surf, (220,205,180), (sx+2, sy+2, T-4, T-4))

        elif tile == FLOOR:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.line(surf, C["floor_detail"], (sx,sy+10),(sx+T,sy+10),1)
            pygame.draw.line(surf, C["floor_detail"], (sx,sy+21),(sx+T,sy+21),1)

        elif tile == WALL:
            pygame.draw.rect(surf, C["wall_outer"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["wall_top"],   (sx, sy, T, T//3+2))
            pygame.draw.rect(surf, C["wall_inner"],
                             (sx+2, sy+T//3+2, T-4, T*2//3-4))

        elif tile == BOARD:
            pygame.draw.rect(surf, C["wall_outer"],  (sx, sy, T, T))
            pygame.draw.rect(surf, C["blackboard"],  (sx+1, sy+3, T-2, T-6))
            for ox in (3, 9, 15):
                pygame.draw.line(surf, C["chalk"],
                                 (sx+ox, sy+T//2-2),(sx+ox+5, sy+T//2+2),1)

        elif tile == DOOR_OPEN:
            pygame.draw.rect(surf, C["floor_hall"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["door_frame"], (sx, sy, T, 3))
            pygame.draw.rect(surf, C["door_frame"], (sx, sy+T-3, T, 3))
            pygame.draw.rect(surf, C["door_wood"],  (sx+2, sy+3, 5, T-6), border_radius=1)

        elif tile == LOCKED_DOOR:
            pygame.draw.rect(surf, C["locked_door"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["locked_bar"],  (sx+8, sy+14, 14, 10), border_radius=2)
            pygame.draw.arc(surf,  C["locked_bar"],
                            (sx+10, sy+7, 10, 12), 0, math.pi, 2)
            pygame.draw.circle(surf, C["floor_wood"], (sx+15, sy+19), 2)

        elif tile == WINDOW:
            pygame.draw.rect(surf, C["wall_inner"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["window_sky"], (sx+3, sy+3, T-6, T-6))
            pygame.draw.rect(surf, C["window_frame"],(sx+3,sy+3,T-6,T-6),1)
            pygame.draw.line(surf, C["window_frame"],(sx+T//2,sy+3),(sx+T//2,sy+T-3),1)
            pygame.draw.line(surf, C["window_frame"],(sx+3,sy+T//2),(sx+T-3,sy+T//2),1)

        elif tile == DESK:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["desk"],       (sx+2, sy+3, T-4, T-10), border_radius=2)
            pygame.draw.rect(surf, C["desk_dark"],  (sx+2, sy+T-9, T-4, 4))
            pygame.draw.rect(surf, C["sakura"],     (sx+5, sy+5, 8, 6), border_radius=1)

        else:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
