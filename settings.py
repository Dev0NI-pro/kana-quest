import pygame

SW, SH = 800, 600
TILE    = 32
FPS     = 60
TITLE   = "Kana Quest"

# ── Pastel Japanese Dream Palette ─────────────────────────────────────────────
C = {
    # Sky & nature
    "sky":           (210, 235, 255),
    "sky2":          (230, 245, 255),
    "sakura":        (255, 192, 210),
    "sakura_dark":   (235, 155, 185),
    "sakura_light":  (255, 220, 230),
    "leaf":          (160, 210, 160),
    "grass":         (190, 230, 175),
    "grass2":        (170, 215, 155),
    "path":          (235, 220, 195),
    # School building
    "wall_outer":    (240, 220, 235),   # soft pinkish-white
    "wall_top":      (255, 235, 245),
    "wall_inner":    (250, 240, 248),
    "floor_wood":    (240, 220, 185),   # warm honey wood
    "floor_hall":    (230, 215, 205),
    "floor_detail":  (225, 205, 170),
    "blackboard":    (130, 180, 150),   # sage green
    "chalk":         (245, 240, 235),
    "desk":          (210, 175, 130),
    "desk_dark":     (185, 148, 100),
    "door_wood":     (195, 148, 100),
    "door_frame":    (165, 118, 78),
    "window_sky":    (190, 225, 245),
    "window_frame":  (220, 195, 210),
    "locker":        (180, 210, 235),
    "locker_stripe": (160, 190, 215),
    "carpet":        (220, 180, 200),
    "locked_door":   (180, 165, 175),
    "locked_bar":    (150, 135, 145),
    "sign":          (255, 240, 215),
    # UI panels
    "bg":            (255, 248, 252),
    "panel":         (250, 235, 245),
    "panel2":        (245, 225, 238),
    "border":        (210, 165, 195),
    "border2":       (235, 185, 215),
    "text":          ( 80,  50,  70),
    "text_dim":      (160, 130, 150),
    "text_light":    (220, 195, 210),
    "gold":          (255, 205,  80),
    "gold2":         (255, 225, 130),
    "green":         (100, 200, 140),
    "red":           (220,  90,  90),
    "blue":          (110, 170, 235),
    "purple":        (180, 140, 220),
    "white":         (255, 255, 255),
    "black":         (  0,   0,   0),
    # Character (player)
    "skin":          (255, 218, 190),
    "skin_shadow":   (235, 190, 160),
    "hair":          ( 45,  30,  20),
    "hair2":         ( 70,  50,  35),
    "cheek":         (255, 185, 185),
    "eye":           ( 45,  28,  18),
    "eye_shine":     (255, 255, 255),
    "uniform":       (100, 115, 180),   # soft navy blue uniform
    "uniform2":      ( 75,  88, 155),
    "shirt":         (255, 253, 248),
    "shoe":          ( 55,  40,  30),
    "bag":           (200,  60,  60),   # red randoseru
    "bag2":          (170,  45,  45),
    # NPC grade colors (name badge/ribbon)
    "grade1":        (255, 180, 190),   # pink  - CP
    "grade2":        (180, 225, 180),   # mint  - CE1
    "grade3":        (180, 200, 240),   # blue  - CE2
    "grade4":        (220, 190, 240),   # lavender - CM1
    "grade5":        (255, 215, 150),   # peach/gold - CM2
    "teacher_coat":  (250, 248, 255),
    "teacher_tie":   (180, 100, 130),
}

# ── Tile IDs ──────────────────────────────────────────────────────────────────
FLOOR      = 0
WALL       = 1
DESK       = 2
BOARD      = 3
DOOR_OPEN  = 4
WINDOW     = 5
LOCKER     = 6
BOOKSHELF  = 7
CARPET     = 8
PATH       = 9
GRASS      = 10
DESK2      = 11
LOCKED_DOOR= 12
SIGN       = 13
STAIR      = 14
SAKURA     = 15

PASSABLE   = {FLOOR, DOOR_OPEN, CARPET, PATH, GRASS, STAIR}

FONTS: dict = {}

def load_fonts():
    global FONTS
    jp = None
    for name in ["msgothic","meiryo","ms gothic","noto sans jp","unifont","segoeuisymbol"]:
        try:
            t = pygame.font.SysFont(name, 40)
            if t.render("あ", True, (0,0,0)).get_width() > 5:
                jp = name; break
        except Exception:
            pass
    ui = "consolas"
    FONTS["xl"]     = pygame.font.SysFont(ui, 62, bold=True)
    FONTS["lg"]     = pygame.font.SysFont(ui, 38, bold=True)
    FONTS["md"]     = pygame.font.SysFont(ui, 24, bold=True)
    FONTS["sm"]     = pygame.font.SysFont(ui, 19)
    FONTS["xs"]     = pygame.font.SysFont(ui, 14)
    FONTS["kana"]   = pygame.font.SysFont(jp or "segoeuisymbol", 68, bold=True)
    FONTS["kana_sm"]= pygame.font.SysFont(jp or "segoeuisymbol", 34)
    FONTS["kana_xs"]= pygame.font.SysFont(jp or "segoeuisymbol", 22)
