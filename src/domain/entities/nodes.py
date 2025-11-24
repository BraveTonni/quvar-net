from dataclasses import dataclass


@dataclass
class NodeInfo:
    ip: str
    port: int

    created_at: int
