import pygame
# from board_in_c import Board
from pygame import Surface
from pygame.event import Event

from decision_maker import DecisionMaker
from decision_maker.score_base import ScoreBasedDecisionMaker
from game_data import ActorCode, TeamCode
from game_viewer import Viewer


class Director:
    def __init__(self, surf: Surface):
        self.board = Board()
        self.viewer = Viewer(surf, board=self.board)
        self.north_decision_maker: DecisionMaker = ScoreBasedDecisionMaker()
        self.south_decision_maker: DecisionMaker = ScoreBasedDecisionMaker()
        self.turn_count = 1

    @property
    def current_decision_maker(self) -> DecisionMaker:
        if self.board.turn_own_team == TeamCode.North:
            return self.north_decision_maker
        else:
            return self.south_decision_maker

    def step(self):
        self.viewer.step()

        if self.board.is_ended_game is False:
            if self.viewer.events:
                pass
            elif self.current_decision_maker.is_not_busy and not self.current_decision_maker.is_decision_ready:
                self.current_decision_maker.request_decision(self.board)
            elif self.current_decision_maker.is_decision_ready:
                decision = self.current_decision_maker.get_decision()
                self.turn_count += 1

                move_duration = self.viewer.add_event(
                    Viewer.Event.Type.Move,
                    code1=decision.actor_code,
                    x1=decision.old_x,
                    y1=decision.old_y,
                    x2=decision.new_x,
                    y2=decision.new_y
                ).duration
                if self.board[decision.new_x, decision.new_y] != ActorCode.Null:
                    self.viewer.add_event(
                        Viewer.Event.Type.Delete,
                        duration=move_duration + 0.5,
                        code1=self.board[decision.new_x, decision.new_y],
                        x1=decision.new_x,
                        y1=decision.new_y,
                        code2=self.board[decision.old_x, decision.old_y],
                        x2=decision.old_x,
                        y2=decision.old_y,
                    )
                self.board = self.board.sub_board(decision)
                self.viewer.board = self.board
            else:
                self.current_decision_maker.step(viewer=self.viewer)

    def input(self, e: Event):
        self.current_decision_maker.input(e)
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_1:
                self.viewer.add_earth_quake(force=0.5, time=0)
            if e.key == pygame.K_2:
                self.viewer.add_earth_quake(force=1.85, time=1)
            if e.key == pygame.K_3:
                self.viewer.add_earth_quake(force=2.25, time=1)
