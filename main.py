import asyncio

from src.app import bootstrap
from src.utils.log import setup_logger

from loguru import logger


async def main() -> None:
    setup_logger()

    await asyncio.gather(*(bootstrap.run_bootstrap(), bootstrap.run()))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.bind(module=__name__, cls="main").critical(
            "Приложение остановлено с помощью Ctrl+C"
        )
