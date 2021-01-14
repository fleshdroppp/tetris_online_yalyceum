from json import decoder

import requests
import pygame

running = True

ADDRESS = "localhost:5000"

WIDTH, HEIGHT = 10, 20
CELL_SIZE = 45

GAME_RESOLUTION = WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE
WINDOW_RESOLUTION = 750, 940
FPS = 20
win_screen = pygame.display.set_mode(WINDOW_RESOLUTION)
screen = pygame.Surface(GAME_RESOLUTION)
clock = pygame.time.Clock()
grid = [pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) for x in range(WIDTH) for y in range(HEIGHT)]
count_req = 0
pygame.init()


def move(direction, user_id):
    try:
        requests.get(f'http://{ADDRESS}/move/{direction}/{user_id}')
    except requests.exceptions.ConnectionError:
        exit('Unable to send player\'s command')


if __name__ == '__main__':
    user_id = requests.get(f'http://{ADDRESS}/new_user').json()['id']

    while running:
        win_screen.fill('black')
        win_screen.blit(screen, (20, 20))
        screen.fill('black')
        d_x, rotation = 0, False
        sent = 0
        old_sent = 0
        blocks = {}
        try:
            blocks = requests.get(f'http://{ADDRESS}/move/send/{user_id}').json()
        except decoder.JSONDecodeError:
            exit('Unable to get data from server. May it be down?')

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move('right', user_id)
                elif event.key == pygame.K_LEFT:
                    move('left', user_id)
                elif event.key == pygame.K_DOWN:
                    move('down', user_id)
                elif event.key == pygame.K_UP:
                    move('rotate', user_id)
            if event.type == pygame.QUIT:
                requests.get(f'http://{ADDRESS}/quit')
                running = False

        [pygame.draw.rect(screen, (50, 50, 50), item, 1) for item in grid]

        count_req += 1

        if blocks:
            if blocks.get('run'):
                for block in blocks.get('blocks'):
                    pygame.draw.rect(screen, 'white', pygame.Rect(block[0], block[1], 43, 43))
            else:
                running = False

        pygame.display.flip()
        clock.tick(FPS)
