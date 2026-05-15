import pygame
import sys
from settings import SW, SH, FPS, TITLE, load_fonts


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SW, SH))
        pygame.display.set_caption(TITLE)
        self.clock  = pygame.time.Clock()
        load_fonts()

        self.lang      = "en"
        self.overworld = None   # set after lang select
        self.state     = None
        self._go_lang_select()

    def _go_lang_select(self):
        from states.lang_select import LangSelectState
        self.state = LangSelectState(self)

    def start_overworld(self):
        from states.overworld import OverworldState
        self.overworld = OverworldState(self)
        self.state     = self.overworld

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.state.handle(event)

            self.state.update()
            self.state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    Game().run()
