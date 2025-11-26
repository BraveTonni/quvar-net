import uuid

from dataclasses import dataclass

from asyncio import StreamWriter, StreamReader

from src.domain.entities.message import Message
from src.domain.mappers.message import MessageMapper

from enum import StrEnum, auto


class ClientRole(StrEnum):
    ALL = auto()


@dataclass
class ClientInfo:
    """Хранение информации о клиенте"""

    role: ClientRole

    os_info: dict

    local_ip: str

    user: str

    cpu: str
    ram_gb: float
    gpu: str

    is_admin: bool

    created_at: int


@dataclass
class Client:
    uuid: uuid.UUID

    writer: StreamWriter
    reader: StreamReader

    info: ClientInfo

    def __post_init__(self):
        if self.uuid is None:
            self.uuid = uuid.uuid4()

    async def send_message(self, message: Message):
        data = MessageMapper.to_bytes(message)

        self.writer.write(data + b"\n")

        await self.writer.drain()
