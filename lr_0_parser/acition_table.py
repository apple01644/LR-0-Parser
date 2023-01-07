from typing import Dict

from lr_0_parser.action import Action
from lr_0_parser.item_set import ItemSet


class ActionTable:
    def __init__(self):
        self.rows: Dict[int, Dict[str, Action]] = {}

    def add_transition(self, src: ItemSet, sym: str, act: Action):
        if src.id not in self.rows:
            self.rows[src.id] = dict()
        row = self.rows[src.id]
        row[sym] = act
