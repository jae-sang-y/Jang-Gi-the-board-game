from dataset.actor_type import ActorType
from dataset.board import Board


class Evaluator:
    @classmethod
    def basic(cls, board: Board) -> int:
        result: int = 0
        # If the board seems like the red is win. it returns positive
        # If not, it returns negative.
        # Bigger number means bolder signal.
        for row in board.data:
            for actor in row:
                if actor is None:
                    continue
                value: int = 0
                if actor.actor_type == ActorType.KING:
                    value = 10000
                elif actor.actor_type == ActorType.KART:
                    value = 13
                elif actor.actor_type == ActorType.CANNON:
                    value = 7
                elif actor.actor_type == ActorType.HORSE:
                    value = 5
                elif actor.actor_type == ActorType.ELEPHANT:
                    value = 3
                elif actor.actor_type == ActorType.DUKE:
                    value = 3
                elif actor.actor_type == ActorType.ARMY:
                    value = 2
                if actor.is_red:
                    result += value
                else:
                    result -= value
        return result
