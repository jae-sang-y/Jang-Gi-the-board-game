from threading import Thread
from typing import Optional, List, Tuple, final, NoReturn

from pygame.event import Event

from game_data import Board, ActorCode, TeamCode
from game_viewer import Viewer

Pos = Tuple[int, int]
Actor = Tuple[int, int, int]


class Decision:
    def __init__(self, *, old_x: int, old_y: int, act_code: int, new_x: int, new_y: int):
        self.old_x = old_x
        self.old_y = old_y
        self.act_code = act_code
        self.new_x = new_x
        self.new_y = new_y

    def __repr__(self) -> str:
        return str(self)

    def __str__(self):
        return '<Decision={:<14s} ({:> 2d}, {:> 2d}) -> ({:> 2d}, {:> 2d})'.format(
            ActorCode.get_name(self.act_code),
            self.old_x,
            self.old_y,
            self.new_x,
            self.new_y,
        )


class DecisionMaker:
    def __init__(self):
        self.board: Optional[Board] = None
        self.prefer_team: Optional[int] = None
        self.decision_queue: List[Decision] = []
        self.decision: Optional[Decision] = None
        self.thread: Optional[Thread] = None

    @final
    def get_actors(self) -> List[Actor]:
        result = []
        for x, y, act_code in self.board:
            if act_code == ActorCode.Null:
                continue
            if TeamCode.from_act_code(act_code) != self.board.turn_own_team:
                continue
            result.append((x, y, act_code))
        return result

    @final
    @property
    def is_decision_ready(self) -> bool:
        return self.decision is not None

    @final
    def get_decision(self) -> Optional[Decision]:
        decision, self.decision = self.decision, None
        return decision

    @final
    @property
    def is_busy(self) -> bool:
        return self.thread is not None

    @final
    @property
    def is_not_busy(self) -> bool:
        return not self.is_busy

    @final
    def request_decision(self, board: Board) -> NoReturn:
        self.board = board
        assert self.decision is None
        assert self.decision_queue == []
        self.decision_queue = []
        self.thread = Thread(target=self.make_decision, args=(self.decision_queue,))
        self.thread.name = self.thread.name.replace('Thread', type(self).__name__)
        self.thread.start()

    def input(self, e: Event) -> NoReturn:
        pass

    def step(self, viewer: Viewer) -> NoReturn:
        if self.thread is not None:
            if not self.thread.is_alive():
                assert len(self.decision_queue) == 1, self.decision_queue
                self.decision = self.decision_queue[0]
                self.decision_queue = []
                self.thread = None

    def make_decision(self, decision_queue: List[Decision]) -> NoReturn:
        raise NotImplemented()
