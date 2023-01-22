import itertools
from dataclasses import dataclass
from typing import Tuple, List

from dataset.actor_type import ActorType


@dataclass
class Actor:
    actor_type: ActorType
    is_red: bool

    def get_actor_code(self) -> int:
        return self.actor_type.value + (
            0 if self.is_red is True else 7
        )

    @classmethod
    def get_four_directions(cls):
        return [
            (0, +1), (0, -1),
            (+1, 0), (-1, 0),
        ]

    @classmethod
    def get_crossing_directions(cls):
        return [
            (+1, +1), (-1, -1),
            (+1, -1), (-1, +1),
        ]

    def move_cases(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        if self.actor_type == ActorType.KING:
            return self.move_cases_as_king_or_duke(board=board, pos=pos)

        if self.actor_type == ActorType.KART:
            return self.move_cases_as_kart(board=board, pos=pos)

        if self.actor_type == ActorType.HORSE:
            return self.move_cases_as_horse(board=board, pos=pos)

        if self.actor_type == ActorType.ELEPHANT:
            return self.move_cases_as_elephant(board=board, pos=pos)

        if self.actor_type == ActorType.CANNON:
            return self.move_cases_as_cannon(board=board, pos=pos)

        if self.actor_type == ActorType.DUKE:
            return self.move_cases_as_king_or_duke(board=board, pos=pos)

        if self.actor_type == ActorType.ARMY:
            return self.move_cases_as_army(board=board, pos=pos)

        return []

    def move_cases_as_king_or_duke(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        result = list()
        move_directions = self.get_four_directions()
        if board.is_on_ears_of_palaces(pos) or board.is_on_center_of_palaces(pos):
            move_directions += self.get_crossing_directions()

        for dx, dy in move_directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if board.is_on_palace(new_pos):
                other: Actor = board.get_actor(new_pos)
                if other is None or other.is_red != self.is_red:
                    result.append(new_pos)

        return result

    def move_cases_as_kart(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        result = list()

        for is_crossing, dx, dy in itertools.chain(
                map(lambda tup: (False, *tup), self.get_four_directions()),
                map(lambda tup: (True, *tup), self.get_crossing_directions())
        ):
            if is_crossing and not (board.is_on_ears_of_palaces(pos) or board.is_on_center_of_palaces(pos)):
                continue
            for c in range(1, 9):
                new_pos = (pos[0] + dx * c, pos[1] + dy * c)
                if board.is_pos_in_board(new_pos) is False:
                    break
                if is_crossing and board.is_on_palace(new_pos) is False:
                    break
                other = board.get_actor(new_pos)
                if other is not None:
                    if other.is_red != self.is_red:
                        result.append(new_pos)
                    break
                result.append(new_pos)
        return result

    def move_cases_as_horse(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        result = list()
        for dx_1, dy_1 in self.get_four_directions():
            road_1 = (pos[0] + dx_1, pos[1] + dy_1)
            if board.is_pos_in_board(road_1) is False:
                continue
            other = board.get_actor(road_1)
            if other is not None:
                continue
            if dx_1 == 0:
                tilted_direction = [
                    (-1, 0), (+1, 0),
                ]
            else:
                tilted_direction = [
                    (0, -1), (0, +1),
                ]

            for dx_2, dy_2 in tilted_direction:
                final = (road_1[0] + dx_1 + dx_2, road_1[1] + dy_1 + dy_2)
                if board.is_pos_in_board(final) is False:
                    break
                other = board.get_actor(final)
                if other is None or other.is_red != self.is_red:
                    result.append(final)

        return result

    def move_cases_as_elephant(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        result = list()
        for dx_1, dy_1 in self.get_four_directions():
            road_1 = (pos[0] + dx_1, pos[1] + dy_1)
            if board.is_pos_in_board(road_1) is False:
                continue
            other = board.get_actor(road_1)
            if other is not None:
                continue
            if dx_1 == 0:
                tilted_direction = [
                    (-1, 0), (+1, 0),
                ]
            else:
                tilted_direction = [
                    (0, -1), (0, +1),
                ]

            for dx_2, dy_2 in tilted_direction:
                road_2 = (road_1[0] + dx_1 + dx_2, road_1[1] + dy_1 + dy_2)
                if board.is_pos_in_board(road_2) is False:
                    continue
                other = board.get_actor(road_2)
                if other is not None:
                    continue

                final = (road_2[0] + dx_1 + dx_2, road_2[1] + dy_1 + dy_2)
                if board.is_pos_in_board(final) is False:
                    break
                other = board.get_actor(final)
                if other is None or other.is_red != self.is_red:
                    result.append(final)

        return result

    def move_cases_as_cannon(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        result = list()

        for is_crossing, dx, dy in itertools.chain(
                map(lambda tup: (False, *tup), self.get_four_directions()),
                map(lambda tup: (True, *tup), self.get_crossing_directions())
        ):
            meet_non_cannon = False
            if is_crossing and not (board.is_on_ears_of_palaces(pos) or board.is_on_center_of_palaces(pos)):
                continue
            for c in range(1, 9):
                new_pos = (pos[0] + dx * c, pos[1] + dy * c)
                if board.is_pos_in_board(new_pos) is False:
                    break
                if is_crossing and board.is_on_palace(new_pos) is False:
                    break
                other: Actor = board.get_actor(new_pos)
                if meet_non_cannon:
                    if other is not None:
                        if other.is_red != self.is_red and other.actor_type != ActorType.CANNON:
                            result.append(new_pos)
                        break
                    else:
                        result.append(new_pos)
                else:
                    if other is not None:
                        if other.actor_type != ActorType.CANNON:
                            meet_non_cannon = True
                        else:
                            break
        return result

    def move_cases_as_army(self, board: 'Board', pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        result = list()
        if self.is_red:
            dy = -1
        else:
            dy = +1

        new_pos = (pos[0], pos[1] + dy)
        if board.is_pos_in_board(new_pos):
            other: Actor = board.get_actor(new_pos)
            if other is None or other.is_red != self.is_red:
                result.append(new_pos)

        for dx in (-1, +1):
            new_pos = (pos[0] + dx, pos[1])
            if board.is_pos_in_board(new_pos):
                other: Actor = board.get_actor(new_pos)
                if other is None or other.is_red != self.is_red:
                    result.append(new_pos)
        return result
