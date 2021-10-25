import datetime
import enum
import math
import random
from typing import List, Optional, Tuple, Final

import pygame.surface
from board_in_c import Board
from pygame.surface import Surface

from game_data import block_width, screen_width, MoveCode, ActorCode, screen_width, screen_resolution

actor_width = int(block_width * 1.5)


def sign(num: float) -> float:
    return +1 if num >= 0 else -1


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

    def from_actor_code(self, actor_code: int) -> Surface:
        return self.normal[actor_code]


class Viewer:
    class Event:
        class Type(enum.Enum):
            Move = 1
            Delete = 2

        def __init__(self, event_type: Type, *,
                     x1: int, y1: int,
                     duration: float = None,
                     code1: int = None, code2: int = None,
                     x2: int = None, y2: int = None):
            self.event_type: Final = event_type
            self.born_time: Final = datetime.datetime.now()
            self.code1: Final = code1
            self.code2: Final = code2
            self.x1: Final = x1
            self.y1: Final = y1
            self.x2: Final = x2
            self.y2: Final = y2
            self.let_me_die = False

            if self.event_type == self.Type.Move:
                length = math.sqrt(
                    (self.x1 - self.x2) ** 2 +
                    (self.y1 - self.y2) ** 2
                )
                duration = 0.5 + (length - 1) * 0.05
            elif self.event_type == self.Type.Delete:
                pass
            else:
                raise ValueError(self.event_type)

            self.duration: Final = duration

        @property
        def progress(self) -> float:
            return (datetime.datetime.now() - self.born_time).total_seconds() / self.duration

    sprites = Sprites()

    def __init__(self, surf: Surface, board: Board):
        self.surf: Surface = surf
        self.board: Board = board
        self.events: List[Viewer.Event] = []

        self.time = datetime.datetime.now()
        self.earth_quake_potential = [0, 0]
        self.earth_quake_velocity = [0, 0]
        self.earth_quake_time = 0
        self.earth_quake_direction = [
            [random.uniform(0, math.pi * 2) for x in range(9)] for y in range(10)
        ]

    def draw_borders(self):
        border_color = (200, 140, 60)

        ex, ey = self.earth_quake_potential
        ex *= 1e-1
        ey *= 1e-1

        for x1, y1, x2, y2 in (
                (4, 8, 6, 10),
                (6, 8, 4, 10),
                (4, 1, 6, 3),
                (6, 1, 4, 3),
        ):
            try:
                pygame.draw.line(
                    self.surf,
                    color=border_color,
                    start_pos=(block_width * x1 + ex, block_width * y1 * screen_resolution + ey),
                    end_pos=(block_width * x2 + ex, block_width * y2 * screen_resolution + ey),
                    width=5
                )
            except Exception as e:
                print(ex, ey)
                raise e

        for x in range(9):
            x += 1
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * x + ex, block_width * 1 * screen_resolution + ey),
                end_pos=(block_width * x + ex, block_width * 10 * screen_resolution + ey),
                width=3
            )
        for y in range(10):
            y += 1
            pygame.draw.line(
                self.surf,
                color=border_color,
                start_pos=(block_width * 1 + ex, block_width * y * screen_resolution + ey),
                end_pos=(block_width * 9 + ex, block_width * y * screen_resolution + ey),
                width=3
            )

    def draw_actors(self):
        for x, y, actor_code in self.board:
            if actor_code == 0:
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

            # ex = math.cos(self.earth_quake_direction[x][y]) * (self.earth_quake_potential[0] + self.earth_quake_potential[1]) * 0.5
            # ey = math.sin(self.earth_quake_direction[x][y]) * (                        self.earth_quake_potential[0] + self.earth_quake_potential[1]) * 0.5
            ex = 1e-2 * math.cos(self.earth_quake_direction[y][x]) * self.earth_quake_velocity[0]
            ey = 1e-2 * math.sin(self.earth_quake_direction[y][x]) * self.earth_quake_velocity[1]

            self.surf.blit(
                self.sprites.from_actor_code(actor_code),
                dest=(
                    (x + 0.5) * block_width - (actor_width - block_width) / 2 + ex,
                    (y / screen_resolution + 0.5) * block_width - (actor_width - block_width) / 2 + ey,
                    block_width,
                    block_width
                )
            )

    def draw_decisions(self, old_x: int, old_y: int, actor_code: int, positions: List[Tuple[int, int]]):
        for new_x, new_y in positions:
            self.surf.blit(
                self.sprites.shadowed[actor_code],
                dest=(
                    (new_x + 0.5) * block_width - (actor_width - block_width) / 2,
                    (new_y + 0.5) * block_width - (actor_width - block_width) / 2,
                    block_width,
                    block_width
                )
            )

        self.surf.blit(
            self.sprites.glowed[actor_code],
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

                new_actor_surf = self.sprites.normal[event.code1]
                p = event.progress
                if p < 1 - 0.5 / event.duration:
                    self.surf.blit(
                        new_actor_surf,
                        dest=(
                            (event.x1 + 0.5) * block_width - (actor_width - block_width) / 2,
                            (event.y1 + 0.5) * block_width - (actor_width - block_width) / 2,
                            block_width,
                            block_width
                        )
                    )
                else:
                    self.surf.blit(
                        self.sprites.normal[event.code2],
                        dest=(
                            (event.x1 + 0.5) * block_width - (actor_width - block_width) / 2,
                            (event.y1 + 0.5) * block_width - (actor_width - block_width) / 2,
                            block_width,
                            block_width
                        )
                    )
                    t = p * event.duration
                    p = (t - (event.duration - 0.5)) / 0.5
                    p = 0.5 * (
                            + 5 * p
                            - 9 * (p ** 2)
                            + 6 * (p ** 3)
                    )
                    if event.code2 > 0:
                        if self.earth_quake_time <= 0:
                            if MoveCode.from_actor_code(event.code1) in (
                                    MoveCode.Cart, MoveCode.Artillery, MoveCode.CastleMan) and \
                                    event.code1 not in (ActorCode.NorthBishop, ActorCode.SouthBishop):
                                self.add_earth_quake(force=2.25, time=1)
                            elif MoveCode.from_actor_code(event.code1) == MoveCode.Horse or \
                                    event.code1 not in (ActorCode.NorthBishop, ActorCode.SouthBishop):
                                self.add_earth_quake(force=1.85, time=1)
                            else:
                                self.add_earth_quake(force=0.5, time=1)

                    new_actor_surf.set_alpha(int(0xff * (1 - p)))
                    for z in range(1, 21):
                        r = z / 20 * math.pi * 2 + event.born_time.microsecond
                        dx = math.cos(r) * p * 400
                        dy = math.sin(r) * p * 400
                        self.surf.blit(
                            new_actor_surf,
                            dest=(
                                (event.x1 + 0.5) * block_width - (actor_width - block_width) / 2 + dx,
                                (event.y1 + 0.5) * block_width - (actor_width - block_width) / 2 + dy,
                                block_width,
                                block_width
                            )
                        )
                    new_actor_surf.set_alpha(0xff)
            else:
                raise ValueError(event.event_type)
        self.events = [event for event in self.events if not event.let_me_die]

    def step(self):
        now = datetime.datetime.now()
        dt = (now - self.time).total_seconds()
        self.time = now

        pygame.draw.rect(self.surf, color=(40, 40, 40), rect=(0, 0, screen_width, screen_width))
        self.draw_borders()
        self.draw_actors()
        self.draw_event_effects()

        x, y = self.earth_quake_potential
        length = (x ** 2 + y ** 2) ** 0.5
        x, y = self.earth_quake_velocity

        velocity = (x ** 2 + y ** 2) ** 0.5
        friction = (velocity ** 2) * 0.5

        if velocity <= friction or velocity <= 5:
            if length < 1:
                self.earth_quake_potential = [0, 0]
                self.earth_quake_velocity = [0, 0]
        else:
            norm_vec = x / velocity, y / velocity
            for k in range(2):
                self.earth_quake_velocity[k] -= dt * norm_vec[k] * friction

        if length < 0.1:
            self.earth_quake_potential = [0, 0]
            self.earth_quake_time = 0
        else:

            for k in range(2):
                self.earth_quake_potential[k] -= \
                    self.earth_quake_potential[k] * dt * \
                    (21 - max(1 - self.earth_quake_time, 0) * 20)
            if self.earth_quake_time > 0:
                for k in range(2):
                    self.earth_quake_potential[k] += self.earth_quake_velocity[k] * dt
                self.earth_quake_time -= dt
                vec = self.earth_quake_potential
                for k in range(2):
                    self.earth_quake_velocity[k] -= 1e4 * self.earth_quake_time * vec[k] / length * dt
            else:
                self.earth_quake_time = 0

    def add_earth_quake(self, *, force: float, time: float):
        r = random.uniform(-1, 1) * math.pi

        self.earth_quake_potential[0] += math.cos(r) * (10 ** force)
        self.earth_quake_potential[1] += math.sin(r) * (10 ** force)
        r = random.uniform(-1, 1) * math.pi
        self.earth_quake_velocity[0] += math.cos(r) * (10 ** force)
        self.earth_quake_velocity[1] += math.sin(r) * (10 ** force)
        self.earth_quake_time = time
        self.earth_quake_direction = [
            [random.uniform(0, math.pi * 2) for x in range(9)] for y in range(10)
        ]

    def add_event(self, *args, **kwargs) -> Event:
        e = self.Event(*args, **kwargs)
        self.events.append(e)
        return e
