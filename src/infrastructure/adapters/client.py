import asyncio
from typing import Optional

from src.infrastructure.adapters.base import BaseAdapter
from src.domain.mappers.message import MessageMapper
from src.domain.entities.message import Message
from src.domain.entities.events import EventKind
from src.utils.helpers.event_helper import EventHelper
from src.domain.events.client import ClientEvent


class ClientAdapter(BaseAdapter):
    def __init__(self, host: str = "127.0.0.1", port: int = 7583):
        super().__init__(host, port)
        self.event_helper = EventHelper(ClientEvent)
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._receive_task: Optional[asyncio.Task] = None
        self._nodes_request_task: Optional[asyncio.Task] = None
        self._reconnect_delay = 5
        self._stopped = asyncio.Event()
        self._registred = asyncio.Event()

    async def start(self) -> None:
        self._stopped.clear()
        while not self._stopped.is_set():
            try:
                self._reader, self._writer = await asyncio.open_connection(
                    self.host, self.port
                )
                peer = self._writer.get_extra_info("peername")
                self._logger.info(f"Подключено к {peer[0]}:{peer[1]}")
                self._receive_task = asyncio.create_task(self._receive_loop())
                self._nodes_request_task = asyncio.create_task(
                    self._periodic_nodes_request()
                )
                await asyncio.gather(
                    self._receive_task, self._nodes_request_task, return_exceptions=True
                )
            except (ConnectionRefusedError, OSError) as e:
                self._logger.warning(f"Не удалось подключиться: {e}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.exception(f"Ошибка в клиенте: {e}")
            await self._cleanup()
            if not self._stopped.is_set():
                self._logger.info(
                    f"Переподключение через {self._reconnect_delay} сек..."
                )
                await asyncio.sleep(self._reconnect_delay)

    async def _receive_loop(self) -> None:
        try:
            while True:
                data = await self._reader.readuntil(b"\n")
                if not data:
                    break
                message = MessageMapper.to_domain(data.strip())
                if message:
                    await self._process_message(message)
        except asyncio.IncompleteReadError:
            pass
        except ConnectionResetError:
            pass
        except Exception as e:
            self._logger.exception(f"Ошибка в _receive_loop: {e}")

    async def _cleanup(self) -> None:
        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        if self._writer and not self._writer.is_closing():
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
        self._reader = None
        self._writer = None
        self._receive_task = None

    async def stop(self) -> None:
        self._stopped.set()
        await self._cleanup()
        self._logger.info("Клиент остановлен")

    async def send(self, message: Message) -> None:
        if not self._writer or self._writer.is_closing():
            raise ConnectionError("Нет активного соединения с сервером")
        data = MessageMapper.to_bytes(message)
        self._writer.write(data + b"\n")
        await self._writer.drain()
        self._logger.debug(
            f"→ Отправлено: {message.event.value} {message.params}"[:150]
        )

    async def _process_message(self, message: Message) -> None:
        handler = self.event_helper.get(message.event)
        if not handler:
            self._logger.warning(f"Неизвестное событие от сервера: {message.event}")
            return

        self._logger.debug(f"← Получено: {message.event.value} {message.params}")
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(self, **message.params)
            else:
                await asyncio.get_event_loop().run_in_executor(
                    None, handler, self, **message.params
                )
        except Exception as exc:
            self._logger.error(f"Ошибка в обработчике {message.event.value}: {exc}")

    async def _periodic_nodes_request(self):
        await self._registred.wait()

        """Периодически запрашивает список нод у bootstrap"""
        while True:
            try:
                if self._writer and not self._writer.is_closing():
                    await self.send(Message(EventKind.NODES_INFO))
                    self._logger.debug("Запрошен список нод у bootstrap")

                await asyncio.sleep(3 * 60)

            except (ConnectionError, BrokenPipeError):
                break
            except asyncio.CancelledError:
                break
            except Exception as e:
                self._logger.error(f"Ошибка при запросе нод: {e}")
                await asyncio.sleep(5)
