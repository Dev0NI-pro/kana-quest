import pygame, math
from settings import C, FONTS, TILE, SW, SH, PASSABLE
from game.player  import Player, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP
from game.tilemap import Tilemap, NPC_DATA, SIGNS_DATA, LOCK_DATA
from game.npc     import NPC

INTERACT_KEY = pygame.K_SPACE

# Which lessons belong to which grade
GRADE_LESSONS = {
    1: {"greetings", "hiragana_vowels", "numbers_1_10"},
    2: {"hiragana_ta", "school_items", "days_of_week"},
    3: {"katakana_basic", "food", "telling_time"},
    4: {"katakana_loanwords", "adjectives", "verbs_basic"},
    5: {"kanji_n5_numbers", "sentences_basic"},
    6: {"kanji_n5_nature", "grammar_te_form"},
}


class DialogBox:
    def __init__(self, text, lang="en"):
        self.lines     = text.split("\n")
        self.char_idx  = 0
        self.total     = sum(len(l) for l in self.lines)
        self.done      = False
        self.frame     = 0

    def update(self):
        self.frame += 1
        if self.char_idx < self.total:
            self.char_idx = min(self.total, self.char_idx + 2)
        else:
            self.done = True

    def draw(self, surf, lang="en"):
        panel = pygame.Rect(20, SH - 150, SW - 40, 130)
        # Semi-transparent panel
        ps = pygame.Surface((panel.w, panel.h), pygame.SRCALPHA)
        pygame.draw.rect(ps, (*C["panel"], 235), (0, 0, panel.w, panel.h), border_radius=8)
        pygame.draw.rect(ps, (*C["border"], 200), (0, 0, panel.w, panel.h), 3, border_radius=8)
        surf.blit(ps, (panel.x, panel.y))

        drawn = 0
        for li, line in enumerate(self.lines):
            visible = ""
            for ch in line:
                if drawn >= self.char_idx:
                    break
                visible += ch
                drawn   += 1
            s = FONTS["sm"].render(visible, True, C["text"])
            surf.blit(s, (panel.x + 16, panel.y + 14 + li * 30))
            if drawn >= self.char_idx:
                break

        if self.done and (self.frame // 22) % 2 == 0:
            prompt = "▶  SPACE" if lang == "en" else "▶  ESPACE"
            ps2 = FONTS["xs"].render(prompt, True, C["gold"])
            surf.blit(ps2, (panel.right - ps2.get_width() - 14, panel.bottom - 20))


class OverworldState:
    MOVE_DELAY = 8

    def __init__(self, game):
        self.game    = game
        self.tilemap = Tilemap()
        self.player  = Player(11, 7)    # starts in entrance hall
        self.npcs    = [NPC(*d) for d in NPC_DATA]
        self.dialog  = None
        self.pending_npc = None
        self.move_timers = {k: 0 for k in [pygame.K_UP, pygame.K_DOWN,
                                            pygame.K_LEFT, pygame.K_RIGHT]}
        self.cam_x = 0
        self.cam_y = 0
        self.interact_prompt = None
        self.locked_prompt   = None
        self.frame           = 0
        # Grade progress: set of grade numbers with all lessons done
        self.grade_done: set  = game.grade_done
        self.lesson_done: set = game.lesson_done
        self._update_locks()
        self._update_camera(snap=True)

    def _update_locks(self):
        """Visually open locked doors when grades are completed."""
        for lx, ly, required in LOCK_DATA:
            if all(g in self.grade_done for g in required):
                self.tilemap.unlock_visually(lx, ly)
                self.tilemap.unlock_visually(lx + 1, ly)  # double-wide door

    def _update_camera(self, snap=False):
        target_cx = self.player.px - SW // 2 + TILE // 2
        target_cy = self.player.py - SH // 2 + TILE // 2
        max_cx = max(0, self.tilemap.width  * TILE - SW)
        max_cy = max(0, self.tilemap.height * TILE - SH)
        tx = max(0, min(max_cx, target_cx))
        ty = max(0, min(max_cy, target_cy))
        if snap:
            self.cam_x, self.cam_y = tx, ty
        else:
            self.cam_x += (tx - self.cam_x) // 5 + 1
            self.cam_y += (ty - self.cam_y) // 5 + 1
            self.cam_x = max(0, min(max_cx, self.cam_x))
            self.cam_y = max(0, min(max_cy, self.cam_y))

    # ── Input ─────────────────────────────────────────────────────────────────
    def handle(self, event):
        if self.dialog:
            if event.type == pygame.KEYDOWN and event.key == INTERACT_KEY:
                if self.dialog.done:
                    self.dialog = None
                    if self.pending_npc:
                        self._start_minigame(self.pending_npc)
                        self.pending_npc = None
                else:
                    self.dialog.char_idx = self.dialog.total
            return

        if event.type == pygame.KEYDOWN:
            if event.key == INTERACT_KEY:
                self._try_interact()
            elif event.key == pygame.K_ESCAPE:
                from states.lang_select import LangSelectState
                self.game.state = LangSelectState(self.game)

    def _try_interact(self):
        fx, fy = self.player.facing_tile()
        for npc in self.npcs:
            if npc.tx == fx and npc.ty == fy:
                text = npc.dialog[self.game.lang]
                self.dialog      = DialogBox(text, self.game.lang)
                self.pending_npc = npc if npc.lesson_id != "tutorial" else None
                return
        # Check locked door
        for lx, ly, required in LOCK_DATA:
            if abs(fx - lx) <= 2 and fy == ly:
                if not all(g in self.grade_done for g in required):
                    needed = sorted(required - self.grade_done)
                    if self.game.lang == "en":
                        msg = f"Door is locked!\nComplete Grade {needed[0]} first!"
                    else:
                        msg = f"Porte verrouillée !\nTermine le niveau {needed[0]} d'abord !"
                    self.dialog = DialogBox(msg, self.game.lang)

    def _start_minigame(self, npc):
        from data.lessons import get_lesson
        lesson = get_lesson(npc.grade, npc.lesson_id)
        if lesson:
            from states.minigame import MinigameState
            mg = MinigameState(self.game, lesson, npc.grade)
            mg.on_complete = lambda score: self._on_lesson_done(npc.lesson_id, npc.grade)
            self.game.state = mg

    def _on_lesson_done(self, lesson_id, grade):
        self.lesson_done.add(lesson_id)
        # Check if grade is fully done
        required = GRADE_LESSONS.get(grade, set())
        if required and required.issubset(self.lesson_done):
            self.grade_done.add(grade)
            self._update_locks()

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self):
        self.frame += 1
        if self.dialog:
            self.dialog.update()
            for npc in self.npcs: npc.update()
            return

        keys = pygame.key.get_pressed()
        dir_map = {pygame.K_UP:   (0,-1), pygame.K_DOWN:  (0, 1),
                   pygame.K_LEFT: (-1,0), pygame.K_RIGHT: (1, 0)}

        if not self.player.moving:
            for key, (dx, dy) in dir_map.items():
                if keys[key]:
                    self.move_timers[key] += 1
                    if self.move_timers[key] == 1 or self.move_timers[key] > self.MOVE_DELAY:
                        moved = self._try_walk(dx, dy)
                        break
                else:
                    self.move_timers[key] = 0

        self.player.update()
        self._update_camera()
        for npc in self.npcs: npc.update()

        # Interaction / locked prompts
        fx, fy = self.player.facing_tile()
        self.interact_prompt = None
        self.locked_prompt   = None
        for npc in self.npcs:
            if npc.tx == fx and npc.ty == fy:
                lang = self.game.lang
                if npc.lesson_id in self.lesson_done:
                    self.interact_prompt = ("✓ " + ("Done!" if lang=="en" else "Fait !"))
                else:
                    self.interact_prompt = ("SPACE — Talk" if lang=="en" else "ESPACE — Parler")
                break
        for lx, ly, required in LOCK_DATA:
            if abs(fx - lx) <= 2 and fy == ly:
                if not all(g in self.grade_done for g in required):
                    self.locked_prompt = ("🔒 Locked" if self.game.lang=="en" else "🔒 Verrouillé")

    def _try_walk(self, dx, dy):
        # Pass grade progress so locked doors block correctly
        nx, ny = self.player.tx + dx, self.player.ty + dy
        if self.player.dir == [DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP][[0,1,-1,0].index(dy) if dy != 0 else [0,1,-1,0].index(dx)+2] if False else True:
            pass
        if self.tilemap.is_passable(nx, ny, self.grade_done):
            self.player.try_move(dx, dy, self.tilemap)
            return True
        else:
            # Face direction even if blocked
            if dx == -1: self.player.dir = DIR_LEFT
            if dx ==  1: self.player.dir = DIR_RIGHT
            if dy == -1: self.player.dir = DIR_UP
            if dy ==  1: self.player.dir = DIR_DOWN
            return False

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf):
        surf.fill(C["sky"])
        self.tilemap.draw(surf, self.cam_x, self.cam_y, SW, SH)

        # NPCs
        for npc in self.npcs:
            npc.draw(surf, self.cam_x, self.cam_y)

        # Player
        self.player.draw(surf, self.cam_x, self.cam_y)

        # Signs
        for (tx, ty, ten, tfr) in SIGNS_DATA:
            sx = tx * TILE - self.cam_x
            sy = ty * TILE - self.cam_y - 14
            if -80 < sx < SW + 80 and -20 < sy < SH + 20:
                label = ten if self.game.lang == "en" else tfr
                ls    = FONTS["xs"].render(label, True, C["text"])
                bg    = pygame.Surface((ls.get_width() + 8, ls.get_height() + 4), pygame.SRCALPHA)
                pygame.draw.rect(bg, (*C["sign"], 200),
                                 (0, 0, bg.get_width(), bg.get_height()), border_radius=3)
                surf.blit(bg, (sx - 4, sy - 2))
                surf.blit(ls, (sx, sy))

        # Interaction prompt bubble
        prompt_text = self.interact_prompt or self.locked_prompt
        if prompt_text:
            px = self.player.px - self.cam_x - 30 + TILE // 2
            py = self.player.py - self.cam_y - 28
            ps = FONTS["xs"].render(prompt_text, True, C["text"])
            bubble = pygame.Surface((ps.get_width() + 12, ps.get_height() + 8), pygame.SRCALPHA)
            col = (*C["panel"], 220) if self.interact_prompt else (*C["locked_door"], 220)
            pygame.draw.rect(bubble, col,
                             (0, 0, bubble.get_width(), bubble.get_height()), border_radius=5)
            pygame.draw.rect(bubble, (*C["border"], 180),
                             (0, 0, bubble.get_width(), bubble.get_height()), 1, border_radius=5)
            surf.blit(bubble, (px, py))
            surf.blit(ps, (px + 6, py + 4))

        # Dialog
        if self.dialog:
            self.dialog.draw(surf, self.game.lang)

        # HUD top-left
        lang = self.game.lang
        done_c = len(self.grade_done)
        grade_txt = (f"Grades done: {done_c}/6" if lang=="en"
                     else f"Niveaux validés : {done_c}/6")
        gs = FONTS["xs"].render(grade_txt, True, C["text_dim"])
        surf.blit(gs, (8, 8))

        # Lesson progress bar
        total_l  = sum(len(v) for v in GRADE_LESSONS.values())
        done_l   = len(self.lesson_done)
        bw, bh   = 160, 6
        bx, by   = 8, 22
        pygame.draw.rect(surf, C["panel2"], (bx, by, bw, bh), border_radius=3)
        fw = int(bw * done_l / max(1, total_l))
        if fw > 0:
            pygame.draw.rect(surf, C["sakura_dark"], (bx, by, fw, bh), border_radius=3)
        pygame.draw.rect(surf, C["border"], (bx, by, bw, bh), 1, border_radius=3)

        # Controls hint
        ctrl = ("↑↓←→ Move  SPACE Talk" if lang=="en"
                else "↑↓←→ Bouger  ESPACE Parler")
        cs = FONTS["xs"].render(ctrl, True, C["text_dim"])
        surf.blit(cs, (SW - cs.get_width() - 8, 8))
