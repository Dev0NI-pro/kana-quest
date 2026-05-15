import pygame, math
from settings import *

# ── Grade progression zones ───────────────────────────────────────────────────
# Map: 22 cols × 26 rows  (0-indexed)
# Layout (rows from TOP):
#  0    : top wall
#  1-3  : exterior grass + sakura + path
#  4    : school front wall (entrance door at cols 10-11)
#  5-7  : entrance hall (principal NPC at col 11, row 6)
#  8    : inner wall - door to CP (col 4) door to CE1 (col 17)
#  9-14 : CP classroom (cols 0-10)  |  CE1 classroom (cols 11-21)
#  15   : wall - LOCKED door to CE2/CM1 (unlocks after CP+CE1 done)
#  16-21: CE2 classroom (cols 0-10) |  CM1 classroom (cols 11-21)
#  22   : wall - LOCKED door to CM2 (unlocks after CE2+CM1 done)
#  23-25: CM2 classroom (full width)

# Tile aliases
F  = FLOOR
W  = WALL
D  = DESK
B  = BOARD
O  = DOOR_OPEN
X  = WINDOW
L  = LOCKER
P  = PATH
G  = GRASS
LK = LOCKED_DOOR
SK = SAKURA
ST = STAIR

_MAP = [
# col:0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],  # 0
    [W, G, G, SK,G, G, G, G, G, G, G, G, G, G, G, G, SK,G, G, G, G, W],  # 1
    [W, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, G, W],  # 2
    [W, G, G, G, G, G, P, P, P, P, P, P, P, P, P, P, G, G, G, G, G, W],  # 3  path
    [W, W, W, W, W, W, W, W, W, W, O, O, W, W, W, W, W, W, W, W, W, W],  # 4  entrance wall
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 5  entrance hall
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 6  principal here
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 7
    [W, W, W, W, O, W, W, W, W, W, W, W, W, W, W, W, W, O, W, W, W, W],  # 8  CP/CE1 doors
    [W, B, B, B, B, B, W, X, W, W, W, W, W, X, W, B, B, B, B, B, W, W],  # 9  boards
    [W, F, F, F, F, F, F, F, F, F, F, W, F, F, F, F, F, F, F, F, F, W],  # 10 teacher row
    [W, F, D, F, D, F, F, F, F, F, F, W, F, F, F, F, D, F, D, F, F, W],  # 11 desks
    [W, F, F, F, F, F, F, D, F, F, F, W, F, F, D, F, F, F, F, F, F, W],  # 12 desks
    [W, F, F, F, F, F, F, F, F, F, F, W, F, F, F, F, F, F, F, F, F, W],  # 13
    [W, F, L, L, F, F, F, F, F, F, F, W, F, F, F, F, F, F, L, L, F, W],  # 14 lockers
    [W, W, W, W, W, W, W, LK,W, W, W, W, W, W, W, LK,W, W, W, W, W, W],  # 15 LOCKED DOOR
    [W, B, B, B, B, B, W, X, W, W, W, W, W, X, W, B, B, B, B, B, W, W],  # 16 boards
    [W, F, F, F, F, F, F, F, F, F, F, W, F, F, F, F, F, F, F, F, F, W],  # 17 teacher row
    [W, F, D, F, D, F, F, F, F, F, F, W, F, F, F, F, D, F, D, F, F, W],  # 18 desks
    [W, F, F, F, F, F, F, D, F, F, F, W, F, F, D, F, F, F, F, F, F, W],  # 19 desks
    [W, F, F, F, F, F, F, F, F, F, F, W, F, F, F, F, F, F, F, F, F, W],  # 20
    [W, F, L, L, F, F, F, F, F, F, F, W, F, F, F, F, F, F, L, L, F, W],  # 21 lockers
    [W, W, W, W, W, W, W, W, W, W, W, LK,W, W, W, W, W, W, W, W, W, W],  # 22 LOCKED DOOR CM2
    [W, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W],  # 23 CM2 board
    [W, F, F, F, D, F, D, F, F, F, F, F, F, F, F, D, F, D, F, F, F, W],  # 24 desks
    [W, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, W],  # 25 CM2 floor
]

# NPC definitions: (tx, ty, grade, lesson_id, dialog_en, dialog_fr)
# ALL positions verified to be FLOOR tiles in _MAP above
NPC_DATA = [
    # ── Entrance Hall ─────────────────────────────────────────────────────────
    (11, 6, 0, "tutorial",
     "Welcome to Sakura Elementary!\nUse ARROW KEYS to walk.\nPress SPACE to talk to people.",
     "Bienvenue à l'École Sakura !\nUtilise les FLÈCHES pour marcher.\nAppuie sur ESPACE pour parler.",
     0),

    # ── Grade 1 / CP classroom (rows 9-14, cols 1-10) ─────────────────────────
    (5, 10, 1, "greetings",
     "こんにちは！ I'm your CP teacher!\nLet's learn greetings first!",
     "こんにちは！ Je suis ton prof de CP !\nApprenons les salutations d'abord !", 0),
    (4, 13, 1, "hiragana_vowels",
     "あいうえお！ These are the 5 vowels.\nThe foundation of Japanese!",
     "あいうえお！ Ce sont les 5 voyelles.\nLa base du japonais !", 0),
    (7, 12, 1, "numbers_1_10",
     "いち、に、さん！\nCan you count to 10 in Japanese?",
     "いち、に、さん！\nTu sais compter jusqu'à 10 ?", 0),

    # ── Grade 2 / CE1 classroom (rows 9-14, cols 12-21) ──────────────────────
    (16, 10, 2, "hiragana_ta",
     "Welcome to CE1! I'm your teacher.\nToday: TA, NA and HA rows!",
     "Bienvenue en CE1 ! Je suis ton prof.\nAujourd'hui : les lignes TA, NA, HA !", 0),
    (17, 12, 2, "school_items",
     "えんぴつ、ほん、かばん...\nKnow your school supplies!",
     "えんぴつ、ほん、かばん...\nTu connais tes fournitures scolaires ?", 0),
    (19, 13, 2, "days_of_week",
     "げつようび、かようび...\nLet's learn the days of the week!",
     "げつようび、かようび...\nApprenons les jours de la semaine !", 0),

    # ── Grade 3 / CE2 classroom (rows 16-21, cols 1-10) ──────────────────────
    (5, 17, 3, "katakana_basic",
     "Welcome to CE2! Katakana time!\nア、イ、ウ、エ、オ！",
     "Bienvenue en CE2 ! Les katakana !\nア、イ、ウ、エ、オ !", 0),
    (4, 19, 3, "food",
     "ごはん、すし、ラーメン！\nLearn delicious Japanese food!",
     "ごはん、すし、ラーメン !\nApprenons les plats japonais !", 0),
    (8, 20, 3, "telling_time",
     "いまなんじですか？\nWhat time is it? Let's practice!",
     "いまなんじですか？\nQuelle heure est-il ? Pratiquons !", 0),

    # ── Grade 4 / CM1 classroom (rows 16-21, cols 12-21) ─────────────────────
    (16, 17, 4, "katakana_loanwords",
     "CM1 - Katakana foreign words!\nテレビ、スマホ、コンピュータ！",
     "CM1 - Mots étrangers en katakana !\nテレビ、スマホ、コンピュータ !", 0),
    (18, 19, 4, "adjectives",
     "おおきい！ ちいさい！\nAdjectives make speech colorful!",
     "おおきい！ ちいさい！\nLes adjectifs colorent le discours !", 0),
    (20, 20, 4, "verbs_basic",
     "たべます、いきます、みます！\nBasic verbs — let's go!",
     "たべます、いきます、みます !\nVerbes de base — c'est parti !", 0),

    # ── Grade 5-6 / CM2 classroom (rows 23-25) ───────────────────────────────
    (5, 24, 5, "kanji_n5_numbers",
     "CM2! Time for Kanji!\nStart with numbers: 一二三四五！",
     "CM2 ! Les Kanji vous attendent !\nCommençons par les nombres !", 0),
    (11, 25, 5, "sentences_basic",
     "〜はなんですか？\nBasic Japanese sentences!",
     "〜はなんですか？\nPhrases japonaises de base !", 0),
    (16, 24, 6, "kanji_n5_nature",
     "山、川、木、森...\nNature kanji from JLPT N5!",
     "山、川、木、森...\nKanji de la nature JLPT N5 !", 0),
    (19, 25, 6, "grammar_te_form",
     "食べてください！\nThe て-form — Japanese grammar!",
     "食べてください！\nLa forme て — grammaire japonaise !", 0),
]

# Signs: (tx, ty, text_en, text_fr)
SIGNS_DATA = [
    (11, 5,  "SAKURA ELEMENTARY SCHOOL",    "ÉCOLE PRIMAIRE SAKURA"),
    (5,  8,  "Grade 1  CP  一年",            "CP  一年組"),
    (17, 8,  "Grade 2  CE1  二年",           "CE1  二年組"),
    (5,  15, "Grade 3  CE2  三年",           "CE2  三年組"),
    (17, 15, "Grade 4  CM1  四年",           "CM1  四年組"),
    (11, 22, "Grade 5-6  CM2  五六年",       "CM2  五・六年組"),
]

# Grade locked doors: (tx, ty, required_grades_done)
LOCK_DATA = [
    (7,  15, {1, 2}),   # needs CP+CE1 to unlock CE2/CM1
    (15, 15, {1, 2}),   # same gate
    (11, 22, {3, 4}),   # needs CE2+CM1 to unlock CM2
]

# Classroom grade zones: grade -> set of (tx,ty) tuples that are LOCKED until prev grade
GRADE_ZONES = {
    3: [(col, row) for row in range(15, 22) for col in range(0, 22)],
    4: [(col, row) for row in range(15, 22) for col in range(0, 22)],
    5: [(col, row) for row in range(22, 26) for col in range(0, 22)],
    6: [(col, row) for row in range(22, 26) for col in range(0, 22)],
}


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
            # Check which lock this door belongs to
            for lx, ly, required in LOCK_DATA:
                if abs(tx - lx) <= 2 and ty == ly:
                    return all(g in grade_progress for g in required)
            return False
        return tile in PASSABLE

    def unlock_visually(self, tx, ty):
        if self.get(tx, ty) == LOCKED_DOOR:
            self.data[ty][tx] = DOOR_OPEN

    def draw(self, surf, cam_x, cam_y, sw, sh):
        stx = cam_x // TILE
        sty = cam_y // TILE
        etx = stx + sw // TILE + 2
        ety = sty + sh // TILE + 2
        for ty in range(max(0, sty), min(self.height, ety)):
            for tx in range(max(0, stx), min(self.width, etx)):
                tile = self.data[ty][tx]
                sx = tx * TILE - cam_x
                sy = ty * TILE - cam_y
                self._draw_tile(surf, tile, sx, sy, tx, ty)

    def _draw_tile(self, surf, tile, sx, sy, tx, ty):
        T = TILE
        if tile == GRASS:
            color = C["grass"] if (tx + ty) % 2 == 0 else C["grass2"]
            pygame.draw.rect(surf, color, (sx, sy, T, T))

        elif tile == SAKURA:
            pygame.draw.rect(surf, C["grass"], (sx, sy, T, T))
            # Sakura tree trunk
            pygame.draw.rect(surf, (160, 120, 80), (sx + T//2 - 2, sy + T//2, 4, T//2))
            # Sakura puff
            pygame.draw.circle(surf, C["sakura"],       (sx + T//2, sy + T//2 - 2), 10)
            pygame.draw.circle(surf, C["sakura_light"],  (sx + T//2 - 4, sy + T//2 - 5), 6)
            pygame.draw.circle(surf, C["sakura_dark"],   (sx + T//2 + 4, sy + T//2), 5)

        elif tile == PATH:
            pygame.draw.rect(surf, C["path"], (sx, sy, T, T))
            pygame.draw.rect(surf, (220, 205, 180), (sx+2, sy+2, T-4, T-4))

        elif tile == FLOOR:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.line(surf, C["floor_detail"], (sx, sy + 10), (sx + T, sy + 10), 1)
            pygame.draw.line(surf, C["floor_detail"], (sx, sy + 21), (sx + T, sy + 21), 1)

        elif tile == WALL:
            pygame.draw.rect(surf, C["wall_outer"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["wall_top"],   (sx, sy, T, T // 3 + 2))
            pygame.draw.rect(surf, C["wall_inner"],
                             (sx + 2, sy + T//3 + 2, T - 4, T*2//3 - 4))

        elif tile == BOARD:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["blackboard"], (sx + 1, sy + 3, T - 2, T - 6))
            # Chalk marks
            for i, col_offset in enumerate([4, 10, 16]):
                pygame.draw.line(surf, C["chalk"],
                                 (sx + col_offset, sy + T//2 - 3),
                                 (sx + col_offset + 5, sy + T//2 + 1), 1)

        elif tile == DESK:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["desk"],       (sx + 2, sy + 3, T - 4, T - 10), border_radius=2)
            pygame.draw.rect(surf, C["desk_dark"],  (sx + 2, sy + T - 9, T - 4, 4))
            # cute book on desk
            pygame.draw.rect(surf, C["sakura"],     (sx + 5, sy + 5, 8, 6), border_radius=1)

        elif tile == DOOR_OPEN:
            pygame.draw.rect(surf, C["floor_hall"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["door_frame"], (sx, sy, T, 3))
            pygame.draw.rect(surf, C["door_frame"], (sx, sy + T - 3, T, 3))
            pygame.draw.rect(surf, C["door_wood"],  (sx + 2, sy + 3, 5, T - 6), border_radius=1)

        elif tile == LOCKED_DOOR:
            pygame.draw.rect(surf, C["locked_door"], (sx, sy, T, T))
            # Lock symbol
            pygame.draw.rect(surf, C["locked_bar"],  (sx + 8, sy + 14, 14, 10), border_radius=2)
            pygame.draw.arc(surf, C["locked_bar"],
                            (sx + 10, sy + 7, 10, 12), 0, math.pi, 2)
            pygame.draw.circle(surf, C["floor_wood"], (sx + 15, sy + 19), 2)

        elif tile == WINDOW:
            pygame.draw.rect(surf, C["wall_inner"],   (sx, sy, T, T))
            pygame.draw.rect(surf, C["window_sky"],   (sx + 3, sy + 3, T - 6, T - 6))
            pygame.draw.rect(surf, C["window_frame"], (sx + 3, sy + 3, T - 6, T - 6), 1)
            # Cross
            pygame.draw.line(surf, C["window_frame"],
                             (sx + T//2, sy + 3), (sx + T//2, sy + T - 3), 1)
            pygame.draw.line(surf, C["window_frame"],
                             (sx + 3, sy + T//2), (sx + T - 3, sy + T//2), 1)

        elif tile == LOCKER:
            pygame.draw.rect(surf, C["locker"],        (sx, sy, T, T))
            pygame.draw.rect(surf, C["locker_stripe"], (sx + 2, sy + 2, T - 4, T//2 - 2), border_radius=1)
            pygame.draw.rect(surf, C["locker_stripe"], (sx + 2, sy + T//2 + 1, T - 4, T//2 - 3), border_radius=1)
            pygame.draw.circle(surf, C["gold"],        (sx + T - 6, sy + T//4), 2)
            pygame.draw.circle(surf, C["gold"],        (sx + T - 6, sy + 3*T//4), 2)

        else:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
