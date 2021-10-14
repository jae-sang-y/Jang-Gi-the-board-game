import random
import time
from typing import List, NoReturn

from decision_maker import DecisionMaker, Decision


class RandomDecisionMaker(DecisionMaker):
    def __init__(self, delay: float):
        DecisionMaker.__init__(self)
        self.delay = delay

    def make_decision(self, decision_queue: List[Decision]) -> NoReturn:
        decision = None
        decision_count = 1
        for actor in self.get_actors():
            old_x, old_y, act_code = actor
            pos_list = self.board.get_movable_positions(*actor)
            for pos in pos_list:
                new_x, new_y = pos
                if 1 / decision_count > random.uniform(0, 1):
                    decision = Decision(old_x=old_x, old_y=old_y, act_code=act_code, new_x=new_x, new_y=new_y)
                decision_count += 1
        if decision:
            decision_queue.append(decision)
            time.sleep(self.delay)
