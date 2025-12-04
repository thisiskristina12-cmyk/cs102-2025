import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        max_y, max_x = screen.getmaxyx()
        for x in range(max_x):
            screen.addch(0, x, "#")
            screen.addch(max_y - 1, x, "#")
        for y in range(max_y):
            screen.addch(y, 0, "#")
            screen.addch(y, max_x - 1, "#")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                ch = "O" if cell == 1 else " "
                screen.addch(y + 1, x + 1, ch)

    def run(self) -> None:
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)
        running = True
        while running:
            screen.clear()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            if self.life.is_changing and not self.life.is_max_generations_exceeded:
                self.life.step()
            ch = screen.getch()
            if ch == ord("q") or not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            curses.napms(100)
        curses.endwin()
