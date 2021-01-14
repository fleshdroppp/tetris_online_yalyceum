from random import choice
import logging

from copy import deepcopy
import pygame

game_data = {
    'event': '',
    'to_send': [],
    'users': 0,
    'current_player': True,  # True means first player
    'running': True,
    'ready_to_start': False,
    'turn': 0,
    'score': 0
}


def game():
    global game_data

    logging.debug('Starting the game')

    while not game_data['ready_to_start']:
        continue

    width, height = 10, 20
    cell_size = 45

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
    clock = pygame.time.Clock()

    logging.debug('Game initialized')

    def check_pos():
        logging.info('Checking position')

        if current_figure[cell].x < 0 or current_figure[cell].x >= width:
            logging.debug('False')
            return False
        elif current_figure[cell].y >= height or \
                board[current_figure[cell].y][current_figure[cell].x]:
            logging.debug('False')
            return False

        logging.debug('True')
        return True

    while game_data['running']:
        blocks = []
        d_x, rotation = 0, False
        if game_data['event'] == 'right':
            d_x += 1
            game_data['event'] = ''
        if game_data['event'] == 'left':
            d_x -= 1
            game_data['event'] = ''
        if game_data['event'] == 'quit':
            game_data['running'] = False
            game_data['event'] = ''
        if game_data['event'] == 'rotate':
            rotation = True
            game_data['event'] = ''
        if game_data['event'] == 'down':
            anim_limit = 100
            game_data['event'] = ''

        old_figure = deepcopy(current_figure)
        for cell in range(4):
            current_figure[cell].x += d_x
            if not check_pos():
                current_figure = deepcopy(old_figure)
                break

        anim_count += anim_speed
        game_data['turn'] = False
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
                    game_data['turn'] = True
                    game_data['current_player'] = not game_data['current_player']
                    break

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
                game_data['score'] += 1

        for cell in range(4):
            figure_rect.x = current_figure[cell].x * cell_size + 1
            figure_rect.y = current_figure[cell].y * cell_size + 1
            blocks.append([figure_rect.x, figure_rect.y])

        for y, row in enumerate(board):
            for x, col in enumerate(row):
                if col:
                    figure_rect.x, figure_rect.y = x * cell_size + 1, y * cell_size + 1
                blocks.append([figure_rect.x, figure_rect.y])

        game_data['to_send'] = deepcopy(blocks)

        for col in range(width):
            if board[0][col]:
                board = [[0 for i in range(width)] for i in range(height)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                running = False
        clock.tick(60)
