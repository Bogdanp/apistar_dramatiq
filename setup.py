import os

from setuptools import setup


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


with open(rel("apistar_dramatiq", "__init__.py"), "r") as f:
    version_marker = "__version__ = "
    for line in f:
        if line.startswith(version_marker):
            _, version = line.split(version_marker)
            version = version.strip().strip('"')
            break
    else:
        raise RuntimeError("Version marker not found.")


setup(
    name="apistar_dramatiq",
    version=version,
    description="Dramatiq integration for API Star.",
    long_description="Visit https://github.com/Bogdanp/apistar_dramatiq for more information.",
    packages=["apistar_dramatiq"],
    include_package_data=True,
    install_requires=[
        "apistar>=0.3",
        "dramatiq>=0.15",
    ],
)
