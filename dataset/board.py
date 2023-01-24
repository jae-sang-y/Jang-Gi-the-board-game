from typing import Optional, List, Tuple, Iterable

from jangi_extension import Actor


class Board:
    def __init__(self):
        self.data: List[List[Optional[Actor]]] = [
            [None for _ in range(10)] for _ in range(9)
        ]

    @classmethod
    def is_pos_in_board(cls, pos: Tuple[int, int]) -> bool:
        if 0 <= pos[0] < 9 and 0 <= pos[1] < 10:
            return True
        else:
            return False

    @classmethod
    def is_on_palace(cls, pos: Tuple[int, int]) -> bool:
        if (3 <= pos[0] <= 5 and 0 <= pos[1] <= 2) or \
                (3 <= pos[0] <= 5 and 7 <= pos[1] <= 9):
            return True
        else:
            return False

    @classmethod
    def is_on_ears_of_palaces(cls, pos: Tuple[int, int]) -> bool:
        if (pos[0] in (3, 5) and pos[1] in (0, 2)) or \
                (pos[0] in (3, 5) and pos[1] in (7, 9)):
            return True
        else:
            return False

    @classmethod
    def is_on_center_of_palaces(cls, pos: Tuple[int, int]) -> bool:
        if pos == (4, 1) or pos == (4, 8):
            return True
        else:
            return False

    def get_actor(self, pos: Tuple[int, int]) -> Optional[Actor]:
        return self.data[pos[0]][pos[1]]

    def move_actor(self, src: Tuple[int, int], dst: Tuple[int, int]):
        self.data[dst[0]][dst[1]] = self.data[src[0]][src[1]]
        self.data[src[0]][src[1]] = None

    def foreach_actors(self) -> Iterable[Tuple[Actor, int, int]]:
        for x in range(9):
            for y in range(10):
                actor = self.data[x][y]
                if actor is None:
                    continue
                yield actor, x, y
