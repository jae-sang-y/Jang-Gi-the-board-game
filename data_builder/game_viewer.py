from typing import List, Optional

import pygame.surface
from pygame.surface import Surface

from game_data import block_width, screen_width, Board

actor_width = int(block_width * 1.5)


class Sprites:
    def __init__(self):
        self.sprite_list: List[Surface] = [None]
        pygame.transform.set_smoothscale_backend('SSE')
        for x in range(1, 15):
            path = 'grp/images/actors_{:02d}.png'.format(x)
            self.sprite_list.append(pygame.transform.smoothscale(
                pygame.image.load(path),
                (actor_width, actor_width)
            ))

    def from_act_code(self, act_code: int) -> Surface:
        return self.sprite_list[act_code]


class Viewer:
    sprites = Sprites()

    def __init__(self, surf: Surface):
        self.surf: Surface = surf
        self.board: Optional[Board] = None

    def draw_borders(self):
        border_color = (200, 140, 60)

        for x1, y1, x2, y2 in (
                (4, 7, 6, 9),
                (6, 7, 4, 9),
                (4, 1, 6, 3),
                (6, 1, 4, 3),
        ):
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * x1, block_width * y1),
                end_pos=(block_width * x2, block_width * y2),
                width=5
            )

        for x in range(9):
            x += 1
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * x, block_width * 1),
                end_pos=(block_width * x, block_width * 9),
                width=3
            )
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * 1, block_width * x),
                end_pos=(block_width * 9, block_width * x),
                width=3
            )

    def draw_actors(self):
        for x, y, act_code in self.board:
            if act_code == 0:
                continue
            self.surf.blit(
                self.sprites.from_act_code(act_code),
                dest=(
                    (x + 0.5) * block_width - (actor_width - block_width) / 2,
                    (y + 0.5) * block_width - (actor_width - block_width) / 2,
                    block_width,
                    block_width
                )
            )

    def step(self):
        pygame.draw.rect(self.surf, color=(40, 40, 40), rect=(0, 0, screen_width, screen_width))
        self.draw_borders()
        self.draw_actors()

