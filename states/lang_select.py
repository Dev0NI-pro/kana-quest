import pygame, random, math
from settings import C, FONTS, SW, SH


class LangSelectState:
    def __init__(self, game):
        self.game   = game
        self.frame  = 0
        self.title_y = -100
        self.petals  = [self._new_petal() for _ in range(25)]

    def _new_petal(self):
        return {"x": random.uniform(0, SW), "y": random.uniform(-40, SH),
                "spd": random.uniform(0.4, 1.2), "drift": random.uniform(-0.2, 0.2),
                "angle": random.uniform(0, 360), "spin": random.uniform(-1, 1),
                "size": random.randint(3, 7)}

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if pygame.Rect(SW//2-170, 340, 140, 52).collidepoint(mx, my):
                self.game.lang = "en"; self.game.start_tutorial()
            elif pygame.Rect(SW//2+30, 340, 140, 52).collidepoint(mx, my):
                self.game.lang = "fr"; self.game.start_tutorial()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e: self.game.lang = "en"; self.game.start_tutorial()
            elif event.key == pygame.K_f: self.game.lang = "fr"; self.game.start_tutorial()

    def update(self):
        self.frame += 1
        if self.title_y < 80: self.title_y += 5
        for p in self.petals:
            p["y"] += p["spd"]; p["x"] += p["drift"]; p["angle"] += p["spin"]
            if p["y"] > SH + 20: p.update(self._new_petal()); p["y"] = -10

    def draw(self, surf):
        # Sky gradient
        for i in range(SH):
            r = int(200 + 55 * i / SH)
            g = int(225 + 20 * i / SH)
            b = 255
            pygame.draw.line(surf, (r, g, b), (0, i), (SW, i))

        # Petals
        for p in self.petals:
            s = p["size"]
            pts = []
            for j in range(5):
                a = math.radians(p["angle"] + j * 72)
                r1, r2 = s, s // 2
                pts.append((p["x"] + r1*math.cos(a), p["y"] + r1*math.sin(a)))
                a2 = math.radians(p["angle"] + j*72+36)
                pts.append((p["x"] + r2*math.cos(a2), p["y"] + r2*math.sin(a2)))
            ps = pygame.Surface((s*3, s*3), pygame.SRCALPHA)
            lp = [(x-p["x"]+s*1.5, y-p["y"]+s*1.5) for x,y in pts]
            pygame.draw.polygon(ps, (*C["sakura"], 170), lp)
            surf.blit(ps, (p["x"]-s*1.5, p["y"]-s*1.5))

        ty = int(self.title_y)

        # Japanese title decoration
        jp_s = FONTS["kana"].render("日本語", True, C["sakura_dark"])
        jp_s2 = FONTS["kana"].render("日本語", True, C["sakura"])
        surf.blit(jp_s2, (SW//2 - jp_s.get_width()//2 + 2, ty - 20))
        surf.blit(jp_s,  (SW//2 - jp_s.get_width()//2,     ty - 22))

        # Title
        t1 = FONTS["xl"].render("KANA", True, C["text"])
        t2 = FONTS["xl"].render("QUEST", True, C["sakura_dark"])
        surf.blit(t1, (SW//2 - t1.get_width()//2, ty + 60))
        surf.blit(t2, (SW//2 - t2.get_width()//2, ty + 120))

        sub_text = ("Learn Japanese through adventure!" if True
                    else "Apprends le japonais par l'aventure !")
        sub = FONTS["sm"].render("Learn Japanese through adventure!", True, C["text_dim"])
        surf.blit(sub, (SW//2 - sub.get_width()//2, ty + 195))

        # Language panel
        panel = pygame.Rect(SW//2 - 200, 310, 400, 110)
        ps = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        pygame.draw.rect(ps, (*C["panel"], 210), (0,0,panel.w,panel.h), border_radius=10)
        pygame.draw.rect(ps, (*C["border"], 180), (0,0,panel.w,panel.h), 2, border_radius=10)
        surf.blit(ps, (panel.x, panel.y))

        choose = "Choose your language / Choisissez votre langue"
        cs = FONTS["xs"].render(choose, True, C["text_dim"])
        surf.blit(cs, (SW//2 - cs.get_width()//2, 320))

        mouse = pygame.mouse.get_pos()
        for rect, label in [
            (pygame.Rect(SW//2-170, 340, 140, 52), "ENGLISH  [E]"),
            (pygame.Rect(SW//2+30,  340, 140, 52), "FRANÇAIS [F]"),
        ]:
            hover = rect.collidepoint(mouse)
            bg  = C["panel2"] if hover else C["panel"]
            bd  = C["sakura_dark"] if hover else C["border"]
            pygame.draw.rect(surf, bg,  rect, border_radius=7)
            pygame.draw.rect(surf, bd,  rect, 2, border_radius=7)
            ls = FONTS["sm"].render(label, True, C["text"] if not hover else C["sakura_dark"])
            surf.blit(ls, (rect.x + (rect.w-ls.get_width())//2,
                           rect.y + (rect.h-ls.get_height())//2))
