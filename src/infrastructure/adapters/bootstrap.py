import asyncio
import socket
import uuid

from src.domain.mappers.message import MessageMapper
from src.domain.entities.message import Message
from src.domain.events.server import ServerEvent
from src.domain.entities.client import Client
from src.domain.entities.nodes import NodeInfo

from src.exceptions.events import NotEventFound
from src.utils.helpers.event_helper import EventHelper

from src.infrastructure.admin.app import WebPanel
from src.infrastructure.adapters.base import BaseAdapter

from typing import Optional


class BootstrapAdapter(BaseAdapter):
    def __init__(self, host: str = "127.0.0.1", port: int = 7583):
        super().__init__(host, port)
        self.event_helper = EventHelper(ServerEvent)
        self._server: asyncio.Server | None = None
        self._panel = WebPanel(self)

        self.__clients: list[Client] = []

        self.nodes: list[NodeInfo] = []

    async def start(self):
        self._server = await asyncio.start_server(
            self._handle_client,
            self.host,
            self.port,
            family=socket.AF_INET,
            reuse_address=True,
        )
        addr = self._server.sockets[0].getsockname()
        self._logger.info(f"Бутстрап узел запущен на {addr[0]}:{addr[1]}")

        # Запуск админ панели
        await self._panel.start()

        # Запуск сокета
        async with self._server:
            await self._server.serve_forever()

    async def stop(self):
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
            self._logger.info("Бутстрап остановлен")

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        addr = writer.get_extra_info("peername")
        self._logger.debug(f"Подключение от {addr}")

        client = Client(None, writer, reader, None)

        self.__clients.append(client)

        try:
            while True:
                data = await reader.readuntil(b"\n")

                message_data = data.rstrip(b"\n")
                if not message_data:
                    print('no msg data')
                    continue

                message = MessageMapper.to_domain(message_data)
                if not message:
                    print('no msg')
                    continue

                await self.__process_event(client, message)

        except (asyncio.CancelledError, ConnectionResetError):
            pass
        except Exception as exc:
            self._logger.exception(f"Ошибка в соединении с {addr}: {exc}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def __process_event(self, client: Client, message: Message) -> None:
        handler = self.event_helper.get(message.event)

        if not handler:
            raise NotEventFound(f"Неизвестное событие: {message.event}")

        self._logger.debug(f"Обработка события {message.event} от клиента")

        if asyncio.iscoroutinefunction(handler):
            await handler(self, client, **message.params)
        else:
            handler(self, client, **message.params)

    def get_clients(self) -> list[Client]:
        return [client for client in self.__clients if client.info]

    def get_client_by_uuid(self, uuid_input: str | uuid.UUID) -> Optional[Client]:
        try:
            target = uuid.UUID(str(uuid_input))
        except (ValueError, AttributeError):
            return None

        return next((c for c in self.__clients if c.uuid == target), None)
