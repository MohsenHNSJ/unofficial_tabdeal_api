# Unofficial Tabdeal API

a Package to communicate with Tabdeal platform

## Requirements

- `aiohttp`

## Usage

1. Initialize an `aiohttp.ClientSession` asynchronously via:
`async with aiohttp.ClientSession() as client_session:`

2. Create a `TabdealClient` object inside the async wrap:
`my_client: TabdealClient = TabdealClient(USER_HASH, USER_AUTHORIZATION_KEY, client_session)`
3. Run your desired commands, Remember to `await` the methods as all of them (except a very few) are asynchronous:
`bomeusdt_asset_id = await my_client.get_margin_asset_id("BOMEUSDT")`

## Current problems

- Most exceptions are caught broadly using the `except Exception as exception`
  , This raises [Pylint-W0718](https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/broad-exception-caught.html), but i currently don't have a fix for it.

- Some parts of the code works flawlessly but raises [Pylance-reportCallIssue](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportCallIssue), [Pylance-reportArgumentType](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportArgumentType) or [Mypy-call-overload](https://mypy.readthedocs.io/en/latest/error_code_list.html#code-call-overload) which i mitigate by adding `# type: ignore` at the end of the line. This must be investigated later and fixed with a proper solution. I don't know a solution for it yet.

## Building

NEW METHOD:

- `pip install --upgrade build`

- Use the `build` command (`python -m build`)

## TODO

- Use `README.rst` instead of `README.md`

- Fix [Pylint-W0718](https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/broad-exception-caught.html)

- Fix [Pylance-reportCallIssue](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportCallIssue), [Pylance-reportArgumentType](https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportArgumentType) or [Mypy-call-overload](https://mypy.readthedocs.io/en/latest/error_code_list.html#code-call-overload) which i mitigate by adding `# type: ignore` at the end of the line.
