from src.domain.events.server import ServerEvent

from src.domain.entities.client import Client
from src.domain.entities.message import Message, EventKind
from loguru import logger

from src.infrastructure.adapters.bootstrap import BootstrapAdapter


class NodesInfoEvent(ServerEvent):
    @staticmethod
    async def handle(adapter: BootstrapAdapter, client: Client):
        _logger = logger.bind(
            module=NodesInfoEvent.__class__.__module__,
            cls=NodesInfoEvent.__class__.__name__,
        )

        _logger.debug(f"Клиенту {client.uuid} отправлен список нод")
        await client.send_message(Message(EventKind.RECEIVE_NODES, dict(nodes=adapter.nodes)))
