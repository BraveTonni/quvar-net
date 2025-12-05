from loguru import logger
import uuid

from abc import ABC, abstractmethod


class BaseAdapter(ABC):
    """Обработчик соединения"""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self._logger = logger.bind(module=self.__class__.__module__, cls=self.__class__.__name__)
        self._uid = str(uuid.uuid4())

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()
