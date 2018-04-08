import apistar_dramatiq

from apistar import App, Component, Route
from apistar_dramatiq import actor


class Settings(dict):
    pass


SETTINGS = Settings(**{
    "EXAMPLE": 42,
})


class SettingsComponent(Component):
    def resolve(self) -> Settings:
        return SETTINGS


@actor
def print_x_and_settings(x, settings: Settings):
    print(x)
    print(settings)


def index() -> dict:
    print_x_and_settings.send(42)
    return {}


routes = [
    Route("/", method="GET", handler=index),
]

components = [
    SettingsComponent(),
]

app = App(routes=routes, components=components)
apistar_dramatiq.setup(components)
