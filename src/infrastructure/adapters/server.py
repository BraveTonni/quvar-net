import socket
import asyncio

from src.infrastructure.adapters.base import BaseAdapter
from src.domain.mappers.message import MessageMapper
from src.domain.entities.message import Message

from src.domain.events.server import ServerEvent
from src.exceptions.events import NotEventFound

from src.utils.helpers.event_helper import EventHelper


class ServerAdapter(BaseAdapter):
    """Адаптер принимающий запросы"""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)

        self.event_helper = EventHelper(ServerEvent)
        self.__socket = socket.socket()

    async def start(self):
        """Запуск сокета"""
        self.__socket.setblocking(False)
        self.__socket.bind((self.host, self.port))
        self.__socket.listen()

        asyncio.create_task(self.__listen_connections())

        self._logger.info(f"Сервер запущен на адресе: {self.host}:{self.port}")

    async def stop(self):
        """Остановка сокета"""
        self.__socket.close()

        self._logger.info(f"Сервер остановлен на адресе: {self.host}:{self.port}")

    async def __listen_connections(self):
        """Слушаем подключения к сокету"""
        loop = asyncio.get_running_loop()
        while True:
            try:
                connection, address = await loop.sock_accept(self.__socket)
                connection.setblocking(False)
                self._logger.debug(f"Новое подключение: {address}")
                asyncio.create_task(self.__receive_messages(connection, address))
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.error(f"Ошибка accept: {e}")
                continue

    async def __receive_messages(
        self, connection: socket.socket, address: tuple[str, int]
    ):
        """Получение сообщений"""
        loop = asyncio.get_running_event_loop()
        while True:
            try:
                data = await loop.sock_recv(connection, 4096)
                if not data:
                    self._logger.debug(f"Клиент {address} отключился")
                    break
                message = MessageMapper.to_domain(data.strip())
                await self.__process_events(message)
            except ConnectionResetError:
                break
            except Exception as e:
                self._logger.error(f"Ошибка чтения от {address}: {e}")
                break

        connection.close()

    async def __process_events(self, message: Message) -> None:
        """Обработка событий"""
        event = self.event_helper.events.get(message.event)

        if not event:
            raise NotEventFound(f"Получено неизвестное сообщение {message=}")

        self._logger.debug(f"Вызов события {message.event}")

        event(**message.params)
