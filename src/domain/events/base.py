from abc import ABC, abstractmethod


class BaseEvent(ABC):
    """Обработчик событий от клиента"""
    @abstractmethod
    async def handle():
        """Обработчик события"""
        raise NotImplementedError()
