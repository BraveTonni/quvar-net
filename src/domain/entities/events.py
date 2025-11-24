from enum import StrEnum, auto


class EventKind(StrEnum):
    INFO = auto()
    NODES_INFO = auto()
    NEW_NODE = auto()
    RECEIVE_NODES = auto()
