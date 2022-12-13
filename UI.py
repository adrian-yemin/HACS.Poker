import os.path

import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.mixer.init()
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((34, 139, 34))

    x, y = pygame.mouse.get_pos()

    card = pygame.image.load(os.path.join('res', '10h.png'))

    screen.blit(card, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    pygame.display.flip()

pygame.quit()
