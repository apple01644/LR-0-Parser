import enum
from typing import List, Optional


DOT = '●'


class ActionType(enum.Enum):
    SHIFT: int = 1
    REDUCE: int = 2
    ACCEPT: int = 3


class ParseTree:
    def __init__(self, lhs: str):
        self.lhs = lhs
        self.rhs: List['ParseTree'] = list()

    def __repr__(self, indent_size: int = 0):
        indent = ' ' * indent_size
        text = indent + '<PT {!r}'.format(self.lhs)
        if self.rhs:
            text += '\n'
            for child in self.rhs:
                text += child.__repr__(indent_size=indent_size + 4) + '\n'
            text += indent
        text += '>'
        return text


class CFG:
    def __init__(self, lhs: str, rhs: List[str]):
        self.lhs = lhs
        self.rhs = rhs
        self.id: Optional[int] = None

    def __repr__(self):
        return '<CFG {} → {}>'.format(self.lhs, ' '.join(self.rhs))


