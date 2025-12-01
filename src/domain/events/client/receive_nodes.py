from src.domain.events import ClientEvent

from loguru import logger

from src.infrastructure.adapters.bootstrap import BootstrapAdapter


class ReceiveNodesEvent(ClientEvent):
    @staticmethod
    async def handle(adapter: BootstrapAdapter, nodes: dict):
        _logger = logger.bind(
            module=ReceiveNodesEvent.__class__.__module__,
            cls=ReceiveNodesEvent.__class__.__name__,
        )

        _logger.info(f"Получен список доступных нод от сервера: {nodes}")
