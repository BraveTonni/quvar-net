import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    from src.utils import log

    log.setup_logger()
