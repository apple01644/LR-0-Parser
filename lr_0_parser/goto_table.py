from typing import Dict

from lr_0_parser.item_set import ItemSet


class GotoTable:
    def __init__(self):
        self.rows: Dict[int, Dict[str, int]] = {}

    def add_transition(self, src: ItemSet, sym: str, dst: ItemSet):
        if src.id not in self.rows:
            self.rows[src.id] = dict()
        row = self.rows[src.id]
        row[sym] = dst.id
