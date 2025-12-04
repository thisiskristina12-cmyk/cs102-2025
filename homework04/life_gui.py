from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    import pygame as pg  # type: ignore[import-not-found]
    from pygame.time import Clock  # type: ignore[import-not-found]

try:
    import pygame  # type: ignore[import-not-found]
    from pygame.locals import (  # type: ignore[import-not-found]
        K_SPACE,
        KEYDOWN,
        MOUSEBUTTONDOWN,
        QUIT,
    )
except ImportError:  # pragma: no cover - GUI optional
    pygame = None  # type: ignore
    KEYDOWN = K_SPACE = MOUSEBUTTONDOWN = QUIT = 0  # type: ignore[misc]

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height
        self.screen: Optional["pg.Surface"] = (
            pygame.display.set_mode(self.screen_size) if pygame else None  # type: ignore[attr-defined]
        )
        self.clock: Optional["Clock"] = pygame.time.Clock() if pygame else None
        self.paused = False

    def draw_lines(self) -> None:
        if not pygame or not self.screen:
            return
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        if not pygame or not self.screen:
            return
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 1:
                    rect = pygame.Rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    )
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)

    def run(self) -> None:
        if not pygame or not self.screen or not self.clock:
            return
        pygame.init()
        pygame.display.set_caption("Game of Life")
        assert self.screen is not None and self.clock is not None
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.paused = not self.paused
                if self.paused and event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    col = mx // self.cell_size
                    row = my // self.cell_size
                    if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                        self.life.curr_generation[row][col] ^= 1

            self.screen.fill(pygame.Color("white"))
            if not self.paused and self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()

            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            self.clock.tick(self.speed)
        pygame.quit()
