import pygame
import random
from settings import C, FONTS, SW, SH

QUESTIONS_PER_LESSON = 8


class MinigameState:
    """Quiz mini-game: show JP character/word, pick from 4 choices."""

    def __init__(self, game, lesson: dict, npc_grade: int, on_complete=None):
        self.game     = game
        self.lesson   = lesson
        self.grade    = npc_grade
        self.lang     = game.lang
        self.items    = lesson["items"][:]
        random.shuffle(self.items)
        self.items    = self.items[:QUESTIONS_PER_LESSON]
        self.pool     = self._build_pool()

        self.score    = 0
        self.lives    = 3
        self.idx      = 0
        self.answered = False
        self.feedback = None
        self.feedback_timer = 0
        self.chosen_idx     = -1

        self.stars      = self._make_stars()
        self.frame      = 0
        self.on_complete = on_complete  # callback when lesson finished
        self._build_question()

    def _build_pool(self):
        """All items from all grades for wrong-answer pool."""
        from data.lessons import GRADES
        pool = []
        for g in GRADES.values():
            for les in g["lessons"]:
                pool.extend(les["items"])
        # Remove current lesson items
        lesson_jps = {i["jp"] for i in self.lesson["items"]}
        return [i for i in pool if i["jp"] not in lesson_jps]

    def _make_stars(self, n=60):
        import random as r
        return [(r.randint(0, SW), r.randint(0, SH//3),
                 r.randint(1,2), r.uniform(0.4,1.2), r.randint(60,200))
                for _ in range(n)]

    def _animate_stars(self):
        result = []
        for (x, y, r2, spd, b) in self.stars:
            b += spd
            if b > 255 or b < 60:
                spd = -spd
            result.append((x, y, r2, spd, b))
        self.stars = result

    def _build_question(self):
        if self.idx >= len(self.items):
            self._finish()
            return
        self.current  = self.items[self.idx]
        wrongs        = random.sample(self.pool, min(3, len(self.pool)))
        choices       = wrongs + [self.current]
        random.shuffle(choices)
        self.choices  = choices
        self.answered = False
        self.feedback = None
        self.chosen_idx = -1
        self._build_buttons()

    def _build_buttons(self):
        self.btn_rects = []
        for i in range(4):
            row = i // 2
            col = i %  2
            bx  = 60  + col * 340
            by  = 400 + row * 75
            self.btn_rects.append(pygame.Rect(bx, by, 310, 58))

    def _get_label(self, item: dict) -> str:
        """Get display label for a choice — always romaji for kana, translation for kanji/vocab."""
        jp = item.get("jp","")
        # If it's a single kana character, show romaji
        if len(jp) == 1 and ord(jp[0]) in range(0x3040, 0x30FF+1):
            return item.get("romaji","?")
        # For words, show translation in current language
        return item.get(self.lang, item.get("romaji","?"))

    def _check(self, idx: int):
        if self.answered:
            return
        self.answered   = True
        self.chosen_idx = idx
        correct         = (self.choices[idx] == self.current)
        if correct:
            self.feedback = "correct"
            self.score   += 10
        else:
            self.feedback = "wrong"
            self.lives   -= 1
            if self.lives <= 0:
                self.feedback_timer = 90
                return
        self.feedback_timer = 75

    def _finish(self):
        if self.on_complete:
            self.on_complete(self.score)
        from states.result import ResultState
        self.game.state = ResultState(
            self.game, self.score, len(self.items), self.lesson, self.grade)

    # ── Event / Update / Draw ─────────────────────────────────────────────────
    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not self.answered:
                from states.overworld import OverworldState
                self.game.state = self.game.overworld
                return
            nums = {pygame.K_1:0, pygame.K_2:1, pygame.K_3:2, pygame.K_4:3}
            if event.key in nums and not self.answered:
                self._check(nums[event.key])
        if event.type == pygame.MOUSEBUTTONDOWN and not self.answered:
            for i, r in enumerate(self.btn_rects):
                if r.collidepoint(event.pos):
                    self._check(i)

    def update(self):
        self.frame += 1
        self._animate_stars()
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0:
                if self.lives <= 0:
                    self._finish()
                    return
                self.idx += 1
                self._build_question()

    def draw(self, surf: pygame.Surface):
        # Background
        surf.fill(C["bg"])
        for (x, y, r2, spd, b) in self.stars:
            bv = max(0, min(255, int(b)))
            pygame.draw.circle(surf, (bv, bv, bv), (int(x), int(y)), r2)

        # Header bar
        hbar = pygame.Rect(0, 0, SW, 72)
        pygame.draw.rect(surf, C["panel"], hbar)
        pygame.draw.rect(surf, C["border"], hbar, 2)

        lesson_name = self.lesson["name"][self.lang]
        ln_txt = FONTS["md"].render(lesson_name, True, C["gold"])
        surf.blit(ln_txt, (16, 10))

        # Score
        sc = FONTS["sm"].render(f"Score: {self.score}", True, C["text"])
        surf.blit(sc, (16, 42))

        # Progress dots
        for i in range(len(self.items)):
            col = C["green"] if i < self.idx else (C["gold"] if i == self.idx else C["panel2"])
            pygame.draw.circle(surf, col, (SW//2 - len(self.items)*9 + i*18, 36), 7)
            pygame.draw.circle(surf, C["border"], (SW//2 - len(self.items)*9 + i*18, 36), 7, 1)

        # Lives (hearts)
        for i in range(3):
            hx = SW - 30 - i * 30
            hy = 20
            col = C["red"] if i < self.lives else C["panel2"]
            pts = [(hx+10,hy+3),(hx+13,hy),(hx+18,hy),(hx+20,hy+4),
                   (hx+20,hy+8),(hx+10,hy+18),(hx,hy+8),(hx,hy+4),
                   (hx+2,hy),(hx+7,hy)]
            pygame.draw.polygon(surf, col, pts)

        # Question panel
        qpanel = pygame.Rect(SW//2-180, 85, 360, 290)
        pygame.draw.rect(surf, C["panel"],  qpanel, border_radius=8)
        pygame.draw.rect(surf, C["panel2"], qpanel.inflate(-4,-4), border_radius=7)
        pygame.draw.rect(surf, C["border"], qpanel, 3, border_radius=8)

        # "What is this?"
        lang = self.lang
        q_lbl = {"en":"What does this mean?","fr":"Que signifie ceci ?"}[lang]
        ql = FONTS["xs"].render(q_lbl, True, C["text_dim"])
        surf.blit(ql, (qpanel.x + (qpanel.w - ql.get_width())//2, qpanel.y+10))

        # Main character / word
        jp = self.current.get("jp","?")
        font = FONTS["kana"] if len(jp) <= 2 else FONTS["kana_sm"]
        ch_surf = font.render(jp, True, C["white"])
        # glow
        glow   = font.render(jp, True, C["border2"])
        cx_pos = qpanel.x + (qpanel.w - ch_surf.get_width())//2
        cy_pos = qpanel.y + (qpanel.h - ch_surf.get_height())//2 + 10
        surf.blit(glow, (cx_pos+2, cy_pos+2))
        surf.blit(ch_surf, (cx_pos, cy_pos))

        # Romaji hint (small) for multi-char words
        if len(jp) > 1:
            hint = FONTS["xs"].render(f"({self.current.get('romaji','')})", True, C["text_dim"])
            surf.blit(hint, (qpanel.x + (qpanel.w - hint.get_width())//2,
                             qpanel.y + qpanel.h - 28))

        # Feedback overlay
        if self.feedback:
            fb_col   = C["green"] if self.feedback == "correct" else C["red"]
            fb_label = {"correct":{"en":"CORRECT!","fr":"CORRECT !"},
                        "wrong":  {"en":"WRONG!",  "fr":"FAUX !"}}[self.feedback][lang]
            fb_surf  = FONTS["lg"].render(fb_label, True, fb_col)
            fsx      = qpanel.x + (qpanel.w - fb_surf.get_width())//2
            surf.blit(fb_surf, (fsx, qpanel.y + qpanel.h - 55))

            ans_label = self.current.get(lang, self.current.get("romaji",""))
            ans_surf  = FONTS["xs"].render(
                f'{"Answer" if lang=="en" else "Réponse"}: {ans_label}',
                True, C["text_dim"])
            surf.blit(ans_surf, (qpanel.x + (qpanel.w - ans_surf.get_width())//2,
                                 qpanel.y + qpanel.h - 28))

        # Choices
        mouse = pygame.mouse.get_pos()
        for i, (rect, item) in enumerate(zip(self.btn_rects, self.choices)):
            label = self._get_label(item)
            hover = rect.collidepoint(mouse) and not self.answered

            if self.answered:
                if item == self.current:
                    bg, border = C["panel2"], C["green"]
                elif i == self.chosen_idx:
                    bg, border = C["panel2"], C["red"]
                else:
                    bg, border = C["panel"], C["panel2"]
            else:
                bg     = C["panel2"] if hover else C["panel"]
                border = C["border2"] if hover else C["border"]

            pygame.draw.rect(surf, bg,     rect, border_radius=6)
            pygame.draw.rect(surf, border, rect, 2, border_radius=6)

            num_s = FONTS["xs"].render(str(i+1), True, C["text_dim"])
            surf.blit(num_s, (rect.x+6, rect.y+4))

            lbl_s = FONTS["md"].render(label, True, C["text"] if not hover else C["white"])
            surf.blit(lbl_s, (rect.x + (rect.w - lbl_s.get_width())//2,
                               rect.y + (rect.h - lbl_s.get_height())//2))

        # Bottom hint
        hint = "1–4 or click  •  ESC to cancel" if lang=="en" else "1–4 ou clic  •  ÉCHAP pour annuler"
        hs   = FONTS["xs"].render(hint, True, C["text_dim"])
        surf.blit(hs, (SW - hs.get_width() - 10, SH - 18))
