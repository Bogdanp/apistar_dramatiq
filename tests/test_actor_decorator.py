import logging
logging.basicConfig(level=logging.DEBUG)
import dramatiq
import pytest

from apistar.test import TestClient
from unittest.mock import PropertyMock, call, patch

from .app import app, broker as _broker, log_inputs, missing_dep


@pytest.fixture
def broker():
    _broker.flush_all()
    yield _broker


@pytest.fixture
def worker(broker):
    worker = dramatiq.Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@patch("tests.app.log_inputs.logger", new_callable=PropertyMock)
def test_can_inject_params(logger_mock, broker, worker):
    # Given an apistar app client
    # And a mocked actor logger
    client = TestClient(app)

    # When I visit an endpoint that enqueues a task
    response = client.get("/log")
    assert response.status_code == 200

    # And wait for the worker to process jobs
    broker.join(log_inputs.queue_name)
    worker.join()

    # The the logger should have been called with the appropriate data
    logger_mock.info.assert_has_calls([
        call(1),
        call(2),
        call(42),
        call({"EXAMPLE": 42}),
    ])


def test_can_fail_to_inject_params(broker, worker):
    # Given an apistar app client
    client = TestClient(app)

    # When I visit an endpoint that enqueues a task that has a missing dep
    response = client.get("/missing")
    assert response.status_code == 200

    # And wait for the worker to process jobs
    broker.join(missing_dep.queue_name)
    worker.join()

    # Then my actor should fail
    assert broker.dead_letters
