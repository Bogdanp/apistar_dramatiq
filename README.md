# apistar_dramatiq

[![Build Status](https://travis-ci.org/Bogdanp/apistar_dramatiq.svg?branch=master)](https://travis-ci.org/Bogdanp/apistar_dramatiq)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9848a606e3332b808329/test_coverage)](https://codeclimate.com/github/Bogdanp/apistar_dramatiq/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/9848a606e3332b808329/maintainability)](https://codeclimate.com/github/Bogdanp/apistar_dramatiq/maintainability)
[![PyPI version](https://badge.fury.io/py/apistar-dramatiq.svg)](https://badge.fury.io/py/apistar-dramatiq)

[Dramatiq] integration for [API Star] apps.  Adds support for using
dependency injection inside Dramatiq actors.


## Requirements

* [API Star] 0.3+
* [Dramatiq] 0.15+


## Installation

Use [pipenv] (or plain pip) to install the package:

    pipenv install apistar_dramatiq

Then use `apistar_dramatiq.actor` in place of `dramatiq.actor`
wherever you want dependency injection:

``` python
from apistar import Settings
from apistar_dramatiq import actor


@actor(queue_name="example")
def print_settings(settings: Settings):
    print(settings)
```


## License

apistar_dramatiq is licensed under Apache 2.0.  Please see [LICENSE]
for licensing details.


[API Star]: https://github.com/encode/apistar/
[Dramatiq]: https://dramatiq.io
[pipenv]: https://docs.pipenv.org
[LICENSE]: https://github.com/Bogdanp/apistar_dramatiq/blob/master/LICENSE
