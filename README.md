# Unofficial Tabdeal API

[![PyPI](https://img.shields.io/pypi/v/unofficial-tabdeal-api.svg?style=flat-square)][package url]
[![Status](https://img.shields.io/pypi/status/unofficial-tabdeal-api.svg?style=flat-square)][package url]
[![Python Version](https://img.shields.io/pypi/pyversions/unofficial-tabdeal-api?style=flat-square)][package url]
[![License](https://img.shields.io/pypi/l/unofficial-tabdeal-api?style=flat-square)][MIT License]
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)][Code of Conduct]
[![Documentation Status](https://readthedocs.org/projects/unofficial-tabdeal-api/badge/?version=latest)][ReadTheDocs]

a Package to communicate with Tabdeal platform

## Features

- TODO

## Requirements

- `aiohttp`

## Installation

You can install _unofficial tabdeal api_ via [pip] from [PyPI]:

```console
pip install unofficial-tabdeal-api
```

## Usage

1. Initialize an `aiohttp.ClientSession` asynchronously via:
`async with aiohttp.ClientSession() as client_session:`

2. Create a `TabdealClient` object inside the async wrap:
`my_client: TabdealClient = TabdealClient(USER_HASH, USER_AUTHORIZATION_KEY, client_session)`
3. Run your desired commands, Remember to `await` the methods as all of them (except a very few) are asynchronous:
`bomeusdt_asset_id = await my_client.get_margin_asset_id("BOMEUSDT")`

## Issues

- Most exceptions are caught broadly using the `except Exception as exception`
  , This raises [Pylint-W0718], but i currently don't have a fix for it.

- Some parts of the code works flawlessly but raises [Pylance-reportCallIssue], [Pylance-reportArgumentType] or [Mypy-call-overload] which i mitigate by adding `# type: ignore` at the end of the line. This must be investigated later and fixed with a proper solution. I don't know a solution for it yet.

If you encounter any problems,
please [file an issue] along with a detailed description.

## TODO

- Use `README.rst` instead of `README.md`

- Fix [Pylint-W0718] by catching specific exceptions instead of catching all exceptions.

- Fix [Pylance-reportCallIssue], [Pylance-reportArgumentType] or [Mypy-call-overload].

- Fix missing library stubs or py.typed marker `MyPy-import-untyped`

- Improve documentation for setup and usage.

## License

Distributed under the terms of the [MIT license],
_unofficial tabdeal api_ is free and open source software.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## Credits

This project was created with the help of [@cjolowicz]'s [Hypermodern Python Cookiecutter] template and [@fpgmaas]'s [Cookiecutter Poetry] template.

<!-- Links -->
<!-- Badges section -->
[package url]: https://pypi.org/project/unofficial-tabdeal-api/
[ReadTheDocs]: https://unofficial-tabdeal-api.readthedocs.io/en/latest/?badge=latest

<!-- Installation section -->
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/

<!-- Issues section -->
[file an issue]: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues/new

<!-- TODO section -->
[Pylint-W0718]: https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/broad-exception-caught.html
[Pylance-reportCallIssue]: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportCallIssue
[Pylance-reportArgumentType]: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportArgumentType
[Mypy-call-overload]: https://mypy.readthedocs.io/en/latest/error_code_list.html#code-call-overload

<!-- Credits section -->
[@cjolowicz]: https://github.com/cjolowicz
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[@fpgmaas]: https://github.com/fpgmaas
[Cookiecutter Poetry]: https://github.com/fpgmaas/cookiecutter-poetry

<!-- Github Only -->
<!-- This section should be ignored by ReadTheDocs -->
<!-- Badges Section -->
[Code of Conduct]: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CODE_OF_CONDUCT.md
<!-- Contributing section -->
[Contributor Guide]: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CONTRIBUTING.md
<!-- License section -->
[MIT License]: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/LICENSE.txt
