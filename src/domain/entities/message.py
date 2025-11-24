from dataclasses import dataclass, field

from .events import EventKind


@dataclass
class Message:
    event: EventKind
    params: dict = field(default_factory=dict)
