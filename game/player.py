import pygame
from settings import C, TILE

SPEED  = 3
ANIM_SPEED = 8   # frames per step

DIR_DOWN  = 0
DIR_LEFT  = 1
DIR_RIGHT = 2
DIR_UP    = 3


class Player:
    def __init__(self, tx: int, ty: int):
        self.tx      = tx        # tile x
        self.ty      = ty        # tile y
        self.px      = tx * TILE # pixel x
        self.py      = ty * TILE # pixel y
        self.dir     = DIR_DOWN
        self.frame   = 0
        self.moving  = False
        self.step    = 0         # walk cycle 0-3

        # target pixel position (for smooth movement)
        self.target_px = self.px
        self.target_py = self.py

    # ── Input / movement ──────────────────────────────────────────────────────
    def try_move(self, dx: int, dy: int, tilemap) -> bool:
        """Returns True if move was accepted."""
        nx, ny = self.tx + dx, self.ty + dy
        if tilemap.is_passable(nx, ny):
            self.tx        = nx
            self.ty        = ny
            self.target_px = nx * TILE
            self.target_py = ny * TILE
            self.moving    = True
            if dx == -1: self.dir = DIR_LEFT
            if dx ==  1: self.dir = DIR_RIGHT
            if dy == -1: self.dir = DIR_UP
            if dy ==  1: self.dir = DIR_DOWN
            return True
        else:
            # Face the direction even if blocked
            if dx == -1: self.dir = DIR_LEFT
            if dx ==  1: self.dir = DIR_RIGHT
            if dy == -1: self.dir = DIR_UP
            if dy ==  1: self.dir = DIR_DOWN
        return False

    def update(self):
        # Smooth pixel movement toward target
        spd = SPEED * 2
        if self.px < self.target_px:
            self.px = min(self.px + spd, self.target_px)
        elif self.px > self.target_px:
            self.px = max(self.px - spd, self.target_px)
        if self.py < self.target_py:
            self.py = min(self.py + spd, self.target_py)
        elif self.py > self.target_py:
            self.py = max(self.py - spd, self.target_py)

        self.moving = (self.px != self.target_px or self.py != self.target_py)
        if self.moving:
            self.frame += 1
            if self.frame % ANIM_SPEED == 0:
                self.step = (self.step + 1) % 4

    # ── Drawing ───────────────────────────────────────────────────────────────
    def draw(self, surf: pygame.Surface, cam_x: int, cam_y: int):
        sx = self.px - cam_x
        sy = self.py - cam_y
        self._draw_sprite(surf, sx, sy)

    def _draw_sprite(self, surf, x, y):
        """Draw a chibi-style school student sprite using primitives."""
        step   = self.step if self.moving else 0
        d      = self.dir
        S      = TILE  # sprite fits in one tile (32x32)

        cx  = x + S // 2   # center x
        top = y + 2         # top of sprite

        # ── Shadow ────────────────────────────────────────────────────────────
        pygame.draw.ellipse(surf, (0, 0, 0, 60),
                            (cx - 8, y + S - 6, 16, 5))

        # ── Legs / feet ───────────────────────────────────────────────────────
        leg_col  = C["uniform_m"]
        shoe_col = C["shoe"]
        if d == DIR_DOWN or d == DIR_UP:
            # Two legs side by side with walk bob
            bob_l = -2 if step in (1,) else (2 if step == 3 else 0)
            bob_r = -2 if step in (3,) else (2 if step == 1 else 0)
            # Left leg
            pygame.draw.rect(surf, leg_col,  (cx-8, top+20+bob_l, 6, 7))
            pygame.draw.rect(surf, shoe_col, (cx-9, top+26+bob_l, 7, 4))
            # Right leg
            pygame.draw.rect(surf, leg_col,  (cx+2, top+20+bob_r, 6, 7))
            pygame.draw.rect(surf, shoe_col, (cx+2, top+26+bob_r, 7, 4))
        else:
            # Side view — one leg front, one back
            bob = 2 if step in (1, 3) else 0
            pygame.draw.rect(surf, leg_col,  (cx-6, top+20, 6, 7+bob))
            pygame.draw.rect(surf, shoe_col, (cx-7, top+26+bob, 7, 4))
            pygame.draw.rect(surf, leg_col,  (cx,   top+20, 6, 7-bob))
            pygame.draw.rect(surf, shoe_col, (cx,   top+26-bob, 7, 4))

        # ── Body (uniform) ────────────────────────────────────────────────────
        body_color = C["uniform_m"]
        pygame.draw.rect(surf, body_color,  (cx-9, top+11, 18, 11), border_radius=2)
        # Collar / shirt
        pygame.draw.rect(surf, C["shirt"],  (cx-4, top+11, 8, 5),  border_radius=1)

        # ── Arms ──────────────────────────────────────────────────────────────
        arm_col = body_color
        if d in (DIR_DOWN, DIR_UP):
            arm_bob = 3 if step in (0, 2) else -1
            # Left arm
            pygame.draw.rect(surf, arm_col, (cx-13, top+11, 5, 9+arm_bob))
            pygame.draw.rect(surf, C["skin"], (cx-13, top+19+arm_bob, 5, 4))
            # Right arm
            pygame.draw.rect(surf, arm_col, (cx+8, top+11, 5, 9-arm_bob))
            pygame.draw.rect(surf, C["skin"], (cx+8, top+19-arm_bob, 5, 4))
        else:
            arm_bob = 2 if step in (1, 3) else 0
            pygame.draw.rect(surf, arm_col, (cx-12, top+12, 5, 8+arm_bob))
            pygame.draw.rect(surf, C["skin"], (cx-12, top+19+arm_bob, 5, 4))
            pygame.draw.rect(surf, arm_col, (cx+7, top+12, 5, 8-arm_bob))
            pygame.draw.rect(surf, C["skin"], (cx+7, top+19-arm_bob, 5, 4))

        # ── Head ──────────────────────────────────────────────────────────────
        head_y = top + 2
        pygame.draw.ellipse(surf, C["skin"],  (cx-8, head_y, 16, 14))

        # ── Hair ──────────────────────────────────────────────────────────────
        pygame.draw.ellipse(surf, C["hair"],  (cx-8, head_y,     16, 8))
        pygame.draw.rect(surf,    C["hair"],  (cx-8, head_y,     16, 5))
        # Side hair
        if d == DIR_LEFT:
            pygame.draw.rect(surf, C["hair"], (cx-8, head_y+4, 4, 6))
        elif d == DIR_RIGHT:
            pygame.draw.rect(surf, C["hair"], (cx+4, head_y+4, 4, 6))

        # ── Face ──────────────────────────────────────────────────────────────
        if d == DIR_DOWN:
            # Eyes
            pygame.draw.circle(surf, (30,20,10), (cx-3, head_y+7), 2)
            pygame.draw.circle(surf, (30,20,10), (cx+3, head_y+7), 2)
            # Eye shine
            pygame.draw.circle(surf, (255,255,255), (cx-2, head_y+6), 1)
            pygame.draw.circle(surf, (255,255,255), (cx+4, head_y+6), 1)
            # Smile
            pygame.draw.arc(surf, (200,120,100),
                            (cx-3, head_y+9, 6, 4), 3.14, 0, 1)
        elif d == DIR_UP:
            # Back of head — no face
            pass
        elif d == DIR_LEFT:
            pygame.draw.circle(surf, (30,20,10), (cx-4, head_y+7), 2)
            pygame.draw.circle(surf, (255,255,255), (cx-3, head_y+6), 1)
        elif d == DIR_RIGHT:
            pygame.draw.circle(surf, (30,20,10), (cx+4, head_y+7), 2)
            pygame.draw.circle(surf, (255,255,255), (cx+5, head_y+6), 1)

        # ── Randoseru (school backpack) ───────────────────────────────────────
        if d == DIR_UP or d == DIR_DOWN:
            pack_color = (180, 40, 40)   # red randoseru
            pygame.draw.rect(surf, pack_color,
                             (cx-11, top+12, 6, 8), border_radius=1)

    # ── Interaction target tile ───────────────────────────────────────────────
    def facing_tile(self):
        """Returns (tx, ty) of the tile the player is facing."""
        dx = [0, -1, 1, 0][self.dir]
        dy = [1,  0, 0,-1][self.dir]
        return self.tx + dx, self.ty + dy
