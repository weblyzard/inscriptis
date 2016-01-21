from enum import Enum

class Display(Enum):
    inline = 1
    block = 2
    none = 3

class WhiteSpace(Enum):
    normal = 1 # sequences of whitespace will collapse into a single one
    pre = 3 # sequences of whitespace will be preserved

