import datetime
import enum
import math
import random
from typing import List, Optional, Tuple

import pygame.surface
from pygame.surface import Surface

from game_data import block_width, screen_width, Board, MoveCode

actor_width = int(block_width * 1.5)


class Sprites:
    def __init__(self):
        self.normal: List[Optional[Surface]] = [None]
        self.glowed: List[Optional[Surface]] = [None]
        self.shadowed: List[Optional[Surface]] = [None]
        for x in range(1, 15):
            path = 'grp/images/actors_{:02d}.png'.format(x)
            self.normal.append(pygame.transform.smoothscale(
                pygame.image.load(path),
                (actor_width, actor_width)
            ))

        for m in range(1, 15):
            w, h = self.normal[m].get_size()
            glowed = Surface((w, h), flags=self.normal[m].get_flags())
            shadowed = Surface((w, h), flags=self.normal[m].get_flags())
            for x in range(w):
                for y in range(h):
                    r, g, b, a = self.normal[m].get_at((x, y))
                    k = (r + g + b) / 3
                    if r + g + b >= 0x30 * 3:
                        r = int(k * 2)
                        g = int(k * 2)
                        b = int(k * 0.5)
                        r = max(0, min(r, 0xff))
                        g = max(0, min(g, 0xff))
                        b = max(0, min(b, 0xff))
                    glowed.set_at((x, y), (r, g, b, a))

                    l = math.sqrt((1 - x / (w / 2)) ** 2 + (1 - y / (h / 2)) ** 2) / math.sqrt(2)
                    if a > 0:
                        a = int((1 - l) ** 4 * 0xff)
                        a = max(0, min(a, 0xff))
                    shadowed.set_at((x, y), (int(k), int(k), int(k), a))
            self.glowed.append(glowed)
            self.shadowed.append(shadowed)

    def from_act_code(self, act_code: int) -> Surface:
        return self.normal[act_code]


class Viewer:
    class Event:
        class Type(enum.Enum):
            Move = 1
            Delete = 2

        def __init__(self, event_type: Type, *,
                     x1: int, y1: int,
                     code1: int = None, code2: float = None,
                     x2: int = None, y2: int = None):
            self.event_type = event_type
            self.born_time = datetime.datetime.now()
            self.code1 = code1
            self.code2 = code2
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.duration = 0
            self.let_me_die = False
            if self.event_type == self.Type.Move:
                length = math.sqrt(
                    (self.x1 - self.x2) ** 2 +
                    (self.y1 - self.y2) ** 2
                )
                self.duration = 0.5 + (length - 1) * 0.05
            elif self.event_type == self.Type.Delete:
                self.duration = self.code2

        @property
        def progress(self) -> float:
            return (datetime.datetime.now() - self.born_time).total_seconds() / self.duration

    sprites = Sprites()

    def __init__(self, surf: Surface):
        self.surf: Surface = surf
        self.board: Optional[Board] = None
        self.events: List[Viewer.Event] = []
        self.earth_quake = [0, 0]
        self.earth_quake_velocity = [0, 0]
        self.earth_quake_direction = [
            [random.uniform(0, math.pi * 2) for x in range(9)] for y in range(9)
        ]

    def draw_borders(self):
        border_color = (200, 140, 60)

        ex, ey = self.earth_quake

        for x1, y1, x2, y2 in (
                (4, 7, 6, 9),
                (6, 7, 4, 9),
                (4, 1, 6, 3),
                (6, 1, 4, 3),
        ):
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * x1 + ex, block_width * y1 + ey),
                end_pos=(block_width * x2 + ex, block_width * y2 + ey),
                width=5
            )

        for x in range(9):
            x += 1
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * x + ex, block_width * 1 + ey),
                end_pos=(block_width * x + ex, block_width * 9 + ey),
                width=3
            )
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * 1 + ex, block_width * x + ey),
                end_pos=(block_width * 9 + ex, block_width * x + ey),
                width=3
            )

    def draw_actors(self):
        for x, y, act_code in self.board:
            if act_code == 0:
                continue
            is_animating = False
            for event in self.events:
                if event.x1 == x and event.y1 == y:
                    is_animating = True
                    break
                if event.x2 == x and event.y2 == y:
                    is_animating = True
                    break
            if is_animating:
                continue

            ex = math.cos(self.earth_quake_direction[x][y]) * (self.earth_quake[0] + self.earth_quake[1]) * 0.5
            ey = math.sin(self.earth_quake_direction[x][y]) * (self.earth_quake[0] + self.earth_quake[1]) * 0.5
            self.surf.blit(
                self.sprites.from_act_code(act_code),
                dest=(
                    (x + 0.5) * block_width - (actor_width - block_width) / 2 + ex,
                    (y + 0.5) * block_width - (actor_width - block_width) / 2 + ey,
                    block_width,
                    block_width
                )
            )

    def draw_decisions(self, old_x: int, old_y: int, act_code: int, positions: List[Tuple[int, int]]):
        for new_x, new_y in positions:
            self.surf.blit(
                self.sprites.shadowed[act_code],
                dest=(
                    (new_x + 0.5) * block_width - (actor_width - block_width) / 2,
                    (new_y + 0.5) * block_width - (actor_width - block_width) / 2,
                    block_width,
                    block_width
                )
            )

        self.surf.blit(
            self.sprites.glowed[act_code],
            dest=(
                (old_x + 0.5) * block_width - (actor_width - block_width) / 2,
                (old_y + 0.5) * block_width - (actor_width - block_width) / 2,
                block_width,
                block_width
            )
        )

    def draw_event_effects(self):
        for event in self.events:
            if event.progress >= 1:
                event.let_me_die = True
            if event.event_type == self.Event.Type.Move:
                p = event.progress ** 4
                q = 1 - p
                x = event.x1 * q + event.x2 * p
                y = event.y1 * q + event.y2 * p
                self.surf.blit(
                    self.sprites.normal[event.code1],
                    dest=(
                        (x + 0.5) * block_width - (actor_width - block_width) / 2,
                        (y + 0.5) * block_width - (actor_width - block_width) / 2,
                        block_width,
                        block_width
                    )
                )
            elif event.event_type == self.Event.Type.Delete:

                surf = self.sprites.normal[event.code1]
                p = event.progress
                if p < 1 - 0.5 / event.duration:
                    event.code2 = 1.0
                    continue
                else:
                    t = p * event.duration
                    p = (t - (event.duration - 0.5)) / 0.5
                    print('p %4.2f %4.2f' % (p, p ** 16))
                    p = 0.5 * (
                            + 5 * p
                            - 9 * (p ** 2)
                            + 6 * (p ** 3)
                    )
                if event.code2 > 0:
                    event.code2 = - 1
                    if MoveCode.from_act_code(event.code1) in (MoveCode.Cart, MoveCode.Artillery, MoveCode.CastleMan):
                        self.add_earth_quake(2)
                    elif MoveCode.from_act_code(event.code1) == MoveCode.Horse:
                        self.add_earth_quake(1.6)
                    else:
                        self.add_earth_quake(1.2)

                surf.set_alpha(int(0xff * (1 - p)))
                for z in range(1, 21):
                    r = z / 20 * math.pi * 2 + event.born_time.microsecond
                    dx = math.cos(r) * p * 400
                    dy = math.sin(r) * p * 400
                    self.surf.blit(
                        surf,
                        dest=(
                            (event.x1 + 0.5) * block_width - (actor_width - block_width) / 2 + dx,
                            (event.y1 + 0.5) * block_width - (actor_width - block_width) / 2 + dy,
                            block_width,
                            block_width
                        )
                    )
                surf.set_alpha(0xff)
            else:
                raise ValueError(event.event_type)
        self.events = [event for event in self.events if not event.let_me_die]

    def step(self):
        pygame.draw.rect(self.surf, color=(40, 40, 40), rect=(0, 0, screen_width, screen_width))
        self.draw_borders()
        self.draw_actors()
        self.draw_event_effects()

        x, y = self.earth_quake
        mult = 0.3
        x = -x * mult
        y = -y * mult
        l = x ** 2 + y ** 2
        for k in range(2):
            l += self.earth_quake_velocity[k] ** 2
        if l < 0.06:
            self.earth_quake_velocity = [0, 0]
            self.earth_quake = [0, 0]
        else:

            vec = x, y

            for k in range(2):
                self.earth_quake[k] += self.earth_quake_velocity[k]
            for k in range(2):
                self.earth_quake_velocity[k] += vec[k]
                self.earth_quake_velocity[k] *= 0.5

    def add_earth_quake(self, force: float):
        for k in range(2):
            self.earth_quake_velocity[k] += random.uniform(-1, 1) * (10 ** force)

        self.earth_quake_direction = [
            [random.uniform(0, math.pi * 2) for x in range(9)] for y in range(9)
        ]

    def add_event(self, *args, **kwargs) -> Event:
        e = self.Event(*args, **kwargs)
        self.events.append(e)
        return e
