from typing import List, Optional

from lr_0_parser.defines import CFG, DOT


class Item:
    def __init__(self, lhs: str, rhs: List[str], /, cfg: Optional[CFG], is_kernel: bool = False):
        self.cfg = cfg
        self.lhs = lhs
        self.rhs = rhs
        self.is_kernel: bool = is_kernel

    def get_lead_symbol(self) -> Optional[str]:
        try:
            itr = iter(self.rhs)
            while True:
                sym = next(itr)
                if sym == DOT:
                    sym = next(itr)
                    return sym
        except StopIteration:
            pass

        return None

    def get_dot_shifted_item(self) -> 'Item':
        result = []

        itr = iter(self.rhs)
        try:
            while True:
                sym = next(itr)
                if sym == DOT:
                    sym = next(itr)
                    result.append(sym)
                    result.append(DOT)
                else:
                    result.append(sym)
        except StopIteration:
            pass
        if DOT not in result:
            raise ValueError('This item has no rooms for shifted dot ')
        return Item(self.lhs, result, cfg=self.cfg, is_kernel=True)

    def __eq__(self, other: 'Item') -> bool:
        if self.lhs != other.lhs:
            return False
        if ''.join(self.rhs) != ''.join(other.rhs):
            return False
        return True

    def __hash__(self):
        return hash(self.lhs + '→' + ''.join(self.rhs))

    def __repr__(self):
        text = '<Item '
        if self.is_kernel is False:
            text += '+'
        text += self.lhs
        text += ' → '
        text += ' '.join(self.rhs)
        text += ' >'
        return text
