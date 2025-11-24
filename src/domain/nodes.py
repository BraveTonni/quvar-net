from enum import IntEnum, auto


class NodeType(IntEnum):
    """Внутренняя классификация узла"""

    BOOTSTRAP = auto()
    PEER = auto()
