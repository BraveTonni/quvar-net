from typing import Callable, Dict, TypeVar
from src.domain.entities.events import EventKind

T = TypeVar("T")


class EventHelper:
    """Универсальный помощник для хранения и поиска обработчиков событий по EventKind"""

    def __init__(self, event_enum: type):
        self.enum = event_enum
        self.events: Dict[str, Callable] = {}

    def register(self, kind: EventKind) -> Callable[[Callable], Callable]:
        """Декоратор для регистрации обработчика"""

        def decorator(handler: Callable) -> Callable:
            self.events[kind.value] = handler
            return handler

        return decorator

    def get(self, kind: EventKind) -> Callable | None:
        """Получить обработчик по EventKind"""
        return self.events.get(kind.value)

    def add(self, kind: EventKind, handler: Callable) -> None:
        """Ручная регистрация (если не нравится декоратор)"""
        self.events[kind.value] = handler

    def remove(self, kind: EventKind) -> bool:
        """Удалить обработчик"""
        return self.events.pop(kind.value, None) is not None
