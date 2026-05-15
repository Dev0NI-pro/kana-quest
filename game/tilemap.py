import pygame
from settings import *

# ── School map layout (each cell = 1 tile 32×32px) ───────────────────────────
# Legend:
#  0=floor  1=wall  2=desk  3=blackboard  4=door
#  5=window 6=locker 7=bookshelf 8=carpet 9=path
# 10=grass  11=void  12=desk(south) 13=chair  14=teacher_desk  15=sign

# 30 wide × 28 tall
RAW_MAP = [
# 0         1         2         3
# 0123456789012345678901234567890
  "111111111111111111111111111111",  # 0  top wall
  "100000000000000011000000000001",  # 1  exterior space
  "100000000000000011000000000001",  # 2
  "100001111111111111111111110001",  # 3  school building outline
  "100001133333333313333333310001",  # 4  top classroom row (boards)
  "100001100000000010000000010001",  # 5
  "1000011000D D00010 D D 0010001",  # 6  desks grade 1 / grade 2
  "100001100D D D00010D D D010001",  # 7
  "100001100000000010000000010001",  # 8
  "100001111411111111411111110001",  # 9  walls with doors
  "100001100000000000000000010001",  # 10 hallway (corridor) — floor
  "100001100000000000000000010001",  # 11
  "100001111411111111411111110001",  # 12 walls with doors
  "100001100000000010000000010001",  # 13
  "1000011000D D00010 D D 0010001",  # 14 desks grade 3 / grade 4
  "100001100D D D00010D D D010001",  # 15
  "100001100000000010000000010001",  # 16
  "100001133333333313333333310001",  # 17 boards grade 3/4
  "100001111111111111111111110001",  # 18 bottom wall
  "100001100000000001000000010001",  # 19 teachers room / gym entrance
  "100001100000000001000000010001",  # 20
  "100001111111114111111111110001",  # 21
  "100000000000040000000000000001",  # 22 school entrance / path
  "100000000000090000000000000001",  # 23 front path
  "199999999999999999999999999001",  # 24 main path (horizontal)
  "100000000000000000000000000001",  # 25 front yard grass
  "100000000000000000000000000001",  # 26
  "111111111111111111111111111111",  # 27 bottom wall
]

# We need clean integer tiles, so let's define the map programmatically
def _build_map():
    rows = []
    for row in RAW_MAP:
        line = []
        for ch in row[:30]:
            if ch == '1': line.append(WALL)
            elif ch == '3': line.append(BOARD)
            elif ch == '4': line.append(DOOR_OPEN)
            elif ch == '5': line.append(WINDOW)
            elif ch == '6': line.append(LOCKER)
            elif ch == '7': line.append(BOOKSHELF)
            elif ch == '8': line.append(CARPET)
            elif ch == '9': line.append(PATH)
            elif ch in ('D', 'd'): line.append(DESK)
            else: line.append(FLOOR)
        rows.append(line)
    return rows

# NPC spawn data: (tile_x, tile_y, grade, lesson_id, dialog_en, dialog_fr, facing_dir)
NPC_DATA = [
    # Grade 1 classroom teacher (top-left room)
    (5, 5, 1, "greetings",
     "Welcome! Let's learn greetings!\nSay hello to everyone!",
     "Bienvenue ! Apprenons les salutations !\nDis bonjour à tout le monde !",
     0),  # facing DOWN
    (7, 7, 1, "hiragana_vowels",
     "Hiragana are the first characters\nyou learn in Japan. Let's start!",
     "Les hiragana sont les premiers\ncaractères appris au Japon. Commençons !",
     0),
    (9, 6, 1, "numbers_1_10",
     "いち、に、さん! Can you count\nto 10 in Japanese?",
     "いち、に、さん ! Tu sais compter\njusqu'à 10 en japonais ?",
     0),
    (11, 7, 1, "colors",
     "あか is red, あお is blue...\nLearn all the colors!",
     "あか c'est rouge, あお c'est bleu...\nApprends toutes les couleurs !",
     0),

    # Grade 2 classroom teacher (top-right room)
    (18, 5, 2, "hiragana_ta",
     "Let's continue hiragana!\nTA, NA and HA rows today.",
     "Continuons les hiragana !\nLes lignes TA, NA et HA aujourd'hui.",
     0),
    (20, 7, 2, "school_items",
     "えんぴつ, ほん, かばん...\nDo you know your school items?",
     "えんぴつ, ほん, かばん...\nTu connais tes fournitures ?",
     0),
    (22, 6, 2, "days_of_week",
     "Getsuyoubi, Kayoubi...\nLearn the days of the week!",
     "Getsuyoubi, Kayoubi...\nApprends les jours de la semaine !",
     0),
    (24, 7, 2, "family",
     "Otousan, Okaasan...\nLet's talk about family!",
     "Otousan, Okaasan...\nParlons de la famille !",
     0),

    # Grade 3 classroom teacher (bottom-left room)
    (5, 14, 3, "katakana_basic",
     "Katakana is used for foreign words.\nア、イ、ウ、エ、オ!",
     "Les katakana servent pour les mots étrangers.\nア、イ、ウ、エ、オ !",
     0),
    (7, 15, 3, "food",
     "ごはん, ラーメン, すし...\nLearn delicious Japanese food!",
     "ごはん, ラーメン, すし...\nApprends les délicieux plats japonais !",
     0),
    (9, 14, 3, "telling_time",
     "いまなんじですか？\nWhat time is it? Let's find out!",
     "いまなんじですか？\nQuelle heure est-il ? Apprenons !",
     0),

    # Grade 4 classroom teacher (bottom-right room)
    (18, 14, 4, "katakana_loanwords",
     "テレビ, コンピュータ, スマホ...\nKatakana for loanwords!",
     "テレビ, コンピュータ, スマホ...\nKatakana pour les mots empruntés !",
     0),
    (20, 15, 4, "adjectives",
     "おおきい！ちいさい！\nLearn adjectives today.",
     "おおきい！ちいさい！\nApprenons les adjectifs aujourd'hui.",
     0),
    (22, 14, 4, "verbs_basic",
     "たべます、のみます、みます...\nBasic Japanese verbs await!",
     "たべます、のみます、みます...\nLes verbes de base vous attendent !",
     0),

    # Hallway NPC (student wandering)
    (13, 10, 5, "sentences_basic",
     "Psst! Want to learn\ncool sentences in Japanese?",
     "Psst ! Tu veux apprendre\nde super phrases en japonais ?",
     0),
    (15, 11, 5, "seasons_weather",
     "はるですね！It's spring!\nLearn seasons and weather.",
     "はるですね！C'est le printemps !\nApprends les saisons et la météo.",
     0),

    # Grade 5/6 in teachers room area
    (7, 20, 5, "kanji_n5_numbers",
     "Kanji! The characters of Japanese.\nStart with numbers and time.",
     "Kanji ! Les caractères japonais.\nCommençons par les nombres.",
     0),
    (22, 20, 6, "kanji_n5_nature",
     "山、川、木、森...\nNature kanji from JLPT N5!",
     "山、川、木、森...\nLes kanji de la nature au JLPT N5 !",
     0),
    (13, 20, 6, "grammar_te_form",
     "食べてください！\nLet's learn the て-form!",
     "食べてください！\nApprenons la forme en て !",
     0),
]

# Signs: (tile_x, tile_y, text_en, text_fr)
SIGNS = [
    (13, 3, "SAKURA ELEMENTARY SCHOOL", "ÉCOLE PRIMAIRE SAKURA"),
    (5,  3, "Grade 1  年組",            "CP  一年組"),
    (20, 3, "Grade 2  二年組",           "CE1 二年組"),
    (5, 17, "Grade 3  三年組",           "CE2 三年組"),
    (20,17, "Grade 4  四年組",           "CM1 四年組"),
    (5, 19, "Grade 5–6  五・六年組",     "CM2 五・六年組"),
]


class Tilemap:
    def __init__(self):
        self.data   = _build_map()
        self.height = len(self.data)
        self.width  = len(self.data[0]) if self.data else 0

    def get(self, tx: int, ty: int) -> int:
        if 0 <= ty < self.height and 0 <= tx < self.width:
            return self.data[ty][tx]
        return WALL

    def is_passable(self, tx: int, ty: int) -> bool:
        return self.get(tx, ty) in PASSABLE

    def draw(self, surf: pygame.Surface, cam_x: int, cam_y: int,
             screen_w: int, screen_h: int):
        start_tx = cam_x // TILE
        start_ty = cam_y // TILE
        end_tx   = start_tx + screen_w // TILE + 2
        end_ty   = start_ty + screen_h // TILE + 2

        for ty in range(max(0, start_ty), min(self.height, end_ty)):
            for tx in range(max(0, start_tx), min(self.width, end_tx)):
                tile   = self.data[ty][tx]
                sx     = tx * TILE - cam_x
                sy     = ty * TILE - cam_y
                colors = TILE_COLORS.get(tile, [C["floor_wood"], C["floor_wood"]])
                self._draw_tile(surf, tile, sx, sy, colors)

    def _draw_tile(self, surf, tile, sx, sy, colors):
        T = TILE
        base, detail = colors[0], colors[1]

        if tile == FLOOR:
            pygame.draw.rect(surf, base, (sx, sy, T, T))
            # subtle wood grain lines
            pygame.draw.line(surf, detail, (sx, sy+10), (sx+T, sy+10), 1)
            pygame.draw.line(surf, detail, (sx, sy+21), (sx+T, sy+21), 1)

        elif tile == WALL:
            pygame.draw.rect(surf, C["wall_outer"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["wall_top"],   (sx, sy, T, T//3))
            pygame.draw.rect(surf, C["wall_inner"], (sx+2, sy+T//3, T-4, T*2//3-2))

        elif tile == BOARD:
            pygame.draw.rect(surf, base,   (sx, sy, T, T))
            pygame.draw.rect(surf, detail, (sx+2, sy+4, T-4, T-8), 0)
            # chalk mark
            pygame.draw.line(surf, C["chalk"], (sx+5, sy+T//2), (sx+20, sy+T//2+2), 1)
            pygame.draw.line(surf, C["chalk"], (sx+8, sy+T//2-3), (sx+18, sy+T//2-1), 1)

        elif tile == DOOR_OPEN:
            pygame.draw.rect(surf, C["floor_hall"], (sx, sy, T, T))
            pygame.draw.rect(surf, C["door_frame"], (sx, sy, T, 4))
            pygame.draw.rect(surf, C["door_frame"], (sx, sy+T-4, T, 4))
            pygame.draw.rect(surf, C["door_wood"],  (sx+2, sy+4, 6, T-8))

        elif tile == WINDOW:
            pygame.draw.rect(surf, C["wall_inner"],   (sx, sy, T, T))
            pygame.draw.rect(surf, C["window_sky"],   (sx+4, sy+4, T-8, T-8))
            pygame.draw.line(surf, C["window_frame"], (sx+T//2, sy+4), (sx+T//2, sy+T-4), 1)
            pygame.draw.line(surf, C["window_frame"], (sx+4, sy+T//2), (sx+T-4, sy+T//2), 1)

        elif tile == LOCKER:
            pygame.draw.rect(surf, base,   (sx, sy, T, T))
            pygame.draw.rect(surf, detail, (sx+2, sy+2, T-4, T//2-2))
            pygame.draw.rect(surf, detail, (sx+2, sy+T//2+1, T-4, T//2-3))
            pygame.draw.circle(surf, C["gold"], (sx+T-6, sy+T//4), 2)
            pygame.draw.circle(surf, C["gold"], (sx+T-6, sy+3*T//4), 2)

        elif tile == BOOKSHELF:
            pygame.draw.rect(surf, base,   (sx, sy, T, T))
            for i in range(4):
                bc = [(180,50,50),(50,80,180),(80,160,80),(180,160,50)][i]
                pygame.draw.rect(surf, bc, (sx+2+i*7, sy+4, 6, T-8))

        elif tile == CARPET:
            pygame.draw.rect(surf, base, (sx, sy, T, T))
            pygame.draw.rect(surf, (130,35,35), (sx+2, sy+2, T-4, T-4), 2)

        elif tile == PATH:
            pygame.draw.rect(surf, base, (sx, sy, T, T))
            pygame.draw.rect(surf, (170,155,130), (sx+1, sy+1, T-2, T-2))

        elif tile == GRASS:
            pygame.draw.rect(surf, base, (sx, sy, T, T))
            # grass texture
            pygame.draw.rect(surf, detail, (sx, sy, T//2, T//2))
            pygame.draw.rect(surf, base,   (sx+T//2, sy+T//2, T//2, T//2))

        elif tile == DESK:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.rect(surf, base,   (sx+2, sy+2, T-4, T-10))
            pygame.draw.rect(surf, detail, (sx+2, sy+T-10, T-4, 4))
            # pencil case
            pygame.draw.rect(surf, (200,100,100), (sx+5, sy+4, 8, 4))

        elif tile == TEACHER_DESK:
            pygame.draw.rect(surf, C["floor_wood"], (sx, sy, T, T))
            pygame.draw.rect(surf, base,   (sx+1, sy+2, T-2, T-8))
            pygame.draw.rect(surf, detail, (sx+1, sy+T-8, T-2, 4))

        elif tile == VOID:
            pygame.draw.rect(surf, C["sky"], (sx, sy, T, T))

        else:
            pygame.draw.rect(surf, base, (sx, sy, T, T))
