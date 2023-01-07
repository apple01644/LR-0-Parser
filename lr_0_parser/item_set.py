from _ast import Set
from typing import List, Optional

from lr_0_parser.item import Item


class ItemSet:
    def __init__(self):
        self.items: List[Item] = list()
        self.id: Optional[int] = None

    def __repr__(self):
        text = '<Itemset id={} has {} item(s)'.format(self.id, len(self.items))
        if self.items:
            text += '\n'
            for item in self.items:
                text += '\t' + repr(item) + '\n'
        text += ' >'
        return text

    def get_lead_symbols(self) -> List[str]:
        result: Set[str] = set()
        for item in self.items:
            sym = item.get_lead_symbol()
            if sym:
                result.add(sym)
        return list(result)

    @property
    def kernels(self) -> List[Item]:
        return list(filter(lambda item: item.is_kernel, self.items))

    def has_same_kernels(self, other: 'ItemSet') -> bool:
        this_kernels = set(self.kernels)
        other_kernels = set(other.kernels)
        return this_kernels == other_kernels
