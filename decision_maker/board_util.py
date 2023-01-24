from typing import List, Tuple, Iterable

from jangi_extension import Actor
from dataset.board import Board


class BoardUtil:
    @classmethod
    def get_all_moves(cls, board: Board) -> List[Tuple[int, int, int, int]]:
        result = []
        for actor, x1, y1 in board.foreach_actors():
            move_cases = actor.move_cases(board=board, pos=(x1, y1))
            for x2, y2 in move_cases:
                result.append((x1, y1, x2, y2))
        return result

    @classmethod
    def duplicate_board(cls, old_board: Board) -> Board:
        new_board = Board()
        for actor, x, y in old_board.foreach_actors():
            print(actor.actor_type, actor.is_red)
            new_board.data[x][y] = \
                Actor(
                    actor_type=actor.actor_type,
                    is_red=actor.is_red
                )
        return new_board

    @classmethod
    def create_adjusted_board(cls, old_board: Board, move: Tuple[int, int, int, int]) -> Board:
        new_board = Board()
        for actor, x, y in old_board.foreach_actors():
            new_board.data[x][y] = \
                Actor(
                    actor_type=actor.actor_type,
                    is_red=actor.is_red
                )
        new_board.move_actor(move[0:2], move[2:4])
        return new_board

    @classmethod
    def dumps_board(cls, board: Board) -> bytes:
        result = bytes()
        for x in range(9):
            for y in range(10):
                actor = board.data[x][y]
                if actor is None:
                    result += b'\0'
                else:
                    result += actor.to_actor_code().to_bytes(1, 'big')
        assert len(result) == 90, len(result)
        return result

    @classmethod
    def loads_board(cls, raw_data: bytes) -> Board:
        raw_data = bytearray(raw_data)
        itr: Iterable[int] = iter(raw_data)
        board = Board()
        for y in range(10):
            for x in range(9):
                actor_code = next(itr)
                if actor_code not in (0, 7):
                    board.data[x][y] = Actor.from_actor_code(actor_code)
        return board

    @classmethod
    def pos_to_name(cls, x: int, y: int) -> str:
        if x == 0:
            x_name = '좌변'
        elif x == 8:
            x_name = '우변'
        elif x == 4:
            x_name = '중앙'
        elif x == 3:
            x_name = '좌익'
        elif x == 5:
            x_name = '우익'
        elif x == 2:
            x_name = '좌문'
        elif x == 6:
            x_name = '우문'
        elif x == 1:
            x_name = '좌진'
        elif x == 7:
            x_name = '우진'
        else:
            x_name = f'{x + 1}선'
        y_name = f'{y + 1}선'
        return f'{x_name} {y_name}'
