import pygame

SW, SH   = 800, 600
TILE     = 32
FPS      = 60
TITLE    = "Kana Quest"

# ── Palette ────────────────────────────────────────────────────────────────────
C = {
    # UI
    "bg":          (15,  20,  40),
    "panel":       (28,  42,  72),
    "panel2":      (38,  56,  96),
    "border":      (80, 130, 200),
    "border2":     (140,190, 255),
    "text":        (220,230,255),
    "text_dim":    (120,145,185),
    "gold":        (255,210,  0),
    "green":       ( 70,210,110),
    "red":         (220, 65, 65),
    "white":       (255,255,255),
    "black":       (  0,  0,  0),
    # World tiles
    "floor_wood":  (195,165,115),
    "floor_hall":  (170,185,200),
    "wall_outer":  ( 90, 70, 55),
    "wall_inner":  (175,155,130),
    "wall_top":    (210,190,165),
    "blackboard":  ( 45, 75, 55),
    "chalk":       (230,230,220),
    "desk":        (180,140, 90),
    "desk_dark":   (150,110, 65),
    "window_sky":  (135,205,235),
    "window_frame":(160,140,110),
    "door_wood":   (140,100, 60),
    "door_frame":  (100, 70, 40),
    "grass":       ( 75,145, 60),
    "grass2":      ( 90,165, 70),
    "path":        (190,175,150),
    "sky":         (100,175,235),
    "school_wall": (225,215,195),
    "carpet_red":  (160, 45, 45),
    "locker":      ( 60,110,160),
    "bookshelf":   (120, 80, 40),
    # Character
    "skin":        (255,210,175),
    "hair":        ( 30, 20, 15),
    "uniform_m":   ( 50, 60,120),
    "uniform_f":   ( 50, 60,120),
    "shirt":       (240,240,240),
    "shoe":        ( 30, 25, 20),
    # NPC colors
    "teacher_coat":(240,240,240),
    "student1":    ( 70, 90,160),
    "npc_skin":    (255,200,165),
    "npc_hair":    ( 20, 15, 10),
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
VOID       = 11
DESK2      = 12   # desk facing player (front)
CHAIR      = 13
TEACHER_DESK = 14
SIGN       = 15

PASSABLE = {FLOOR, DOOR_OPEN, CARPET, PATH, GRASS}

TILE_COLORS = {
    FLOOR:       [C["floor_wood"], C["floor_wood"]],
    WALL:        [C["wall_outer"], C["wall_inner"]],
    DESK:        [C["desk"],       C["desk_dark"]],
    BOARD:       [C["blackboard"], C["chalk"]],
    DOOR_OPEN:   [C["door_wood"],  C["door_frame"]],
    WINDOW:      [C["window_sky"], C["window_frame"]],
    LOCKER:      [C["locker"],     C["border"]],
    BOOKSHELF:   [C["bookshelf"],  C["desk_dark"]],
    CARPET:      [C["carpet_red"], C["carpet_red"]],
    PATH:        [C["path"],       C["path"]],
    GRASS:       [C["grass"],      C["grass2"]],
    VOID:        [C["sky"],        C["sky"]],
    DESK2:       [C["desk"],       C["desk_dark"]],
    CHAIR:       [C["desk_dark"],  C["desk"]],
    TEACHER_DESK:[C["desk"],       C["desk_dark"]],
    SIGN:        [C["school_wall"],C["text_dim"]],
}

FONTS: dict = {}

def load_fonts():
    global FONTS
    jp = None
    for name in ["msgothic","meiryo","ms gothic","noto sans jp","unifont"]:
        try:
            t = pygame.font.SysFont(name, 40)
            if t.render("あ", True, (255,255,255)).get_width() > 5:
                jp = name; break
        except Exception:
            pass
    ui = "consolas"
    FONTS["xl"]    = pygame.font.SysFont(ui, 68, bold=True)
    FONTS["lg"]    = pygame.font.SysFont(ui, 40, bold=True)
    FONTS["md"]    = pygame.font.SysFont(ui, 26, bold=True)
    FONTS["sm"]    = pygame.font.SysFont(ui, 20)
    FONTS["xs"]    = pygame.font.SysFont(ui, 15)
    FONTS["kana"]  = pygame.font.SysFont(jp or "segoeuisymbol", 72, bold=True)
    FONTS["kana_sm"]= pygame.font.SysFont(jp or "segoeuisymbol", 36)
