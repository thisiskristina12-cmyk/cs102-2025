import random
import typing as tp

try:
    import pygame  # type: ignore[import-not-found]
    from pygame.locals import QUIT  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - fallback for environments without pygame
    QUIT = "QUIT"

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
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid: Grid = []
        for _ in range(self.cell_height):
            row = []
            for _ in range(self.cell_width):
                row.append(random.randint(0, 1) if randomize else 0)
            grid.append(row)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    rect = pygame.Rect(
                        x * self.cell_size,
                        y * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    )
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours: Cells = []
        row, col = cell
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ny, nx = row + dy, col + dx
                if 0 <= ny < self.cell_height and 0 <= nx < self.cell_width:
                    neighbours.append(self.grid[ny][nx])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = self.create_grid(randomize=False)
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                alive_neighbours = sum(self.get_neighbours((y, x)))
                if self.grid[y][x] == 1:
                    new_grid[y][x] = 1 if alive_neighbours in (2, 3) else 0
                else:
                    new_grid[y][x] = 1 if alive_neighbours == 3 else 0
        return new_grid
