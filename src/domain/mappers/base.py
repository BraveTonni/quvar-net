from abc import ABC, abstractmethod
from typing import TypeVar

from src.domain.entities.events import EventKind


T = TypeVar("T")


class BaseMapper(ABC):
    @staticmethod
    @abstractmethod
    def to_domain(content) -> bool | T:
        """Метод для преобразования контента в сущности"""
        raise NotImplementedError()

    @staticmethod
    def is_valid(data: dict) -> bool:
        """Метод для валидации поступающих данных"""
        event = data.get("event")

        if not event or not EventKind(event):
            return False

        return True
