import cProfile
import os
import pickle
import pstats
import subprocess
import time
from pathlib import Path
from typing import Callable, Tuple, Optional

from dataset.board import Board
from decision_maker.board_util import BoardUtil
from evaluator.evaluator import Evaluator


class Minimax:
    working_temp_path = Path('working_temp') / 'minimax'

    @classmethod
    def negative_max(cls, evaluate: Callable[[Board], float], board: Board, depth: int) -> float:
        if depth == 0:
            return evaluate(board)
        result = None
        for move in BoardUtil.get_all_moves(board=board):
            adjusted_board = BoardUtil.create_adjusted_board(
                board, move
            )
            score = -cls.negative_max(evaluate, adjusted_board, depth - 1)
            if result is None or score > result:
                result = score
        return result

    @classmethod
    def get_best_move(cls, board: Board, minimax_level: int) -> Tuple[int, int, int, int]:
        all_moves = list()
        running_processes = list()
        completed_processes = list()

        for item in cls.working_temp_path.iterdir():
            os.remove(item)

        for actor, x1, y1 in board.foreach_actors():
            if actor.is_red:
                continue
            move_cases = actor.move_cases(board=board, pos=(x1, y1))
            for x2, y2 in move_cases:
                move = (x1, y1, x2, y2)
                all_moves.append(move)

        (cls.working_temp_path / 'board.dat').write_bytes(
            pickle.dumps(board)
        )
        for k, move in enumerate(all_moves):
            (cls.working_temp_path / '{}.input.dat'.format(k)).write_bytes(
                pickle.dumps(move)
            )
            running_processes.append(
                subprocess.Popen(
                    'python run_subprocess.py decision_maker/minimax {} {}'.format(minimax_level, k),
                    shell=True
                )
            )

        while running_processes:
            print('{} / {} processes are running'.format(len(running_processes), len(all_moves)))

            new_running_processes = list()
            for process in running_processes:
                rc = process.poll()
                if rc is None:
                    new_running_processes.append(process)
                else:
                    completed_processes.append(process)
            running_processes = new_running_processes

            time.sleep(0.5)

        result: Optional[Tuple[int, int, int, int]] = None
        result_value = None
        for k, move in enumerate(all_moves):
            move_value = float(
                (cls.working_temp_path / '{}.output.dat'.format(k)).read_text(encoding='utf-8')
            )
            if result_value is None or result_value > move_value:
                result_value = move_value
                result = move
        return result

    @classmethod
    def parallel_execute(cls, minimax_level: str, k: str):
        pr = cProfile.Profile()
        pr.enable()
        minimax_level: int = int(minimax_level)
        k: int = int(k)

        board = pickle.loads((cls.working_temp_path / 'board.dat').read_bytes())
        move = pickle.loads((cls.working_temp_path / '{}.input.dat'.format(k)).read_bytes())

        adjusted_board = BoardUtil.create_adjusted_board(board, move)
        move_value = cls.negative_max(Evaluator.basic, adjusted_board, minimax_level)
        (cls.working_temp_path / '{}.output.dat'.format(k)).write_text(str(move_value), encoding='utf-8')
        pr.disable()
        with (cls.working_temp_path / '{}.profile.dat'.format(k)).open(mode='w',encoding='utf-8') as file:
            ps = pstats.Stats(pr, stream=file).sort_stats(pstats.SortKey.CUMULATIVE)
            ps.print_stats()