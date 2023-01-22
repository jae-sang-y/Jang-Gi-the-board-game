from typing import Optional, List

from pygame.event import Event

from decision_maker import DecisionMaker, Actor, Pos
from game_viewer import Viewer


class HumanDecisionMaker(DecisionMaker):
    def __init__(self):
        DecisionMaker.__init__(self)
        self.user_actor: Optional[Actor] = None
        self.user_actor_positions: List[Pos] = []

    def make_decision(self):
        pass

    def draw(self, viewer: Viewer):
        if self.user_actor:
            x, y, actor_code = self.user_actor
            viewer.draw_decisions(x, y, actor_code, self.user_actor_positions)

    def input(self, e: Event):
        if e.type == pygame.MOUSEBUTTONDOWN:
            click_nothing = True
            for x, y, actor_code in self.board:
                rect = pygame.Rect(
                    (x + 0.5) * block_width - (actor_width - block_width) / 2,
                    (y + 0.5) * block_width - (actor_width - block_width) / 2,
                    block_width,
                    block_width
                )
                cursor_x, cursor_y = e.pos
                if rect.collidepoint(cursor_x, cursor_y):
                    if actor_code != ActorCode.Null:
                        click_nothing = False
                    if actor_code == ActorCode.Null or TeamCode.from_actor_code(actor_code) != self.user_team:
                        if self.user_actor is not None:
                            for new_x, new_y in self.user_actor_positions:
                                if new_x == x and new_y == y:
                                    old_x, old_y, actor_code = self.user_actor
                                    self.board[old_y][old_x] = ActorCode.Null
                                    move_duration = self.viewer.add_event(
                                        Viewer.Event.Type.Move,
                                        code1=actor_code,
                                        x1=old_x, y1=old_y,
                                        x2=new_x, y2=new_y
                                    ).duration
                                    if self.board[new_y][new_x] != ActorCode.Null:
                                        self.viewer.add_event(
                                            Viewer.Event.Type.Delete,
                                            code1=self.board[new_y][new_x],
                                            code2=move_duration,
                                            x1=new_x, y1=new_y
                                        )

                                    self.board[new_y][new_x] = actor_code
                                    self.release_turn()
                                    self.user_actor = None
                                    self.user_actor_positions = []
                                    break

                    else:
                        self.user_actor = x, y, actor_code
                        self.user_actor_positions = self.board.get_movable_positions(x, y, actor_code)
                    break
            if click_nothing:
                self.user_actor = None
                self.user_actor_positions = []
