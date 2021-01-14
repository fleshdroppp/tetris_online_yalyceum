import socket
import pygame
import json
import pickle
from solo import solo_game
from pygame import mixer
from coop_version.client import coop_game

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
    solo = False
    team = False

    while True:
        win_screen.fill('black')

        font = pygame.font.Font('data/ARCADECLASSIC.TTF', 150)
        text = font.render("TETRIS", True, (255, 255, 255))
        win_screen.blit(text, (122, 250))

        pygame.draw.rect(win_screen, '#ff002a', pygame.Rect(146, 393, 458, 76))
        font = pygame.font.Font('data/ARCADECLASSIC.TTF', 80)
        text = font.render("COOP GAME", True, (255, 255, 255))
        win_screen.blit(text, (192, 392))

        pygame.draw.rect(win_screen, '#ff002a', pygame.Rect(146, 495, 458, 76))
        text = font.render("SOLO GAME", True, (255, 255, 255))
        win_screen.blit(text, (192, 494))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if (146 <= x <= 146 + 458) and (393 <= y <= 393 + 76):
                    team = True
                elif (146 <= x <= 146 + 458) and (495 <= y <= 495 + 76):
                    solo = True
            if event.type == pygame.QUIT:
                exit(0)
        if solo or team:
            break
        pygame.display.flip()
        clock.tick(FPS)

    mixer.init()
    mixer.music.load('data/music.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play(loops=0)
    win_screen.fill('black')
    screen.fill('black')
    if solo:
        solo_game()
    elif team:
        coop_game()
