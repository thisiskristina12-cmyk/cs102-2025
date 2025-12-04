import pathlib
import random
import typing as tp
from typing import cast

QUIT: int = 0

try:
    import pygame  # type: ignore[import-not-found]
    from pygame.locals import QUIT as PG_QUIT  # type: ignore[import-not-found]

    QUIT = cast(int, PG_QUIT)
except ImportError:  # pragma: no cover - fallback for environments without pygame

    class _DummyClock:
        def tick(self, *_args, **_kwargs) -> None:
            return None

    class _DummyDisplay:
        def set_mode(self, *_args, **_kwargs):
            return None

        def set_caption(self, *_args, **_kwargs) -> None:
            return None

        def flip(self) -> None:
            return None

    class _DummyDraw:
        @staticmethod
        def line(*_args, **_kwargs) -> None:
            return None

        @staticmethod
        def rect(*_args, **_kwargs) -> None:
            return None

    class _DummyEvent:
        @staticmethod
        def get():
            return []

    class _DummyTime:
        @staticmethod
        def Clock():
            return _DummyClock()

    class _DummyPygame:
        draw = _DummyDraw()
        display = _DummyDisplay()
        event = _DummyEvent()
        time = _DummyTime()

        @staticmethod
        def Color(_name):
            return _name

        @staticmethod
        def Rect(x, y, w, h):
            return (x, y, w, h)

        @staticmethod
        def init():
            return None

        @staticmethod
        def quit():
            return None

    pygame = _DummyPygame()  # type: ignore

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Copy from previous assignment
        grid: Grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(random.randint(0, 1) if randomize else 0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        # Copy from previous assignment
        neighbours: Cells = []
        row, col = cell
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = row + dy, col + dx
                if 0 <= ny < self.rows and 0 <= nx < self.cols:
                    neighbours.append(self.curr_generation[ny][nx])
        return neighbours

    def get_next_generation(self) -> Grid:
        # Copy from previous assignment
        new_grid = self.create_grid(randomize=False)
        for y in range(self.rows):
            for x in range(self.cols):
                alive_neighbours = sum(self.get_neighbours((y, x)))
                if self.curr_generation[y][x] == 1:
                    new_grid[y][x] = 1 if alive_neighbours in (2, 3) else 0
                else:
                    new_grid[y][x] = 1 if alive_neighbours == 3 else 0
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = [row.copy() for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= tp.cast(float, self.max_generations)

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        lines = pathlib.Path(filename).read_text(encoding="utf-8").splitlines()
        rows = len(lines)
        cols = len(lines[0]) if rows else 0
        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = [[int(ch) for ch in line.strip()] for line in lines]
        game.prev_generation = game.create_grid(randomize=False)
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
