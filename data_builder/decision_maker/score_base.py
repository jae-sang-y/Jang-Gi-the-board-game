import math
import random
from typing import List, NoReturn

from board_in_c import Board

from decision_maker import DecisionMaker, Decision
from game_data import TeamCode, ActorCode, MoveCode, Pos


class ScoringChicken:
    @classmethod
    def score_from_actor_code(cls, actor_code: int) -> float:
        if actor_code == ActorCode.Null:
            return 0
        if actor_code in (ActorCode.NorthKing, ActorCode.SouthKing):
            return 1e5
        return {
            MoveCode.Cart: 10,
            MoveCode.CastleMan: 3,
            MoveCode.Artillery: 9,
            MoveCode.Horse: 7,
            MoveCode.Elephant: 2,
            MoveCode.Footman: 1
        }[MoveCode.from_actor_code(actor_code)]

    @classmethod
    def score_direct(cls, board: Board) -> float:
        score = 0
        for actor in board:
            old_x, old_y, actor_code = actor
            if actor_code == ActorCode.Null:
                continue

            team_code = TeamCode.from_actor_code(actor_code)
            if team_code == board.turn_own_team:
                mult = 1
            else:
                mult = -1e-2

            for pos in board.get_movable_positions(*actor):
                prey = board.at(*pos)
                if prey != ActorCode.Null:
                    score += cls.score_from_actor_code(prey) * mult

        return score

    @classmethod
    def score_indirect(cls, board: Board, depth: int) -> float:
        if depth <= 0:
            return cls.score_direct(board)
        score = 0
        count = 0

        for actor in board:
            old_x, old_y, actor_code = actor
            if actor_code == ActorCode.Null:
                continue

            team_code = TeamCode.from_actor_code(actor_code)
            if team_code != board.turn_own_team:
                continue

            for new_x, new_y in board.get_movable_positions(*actor):
                sub_board = board.sub_board(Decision(
                    old_x=old_x,
                    old_y=old_y,
                    actor_code=actor_code,
                    new_x=new_x,
                    new_y=new_y
                ))
                score += cls.score_indirect(sub_board, depth - 1)
                count += 1

        return score / count

    @classmethod
    def they_may_be_killed(cls, board: Board, target_x: int, target_y: int) -> bool:
        for actor in board:
            old_x, old_y, actor_code = actor
            if actor_code == ActorCode.Null:
                continue

            team_code = TeamCode.from_actor_code(actor_code)
            if team_code != board.turn_own_team:
                continue

            for new_x, new_y in board.get_movable_positions(*actor):
                if new_x == target_x and new_y == target_y:
                    return True
        return False

    @classmethod
    def score_by_battle(cls, board: Board, old_pos: Pos, new_pos: Pos) -> float:
        they_may_be_killed = cls.they_may_be_killed(
            board.sub_board(Decision(
                old_x=old_pos[0],
                old_y=old_pos[1],
                actor_code=board.at(*old_pos),
                new_x=new_pos[0],
                new_y=new_pos[1])
            ),
            *new_pos
        )

        if they_may_be_killed:
            need_decrease_value = cls.score_from_actor_code(board.at(*old_pos))
        else:
            need_decrease_value = 0
        need_increase_value = cls.score_from_actor_code(board.at(*new_pos))
        if MoveCode.from_actor_code(board.at(*old_pos)) != MoveCode.CastleMan:
            target_pos = 4.5
            if board.turn_own_team == TeamCode.North:
                target_pos = 9
            else:
                target_pos = 1
            need_increase_value -= 1e-2 * (
                    abs(target_pos - new_pos[1]) - abs(target_pos - old_pos[1])
            )
        return need_increase_value - need_decrease_value


class ScoreBasedDecisionMaker(DecisionMaker):
    def __init__(self):
        DecisionMaker.__init__(self)

    def make_decision(self, decision_queue: List[Decision]) -> NoReturn:
        final_decision = None
        prev_score = - math.inf
        prev_count = 1

        for actor in self.get_actors():
            old_x, old_y, actor_code = actor
            pos_list = self.board.get_movable_positions(*actor)

            score_by_default = 0
            if ScoringChicken.they_may_be_killed(self.board.sub_board(
                    Decision(old_x=old_x, old_y=old_y, actor_code=actor_code, new_x=old_x, new_y=old_y)
            ), target_x=old_x, target_y=old_y):
                score_by_default -= ScoringChicken.score_from_actor_code(actor_code)

            for new_pos in pos_list:
                new_x, new_y = new_pos
                # score = ScoringChicken.score_by_battle(self.board, (old_x, old_y), new_pos)

                decision = Decision(old_x=old_x, old_y=old_y, actor_code=actor_code, new_x=new_x, new_y=new_y)
                score = -1 * ScoringChicken.score_indirect(self.board.sub_board(decision), depth=0)
                score -= score_by_default

                if MoveCode.from_actor_code(actor_code) != MoveCode.CastleMan:
                    if self.board.turn_own_team == TeamCode.North:
                        target_pos = 7
                    else:
                        target_pos = 2
                    need_decrease_value = 1e-1 * (
                            abs(target_pos - new_y) - abs(target_pos - old_y)
                    )
                    score -= need_decrease_value

                if score > prev_score and random.uniform(0, 1) <= 1 / prev_count:
                    prev_score = score
                    final_decision = decision
                    prev_count = 1
                elif score >= prev_score:
                    prev_count += 1

        if final_decision:
            print(prev_score, )
            decision_queue.append(final_decision)
