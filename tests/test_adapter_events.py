import pytest

from src.infrastructure.adapters.server import ServerAdapter
from src.exceptions.events import NotEventFound
from src.domain.events.server import ServerEvent

from src.domain.entities.message import Message
from src.domain.entities.events import EventKind


def generate_adapter():
    return ServerAdapter("127.0.0.1", 5000)


class TestEvent(ServerEvent):
    def handle():
        pass


@pytest.mark.asyncio
async def test_adapter_events():
    adapter = generate_adapter()

    adapter.event_helper.add(kind=EventKind.INFO, handler=TestEvent.handle)

    await adapter._ServerAdapter__process_events(
        Message(event=EventKind.INFO, params={})
    )

    assert adapter.event_helper.remove(EventKind.INFO)

    with pytest.raises(NotEventFound):
        await adapter._ServerAdapter__process_events(
            Message(event=EventKind.INFO, params={})
        )

    with pytest.raises(NotEventFound):
        await adapter._ServerAdapter__process_events(
            Message(event="unknown", params={})
        )
