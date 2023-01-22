from typing import List, Tuple

from dataset.actor import Actor
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
