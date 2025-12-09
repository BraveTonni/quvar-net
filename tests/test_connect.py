import pytest
import asyncio

from src.infrastructure.adapters import BootstrapAdapter, ClientAdapter


@pytest.mark.asyncio
async def test_connect():
    node = BootstrapAdapter("127.0.0.1", 7583)
    node_task = asyncio.create_task(node.start())

    await asyncio.sleep(1)

    client = ClientAdapter("127.0.0.1", 7583)
    client_task = asyncio.create_task(client.start())

    await asyncio.sleep(3)

    client_task.cancel()
    node_task.cancel()

    await client.stop()
    await node.stop()
