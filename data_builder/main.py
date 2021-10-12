import os

import pygame

from game_data import screen_width
from game_director import Director

os.environ['SDL_VIDEO_WINDOW_POS'] = '950,200'
pygame.init()
surf = pygame.display.set_mode((screen_width, screen_width))
director = Director(surf)
main_loop = True

while main_loop:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            main_loop = False
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            main_loop = False

    director.step()

    pygame.display.flip()
pygame.quit()
