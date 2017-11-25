import dramatiq
import pytest

from apistar import Route, Settings
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.test import TestClient
from apistar_dramatiq import actor
from dramatiq.brokers.stub import StubBroker
from unittest.mock import PropertyMock, call, patch

broker = StubBroker()
broker.emit_after("process_boot")
dramatiq.set_broker(broker)


def log():
    log_inputs.send(1, y=2)
    return {}


def missing():
    missing_dep.send()
    return {}


routes = [
    Route("/log", "GET", log),
    Route("/missing", "GET", missing),
]

settings = {
    "EXAMPLE": 42
}

app = App(
    routes=routes,
    settings=settings,
)


@actor(app=app)
def log_inputs(x, y, settings: Settings):
    log_inputs.logger.info(x)
    log_inputs.logger.info(y)
    log_inputs.logger.info(settings)


class SomeComponent:
    pass


@actor(app=app, max_retries=0)
def missing_dep(idontexist: SomeComponent):
    pass


@pytest.fixture
def worker():
    worker = dramatiq.Worker(broker, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


@patch("tests.test_actor_decorator.log_inputs.logger", new_callable=PropertyMock)
def test_can_inject_params(logger_mock, worker):
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
        call(settings),
    ])


def test_can_fail_to_inject_params(worker):
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
