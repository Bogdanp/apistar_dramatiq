import apistar_dramatiq
import dramatiq

from apistar import App, Component, Route
from apistar_dramatiq import actor
from dramatiq.brokers.stub import StubBroker

broker = StubBroker()
broker.emit_after("process_boot")
dramatiq.set_broker(broker)


class Settings(dict):
    pass


class MissingDep:
    pass


class SettingsComponent(Component):
    def resolve(self) -> Settings:
        return {"EXAMPLE": 42}


def log():
    log_inputs.send(1, y=2)
    return {}


def missing():
    missing_dep.send()
    return {}


routes = [
    Route("/log", method="GET", handler=log),
    Route("/missing", method="GET", handler=missing),
]

components = [
    SettingsComponent(),
]

app = App(routes=routes, components=components)
apistar_dramatiq.setup(components)


@actor
def log_inputs(x, y, settings: Settings, z=42):
    log_inputs.logger.info(x)
    log_inputs.logger.info(y)
    log_inputs.logger.info(z)
    log_inputs.logger.info(settings)


@actor(max_retries=0)
def missing_dep(idontexist: MissingDep):
    pass
