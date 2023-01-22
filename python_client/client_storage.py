from typing import Dict

from dataset.board_factory import BoardFactory


class ClientStorage:
    def __init__(self):
        self.board = BoardFactory.get_classic_start()

        self.components: Dict[str, object] = dict()

    def set_component(self, component: object):
        self.components[component.__class__.__name__] = component

    def get_component(self, component_class: type) -> object:
        return self.components[component_class.__name__]
