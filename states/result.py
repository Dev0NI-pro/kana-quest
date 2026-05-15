import pygame, math, random
from settings import C, FONTS, SW, SH


class ResultState:
    def __init__(self, game, score, total, lesson, grade):
        self.game   = game
        self.score  = score
        self.total  = total
        self.lesson = lesson
        self.grade  = grade
        self.lang   = game.lang
        self.frame  = 0
        self.stars_bg = [(random.randint(0,SW), random.randint(0,SH),
                          random.randint(1,2), random.uniform(0.4,1.2),
                          random.randint(60,200)) for _ in range(60)]
        self.stars_earned = min(3, score // (total * 10 // 3 + 1) + 1)
        self.shown_stars  = 0
        self.star_timer   = 0

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                self.game.state = self.game.overworld

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.game.state = self.game.overworld

    def update(self):
        self.frame += 1
        # Animate background stars
        result = []
        for (x, y, r, spd, b) in self.stars_bg:
            b += spd
            if b > 255 or b < 60: spd = -spd
            result.append((x, y, r, spd, b))
        self.stars_bg = result

        # Reveal earned stars one by one
        self.star_timer += 1
        if self.star_timer > 30 and self.shown_stars < self.stars_earned:
            self.shown_stars += 1
            self.star_timer   = 0

    def draw(self, surf: pygame.Surface):
        surf.fill(C["bg"])

        # Background stars
        for (x, y, r, spd, b) in self.stars_bg:
            bv = max(0, min(255, int(b)))
            pygame.draw.circle(surf, (bv,bv,bv), (int(x),int(y)), r)

        # Title
        win  = self.score > 0
        t    = {"en":"LESSON COMPLETE!","fr":"LEÇON TERMINÉE !"}[self.lang] if win else \
               {"en":"KEEP TRYING!",    "fr":"CONTINUE !"}[self.lang]
        col  = C["gold"] if win else C["text_dim"]
        ts   = FONTS["xl"].render(t, True, col)
        surf.blit(ts, (SW//2 - ts.get_width()//2, 80))

        # Lesson name
        ln   = self.lesson["name"][self.lang]
        ls   = FONTS["md"].render(ln, True, C["text_dim"])
        surf.blit(ls, (SW//2 - ls.get_width()//2, 168))

        # Score
        sc_t = f"Score: {self.score} / {self.total * 10}"
        sc_s = FONTS["lg"].render(sc_t, True, C["text"])
        surf.blit(sc_s, (SW//2 - sc_s.get_width()//2, 210))

        # Animated stars
        for i in range(3):
            angle   = math.pi * 0.5
            radius  = 22
            cx_star = SW//2 - 60 + i*60
            cy_star = 290
            pts     = []
            for j in range(10):
                a  = angle + j * math.pi / 5
                r2 = radius if j % 2 == 0 else radius // 2
                pts.append((cx_star + r2*math.cos(a), cy_star + r2*math.sin(a)))

            if i < self.shown_stars:
                # Filled golden star with scale bounce
                scale = min(1.0, (self.frame - (i * 30)) / 15)
                scaled_pts = [(cx_star + (px-cx_star)*scale,
                               cy_star + (py-cy_star)*scale) for px,py in pts]
                pygame.draw.polygon(surf, C["gold"],  scaled_pts)
                pygame.draw.polygon(surf, (200,160,0), scaled_pts, 2)
            else:
                pygame.draw.polygon(surf, C["panel2"], pts)
                pygame.draw.polygon(surf, C["border"], pts, 2)

        # XP bar
        bar_w = 400
        bx    = SW//2 - bar_w//2
        by    = 340
        pygame.draw.rect(surf, C["panel"],  (bx, by, bar_w, 18), border_radius=4)
        ratio = min(1.0, self.score / max(1, self.total * 10))
        fw    = int(bar_w * ratio * min(1.0, self.frame / 60))
        if fw > 0:
            pygame.draw.rect(surf, C["gold"], (bx, by, fw, 18), border_radius=4)
        pygame.draw.rect(surf, C["border"], (bx, by, bar_w, 18), 2, border_radius=4)
        xp_s = FONTS["xs"].render("XP", True, C["text_dim"])
        surf.blit(xp_s, (bx - 28, by + 2))

        # Prompt
        prompt = {"en":"Press ENTER or click to continue",
                  "fr":"Appuie sur ENTRÉE ou clique pour continuer"}[self.lang]
        if (self.frame // 30) % 2 == 0:
            ps = FONTS["sm"].render(prompt, True, C["text_dim"])
            surf.blit(ps, (SW//2 - ps.get_width()//2, SH - 60))
