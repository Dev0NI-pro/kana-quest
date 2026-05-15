import pygame
from settings import C, FONTS, TILE, SW, SH, PASSABLE
from game.player  import Player, DIR_DOWN, DIR_LEFT, DIR_RIGHT, DIR_UP
from game.tilemap import Tilemap, NPC_DATA, SIGNS
from game.npc     import NPC


INTERACT_KEY = pygame.K_SPACE


class DialogBox:
    def __init__(self, text: str, font_sm, font_xs):
        self.lines     = text.split("\n")
        self.font_sm   = font_sm
        self.font_xs   = font_xs
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

    def draw(self, surf: pygame.Surface):
        panel = pygame.Rect(30, SH - 140, SW - 60, 120)
        pygame.draw.rect(surf, C["panel"],  panel, border_radius=6)
        pygame.draw.rect(surf, C["panel2"], panel.inflate(-4,-4), border_radius=5)
        pygame.draw.rect(surf, C["border"], panel, 3, border_radius=6)

        # Render text character by character (typewriter)
        drawn = 0
        for li, line in enumerate(self.lines):
            visible = ""
            for ch in line:
                if drawn >= self.char_idx:
                    break
                visible += ch
                drawn   += 1
            s = self.font_sm.render(visible, True, C["text"])
            surf.blit(s, (panel.x + 14, panel.y + 14 + li * 28))
            if drawn >= self.char_idx:
                break

        if self.done and (self.frame // 20) % 2 == 0:
            prompt = {"en":"SPACE to continue","fr":"ESPACE pour continuer"}
            lang   = "en"  # overridden in OverworldState.draw()
            ps = self.font_xs.render("▶ SPACE", True, C["gold"])
            surf.blit(ps, (panel.right - ps.get_width() - 12, panel.bottom - 22))


class OverworldState:
    MOVE_DELAY = 8   # frames between moves while key held

    def __init__(self, game):
        self.game    = game
        self.tilemap = Tilemap()
        self.player  = Player(13, 22)   # starts at school entrance
        self.npcs    = [NPC(*d) for d in NPC_DATA]
        self.dialog  = None
        self.pending_npc: NPC | None = None
        self.move_timers = {pygame.K_UP:0, pygame.K_DOWN:0,
                            pygame.K_LEFT:0, pygame.K_RIGHT:0}
        self.hud_alpha  = 0
        self.cam_x = 0
        self.cam_y = 0
        self._update_camera()
        self.interact_prompt = None

    # ── Camera ────────────────────────────────────────────────────────────────
    def _update_camera(self):
        target_cx = self.player.px - SW // 2 + TILE // 2
        target_cy = self.player.py - SH // 2 + TILE // 2
        max_cx    = self.tilemap.width  * TILE - SW
        max_cy    = self.tilemap.height * TILE - SH
        self.cam_x += (max(0, min(max_cx, target_cx)) - self.cam_x) // 4 + 1
        self.cam_y += (max(0, min(max_cy, target_cy)) - self.cam_y) // 4 + 1
        self.cam_x  = max(0, min(max_cx, self.cam_x))
        self.cam_y  = max(0, min(max_cy, self.cam_y))

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
                    self.dialog.char_idx = self.dialog.total  # skip typewriter
            return

        if event.type == pygame.KEYDOWN:
            if event.key == INTERACT_KEY:
                self._try_interact()

    def _try_interact(self):
        fx, fy = self.player.facing_tile()
        for npc in self.npcs:
            if npc.tx == fx and npc.ty == fy:
                lang = self.game.lang
                self.dialog      = DialogBox(npc.dialog[lang],
                                             FONTS["sm"], FONTS["xs"])
                self.pending_npc = npc
                return

    def _start_minigame(self, npc: NPC):
        from data.lessons import GRADES, get_lesson
        lesson = get_lesson(npc.grade, npc.lesson_id)
        if lesson:
            from states.minigame import MinigameState
            self.game.state = MinigameState(self.game, lesson, npc.grade)

    # ── Update ────────────────────────────────────────────────────────────────
    def update(self):
        if self.dialog:
            self.dialog.update()
            for npc in self.npcs:
                npc.update()
            return

        # Movement with held-key repeat
        keys = pygame.key.get_pressed()
        dir_map = {
            pygame.K_UP:    (0, -1),
            pygame.K_DOWN:  (0,  1),
            pygame.K_LEFT:  (-1, 0),
            pygame.K_RIGHT: (1,  0),
        }

        # Wait for player to finish moving tile before accepting next
        if not self.player.moving:
            for key, (dx, dy) in dir_map.items():
                if keys[key]:
                    self.move_timers[key] += 1
                    if self.move_timers[key] == 1 or self.move_timers[key] > self.MOVE_DELAY:
                        self.player.try_move(dx, dy, self.tilemap)
                        break
                else:
                    self.move_timers[key] = 0

        self.player.update()
        self._update_camera()

        for npc in self.npcs:
            npc.update()

        # Check for nearby NPC (interaction prompt)
        px, py = self.player.tx, self.player.ty
        self.interact_prompt = None
        fx, fy = self.player.facing_tile()
        for npc in self.npcs:
            if npc.tx == fx and npc.ty == fy:
                lang = self.game.lang
                grade_name = {"en":f"Grade {npc.grade}","fr":f"Grade {npc.grade}"}[lang]
                self.interact_prompt = grade_name
                break

    # ── Draw ──────────────────────────────────────────────────────────────────
    def draw(self, surf: pygame.Surface):
        surf.fill(C["sky"])

        self.tilemap.draw(surf, self.cam_x, self.cam_y, SW, SH)

        # Draw NPCs behind player
        for npc in self.npcs:
            npc.draw(surf, self.cam_x, self.cam_y)

        self.player.draw(surf, self.cam_x, self.cam_y)

        # Signs
        for (tx, ty, ten, tfr) in SIGNS:
            sx = tx * TILE - self.cam_x
            sy = ty * TILE - self.cam_y
            if -60 < sx < SW + 60 and -30 < sy < SH + 30:
                label = ten if self.game.lang == "en" else tfr
                ls    = FONTS["xs"].render(label, True, C["text"])
                pygame.draw.rect(surf, (0,0,0,100),
                                 (sx-2, sy-2, ls.get_width()+6, ls.get_height()+4))
                surf.blit(ls, (sx, sy))

        # Interaction prompt
        if self.interact_prompt:
            lang   = self.game.lang
            prompt = f"[SPACE] {self.interact_prompt}"
            ps     = FONTS["xs"].render(prompt, True, C["gold"])
            px_s   = self.player.px - self.cam_x - ps.get_width()//2 + TILE//2
            py_s   = self.player.py - self.cam_y - 22
            pygame.draw.rect(surf, C["panel"],
                             (px_s-4, py_s-2, ps.get_width()+8, ps.get_height()+4),
                             border_radius=3)
            surf.blit(ps, (px_s, py_s))

        # Dialog box
        if self.dialog:
            self.dialog.draw(surf)

        # Mini HUD (top-left)
        lang   = self.game.lang
        school = {"en":"Sakura Elementary","fr":"École Sakura"}[lang]
        hs     = FONTS["xs"].render(school, True, C["text_dim"])
        surf.blit(hs, (8, 6))

        ctrl = {"en":"Arrows=Move  SPACE=Talk","fr":"Flèches=Bouger  ESPACE=Parler"}[lang]
        cs   = FONTS["xs"].render(ctrl, True, C["text_dim"])
        surf.blit(cs, (SW - cs.get_width() - 8, 6))
