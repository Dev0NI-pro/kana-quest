import pygame, math
from settings import C, TILE

# Height per grade (cute chibi scaling — younger = smaller)
GRADE_SIZE = {0: 26, 1: 24, 2: 25, 3: 26, 4: 27, 5: 28, 6: 28}
GRADE_HEAD = {0: 10, 1:  9, 2:  9, 3: 10, 4: 10, 5: 10, 6: 10}
GRADE_BADGE= {0: C["gold"],   1: C["grade1"], 2: C["grade2"],
              3: C["grade3"],  4: C["grade4"], 5: C["grade5"], 6: C["grade5"]}
GRADE_HAIR = {0: C["hair"],   1: (80, 50, 30),  2: (30, 20, 10),
              3: (50, 35, 20), 4: (40, 25, 15),  5: (25, 15, 8), 6: (25, 15, 8)}


class NPC:
    def __init__(self, tx, ty, grade, lesson_id, dialog_en, dialog_fr, facing=0):
        self.tx         = tx
        self.ty         = ty
        self.grade      = grade
        self.lesson_id  = lesson_id
        self.dialog     = {"en": dialog_en, "fr": dialog_fr}
        self.facing     = facing
        self.frame      = 0
        self.bob        = 0.0
        self.bob_dir    = 1
        self.is_teacher = (lesson_id == "tutorial" or grade == 0 or
                           "vowels" in lesson_id or "greetings" in lesson_id or
                           "_ta" in lesson_id or "katakana_basic" in lesson_id or
                           "loanwords" in lesson_id or "kanji" in lesson_id or
                           "grammar" in lesson_id or "sentences" in lesson_id)

    def update(self):
        self.frame  += 1
        self.bob    += 0.04 * self.bob_dir
        if abs(self.bob) > 1.2:
            self.bob_dir = -self.bob_dir

    def draw(self, surf, cam_x, cam_y):
        sx = self.tx * TILE - cam_x
        sy = self.ty * TILE - cam_y + int(self.bob)
        if -TILE < sx < 900 and -TILE < sy < 700:
            self._draw_chibi_npc(surf, sx, sy)

    def _draw_chibi_npc(self, surf, x, y):
        g       = self.grade
        T       = TILE
        cx      = x + T // 2
        head_r  = GRADE_HEAD.get(g, 9)
        total_h = GRADE_SIZE.get(g, 26)
        is_t    = self.is_teacher
        hair_c  = GRADE_HAIR.get(g, C["hair"])

        head_cy  = y + 4 + head_r
        body_top = head_cy + head_r - 2
        body_h   = total_h - head_r * 2 - 8
        body_w   = 10

        # Shadow
        sh = pygame.Surface((16, 4), pygame.SRCALPHA)
        pygame.draw.ellipse(sh, (0, 0, 0, 40), (0, 0, 16, 4))
        surf.blit(sh, (cx - 8, y + T - 3))

        # Legs
        leg_col = (100, 100, 120) if is_t else C["uniform2"]
        shoe_col = C["shoe"]
        pygame.draw.rect(surf, leg_col,  (cx - 6, body_top + body_h, 4, 5), border_radius=1)
        pygame.draw.rect(surf, shoe_col, (cx - 7, body_top + body_h + 4, 5, 3), border_radius=1)
        pygame.draw.rect(surf, leg_col,  (cx + 2, body_top + body_h, 4, 5), border_radius=1)
        pygame.draw.rect(surf, shoe_col, (cx + 2, body_top + body_h + 4, 5, 3), border_radius=1)

        # Body
        body_col = C["teacher_coat"] if is_t else C["uniform"]
        pygame.draw.rect(surf, body_col, (cx - body_w//2, body_top, body_w, body_h), border_radius=2)

        if is_t:
            # Teacher tie
            pygame.draw.rect(surf, C["teacher_tie"],
                             (cx - 1, body_top + 1, 3, body_h - 2), border_radius=1)
        else:
            # Student collar
            pygame.draw.rect(surf, C["shirt"], (cx - 3, body_top, 6, 4), border_radius=1)

        # Grade badge
        badge_c = GRADE_BADGE.get(g, C["gold"])
        pygame.draw.circle(surf, badge_c,    (cx + body_w//2 - 1, body_top + 3), 4)
        pygame.draw.circle(surf, (0, 0, 0),  (cx + body_w//2 - 1, body_top + 3), 4, 1)

        # Arms
        arm_col = body_col
        pygame.draw.rect(surf, arm_col, (cx - body_w//2 - 3, body_top + 1, 4, 6), border_radius=1)
        pygame.draw.rect(surf, C["skin"], (cx - body_w//2 - 3, body_top + 6, 4, 3), border_radius=1)
        pygame.draw.rect(surf, arm_col, (cx + body_w//2 - 1, body_top + 1, 4, 6), border_radius=1)
        pygame.draw.rect(surf, C["skin"], (cx + body_w//2 - 1, body_top + 6, 4, 3), border_radius=1)

        # Head
        pygame.draw.circle(surf, C["skin_shadow"], (cx + 1, head_cy + 1), head_r)
        pygame.draw.circle(surf, C["skin"], (cx, head_cy), head_r)

        # Hair cap
        pygame.draw.circle(surf, hair_c, (cx, head_cy - 2), head_r + 1)
        pygame.draw.rect(surf, C["skin"], (cx - head_r, head_cy - 1, head_r * 2, head_r + 3))
        pygame.draw.circle(surf, C["skin"], (cx, head_cy), head_r)

        # Teacher — glasses
        if is_t and g >= 3:
            pygame.draw.circle(surf, (100, 100, 120), (cx - 3, head_cy + 1), 3, 1)
            pygame.draw.circle(surf, (100, 100, 120), (cx + 3, head_cy + 1), 3, 1)
            pygame.draw.line(surf, (100, 100, 120), (cx, head_cy + 1), (cx, head_cy + 1), 1)

        # Eyes
        e_r = 3 if head_r >= 10 else 2
        pygame.draw.circle(surf, C["eye"], (cx - 3, head_cy + 1), e_r)
        pygame.draw.circle(surf, C["eye"], (cx + 3, head_cy + 1), e_r)
        pygame.draw.circle(surf, C["eye_shine"], (cx - 2, head_cy), 1)
        pygame.draw.circle(surf, C["eye_shine"], (cx + 4, head_cy), 1)

        # Rosy cheeks
        chk = pygame.Surface((7, 4), pygame.SRCALPHA)
        pygame.draw.ellipse(chk, (*C["cheek"], 130), (0, 0, 7, 4))
        surf.blit(chk, (cx - 8, head_cy + 3))
        surf.blit(chk, (cx + 1, head_cy + 3))

        # Smile
        pygame.draw.arc(surf, (210, 120, 120),
                        (cx - 3, head_cy + 3, 6, 4), math.pi, 2 * math.pi, 1)

        # Speech bubble indicator (when player is close)
        if (self.frame // 25) % 2 == 0:
            bx, by = cx - 4, head_cy - head_r - 10
            pygame.draw.ellipse(surf, (255, 255, 255), (bx, by, 10, 7))
            pygame.draw.ellipse(surf, C["border"], (bx, by, 10, 7), 1)
            dot_s = pygame.font.SysFont("consolas", 8)
            dot_t = dot_s.render("...", True, C["text"])
            surf.blit(dot_t, (bx + 1, by))

    def is_adjacent(self, px, py):
        return abs(px - self.tx) + abs(py - self.ty) <= 1
