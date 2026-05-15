import pygame
from settings import C, TILE

GRADE_COLORS = {
    1: (255, 200,  80),   # gold
    2: ( 80, 200, 120),   # green
    3: ( 80, 160, 255),   # blue
    4: (220,  80, 220),   # purple
    5: (255, 140,  60),   # orange
    6: (255,  80,  80),   # red
}


class NPC:
    def __init__(self, tx, ty, grade, lesson_id,
                 dialog_en, dialog_fr, facing=0):
        self.tx        = tx
        self.ty        = ty
        self.grade     = grade
        self.lesson_id = lesson_id
        self.dialog    = {"en": dialog_en, "fr": dialog_fr}
        self.facing    = facing      # 0=down, 1=left, 2=right, 3=up
        self.frame     = 0
        self.bob       = 0.0
        self.bob_dir   = 1
        # Vary the look by grade
        self.color     = GRADE_COLORS.get(grade, C["npc_skin"])
        self.is_teacher = (grade >= 5 or tx in (5, 18))

    def update(self):
        self.frame += 1
        self.bob  += 0.05 * self.bob_dir
        if abs(self.bob) > 1.5:
            self.bob_dir = -self.bob_dir

    def draw(self, surf: pygame.Surface, cam_x: int, cam_y: int):
        sx = self.tx * TILE - cam_x
        sy = self.ty * TILE - cam_y + int(self.bob)
        self._draw(surf, sx, sy)

    def _draw(self, surf, x, y):
        T  = TILE
        cx = x + T // 2
        top = y + 2

        # Shadow
        pygame.draw.ellipse(surf, (0,0,0),
                            (cx-7, y+T-5, 14, 4))

        # Legs
        leg = C["uniform_m"] if not self.is_teacher else (160,160,160)
        pygame.draw.rect(surf, leg,     (cx-7,  top+20, 5, 7))
        pygame.draw.rect(surf, C["shoe"],(cx-8,  top+26, 6, 4))
        pygame.draw.rect(surf, leg,     (cx+2,  top+20, 5, 7))
        pygame.draw.rect(surf, C["shoe"],(cx+2,  top+26, 6, 4))

        # Body
        body_col = C["teacher_coat"] if self.is_teacher else self.color
        pygame.draw.rect(surf, body_col,  (cx-9, top+11, 18, 11), border_radius=2)
        pygame.draw.rect(surf, C["shirt"],(cx-4, top+11, 8,  5),  border_radius=1)

        # Arms
        pygame.draw.rect(surf, body_col, (cx-13, top+11, 5, 9))
        pygame.draw.rect(surf, C["npc_skin"], (cx-13, top+19, 5, 4))
        pygame.draw.rect(surf, body_col, (cx+8,  top+11, 5, 9))
        pygame.draw.rect(surf, C["npc_skin"], (cx+8,  top+19, 5, 4))

        # Head
        pygame.draw.ellipse(surf, C["npc_skin"], (cx-8, top+2, 16, 14))
        pygame.draw.ellipse(surf, C["npc_hair"],  (cx-8, top+2, 16, 8))
        pygame.draw.rect(surf,    C["npc_hair"],  (cx-8, top+2, 16, 4))

        # Eyes
        pygame.draw.circle(surf, (20,15,10), (cx-3, top+9), 2)
        pygame.draw.circle(surf, (20,15,10), (cx+3, top+9), 2)
        pygame.draw.circle(surf, (255,255,255), (cx-2, top+8), 1)

        # Grade badge
        badge_col = self.color if self.is_teacher else (255,255,255)
        pygame.draw.circle(surf, badge_col, (cx+7, top+13), 5)
        pygame.draw.circle(surf, (0,0,0),   (cx+7, top+13), 5, 1)

    def is_adjacent(self, px: int, py: int) -> bool:
        """Check if player tile is adjacent to this NPC."""
        return abs(px - self.tx) + abs(py - self.ty) <= 1
