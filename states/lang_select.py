import pygame
import random
from settings import C, FONTS, SW, SH


class LangSelectState:
    def __init__(self, game):
        self.game  = game
        self.stars = [(random.randint(0,SW), random.randint(0,SH),
                       random.randint(1,2), random.uniform(0.3,1.2),
                       random.randint(60,200)) for _ in range(80)]
        self.frame   = 0
        self.title_y = -80

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if pygame.Rect(200, 330, 150, 55).collidepoint(mx, my):
                self.game.lang = "en"
                self.game.start_overworld()
            elif pygame.Rect(450, 330, 150, 55).collidepoint(mx, my):
                self.game.lang = "fr"
                self.game.start_overworld()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.game.lang = "en"; self.game.start_overworld()
            elif event.key == pygame.K_f:
                self.game.lang = "fr"; self.game.start_overworld()

    def update(self):
        self.frame += 1
        if self.title_y < 100:
            self.title_y += 4
        result = []
        for (x, y, r, spd, b) in self.stars:
            b += spd
            if b > 255 or b < 60: spd = -spd
            result.append((x, y, r, spd, b))
        self.stars = result

    def draw(self, surf: pygame.Surface):
        surf.fill(C["bg"])
        for (x, y, r, spd, b) in self.stars:
            bv = max(0, min(255, int(b)))
            pygame.draw.circle(surf, (bv,bv,bv), (int(x),int(y)), r)

        ty = int(self.title_y)
        kana = FONTS["kana"].render("日本語", True, C["gold"])
        surf.blit(kana, (SW//2 - kana.get_width()//2, ty - 10))

        t1 = FONTS["xl"].render("KANA", True, C["gold"])
        t2 = FONTS["xl"].render("QUEST", True, C["border2"])
        surf.blit(t1, (SW//2 - t1.get_width()//2, ty + 70))
        surf.blit(t2, (SW//2 - t2.get_width()//2, ty + 130))

        sub = FONTS["sm"].render("Learn Japanese through adventure!", True, C["text_dim"])
        surf.blit(sub, (SW//2 - sub.get_width()//2, ty + 210))

        # Language buttons
        for rect, label, key in [
            (pygame.Rect(200, 330, 150, 55), "ENGLISH [E]",  "en"),
            (pygame.Rect(450, 330, 150, 55), "FRANÇAIS [F]", "fr"),
        ]:
            hover = rect.collidepoint(pygame.mouse.get_pos())
            bg    = C["panel2"] if hover else C["panel"]
            bd    = C["border2"] if hover else C["border"]
            pygame.draw.rect(surf, bg,  rect, border_radius=6)
            pygame.draw.rect(surf, bd,  rect, 2, border_radius=6)
            ls = FONTS["md"].render(label, True, C["white"] if hover else C["text"])
            surf.blit(ls, (rect.x + (rect.w-ls.get_width())//2,
                           rect.y + (rect.h-ls.get_height())//2))

        hint = FONTS["xs"].render("Choose your language / Choisissez votre langue", True, C["text_dim"])
        surf.blit(hint, (SW//2 - hint.get_width()//2, 410))
