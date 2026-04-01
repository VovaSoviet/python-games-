# ТЕТРИС — полная версия для pygame-ce и Python 3.14
import pygame
import random
import sys

# ========== НАСТРОЙКИ ==========
pygame.init()

# Размеры
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Создаём окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ТЕТРИС — Владимир")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ========== ФИГУРЫ ==========
SHAPES = [
    ([[-2, 0], [-1, 0], [0, 0], [1, 0]], CYAN),  # I
    ([[-1, -1], [0, -1], [-1, 0], [0, 0]], YELLOW),  # O
    ([[-1, 0], [0, 0], [1, 0], [0, -1]], MAGENTA),  # T
    ([[-1, 0], [0, 0], [0, -1], [1, -1]], GREEN),  # S
    ([[-1, -1], [0, -1], [0, 0], [1, 0]], RED),  # Z
    ([[-1, -1], [-1, 0], [0, 0], [1, 0]], ORANGE),  # L
    ([[1, -1], [-1, 0], [0, 0], [1, 0]], BLUE)  # J
]

# Игровое поле
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]


def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if color != 0:
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
            else:
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, GRAY, rect, 1)


class Tetromino:
    def __init__(self, shape_index):
        self.shape_index = shape_index
        self.shape, self.color = SHAPES[shape_index]
        self.x = COLS // 2 - 1
        self.y = 0

    def get_blocks(self):
        return [[self.x + dx, self.y + dy] for dx, dy in self.shape]

    def rotate(self):
        new_shape = [[-dy, dx] for dx, dy in self.shape]
        old_shape = self.shape
        self.shape = new_shape
        if not self.is_valid():
            self.shape = old_shape

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if not self.is_valid():
            self.x -= dx
            self.y -= dy
            return False
        return True

    def is_valid(self):
        for x, y in self.get_blocks():
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and grid[y][x] != 0:
                return False
        return True

    def lock(self):
        for x, y in self.get_blocks():
            if y >= 0:
                grid[y][x] = self.color
        clear_lines()


# ========== ЛИНИИ И СЧЁТ ==========
score = 0
level = 1
lines_cleared = 0


def clear_lines():
    global score, lines_cleared, level
    rows_to_clear = []

    for row in range(ROWS):
        if all(grid[row][col] != 0 for col in range(COLS)):
            rows_to_clear.append(row)

    for row in sorted(rows_to_clear, reverse=True):
        del grid[row]
        grid.insert(0, [0 for _ in range(COLS)])

    if rows_to_clear:
        lines = len(rows_to_clear)
        points = {1: 100, 2: 300, 3: 500, 4: 800}.get(lines, 100 * lines)
        score += points
        lines_cleared += lines
        level = 1 + lines_cleared // 10


def draw_info():
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    level_text = font.render(f"Уровень: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))


def draw_game_over():
    text1 = font.render("ИГРА ОКОНЧЕНА", True, RED)
    text2 = font.render("Нажми R для новой игры", True, WHITE)
    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2))


# ========== ГЛАВНЫЙ ЦИКЛ ==========
def main():
    global score, lines_cleared, level, grid

    current_piece = Tetromino(random.randint(0, 6))
    next_piece_index = random.randint(0, 6)
    fall_time = 0
    fall_speed = 500
    game_over = False
    running = True

    while running:
        dt = clock.tick(60)
        fall_time += dt

        if not game_over and fall_time >= fall_speed / level:
            fall_time = 0
            if not current_piece.move(0, 1):
                current_piece.lock()
                current_piece = Tetromino(next_piece_index)
                next_piece_index = random.randint(0, 6)
                if not current_piece.is_valid():
                    game_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                elif event.key == pygame.K_SPACE:
                    while current_piece.move(0, 1):
                        pass
                    current_piece.lock()
                    current_piece = Tetromino(next_piece_index)
                    next_piece_index = random.randint(0, 6)
                    if not current_piece.is_valid():
                        game_over = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                score = 0
                lines_cleared = 0
                level = 1
                current_piece = Tetromino(random.randint(0, 6))
                next_piece_index = random.randint(0, 6)
                game_over = False

        screen.fill(BLACK)
        draw_grid()

        if not game_over:
            for x, y in current_piece.get_blocks():
                if y >= 0:
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, current_piece.color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)

        draw_info()
        if game_over:
            draw_game_over()

        pygame.display.flip()


if __name__ == "__main__":
    main()
