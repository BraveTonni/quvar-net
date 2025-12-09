import asyncio

from src.infrastructure.adapters.client import ClientAdapter


async def main():
    client = ClientAdapter("127.0.0.1", 46729)

    asyncio.create_task(client.start())

    while client._writer is None or client._writer.is_closing():
        await asyncio.sleep(0.01)

    print("Подключено, отправляем INFO")


if __name__ == "__main__":
    asyncio.run(
        main()
    )
