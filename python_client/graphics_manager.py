import math
from typing import Tuple, Dict, List, Optional

import pygame

from dataset.board import Board
from python_client.client_storage import ClientStorage


class GraphicsManager:
    COLOR_BLACK = (40, 40, 40)
    BORDER_COLOR = (200, 140, 60)

    def __init__(self, client_storage: ClientStorage):
        self.client_storage = client_storage
        self.screen_width = 600
        self.screen_height = int(self.screen_width * 10 / 9)
        self.surf = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.entire_screen = (0, 0, self.screen_width, self.screen_height)

        self.border_margin = int((self.screen_width / 9) / 2)
        self.space_between_lines = (self.screen_width - self.border_margin * 2) / 8
        self.block_width = 80
        self.actor_sprites = dict()
        for k in range(1, 15):
            self.actor_sprites[k] = \
                pygame.transform.smoothscale(
                    pygame.image.load('resources/grp/images/actors_{:02d}.png'.format(k)),
                    (self.block_width, self.block_width)
                )
        self.highlighted_blocks: List[Dict] = list()
        self.arrow: Optional[Tuple[int, int, int, int]] = None

    def draw(self):
        pygame.draw.rect(self.surf, color=self.COLOR_BLACK, rect=self.entire_screen)
        self.draw_000_grid_lines()
        self.draw_001_crossing_lines()
        self.draw_002_stars()
        self.draw_003_arrow()
        self.draw_004_actors(self.client_storage.board)
        self.draw_005_highlighted_blocks()

    def draw_000_grid_lines(self):
        for i_x in range(9):
            pos_1: Tuple[int, int] = (
                int(self.border_margin + self.space_between_lines * i_x),
                self.border_margin
            )
            pos_2: Tuple[int, int] = (
                int(self.border_margin + self.space_between_lines * i_x),
                self.screen_height - self.border_margin
            )
            pygame.draw.line(self.surf, color=self.BORDER_COLOR, start_pos=pos_1, end_pos=pos_2)
        for i_y in range(10):
            pos_1: Tuple[int, int] = (
                self.border_margin,
                int(self.border_margin + self.space_between_lines * i_y),
            )
            pos_2: Tuple[int, int] = (
                self.screen_width - self.border_margin,
                int(self.border_margin + self.space_between_lines * i_y),
            )
            pygame.draw.line(self.surf, color=self.BORDER_COLOR, start_pos=pos_1, end_pos=pos_2)
        return

    def draw_001_crossing_lines(self):
        for x1, y1, x2, y2 in [
            (3, 0, 5, 2),
            (3, 2, 5, 0),
            (3, 7, 5, 9),
            (3, 9, 5, 7),
        ]:
            pos_1 = (
                int(self.border_margin + self.space_between_lines * x1),
                int(self.border_margin + self.space_between_lines * y1),
            )
            pos_2 = (
                int(self.border_margin + self.space_between_lines * x2),
                int(self.border_margin + self.space_between_lines * y2),
            )
            pygame.draw.line(self.surf, color=self.BORDER_COLOR, start_pos=pos_1, end_pos=pos_2)
        return

    def draw_002_stars(self):
        outer_star_size = 9
        inner_star_size = 3
        local_points = list()
        for r in range(10):
            if r % 2 == 0:
                star_size = outer_star_size
            else:
                star_size = inner_star_size
            dy = -star_size * math.cos(math.pi * 2 * (r / 10))
            dx = +star_size * math.sin(math.pi * 2 * (r / 10))
            local_points.append((dx, dy))
        for x1, y1 in [
            (0, 3), (0, 6),
            (2, 3), (2, 6),
            (4, 3), (4, 6),
            (6, 3), (6, 6),
            (8, 3), (8, 6),
            (1, 2), (1, 7),
            (7, 2), (7, 7),
        ]:
            pos_1 = (
                int(self.border_margin + self.space_between_lines * x1),
                int(self.border_margin + self.space_between_lines * y1),
            )
            global_points = list()
            for p in local_points:
                global_points.append(
                    (
                        p[0] + pos_1[0],
                        p[1] + pos_1[1],
                    )
                )

            pygame.draw.polygon(self.surf, color=self.BORDER_COLOR, points=global_points)
        return

    def draw_003_arrow(self):
        if self.arrow is None:
            return
        grid_to_screen = lambda x: self.border_margin + self.space_between_lines * x
        pos_1 = list(map(grid_to_screen, self.arrow[0:2]))
        pos_2 = list(map(grid_to_screen, self.arrow[2:4]))

        length = ((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2) ** 0.5
        step_size = 12

        step = [pos_1[0], pos_1[1]]
        dx = (pos_2[0] - pos_1[0]) / length
        dy = (pos_2[1] - pos_1[1]) / length
        r = math.atan2(dy, dx)
        left_wing_r = r + math.pi * 0.8
        right_wing_r = r - math.pi * 0.8
        for c in range(int(length / step_size)):
            step[0] += dx * step_size
            step[1] += dy * step_size
            left_wing_pos = (
                step[0] + step_size * math.cos(left_wing_r),
                step[1] + step_size * math.sin(left_wing_r),
            )
            right_wing_pos = (
                step[0] + step_size * math.cos(right_wing_r),
                step[1] + step_size * math.sin(right_wing_r),
            )
            pygame.draw.line(self.surf, color=self.BORDER_COLOR, width=3, start_pos=step, end_pos=left_wing_pos)
            pygame.draw.line(self.surf, color=self.BORDER_COLOR, width=3, start_pos=step, end_pos=right_wing_pos)

        pygame.draw.line(self.surf, color=self.BORDER_COLOR, width=3, start_pos=pos_1, end_pos=pos_2)

    def draw_004_actors(self, board: Board):
        for x in range(9):
            for y in range(10):
                actor = board.data[x][y]
                if actor is None:
                    continue
                actor_code = actor.get_actor_code()
                self.surf.blit(
                    self.actor_sprites[actor_code],
                    dest=(
                        self.border_margin + self.space_between_lines * x
                        - self.block_width // 2,
                        self.border_margin + self.space_between_lines * y
                        - self.block_width // 2,
                        self.block_width,
                        self.block_width
                    )
                )

    def draw_005_highlighted_blocks(self):

        for highlighted_block in self.highlighted_blocks:
            pos = highlighted_block['pos']

            center_pos = (
                int(self.border_margin + pos[0] * self.space_between_lines),
                int(self.border_margin + pos[1] * self.space_between_lines),
            )
            highlight_width = 60
            s = pygame.Surface((highlight_width, highlight_width), pygame.SRCALPHA)
            s.fill(highlighted_block['color'])
            self.surf.blit(
                s,
                (
                    center_pos[0] - highlight_width // 2,
                    center_pos[1] - highlight_width // 2
                )
            )
