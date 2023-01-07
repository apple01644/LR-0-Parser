from typing import List

from lr_0_parser.acition_table import ActionTable
from lr_0_parser.defines import CFG
from lr_0_parser.goto_table import GotoTable


class CompilerEnvironment:
    def __init__(self):
        self.terminals: List[str] = list()
        self.non_terminals: List[str] = list()
        self.eof_symbol: str = '$'
        self.item_set_size: int = 0
        self.cfg_list: List[CFG] = list()
        self.action_table: ActionTable = ActionTable()
        self.goto_table: GotoTable = GotoTable()
