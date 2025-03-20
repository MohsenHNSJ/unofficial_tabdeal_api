======================
Unofficial Tabdeal API
======================
..
    Badges section

.. list-table::
    :stub-columns: 1

    * - Package
      - |version| |status| |supported-python-versions| |poetry|
    * - Documentation
      - |documentation|
    * - Tests
      - |nox| |github-actions|
    * - Linters
      - |ruff|
    * - License
      - |license|
    * - Stats
      - |contributors| |stars| |downloads|
    * - Misc
      - |contributor-covenant|  |doi|

.. |version| image:: https://img.shields.io/pypi/v/unofficial-tabdeal-api.svg?style=flat-square
    :target: package-url_
    :alt: PyPI

.. |status| image:: https://img.shields.io/pypi/status/unofficial-tabdeal-api.svg?style=flat-square
    :target: package-url_
    :alt: Status

.. |supported-python-versions| image:: https://img.shields.io/pypi/pyversions/unofficial-tabdeal-api?style=flat-square
    :target: package-url_
    :alt: Python Version

.. |license| image:: https://img.shields.io/pypi/l/unofficial-tabdeal-api?style=flat-square
    :target: `MIT License`_
    :alt: License

.. |contributor-covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=flat-square
    :target: `Code of Conduct`_
    :alt: Contributor Covenant

.. |documentation| image:: https://readthedocs.org/projects/unofficial-tabdeal-api/badge/?version=latest&style=flat-square
    :target: Read-The-Docs_
    :alt: Documentation Status

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square
    :target: Ruff_
    :alt: Ruff

.. |nox| image:: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
    :target: Nox_
    :alt: Nox

.. |poetry| image:: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
   :target: Poetry_
    :alt: Poetry

.. |github-actions| image:: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions/workflows/release-packge.yml/badge.svg
    :target: `Github Actions`_
    :alt: Actions Status

.. |contributors| image:: https://img.shields.io/github/contributors/MohsenHNSJ/unofficial_tabdeal_api.svg?style=flat-square
    :target: Contributors_
    :alt: Contributors

.. |stars| image:: https://img.shields.io/github/stars/MohsenHNSJ/unofficial_tabdeal_api?style=social
    :target: Stars_
    :alt: Stars

.. |doi| image:: https://zenodo.org/badge/917705429.svg
    :target: DOI_
    :alt: Digital Object Identifier

.. |downloads| image:: https://static.pepy.tech/badge/unofficial_tabdeal_api
    :target: `Total Downloads`_
    :alt: Total Downloads

a Package to communicate with Tabdeal platform

Features
--------

* TODO

Requirements
------------

* *aiohttp*

Installation
------------

You can install *unofficial tabdeal api* via pip_ from PyPI_:

.. code-block:: sh
    
    pip install unofficial-tabdeal-api

Usage
-----

.. code-block:: python

    # Initialize aiohttp.ClientSession asynchronously
    async with aiohttp.ClientSession() as client_session:

        # Create a TabdealClient object inside the async wrap
        my_client: TabdealClient = TabdealClient(USER_HASH, USER_AUTHORIZATION_KEY, client_session)

        # Run your desired commands, remember to `await` the methods as all of them (except a very few) are asynchronous
        bomeusdt_asset_id = await my_client.get_margin_asset_id("BOMEUSDT")

Learn more at the Documentation_.

Issues
------

* Most exceptions are caught broadly using the ``except Exception as exception``, This raises Pylint-W0718_, but i currently don't have a fix for it.

* Some parts of the code works flawlessly but raises Pylance-reportCallIssue_, Pylance-reportArgumentType_ or Mypy-call-overload_ which i mitigate by adding ``# type: ignore`` at the end of the line. This must be investigated later and fixed with a proper solution. I don't know a solution for it yet.

If you encounter any problems,
please `file an issue`_ along with a detailed description.

TODO
----

* Fix Pylint-W0718_ by catching specific exceptions instead of catching all exceptions.

* Fix Pylance-reportCallIssue_, Pylance-reportArgumentType_ or Mypy-call-overload_.

* Fix missing library stubs or py.typed marker ``MyPy-import-untyped``.

* Improve documentation for setup and usage.

* Use python built-in TypeGuard_ (3.10+) as a pre-processor on server responses to mitigate Type issues. (`TypeGuard example`_) (`Type Narrowing`_)

* `Configure Sphinx`_ thoroughly.
  
* Tidelift?

* Automatic stub generation and stub testing (stubgen & stubtest)

License
-------

Distributed under the terms of the `MIT license`_, *unofficial tabdeal api* is free and open source software.

Contributing
------------

Contributions are very welcome. To learn more, see the `Contributor Guide`_.

Credits
-------

This project was created with the help of `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template and `@fpgmaas`_'s `Cookiecutter Poetry`_ template.

..
    Links
.. 
    Badges
.. _package-url: https://pypi.org/project/unofficial-tabdeal-api/
.. _Read-The-Docs: https://unofficial-tabdeal-api.readthedocs.io/en/latest/?badge=latest
.. _Ruff: https://github.com/astral-sh/ruff
.. _Github Actions: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions
.. _Nox: https://github.com/wntrblm/nox
.. _Poetry: https://python-poetry.org/
.. _Contributors: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/graphs/contributors
.. _Stars: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/stargazers
.. _DOI: https://doi.org/10.5281/zenodo.15035227
.. _Total Downloads: https://pepy.tech/project/unofficial_tabdeal_api

..
    Installation
.. _pip: https://pypi.org/project/pip/
.. _PyPI: https://pypi.org/

..
    Issues
.. _file an issue: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues/new

..
    TODO
.. _Pylint-W0718: https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/broad-exception-caught.html
.. _Pylance-reportCallIssue: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportCallIssue
.. _Pylance-reportArgumentType: https://github.com/microsoft/pyright/blob/main/docs/configuration.md#reportArgumentType
.. _Mypy-call-overload: https://mypy.readthedocs.io/en/latest/error_code_list.html#code-call-overload
.. _TypeGuard: https://typing.python.org/en/latest/spec/narrowing.html#typeguard
.. _TypeGuard example: https://www.slingacademy.com/article/using-typeguard-in-python-python-3-10/
.. _Type Narrowing: https://mypy.readthedocs.io/en/stable/type_narrowing.html
.. _Configure Sphinx: https://www.sphinx-doc.org/en/master/usage/configuration.html

..
    Credits
.. _@cjolowicz: https://github.com/cjolowicz
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _@fpgmaas: https://github.com/fpgmaas
.. _Cookiecutter Poetry: https://github.com/fpgmaas/cookiecutter-poetry

..
    Ignore-in-readthedocs
.. _Documentation: https://unofficial-tabdeal-api.readthedocs.io/en/latest/
.. _Code of Conduct: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CODE_OF_CONDUCT.rst
.. _Contributor Guide: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CONTRIBUTING.rst
.. _MIT License: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/LICENSE
