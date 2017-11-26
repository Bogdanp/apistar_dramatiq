import dramatiq

from apistar import Route, Settings
from apistar.frameworks.wsgi import WSGIApp as App
from apistar_dramatiq import actor
from dramatiq.brokers.stub import StubBroker

broker = StubBroker()
broker.emit_after("process_boot")
dramatiq.set_broker(broker)


class SomeComponent:
    pass


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


@actor(app=app, max_retries=0)
def missing_dep(idontexist: SomeComponent):
    pass
