import datetime
import random
from typing import Tuple, List, Optional

import pygame
from pygame import Surface
from pygame.event import Event

from game_data import Board, ActorCode, MoveCode, TeamCode, FourDirectionDelta, castle_routes, is_inner_castle, \
    castle_routes_cross_only, block_width
from game_viewer import Viewer, actor_width


class Director:
    def __init__(self, surf: Surface):
        self.viewer = Viewer(surf)
        self.board = Board()
        self.last_tick = datetime.datetime.now()
        self.turn_own_team = TeamCode.Red

        self.user_team = TeamCode.Green
        self.user_actor: Optional[Tuple[int, int, int]] = None
        self.user_actor_positions: List[Tuple[int, int]] = []

    def step(self):
        self.viewer.board = self.board
        self.viewer.step()
        if self.user_actor:
            x, y, act_code = self.user_actor
            self.viewer.draw_decisions(x, y, act_code, self.user_actor_positions)

        if self.viewer.events:
            self.last_tick = datetime.datetime.now()
        elif self.turn_own_team != self.user_team:
            tick = datetime.datetime.now()
            delta = tick - self.last_tick
            if delta.total_seconds() >= 0.1:
                self.tick()

    def input(self, e: Event):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                self.viewer.add_earth_quake(force=0.5)
            if e.key == pygame.K_s:
                self.viewer.add_earth_quake(force=1)
            if e.key == pygame.K_d:
                self.viewer.add_earth_quake(force=2)
        if self.turn_own_team != self.user_team:
            return
        if e.type == pygame.MOUSEBUTTONDOWN:
            click_nothing = True
            for x, y, act_code in self.board:
                rect = pygame.Rect(
                    (x + 0.5) * block_width - (actor_width - block_width) / 2,
                    (y + 0.5) * block_width - (actor_width - block_width) / 2,
                    block_width,
                    block_width
                )
                cursor_x, cursor_y = e.pos
                if rect.collidepoint(cursor_x, cursor_y):
                    if act_code != ActorCode.Null:
                        click_nothing = False
                    if act_code == ActorCode.Null or TeamCode.from_act_code(act_code) != self.user_team:
                        if self.user_actor is not None:
                            for new_x, new_y in self.user_actor_positions:
                                if new_x == x and new_y == y:
                                    old_x, old_y, act_code = self.user_actor
                                    self.board[old_y][old_x] = ActorCode.Null
                                    move_duration = self.viewer.add_event(
                                        Viewer.Event.Type.Move,
                                        code1=act_code,
                                        x1=old_x, y1=old_y,
                                        x2=new_x, y2=new_y
                                    ).duration
                                    if self.board[new_y][new_x] != ActorCode.Null:
                                        self.viewer.add_event(
                                            Viewer.Event.Type.Delete,
                                            code1=self.board[new_y][new_x],
                                            code2=move_duration,
                                            x1=new_x, y1=new_y
                                        )

                                    self.board[new_y][new_x] = act_code
                                    self.release_turn()
                                    self.user_actor = None
                                    self.user_actor_positions = []
                                    break

                    else:
                        self.user_actor = x, y, act_code
                        self.user_actor_positions = self.get_movable_positions(x, y, act_code)
                    break
            if click_nothing:
                self.user_actor = None
                self.user_actor_positions = []

    @staticmethod
    def is_possible_position(x: int, y: int) -> bool:
        return 0 <= x <= 8 and 0 <= y <= 8

    def is_empty_position(self, x: int, y: int) -> bool:
        return self.board[y][x] == ActorCode.Null

    def is_enemy_position(self, team_code: int, x: int, y: int) -> bool:
        return TeamCode.from_act_code(self.board[y][x]) != team_code

    def is_movable_or_edible(self, team_code: int, x: int, y: int):
        return self.is_empty_position(x, y) or self.is_enemy_position(team_code, x, y)

    def get_movable_positions(self, x: int, y: int, act_code: int) -> List[Tuple[int, int]]:
        mc = MoveCode.from_act_code(act_code)
        tc = TeamCode.from_act_code(act_code)
        result: List[Tuple[int, int]] = []
        if mc == MoveCode.Footman:
            result.append((x - 1, y))
            result.append((x + 1, y))
            if tc == TeamCode.Red:
                result.append((x, y + 1))
            elif tc == TeamCode.Green:
                result.append((x, y - 1))
            if is_inner_castle(x, y):
                for dx, dy in castle_routes_cross_only[x][y]:
                    if dy == (+1 if tc == TeamCode.Red else -1):
                        result.append((x + dx, y + dy))
        elif mc == MoveCode.Horse:
            for dx, dy in FourDirectionDelta:
                rx = x + dx
                ry = y + dy
                first_pos = rx, ry
                if self.is_possible_position(*first_pos) and self.is_empty_position(*first_pos):
                    pass
                else:
                    continue

                for z in (-1, 1):
                    if dx != 0:
                        pos = (first_pos[0] + dx, first_pos[1] + z)
                    else:
                        pos = (first_pos[0] + z, first_pos[1] + dy)
                    result.append(pos)
        elif mc == MoveCode.Elephant:
            for dx, dy in FourDirectionDelta:
                rx = x + dx
                ry = y + dy
                first_pos = rx, ry
                if self.is_possible_position(*first_pos) and self.is_empty_position(*first_pos):
                    pass
                else:
                    continue

                for z in (-1, 1):
                    if dx != 0:
                        second_pos = [first_pos[0] + dx, first_pos[1] + z]
                    else:
                        second_pos = [first_pos[0] + z, first_pos[1] + dy]

                    if self.is_possible_position(*second_pos) and self.is_empty_position(*second_pos):
                        pass
                    else:
                        continue

                    if dx != 0:
                        third_pos = (second_pos[0] + dx, second_pos[1] + z)
                    else:
                        third_pos = (second_pos[0] + z, second_pos[1] + dy)
                    result.append(third_pos)
        elif mc == MoveCode.Cart:
            directions = list(FourDirectionDelta)
            if is_inner_castle(x, y):
                directions += castle_routes_cross_only[x][y]
                print('castle', castle_routes_cross_only[x][y])

            for dx, dy in directions:
                castle_cross = dx != 0 and dy != 0

                for n in range(1, 9):
                    first_pos = x + dx * n, y + dy * n

                    if not self.is_possible_position(*first_pos):
                        break
                    if castle_cross:
                        if not is_inner_castle(*first_pos):
                            break

                    if self.is_empty_position(*first_pos):
                        result.append(first_pos)
                    else:
                        if self.is_enemy_position(tc, *first_pos):
                            result.append(first_pos)
                        break
        elif mc == MoveCode.Artillery:
            directions = list(FourDirectionDelta)
            if is_inner_castle(x, y):
                directions += castle_routes_cross_only[x][y]
                print('castle', castle_routes_cross_only[x][y])
            for dx, dy in directions:
                castle_cross = dx != 0 and dy != 0
                for n in range(1, 8):
                    fx = x + dx * n
                    fy = y + dy * n
                    first_pos = fx, fy
                    if not self.is_possible_position(*first_pos):
                        break
                    if castle_cross:
                        if not is_inner_castle(*first_pos):
                            break

                    if self.is_empty_position(*first_pos):
                        continue
                    elif MoveCode.from_act_code(self.board[fy][fx]) == MoveCode.Artillery:
                        break

                    for m in range(1, 8):
                        sx = fx + dx * m
                        sy = fy + dy * m
                        second_pos = sx, sy
                        if not self.is_possible_position(*second_pos):
                            break
                        if castle_cross:
                            if not is_inner_castle(*second_pos):
                                break

                        if self.is_empty_position(*second_pos):
                            result.append(second_pos)
                        else:
                            if MoveCode.from_act_code(self.board[sy][sx]) == MoveCode.Artillery:
                                pass
                            elif self.is_enemy_position(tc, *second_pos):
                                result.append(second_pos)
                            break
                    break
        elif mc == MoveCode.CastleMan:
            for dx, dy in castle_routes[x][y]:
                fx = x + dx
                fy = y + dy
                first_pos = (fx, fy)
                result.append(first_pos)

        return [
            pos for pos in result if
            self.is_possible_position(*pos) and (
                self.is_movable_or_edible(tc, *pos)
            )
        ]

    def get_actor(self, team_code: int) -> Tuple[int, int, int]:
        result = None
        n = 1
        for x, y, act_code in self.board:
            if act_code == ActorCode.Null:
                continue
            if team_code != TeamCode.from_act_code(act_code):
                continue
            if random.uniform(0, 1) <= 1 / n:
                result = x, y, act_code
                n += 1

        assert result is not None
        return result

    def tick(self):
        self.last_tick = datetime.datetime.now()

        while True:
            actor = self.get_actor(self.turn_own_team)

            pos_list = self.get_movable_positions(*actor)
            if len(pos_list) > 0:
                old_x, old_y, act_code = actor
                new_x, new_y = pos_list[random.randint(0, len(pos_list) - 1)]

                self.board[old_y][old_x] = ActorCode.Null
                move_duration = self.viewer.add_event(
                    Viewer.Event.Type.Move,
                    code1=act_code,
                    x1=old_x, y1=old_y,
                    x2=new_x, y2=new_y
                ).duration
                if self.board[new_y][new_x] != ActorCode.Null:
                    self.viewer.add_event(
                        Viewer.Event.Type.Delete,
                        code1=self.board[new_y][new_x],
                        code2=move_duration,
                        x1=new_x, y1=new_y
                    )

                self.board[new_y][new_x] = act_code
                print(actor)
                print([new_x, new_y])
                break
        self.release_turn()

    def release_turn(self):
        if self.turn_own_team == TeamCode.Red:
            self.turn_own_team = TeamCode.Green
        else:
            self.turn_own_team = TeamCode.Red
