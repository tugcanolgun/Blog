import logging

import pytest


@pytest.fixture(autouse=True)
def disable_loggers() -> None:
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)
