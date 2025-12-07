import asyncio
import random

from src.infrastructure.adapters import ClientAdapter, ServerAdapter
from src.infrastructure.adapters.bootstrap import BootstrapAdapter

from src.domain.entities.message import Message
from src.domain.entities.events import EventKind
from src.utils.helpers.computer_helper import ComputerHelper

from src.domain.events.server.info import InfoEvent
from src.domain.events.server.nodes_info import NodesInfoEvent
from src.domain.events.server.new_node import NewNodeEvent
from src.domain.events.client.receive_nodes import ReceiveNodesEvent


async def run() -> None:
    await asyncio.sleep(1)

    client = ClientAdapter("127.0.0.1", 7583)

    client_task = asyncio.create_task(client.start())

    while client._writer is None or client._writer.is_closing():
        await asyncio.sleep(0.01)

    info = await ComputerHelper.get_client_info()
    await client.send(Message(EventKind.INFO, dict(info=info)))

    client.event_helper.add(
        kind=EventKind.RECEIVE_NODES, handler=ReceiveNodesEvent.handle
    )

    # говорим адаптеру, что все ивенты зарегистрированы
    client._registred.set()

    print("запуск сервера")
    server_port = random.randrange(46720, 46730)
    server = ServerAdapter("127.0.0.1", server_port)

    asyncio.create_task(server.start())

    await client.send(
        Message(
            event=EventKind.NEW_NODE, params={"ip": "127.0.0.1", "port": server_port}
        )
    )

    try:
        await asyncio.Event().wait()  # вечное ожидание
    except KeyboardInterrupt:
        print("Останавливаем...")
    finally:
        await client.stop()
        client_task.cancel()


async def run_bootstrap() -> None:
    """Запуск приложения как Bootstrap ноды"""

    node = BootstrapAdapter("127.0.0.1", 7583)

    node.event_helper.add(kind=EventKind.INFO, handler=InfoEvent.handle)
    node.event_helper.add(kind=EventKind.NEW_NODE, handler=NewNodeEvent.handle)
    node.event_helper.add(kind=EventKind.NODES_INFO, handler=NodesInfoEvent.handle)

    await node.start()
