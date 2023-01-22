from dataset.actor import Actor
from dataset.actor_type import ActorType
from dataset.board import Board


class BoardFactory:
    @classmethod
    def get_classic_start(cls) -> Board:
        upside = False
        downside = True
        board = Board()
        for x in [0, 2, 4, 6, 8]:
            board.data[x][3] = Actor(actor_type=ActorType.ARMY, is_red=upside)
            board.data[x][6] = Actor(actor_type=ActorType.ARMY, is_red=downside)
        for x in [1, 7]:
            board.data[x][2] = Actor(actor_type=ActorType.CANNON, is_red=upside)
            board.data[x][7] = Actor(actor_type=ActorType.CANNON, is_red=downside)
        for y, is_red in [
            (0, upside),
            (9, downside),
        ]:
            board.data[0][y] = Actor(actor_type=ActorType.KART, is_red=is_red)
            board.data[1][y] = Actor(actor_type=ActorType.HORSE, is_red=is_red)
            board.data[2][y] = Actor(actor_type=ActorType.ELEPHANT, is_red=is_red)

            board.data[3][y] = Actor(actor_type=ActorType.DUKE, is_red=is_red)
            board.data[5][y] = Actor(actor_type=ActorType.DUKE, is_red=is_red)

            board.data[6][y] = Actor(actor_type=ActorType.HORSE, is_red=is_red)
            board.data[7][y] = Actor(actor_type=ActorType.ELEPHANT, is_red=is_red)
            board.data[8][y] = Actor(actor_type=ActorType.KART, is_red=is_red)

        board.data[4][1] = Actor(actor_type=ActorType.KING, is_red=upside)
        board.data[4][8] = Actor(actor_type=ActorType.KING, is_red=downside)
        return board
