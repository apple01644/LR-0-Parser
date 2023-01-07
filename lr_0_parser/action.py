from typing import Optional

from lr_0_parser.defines import ActionType, CFG
from lr_0_parser.item_set import ItemSet


class Action:
    SHIFT: ActionType = ActionType.SHIFT
    REDUCE: ActionType = ActionType.REDUCE
    ACCEPT: ActionType = ActionType.ACCEPT

    def __init__(self, tp_cd: ActionType, reduce_cfg: CFG = None, shift_item_set: ItemSet = None):
        self.tp_cd = tp_cd
        self.reduce_cfg_id: Optional[int] = reduce_cfg.id if reduce_cfg else None
        self.shift_item_set_id: Optional[int] = shift_item_set.id if shift_item_set else None

    def __repr__(self) -> str:
        text = '<Action '
        text += self.tp_cd.name
        if self.tp_cd == Action.REDUCE:
            text += ' %d' % self.reduce_cfg_id
        elif self.tp_cd == Action.SHIFT:
            text += ' %d' % self.shift_item_set_id
        text += '>'
        return text
