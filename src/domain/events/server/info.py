from src.domain.events.server import ServerEvent

from src.infrastructure.adapters.bootstrap import BootstrapAdapter

from src.domain.entities.client import ClientInfo, Client
from loguru import logger


class InfoEvent(ServerEvent):
    @staticmethod
    async def handle(adapter: BootstrapAdapter, client: Client, info: dict):
        _logger = logger.bind(
            module=InfoEvent.__class__.__module__, cls=InfoEvent.__class__.__name__
        )

        client_info = ClientInfo(**info)
        client.info = client_info

        _logger.debug(f"Обновлена информация клиента: {client_info}")
