import itertools
from typing import NoReturn, List, Dict, Optional

from lr_0_parser.action import Action
from lr_0_parser.compiler_env import CompilerEnvironment
from lr_0_parser.defines import DOT
from lr_0_parser.item import Item
from lr_0_parser.item_set import ItemSet


class CompilerBuilder:
    def __init__(self, env: CompilerEnvironment):
        self.env: CompilerEnvironment = env
        self.item_sets: List[ItemSet] = []

    def add_igniting_item_set(self, ignite_symbol: str) -> NoReturn:
        new_born_item_set = ItemSet()
        accept_symbol = ignite_symbol + '`'
        new_born_item_set.items.append(
            Item(accept_symbol, [DOT, ignite_symbol, self.env.eof_symbol], cfg=None, is_kernel=True),
        )
        self.closure_item_set(new_born_item_set)
        self.submit_item_set(new_born_item_set)

    def submit_item_set(self, item_set: ItemSet) -> int:
        item_set.id = len(self.item_sets)
        self.item_sets.append(item_set)
        return item_set.id

    def closure_item_set(self, item_set: ItemSet) -> NoReturn:
        will_expand_non_terminals = item_set.get_lead_symbols()
        expanded_non_terminals = []
        while will_expand_non_terminals:
            sym = will_expand_non_terminals.pop(0)
            print(sym)
            for cfg in self.env.cfg_list:
                if cfg.lhs != sym:
                    continue
                item = Item(cfg.lhs, [DOT] + cfg.rhs, cfg=cfg)
                new_sym = item.get_lead_symbol()
                if new_sym in self.env.non_terminals \
                        and new_sym not in expanded_non_terminals \
                        and new_sym not in will_expand_non_terminals \
                        and new_sym != sym:
                    will_expand_non_terminals.append(new_sym)

                item_set.items.append(item)
            expanded_non_terminals.append(sym)

    def expanding_process(self):
        newly_created_item_sets: List[ItemSet] = list()
        newly_created_item_sets += self.item_sets

        while newly_created_item_sets:
            origin_item_set = newly_created_item_sets.pop(0)
            not_yet_built_items = list(
                filter(lambda item: item.get_lead_symbol() is not None, origin_item_set.items)
            )
            built_items = list(
                filter(lambda item: item.get_lead_symbol() is None, origin_item_set.items)
            )
            built_item: Optional[Item] = built_items[0] if built_items else None
            not_yet_built_items.sort(key=lambda item: item.get_lead_symbol())
            tmp_items_group_by_lead_symbol = itertools.groupby(
                not_yet_built_items, lambda item: item.get_lead_symbol()
            )
            items_group_by_lead_symbol: Dict[str, List[Item]] = {
                s: list(grp) for s, grp in
                tmp_items_group_by_lead_symbol
            }

            if built_item:
                for sym in self.env.terminals + [self.env.eof_symbol]:
                    self.env.action_table.add_transition(
                        src=origin_item_set,
                        sym=sym,
                        act=Action(tp_cd=Action.REDUCE, reduce_cfg=built_item.cfg)
                    )

            for lead_symbol, items in items_group_by_lead_symbol.items():
                new_item_set = ItemSet()
                for origin_item in items:
                    try:
                        new_item_set.items.append(
                            origin_item.get_dot_shifted_item()
                        )
                    except ValueError:
                        pass
                    pass
                if lead_symbol != self.env.eof_symbol:
                    for exists_item_set in self.item_sets:
                        if new_item_set.has_same_kernels(exists_item_set):
                            next_item_set = exists_item_set
                            break
                    else:
                        self.closure_item_set(new_item_set)
                        newly_created_item_sets.append(new_item_set)
                        self.submit_item_set(new_item_set)
                        next_item_set = new_item_set
                    if lead_symbol in self.env.non_terminals:
                        self.env.goto_table.add_transition(
                            src=origin_item_set,
                            sym=lead_symbol,
                            dst=next_item_set
                        )
                    elif lead_symbol in self.env.terminals:
                        self.env.action_table.add_transition(
                            src=origin_item_set,
                            sym=lead_symbol,
                            act=Action(tp_cd=Action.SHIFT, shift_item_set=next_item_set)
                        )
                else:
                    self.env.action_table.add_transition(
                        src=origin_item_set,
                        sym=lead_symbol,
                        act=Action(tp_cd=Action.ACCEPT)
                    )
        self.env.item_set_size = len(self.item_sets)

    def build_compiler(self):
        self.add_igniting_item_set('E')
        self.expanding_process()
