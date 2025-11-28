from loguru import logger
import sys


def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        colorize=True,
        level="DEBUG",
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
            "| <level>{level: <8}</level> "
            "| <cyan>{extra[module]: <40}</cyan> "
            "| <magenta>{extra[cls]: ^20}</magenta> "
            "| <blue>{file}:{line}</blue> "
            "| <level>{message}</level>"
        ),
    )
