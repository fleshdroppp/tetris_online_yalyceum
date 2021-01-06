import pygame
from random import randrange, choice
from copy import deepcopy

WIDTH, HEIGHT = 10, 20
CELL_SIZE = 45

GAME_RESOLUTION = WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE
WINDOW_RESOLUTION = 750, 940
FPS = 60

grid = [pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) for x in range(WIDTH) for y in range(HEIGHT)]

pygame.init()

win_screen = pygame.display.set_mode(WINDOW_RESOLUTION)
screen = pygame.Surface(GAME_RESOLUTION)
clock = pygame.time.Clock()

# ТИПЫ ФИГУР И КООРДИНАТЫ ИХ ПЛИТОК С ИХ ЦВЕТОМ
figures_types = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                 [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                 [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                 [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, -1)],
                 [(0, 0), (0, -1), (0, 1), (1, -1)],
                 [(0, 0), (0, -1), (0, 1), (-1, 0)]]

anim_count, anim_speed, anim_limit = 0, 60, 2000

figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in pos] for pos in figures_types]
figure_rect = pygame.Rect(0, 0, CELL_SIZE - 2, CELL_SIZE - 2)
board = [[0 for col in range(WIDTH)] for row in range(HEIGHT)]

colors = ['#00ff00', '#ff0000', '#ffffff', '#ADD8E6', '#f7ca18', '#bf55ec', '#F08080']
current_figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = colors[figures.index(current_figure)], colors[figures.index(next_figure)]

score = 0


def check_pos():
    if current_figure[cell].x < 0 or current_figure[cell].x > WIDTH - 1:
        return False
    elif current_figure[cell].y > HEIGHT - 1 or \
            board[current_figure[cell].y][current_figure[cell].x]:
        return False
    return True


running = True
while running:
    win_screen.fill('black')
    win_screen.blit(screen, (20, 20))
    screen.fill('black')
    # ДЕЛЬТА Х - ДВИЖЕНИЕ ТЕКУЩЕЙ ФИГУРЫ ВЛЕВО / ВПРАВО
    d_x, rotation = 0, False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                d_x += 1
            elif event.key == pygame.K_LEFT:
                d_x -= 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotation = True
        if event.type == pygame.QUIT:
            running = False

    # ПЕРЕДВИЖЕНИЕ ПО ОСИ Х
    old_figure = deepcopy(current_figure)
    for cell in range(4):
        current_figure[cell].x += d_x
        if not check_pos():
            current_figure = deepcopy(old_figure)
            break

    # ПЕРЕДВИЖЕНИЕ ПО ОСИ У
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        old_figure = deepcopy(current_figure)
        for cell in range(4):
            current_figure[cell].y += 1
            if not check_pos():
                for i in range(4):
                    board[old_figure[i].y][old_figure[i].x] = color
                current_figure, color = next_figure, next_color
                next_figure = deepcopy(choice(figures))
                next_color = colors[figures.index(next_figure)]
                anim_limit = 2000
                break

    # ПОВОРОТ ФИГУРЫ
    center = current_figure[0]
    old_figure = deepcopy(current_figure)
    if rotation:
        for i in range(4):
            x = current_figure[i].y - center.y
            y = current_figure[i].x - center.x
            current_figure[i].x = center.x - x
            current_figure[i].y = center.y + y
            if not check_pos():
                figure = deepcopy(old_figure)
                break

    # ОЧИСТКА ЛИНИЙ, НАЧИСЛЕНИЕ ОЧКОВ, УСКОРЕНИЕ
    line = HEIGHT - 1
    for row in range(HEIGHT - 1, -1, -1):
        cnt_elements = 0
        for col in range(WIDTH):
            if board[row][col]:
                cnt_elements += 1
            board[line][col] = board[row][col]
        if cnt_elements < WIDTH:
            line -= 1
        else:
            anim_speed += 5
            score += 1

    # ОТРИСОВКА СЕТКИ
    [pygame.draw.rect(screen, (50, 50, 50), item, 1) for item in grid]

    # ОТРИСОВКА ПАДАЮЩЕЙ ФИГУРЫ
    for cell in range(4):
        figure_rect.x = current_figure[cell].x * CELL_SIZE
        figure_rect.y = current_figure[cell].y * CELL_SIZE
        pygame.draw.rect(screen, color, figure_rect)

    # ОТРИСОВКА СЛЕДУЮЩЕЙ ФИГУРЫ
    for cell in range(4):
        figure_rect.x = next_figure[cell].x * CELL_SIZE + 380
        figure_rect.y = next_figure[cell].y * CELL_SIZE + 185
        pygame.draw.rect(win_screen, next_color, figure_rect)

    # ОТРИСОВКА ПОЛЯ
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col:
                figure_rect.x, figure_rect.y = x * CELL_SIZE, y * CELL_SIZE
                pygame.draw.rect(screen, col, figure_rect)

    # КОНЕЦ ИГРЫ
    for col in range(WIDTH):
        if board[0][col]:
            board = [[0 for i in range(WIDTH)] for i in range(HEIGHT)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(screen, 'black', i_rect)
                win_screen.blit(screen, (20, 20))
                pygame.display.flip()
    pygame.display.flip()
    clock.tick(FPS)
