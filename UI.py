import os.path
import model
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

hand_positions = [(560, 625), (640, 625), (0, 335), (80, 335), (540, 0), (640, 0), (1040, 335), (1120, 335)]
community_card_positions = [(400, 335), (480, 335), (560, 335), (640, 335), (720, 335)]

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

