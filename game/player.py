import pygame, math
from settings import C, TILE

SPEED      = 4
ANIM_SPEED = 7

DIR_DOWN  = 0
DIR_LEFT  = 1
DIR_RIGHT = 2
DIR_UP    = 3


class Player:
    def __init__(self, tx: int, ty: int):
        self.tx = tx
        self.ty = ty
        self.px = tx * TILE
        self.py = ty * TILE
        self.dir    = DIR_DOWN
        self.frame  = 0
        self.moving = False
        self.step   = 0
        self.target_px = self.px
        self.target_py = self.py
        self.bob    = 0.0

    def try_move(self, dx, dy, tilemap, grade_progress=None):
        if dx == -1: self.dir = DIR_LEFT
        if dx ==  1: self.dir = DIR_RIGHT
        if dy == -1: self.dir = DIR_UP
        if dy ==  1: self.dir = DIR_DOWN
        nx, ny = self.tx + dx, self.ty + dy
        if tilemap.is_passable(nx, ny, grade_progress):
            self.tx = nx; self.ty = ny
            self.target_px = nx * TILE
            self.target_py = ny * TILE
            self.moving = True
            return True
        return False

    def update(self):
        spd = SPEED * 2
        if self.px < self.target_px: self.px = min(self.px + spd, self.target_px)
        elif self.px > self.target_px: self.px = max(self.px - spd, self.target_px)
        if self.py < self.target_py: self.py = min(self.py + spd, self.target_py)
        elif self.py > self.target_py: self.py = max(self.py - spd, self.target_py)
        self.moving = (self.px != self.target_px or self.py != self.target_py)
        if self.moving:
            self.frame += 1
            if self.frame % ANIM_SPEED == 0:
                self.step = (self.step + 1) % 4
        # idle gentle bob
        self.bob = math.sin(self.frame * 0.08) * 0.8

    def draw(self, surf, cam_x, cam_y):
        sx = self.px - cam_x
        sy = self.py - cam_y + (0 if self.moving else int(self.bob))
        self._draw_chibi(surf, sx, sy, self.dir, self.step if self.moving else 0)

    def _draw_chibi(self, surf, x, y, d, step):
        """Cute chibi school student — big head, tiny body, rosy cheeks."""
        T  = TILE
        cx = x + T // 2

        # ── Shadow ────────────────────────────────────────────────────────────
        shadow = pygame.Surface((18, 5), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 50), (0, 0, 18, 5))
        surf.blit(shadow, (cx - 9, y + T - 4))

        # ── Proportions (chibi: head = 45% of total height) ───────────────────
        total_h = 28
        head_r  = 9          # big round head
        head_cx = cx
        head_cy = y + 4 + head_r   # top area

        body_top    = head_cy + head_r - 2  # overlaps slightly
        body_h      = 9
        body_w      = 11

        leg_h   = 6
        leg_w   = 4

        # ── Randoseru (backpack) — behind character ───────────────────────────
        if d == DIR_UP:
            pygame.draw.rect(surf, C["bag2"],
                             (cx - 7, body_top - 1, 6, 8), border_radius=2)
            pygame.draw.rect(surf, C["bag"],
                             (cx - 6, body_top, 4, 6), border_radius=1)
        elif d == DIR_DOWN:
            pygame.draw.rect(surf, C["bag2"],
                             (cx + 1, body_top - 1, 6, 8), border_radius=2)
            pygame.draw.rect(surf, C["bag"],
                             (cx + 2, body_top, 4, 6), border_radius=1)

        # ── Legs ──────────────────────────────────────────────────────────────
        leg_y = body_top + body_h - 1
        walk_l = 2 if step in (1,) else (-2 if step == 3 else 0)
        walk_r = -walk_l
        if d in (DIR_DOWN, DIR_UP):
            pygame.draw.rect(surf, C["uniform2"],
                             (cx - 7, leg_y + walk_l, leg_w, leg_h), border_radius=2)
            pygame.draw.rect(surf, C["shoe"],
                             (cx - 8, leg_y + leg_h + walk_l - 1, leg_w + 1, 3),
                             border_radius=1)
            pygame.draw.rect(surf, C["uniform2"],
                             (cx + 3, leg_y + walk_r, leg_w, leg_h), border_radius=2)
            pygame.draw.rect(surf, C["shoe"],
                             (cx + 2, leg_y + leg_h + walk_r - 1, leg_w + 1, 3),
                             border_radius=1)
        else:
            walk_f = 2 if step in (1, 3) else 0
            pygame.draw.rect(surf, C["uniform2"],
                             (cx - 6, leg_y, leg_w, leg_h + walk_f), border_radius=2)
            pygame.draw.rect(surf, C["shoe"],
                             (cx - 7, leg_y + leg_h + walk_f - 1, leg_w + 1, 3),
                             border_radius=1)
            pygame.draw.rect(surf, C["uniform2"],
                             (cx + 2, leg_y, leg_w, leg_h - walk_f + 2), border_radius=2)
            pygame.draw.rect(surf, C["shoe"],
                             (cx + 1, leg_y + leg_h - walk_f + 1, leg_w + 1, 3),
                             border_radius=1)

        # ── Body ──────────────────────────────────────────────────────────────
        pygame.draw.rect(surf, C["uniform"],
                         (cx - body_w//2, body_top, body_w, body_h), border_radius=3)
        # collar
        pygame.draw.rect(surf, C["shirt"],
                         (cx - 3, body_top, 6, 4), border_radius=1)

        # ── Arms ──────────────────────────────────────────────────────────────
        arm_w, arm_h = 4, 7
        arm_y = body_top + 1
        swing = 3 if step in (0, 2) else -1
        if d in (DIR_DOWN, DIR_UP):
            pygame.draw.rect(surf, C["uniform"],
                             (cx - body_w//2 - arm_w + 1, arm_y + swing, arm_w, arm_h),
                             border_radius=2)
            pygame.draw.rect(surf, C["skin"],
                             (cx - body_w//2 - arm_w + 1, arm_y + arm_h + swing - 1, arm_w, 3),
                             border_radius=1)
            pygame.draw.rect(surf, C["uniform"],
                             (cx + body_w//2 - 1, arm_y - swing, arm_w, arm_h),
                             border_radius=2)
            pygame.draw.rect(surf, C["skin"],
                             (cx + body_w//2 - 1, arm_y + arm_h - swing - 1, arm_w, 3),
                             border_radius=1)
        else:
            pygame.draw.rect(surf, C["uniform"],
                             (cx - body_w//2 - arm_w + 1, arm_y, arm_w, arm_h + swing),
                             border_radius=2)
            pygame.draw.rect(surf, C["skin"],
                             (cx - body_w//2 - arm_w + 1, arm_y + arm_h + swing - 1, arm_w, 3),
                             border_radius=1)
            pygame.draw.rect(surf, C["uniform"],
                             (cx + body_w//2 - 1, arm_y, arm_w, arm_h - swing),
                             border_radius=2)
            pygame.draw.rect(surf, C["skin"],
                             (cx + body_w//2 - 1, arm_y + arm_h - swing - 1, arm_w, 3),
                             border_radius=1)

        # ── Head — BIG and ROUND ───────────────────────────────────────────────
        # head shadow
        pygame.draw.circle(surf, C["skin_shadow"], (head_cx + 1, head_cy + 1), head_r)
        # head base
        pygame.draw.circle(surf, C["skin"], (head_cx, head_cy), head_r)

        # ── Hair ──────────────────────────────────────────────────────────────
        hair_r = head_r + 1
        # full hair cap
        pygame.draw.circle(surf, C["hair"], (head_cx, head_cy - 2), hair_r)
        # cover bottom half with skin to show face
        pygame.draw.rect(surf, C["skin"],
                         (head_cx - head_r, head_cy - 1, head_r * 2, head_r + 3))
        # re-draw skin circle for clean face
        pygame.draw.circle(surf, C["skin"], (head_cx, head_cy), head_r)
        # side hair strands
        if d == DIR_LEFT:
            pygame.draw.ellipse(surf, C["hair"],
                                (head_cx - head_r - 2, head_cy - 4, 5, 9))
        elif d == DIR_RIGHT:
            pygame.draw.ellipse(surf, C["hair"],
                                (head_cx + head_r - 3, head_cy - 4, 5, 9))

        # ── Face ──────────────────────────────────────────────────────────────
        if d == DIR_UP:
            # only back of head + hair visible
            pass
        elif d == DIR_DOWN:
            # Two big round eyes
            pygame.draw.circle(surf, C["eye"], (head_cx - 3, head_cy + 1), 3)
            pygame.draw.circle(surf, C["eye"], (head_cx + 3, head_cy + 1), 3)
            # Eye shine
            pygame.draw.circle(surf, C["eye_shine"], (head_cx - 2, head_cy), 1)
            pygame.draw.circle(surf, C["eye_shine"], (head_cx + 4, head_cy), 1)
            # Rosy cheeks
            chk = pygame.Surface((8, 5), pygame.SRCALPHA)
            pygame.draw.ellipse(chk, (*C["cheek"], 150), (0, 0, 8, 5))
            surf.blit(chk, (head_cx - 9, head_cy + 3))
            surf.blit(chk, (head_cx + 1, head_cy + 3))
            # Smile
            pygame.draw.arc(surf, (210, 120, 120),
                            (head_cx - 3, head_cy + 3, 6, 4), math.pi, 2 * math.pi, 1)
        elif d == DIR_LEFT:
            pygame.draw.circle(surf, C["eye"], (head_cx - 3, head_cy + 1), 3)
            pygame.draw.circle(surf, C["eye_shine"], (head_cx - 2, head_cy), 1)
            chk = pygame.Surface((7, 5), pygame.SRCALPHA)
            pygame.draw.ellipse(chk, (*C["cheek"], 140), (0, 0, 7, 5))
            surf.blit(chk, (head_cx - 8, head_cy + 3))
            pygame.draw.arc(surf, (210, 120, 120),
                            (head_cx - 5, head_cy + 3, 6, 4), math.pi, 2 * math.pi, 1)
        elif d == DIR_RIGHT:
            pygame.draw.circle(surf, C["eye"], (head_cx + 3, head_cy + 1), 3)
            pygame.draw.circle(surf, C["eye_shine"], (head_cx + 4, head_cy), 1)
            chk = pygame.Surface((7, 5), pygame.SRCALPHA)
            pygame.draw.ellipse(chk, (*C["cheek"], 140), (0, 0, 7, 5))
            surf.blit(chk, (head_cx + 1, head_cy + 3))
            pygame.draw.arc(surf, (210, 120, 120),
                            (head_cx - 1, head_cy + 3, 6, 4), math.pi, 2 * math.pi, 1)

    def facing_tile(self):
        dx = [0, -1, 1, 0][self.dir]
        dy = [1,  0, 0,-1][self.dir]
        return self.tx + dx, self.ty + dy
