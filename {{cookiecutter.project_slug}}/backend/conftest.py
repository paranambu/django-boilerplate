import pytest
from splinter import Browser


@pytest.fixture(scope='session')
def browser():
    return Browser('django')


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass
