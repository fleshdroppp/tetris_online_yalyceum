import socket
import json
import pickle
from random import randrange, choice
from copy import deepcopy
import pygame

users = []
clock = pygame.time.Clock()
FPS = 60


def send_blocks(data):
    clock.tick(FPS)
    data_string = pickle.dumps(data)
    users[0].send(data_string)


def game():
    width, height = 10, 20
    cell_size = 45
    window_resolution = 750, 940

    game_resolution = width * cell_size, height * cell_size

    # win_screen = pygame.display.set_mode(window_resolution)
    # screen = pygame.Surface(game_resolution)

    pygame.init()

    figures_types = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                     [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                     [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                     [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                     [(0, 0), (0, -1), (0, 1), (-1, -1)],
                     [(0, 0), (0, -1), (0, 1), (1, -1)],
                     [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    anim_count, anim_speed, anim_limit = 0, 60, 2000

    figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in pos] for pos in figures_types]
    figure_rect = pygame.Rect(0, 0, cell_size - 2, cell_size - 2)
    board = [[0 for col in range(width)] for row in range(height)]

    colors = ['#00ff00', '#ff0000', '#ffffff', '#ADD8E6', '#f7ca18', '#bf55ec', '#F08080']
    current_figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = colors[figures.index(current_figure)], colors[figures.index(next_figure)]
    score = 0

    def check_pos():
        if current_figure[cell].x < 0 or current_figure[cell].x >= width:
            return False
        elif current_figure[cell].y >= height or \
                board[current_figure[cell].y][current_figure[cell].x]:
            return False
        return True

    running = True

    while running:
        blocks = []
        d_x, rotation = 0, False
        event = users[0].recv(2048).decode()
        print(event)

        if event == 'right':
            d_x += 1
        if event == 'left':
            d_x -= 1
        if event == 'quit':
            running = False
        if event == 'rotate':
            rotation = True
        if event == 'down':
            anim_limit = 100

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

        # Поворот фигуры
        center = current_figure[0]
        old_figure = deepcopy(current_figure)
        if rotation:
            for cell in range(4):
                x = current_figure[cell].y - center.y
                y = current_figure[cell].x - center.x
                current_figure[cell].x = center.x - x
                current_figure[cell].y = center.y + y
                if not check_pos():
                    current_figure = deepcopy(old_figure)
                    break

        # ОЧИСТКА ЛИНИЙ, НАЧИСЛЕНИЕ ОЧКОВ, УСКОРЕНИЕ
        line = height - 1
        for row in range(height - 1, -1, -1):
            cnt_elements = 0
            for col in range(width):
                if board[row][col]:
                    cnt_elements += 1
                board[line][col] = board[row][col]
            if cnt_elements < width:
                line -= 1
            else:
                anim_speed += 5
                score += 1

        # ОТРИСОВКА ПАДАЮЩЕЙ ФИГУРЫ
        for cell in range(4):
            figure_rect.x = current_figure[cell].x * cell_size + 1
            figure_rect.y = current_figure[cell].y * cell_size + 1
            blocks.append([deepcopy(figure_rect), color, 1])

        # ОБРАБОТКА ВСЕХ СТАТИЧНЫХ ФИГУР ПОЛЯ
        for y, row in enumerate(board):
            for x, col in enumerate(row):
                if col:
                    figure_rect.x, figure_rect.y = x * cell_size, y * cell_size
                    blocks.append([deepcopy(figure_rect), col, 1])

        if event == 'ready':
            send_blocks(blocks)

        # КОНЕЦ ИГРЫ
        for col in range(width):
            if board[0][col]:
                board = [[0 for i in range(width)] for i in range(height)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                running = False  # ENF OF THE GAME


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 4006))
    server.listen(2)

    while len(users) != 1:
        user_sock, address = server.accept()
        users.append(user_sock)

    game()
    server.close()

