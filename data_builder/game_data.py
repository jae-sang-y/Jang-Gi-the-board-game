from typing import Tuple, List, Dict

screen_width = 800
block_width = screen_width // 10


class ActorCode:
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


class TeamCode:
    Red = 1
    Green = 2

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
            return cls.Red
        elif act_code in {
            ac.SouthKing,
            ac.SouthCart,
            ac.SouthHorse,
            ac.SouthElephant,
            ac.SouthArtillery,
            ac.SouthBishop,
            ac.SouthFootman,
        }:
            return cls.Green
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


class Board:
    def __init__(self):
        XX = ActorCode.Null
        NC = ActorCode.NorthCart
        NH = ActorCode.NorthHorse
        NE = ActorCode.NorthElephant
        NB = ActorCode.NorthBishop
        NA = ActorCode.NorthArtillery
        NK = ActorCode.NorthKing
        NF = ActorCode.NorthFootman
        SC = ActorCode.SouthCart
        SH = ActorCode.SouthHorse
        SE = ActorCode.SouthElephant
        SB = ActorCode.SouthBishop
        SA = ActorCode.SouthArtillery
        SK = ActorCode.SouthKing
        SF = ActorCode.SouthFootman
        self.board: List[List[int]] = [
            [NC, NH, NE, NB, XX, NB, NH, NE, NC],
            [XX, XX, XX, XX, NK, XX, XX, XX, XX],
            [XX, NA, XX, XX, XX, XX, XX, NA, XX],
            [NF, XX, NF, XX, NF, XX, NF, XX, NF],
            [XX for _ in range(9)],
            [SF, XX, SF, XX, SF, XX, SF, XX, SF],
            [XX, SA, XX, XX, XX, XX, XX, SA, XX],
            [XX, XX, XX, XX, SK, XX, XX, XX, XX],
            [SC, SH, SE, SB, XX, SB, SH, SE, SC],
        ]

    def __iter__(self) -> Tuple[int, int, int]:
        for y in range(9):
            for x in range(9):
                yield x, y, self.board[y][x]

    def __getitem__(self, y) -> List[int]:
        return self.board[y]


board = Board()

FourDirectionDelta = [
    (0, +1),
    (0, -1),
    (+1, 0),
    (-1, 0),
]

castle_routes: Dict[int, Dict[int, List[Tuple[int, int]]]] = {
    x: {y: [] for y in {0, 1, 2, 6, 7, 8}} for x in {3, 4, 5}
}
for y in {0, 1, 2, 6, 7, 8}:
    for x in {3, 4, 5}:
        if 3 <= x < 5:
            castle_routes[x][y].append((+1, 0))
        if 3 < x <= 5:
            castle_routes[x][y].append((-1, 0))
        if 0 <= y < 2 or 6 <= y < 8:
            castle_routes[x][y].append((0, +1))
        if 0 < y <= 2 or 6 < y <= 8:
            castle_routes[x][y].append((0, -1))

        if (x == 4 and y == 1) or (x == 4 and y == 7):
            for dx, dy in (
                    (-1, +1),
                    (-1, -1),
                    (+1, +1),
                    (+1, -1),
            ):
                castle_routes[x][y].append((+dx, +dy))
                castle_routes[x + dx][y + dy].append((-dx, -dx))

castle_routes_cross_only = {
    a_k: {b_k: [(dx, dy) for dx, dy in b_v if dx != 0 and dy != 0] for b_k, b_v in a_v.items()} for a_k, a_v in
    castle_routes.items()
}


def is_inner_castle(x: int, y: int) -> bool:
    return y in {0, 1, 2, 6, 7, 8} and x in {3, 4, 5}
