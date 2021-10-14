from abc import ABC
from typing import Tuple, List, Dict

screen_width = 800
block_width = screen_width // 10


class EnumClass:
    def __init__(self):
        raise NotImplementedError('EnumClass may not create instance.')


class ActorCode(EnumClass, ABC):
    Null = 0
    NorthKing = 1
    NorthCart = 2
    NorthHorse = 3
    NorthElephant = 4
    NorthArtillery = 5
    NorthBishop = 6
    NorthFootman = 7
    SouthKing = 8
    SouthCart = 9
    SouthHorse = 10
    SouthElephant = 11
    SouthArtillery = 12
    SouthBishop = 13
    SouthFootman = 14

    @classmethod
    def get_name(cls, act_code: int):
        attrs = set(dir(ActorCode)) - set(dir(EnumClass))
        for attr_name in attrs:
            if getattr(cls, attr_name) == act_code:
                return attr_name
        raise ValueError(act_code)


class TeamCode:
    North = 1
    South = 2

    @classmethod
    def from_act_code(cls, act_code: int):
        ac = ActorCode
        if act_code in {
            ac.NorthKing,
            ac.NorthCart,
            ac.NorthHorse,
            ac.NorthElephant,
            ac.NorthArtillery,
            ac.NorthBishop,
            ac.NorthFootman,
        }:
            return cls.North
        elif act_code in {
            ac.SouthKing,
            ac.SouthCart,
            ac.SouthHorse,
            ac.SouthElephant,
            ac.SouthArtillery,
            ac.SouthBishop,
            ac.SouthFootman,
        }:
            return cls.South
        else:
            raise ValueError(act_code)


class MoveCode:
    CastleMan = 1
    Cart = 2
    Horse = 3
    Elephant = 4
    Artillery = 5
    Footman = 7

    @classmethod
    def from_act_code(cls, act_code: int):
        ac = ActorCode
        if act_code in {ac.NorthKing, ac.SouthKing, ac.NorthBishop, ac.SouthBishop}:
            return cls.CastleMan
        elif act_code in {ac.NorthCart, ac.SouthCart}:
            return cls.Cart
        elif act_code in {ac.NorthHorse, ac.SouthHorse}:
            return cls.Horse
        elif act_code in {ac.NorthElephant, ac.SouthElephant}:
            return cls.Elephant
        elif act_code in {ac.NorthArtillery, ac.SouthArtillery}:
            return cls.Artillery
        elif act_code in {ac.NorthFootman, ac.SouthFootman}:
            return cls.Footman
        else:
            raise ValueError(act_code)


def get_castle_routes() -> Dict[int, Dict[int, List[Tuple[int, int]]]]:
    castle_routes = {
        x: {y: [] for y in {0, 1, 2, 6, 7, 8}} for x in {3, 4, 5}
    }
    for y in {0, 1, 2, 6, 7, 8}:
        for x in {3, 4, 5}:
            if 3 <= x < 5:
                castle_routes[x][y].append((+1, 0))
            if 3 < x <= 5:
                castle_routes[x][y].append((-1, 0))
            if (0 <= y < 2) or (6 <= y < 8):
                castle_routes[x][y].append((0, +1))
            if (0 < y <= 2) or (6 < y <= 8):
                castle_routes[x][y].append((0, -1))

            if (x == 4 and y == 1) or (x == 4 and y == 7):
                for dx, dy in (
                        (-1, +1),
                        (-1, -1),
                        (+1, +1),
                        (+1, -1),
                ):
                    castle_routes[x][y].append((+dx, +dy))
                    castle_routes[x + dx][y + dy].append((-dx, -dy))
    return castle_routes


class Board:
    FourDirectionDelta = [
        (0, +1),
        (0, -1),
        (+1, 0),
        (-1, 0),
    ]
    CastleRoutes = get_castle_routes()
    CastleRoutesCrossOnly = {
        a_k: {
            b_k: [
                (dx, dy)
                for dx, dy in b_v if dx != 0 and dy != 0
            ]
            for b_k, b_v in a_v.items()
        }
        for a_k, a_v in CastleRoutes.items()
    }

    def __init__(self):
        initial_of_act_code = {
            'XX': ActorCode.Null,
            'NC': ActorCode.NorthCart,
            'NH': ActorCode.NorthHorse,
            'NE': ActorCode.NorthElephant,
            'NB': ActorCode.NorthBishop,
            'NA': ActorCode.NorthArtillery,
            'NK': ActorCode.NorthKing,
            'NF': ActorCode.NorthFootman,
            'SC': ActorCode.SouthCart,
            'SH': ActorCode.SouthHorse,
            'SE': ActorCode.SouthElephant,
            'SB': ActorCode.SouthBishop,
            'SA': ActorCode.SouthArtillery,
            'SK': ActorCode.SouthKing,
            'SF': ActorCode.SouthFootman,
        }
        map_code = \
            'NC,NH,NE,NB,XX,NB,NH,NE,NC_' \
            'XX,XX,XX,XX,NK,XX,XX,XX,XX_' \
            'XX,NA,XX,XX,XX,XX,XX,NA,XX_' \
            'NF,XX,NF,XX,NF,XX,NF,XX,NF_' \
            'XX,XX,XX,XX,XX,XX,XX,XX,XX_' \
            'SF,XX,SF,XX,SF,XX,SF,XX,SF_' \
            'XX,SA,XX,XX,XX,XX,XX,SA,XX_' \
            'XX,XX,XX,XX,SK,XX,XX,XX,XX_' \
            'SC,SH,SE,SB,XX,SB,SH,SE,SC_'

        self.board: List[List[int]] = []
        for map_row in map_code.split('_'):
            if map_row:
                self.board.append(
                    [initial_of_act_code[initial] for initial in map_row.split(',') if initial]
                )

        self.turn_own_team = TeamCode.North

    def __iter__(self) -> Tuple[int, int, int]:
        for y in range(9):
            for x in range(9):
                yield x, y, self.board[y][x]

    def __getitem__(self, y) -> List[int]:
        return self.board[y]

    @staticmethod
    def is_inner_castle(x: int, y: int) -> bool:
        return y in {0, 1, 2, 6, 7, 8} and x in {3, 4, 5}

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
            if tc == TeamCode.North:
                result.append((x, y + 1))
            elif tc == TeamCode.South:
                result.append((x, y - 1))
            if self.is_inner_castle(x, y):
                for dx, dy in self.CastleRoutesCrossOnly[x][y]:
                    if dy == (+1 if tc == TeamCode.North else -1):
                        result.append((x + dx, y + dy))
        elif mc == MoveCode.Horse:
            for dx, dy in self.FourDirectionDelta:
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
            for dx, dy in self.FourDirectionDelta:
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
            directions = list(self.FourDirectionDelta)
            if self.is_inner_castle(x, y):
                directions += self.CastleRoutesCrossOnly[x][y]

            for dx, dy in directions:
                castle_cross = dx != 0 and dy != 0

                for n in range(1, 9):
                    first_pos = x + dx * n, y + dy * n

                    if not self.is_possible_position(*first_pos):
                        break
                    if castle_cross:
                        if not self.is_inner_castle(*first_pos):
                            break

                    if self.is_empty_position(*first_pos):
                        result.append(first_pos)
                    else:
                        if self.is_enemy_position(tc, *first_pos):
                            result.append(first_pos)
                        break
        elif mc == MoveCode.Artillery:
            directions = list(self.FourDirectionDelta)
            if self.is_inner_castle(x, y):
                directions += self.CastleRoutesCrossOnly[x][y]
            for dx, dy in directions:
                castle_cross = dx != 0 and dy != 0
                for n in range(1, 8):
                    fx = x + dx * n
                    fy = y + dy * n
                    first_pos = fx, fy
                    if not self.is_possible_position(*first_pos):
                        break
                    if castle_cross:
                        if not self.is_inner_castle(*first_pos):
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
                            if not self.is_inner_castle(*second_pos):
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
            for dx, dy in self.CastleRoutes[x][y]:
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

    def is_ended(self: 'Board') -> bool:
        actor_count = {
            TeamCode.North: 0,
            TeamCode.South: 0,
        }

        for x, y, act_code in self:
            if act_code == ActorCode.Null:
                continue
            actor_count[
                TeamCode.from_act_code(act_code)
            ] += 1
        for team_code in {TeamCode.North, TeamCode.South}:
            if actor_count[team_code] == 0:
                return True
        return False
