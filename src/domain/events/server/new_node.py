import time

from loguru import logger

from src.domain.events.server import ServerEvent
from src.domain.entities.client import Client

from src.infrastructure.adapters.bootstrap import BootstrapAdapter

from src.domain.entities.nodes import NodeInfo


class NewNodeEvent(ServerEvent):
    @staticmethod
    async def handle(adapter: BootstrapAdapter, client: Client, ip: str, port: int):
        _logger = logger.bind(
            module=NewNodeEvent.__class__.__module__,
            cls=NewNodeEvent.__class__.__name__,
        )

        _logger.info(f"Клиент {client.uuid} отправил серверную ноду: {ip}:{port}")
        adapter.nodes.append(NodeInfo(ip=ip, port=port, created_at=int(time.time())))
