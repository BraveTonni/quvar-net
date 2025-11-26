import orjson

from json.decoder import JSONDecodeError

from src.domain.entities.message import Message
from src.domain.entities.events import EventKind

from .base import BaseMapper


class MessageMapper(BaseMapper):
    def to_domain(content: bytes) -> bool | Message:
        try:
            data = orjson.loads(content)
        except JSONDecodeError:
            return False

        if not MessageMapper.is_valid(data):
            return False

        return Message(event=EventKind(data.get("event")), params=data.get("params", {}))

    @staticmethod
    def to_bytes(message: Message) -> bytes:
        """Сериализация объекта Message → bytes (JSON)"""
        payload = {
            "event": message.event.value,
            "params": message.params or {},
        }

        return orjson.dumps(payload)
