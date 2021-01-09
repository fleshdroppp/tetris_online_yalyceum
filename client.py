import socket
import pygame
import json
import pickle
running = True

WIDTH, HEIGHT = 10, 20
CELL_SIZE = 45

GAME_RESOLUTION = WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE
WINDOW_RESOLUTION = 750, 940
FPS = 60
win_screen = pygame.display.set_mode(WINDOW_RESOLUTION)
screen = pygame.Surface(GAME_RESOLUTION)
clock = pygame.time.Clock()

pygame.init()
grid = [pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE) for x in range(WIDTH) for y in range(HEIGHT)]

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 4006))

    while running:
        win_screen.fill('black')
        win_screen.blit(screen, (20, 20))
        screen.fill('black')

        d_x, rotation = 0, False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    client.send('right'.encode('utf-8'))
                elif event.key == pygame.K_LEFT:
                    client.send('left'.encode('utf-8'))
                elif event.key == pygame.K_DOWN:
                    client.send('down'.encode('utf-8'))
                elif event.key == pygame.K_UP:
                    client.send('rotate'.encode('utf-8'))
            if event.type == pygame.QUIT:
                client.send('quit'.encode('utf-8'))

        [pygame.draw.rect(screen, (50, 50, 50), item, 1) for item in grid]

        client.send('ready'.encode())

        data = client.recv(4096)
        blocks = pickle.loads(data)

        for block in blocks:
            if block[2] == 1:
                pygame.draw.rect(screen, block[1], block[0])

        pygame.display.flip()
        clock.tick(FPS)

    #     [pygame.draw.rect(screen, (50, 50, 50), item, 1) for item in grid]
    #     pygame.display.flip()
    #     clock.tick(FPS)
    # for block in blocks:
    #     print(block)
    #     pygame.draw.rect(block[2], block[1], block[0])
