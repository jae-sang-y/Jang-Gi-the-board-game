import math
from threading import Thread
from typing import Tuple, Optional, List

import pygame.event

from decision_maker.minimax import Minimax
from python_client.client_storage import ClientStorage
from python_client.graphics_manager import GraphicsManager


class InputManager:

    def __init__(self, client_storage: ClientStorage):
        self.client_storage = client_storage
        self.last_clicked_pos: Optional[Tuple[int, int]] = None
        self.move_cases_of_last_clicked_actor: List[Tuple[int, int]] = list()

    def action_move(self, grid_pos: Tuple[int, int]):
        board = self.client_storage.board
        board.move_actor(self.last_clicked_pos, grid_pos)
        trd = Thread(daemon=True, target=self.ai_move, args=())
        trd.start()

    def ai_move(self):
        # time.sleep(0.2)
        board = self.client_storage.board
        print('hi')
        minimax_level = 2
        result = Minimax.get_best_move(board, minimax_level)
        board.move_actor(result[0:2], result[2:4])
        grp_mgr: GraphicsManager = self.client_storage.get_component(GraphicsManager)
        grp_mgr.arrow = result

    def click_grid(self, grid_pos: Tuple[int, int]):
        grp_mgr: GraphicsManager = self.client_storage.get_component(GraphicsManager)

        board = self.client_storage.board
        actor = board.get_actor(grid_pos)
        if grid_pos in self.move_cases_of_last_clicked_actor:
            self.action_move(grid_pos)
            grp_mgr.arrow = (self.last_clicked_pos[0], self.last_clicked_pos[1], grid_pos[0], grid_pos[1])
            grp_mgr.highlighted_blocks.clear()
            self.move_cases_of_last_clicked_actor.clear()
            self.last_clicked_pos = None
        elif grid_pos == self.last_clicked_pos:
            grp_mgr.highlighted_blocks.clear()
            self.move_cases_of_last_clicked_actor.clear()
            self.last_clicked_pos = None
        else:
            if actor is None:
                grp_mgr.highlighted_blocks.clear()
                self.move_cases_of_last_clicked_actor.clear()
                self.last_clicked_pos = None
                return
            grp_mgr.highlighted_blocks = [
                {'pos': grid_pos, 'color': (128, 128, 128, 128)}
            ]
            move_cases = actor.move_cases(board=board, pos=grid_pos)
            for new_pos in move_cases:
                other = board.get_actor(new_pos)
                grp_mgr.highlighted_blocks.append(
                    {'pos': new_pos, 'color': (255, 0, 0, 128) if other else (0, 255, 0, 128)}
                )
            self.move_cases_of_last_clicked_actor = move_cases
            self.last_clicked_pos = grid_pos

    def process_event(self, e: pygame.event.Event):
        if e.type == pygame.MOUSEBUTTONDOWN:
            grp_mgr: GraphicsManager = self.client_storage.get_component(GraphicsManager)
            screen_pos = e.pos
            screen_to_grid = lambda x: math.floor(
                (x - grp_mgr.border_margin + grp_mgr.space_between_lines / 2) / grp_mgr.space_between_lines)
            self.click_grid(
                (
                    screen_to_grid(screen_pos[0]),
                    screen_to_grid(screen_pos[1]),
                )
            )
