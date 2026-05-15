import pygame, math, random
from settings import C, FONTS, SW, SH


class TutorialState:
    """Intro tutorial shown before the first game."""

    PAGES = [
        {
            "en_title": "Welcome to Kana Quest!",
            "fr_title": "Bienvenue dans Kana Quest !",
            "en_text":  "Learn Japanese through adventure!\nExplore Sakura Elementary School\nand talk to teachers & students.",
            "fr_text":  "Apprends le japonais par l'aventure !\nExplore l'École Primaire Sakura\net parle aux profs et aux élèves.",
            "icon": "日",
        },
        {
            "en_title": "Controls",
            "fr_title": "Contrôles",
            "en_text":  "↑ ↓ ← →   Move your character\nSPACE       Talk to people\nESC         Back to menu",
            "fr_text":  "↑ ↓ ← →   Déplacer le personnage\nESPACE      Parler aux gens\nÉCHAP       Retour au menu",
            "icon": "🎮",
        },
        {
            "en_title": "Grade Progression",
            "fr_title": "Progression par niveau",
            "en_text":  "Start in Grade 1 (CP)!\nComplete all lessons to unlock\nthe next grade: CP → CE1 → … → CM2",
            "fr_text":  "Commence en CP !\nTermine toutes les leçons pour\ndébloquer le niveau suivant.",
            "icon": "🌸",
        },
        {
            "en_title": "Mini-Games",
            "fr_title": "Mini-jeux",
            "en_text":  "Each teacher gives you a quiz!\nSee a Japanese character — pick\nthe right answer from 4 choices.",
            "fr_text":  "Chaque prof te donne un quiz !\nVois un caractère japonais — choisis\nla bonne réponse parmi 4 choix.",
            "icon": "あ",
        },
    ]

    def __init__(self, game):
        self.game  = game
        self.page  = 0
        self.frame = 0
        self.alpha = 0
        self.petals = [self._new_petal() for _ in range(18)]

    def _new_petal(self):
        return {
            "x": random.uniform(0, SW),
            "y": random.uniform(-30, SH),
            "spd": random.uniform(0.5, 1.5),
            "drift": random.uniform(-0.3, 0.3),
            "angle": random.uniform(0, 360),
            "spin": random.uniform(-1.5, 1.5),
            "size": random.randint(4, 8),
        }

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_RIGHT):
                self._next()
            elif event.key == pygame.K_LEFT and self.page > 0:
                self.page -= 1
                self.alpha = 0
            elif event.key == pygame.K_ESCAPE:
                self._finish()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._next()

    def _next(self):
        if self.page < len(self.PAGES) - 1:
            self.page += 1
            self.alpha = 0
        else:
            self._finish()

    def _finish(self):
        self.game.start_overworld()

    def update(self):
        self.frame += 1
        if self.alpha < 255:
            self.alpha = min(255, self.alpha + 8)
        for p in self.petals:
            p["y"]     += p["spd"]
            p["x"]     += p["drift"]
            p["angle"] += p["spin"]
            if p["y"] > SH + 20:
                p.update(self._new_petal())
                p["y"] = -10

    def draw(self, surf: pygame.Surface):
        # Background gradient
        surf.fill(C["sky2"])
        # Sky gradient bands
        for i in range(SH // 4):
            r = int(210 + (255 - 210) * i / (SH // 4))
            g = int(235 + (245 - 235) * i / (SH // 4))
            b = int(255)
            pygame.draw.line(surf, (r, g, b), (0, i), (SW, i))

        # Sakura petals floating
        for p in self.petals:
            s = p["size"]
            pts = []
            for j in range(5):
                a = math.radians(p["angle"] + j * 72)
                r1, r2 = s, s // 2
                px = p["x"] + r1 * math.cos(a)
                py = p["y"] + r1 * math.sin(a)
                pts.append((px, py))
                a2 = math.radians(p["angle"] + j * 72 + 36)
                pts.append((p["x"] + r2 * math.cos(a2),
                             p["y"] + r2 * math.sin(a2)))
            petal_surf = pygame.Surface((s * 3, s * 3), pygame.SRCALPHA)
            local_pts = [(x - p["x"] + s * 1.5, y - p["y"] + s * 1.5) for x, y in pts]
            pygame.draw.polygon(petal_surf, (*C["sakura"], 180), local_pts)
            surf.blit(petal_surf, (p["x"] - s * 1.5, p["y"] - s * 1.5))

        pg   = self.PAGES[self.page]
        lang = self.game.lang

        # Panel
        panel = pygame.Rect(80, 100, SW - 160, SH - 200)
        panel_surf = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, (*C["panel"], 230),
                         (0, 0, panel.w, panel.h), border_radius=16)
        pygame.draw.rect(panel_surf, (*C["border"], 200),
                         (0, 0, panel.w, panel.h), 3, border_radius=16)
        surf.blit(panel_surf, (panel.x, panel.y))

        # Big icon
        icon_txt = pg["icon"]
        try:
            icon_s = FONTS["kana"].render(icon_txt, True, C["sakura_dark"])
            icon_s2 = FONTS["kana"].render(icon_txt, True, C["sakura"])
            surf.blit(icon_s2, (SW // 2 - icon_s.get_width() // 2 + 2, 115))
            surf.blit(icon_s,  (SW // 2 - icon_s.get_width() // 2,     113))
        except Exception:
            pass

        # Title
        title_key = f"{lang}_title"
        title = pg.get(title_key, pg["en_title"])
        ts = FONTS["lg"].render(title, True, C["text"])
        surf.blit(ts, (SW // 2 - ts.get_width() // 2, 195))

        # Body text
        text_key = f"{lang}_text"
        body = pg.get(text_key, pg["en_text"])
        for i, line in enumerate(body.split("\n")):
            ls = FONTS["sm"].render(line, True, C["text"])
            surf.blit(ls, (SW // 2 - ls.get_width() // 2, 255 + i * 32))

        # Page dots
        dot_y = panel.bottom - 35
        for i in range(len(self.PAGES)):
            col = C["sakura_dark"] if i == self.page else C["sakura_light"]
            r   = 6 if i == self.page else 4
            pygame.draw.circle(surf, col,
                               (SW // 2 - len(self.PAGES) * 16 + i * 32, dot_y), r)

        # Next hint
        hint = "SPACE / click to continue →" if lang == "en" else "ESPACE / clic pour continuer →"
        if self.page == len(self.PAGES) - 1:
            hint = "SPACE to start!" if lang == "en" else "ESPACE pour commencer !"
        if (self.frame // 30) % 2 == 0:
            hs = FONTS["xs"].render(hint, True, C["text_dim"])
            surf.blit(hs, (SW // 2 - hs.get_width() // 2, SH - 85))
