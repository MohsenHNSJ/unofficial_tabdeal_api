======================
Unofficial Tabdeal API
======================
..
    Badges section

.. image:: https://img.shields.io/pypi/v/unofficial-tabdeal-api.svg?style=flat-square
    :target: package-url_
    :alt: PyPI
.. image:: https://img.shields.io/pypi/status/unofficial-tabdeal-api.svg?style=flat-square
    :target: package-url_
    :alt: Status
.. image:: https://img.shields.io/pypi/pyversions/unofficial-tabdeal-api?style=flat-square
    :target: package-url_
    :alt: Python Version
.. image:: https://img.shields.io/pypi/l/unofficial-tabdeal-api?style=flat-square
    :target: `MIT License`_
    :alt: License
.. image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?style=flat-square
    :target: `Code of Conduct`_
    :alt: Contributor Covenant
.. image:: https://readthedocs.org/projects/unofficial-tabdeal-api/badge/?version=latest&style=flat-square
    :target: Read-The-Docs_
    :alt: Documentation Status


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

* Fix missing library stubs or py.typed marker ``MyPy-import-untyped``

* Improve documentation for setup and usage.

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

..
    Credits
.. _@cjolowicz: https://github.com/cjolowicz
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _@fpgmaas: https://github.com/fpgmaas
.. _Cookiecutter Poetry: https://github.com/fpgmaas/cookiecutter-poetry

..
    Ignore-in-readthedocs
.. _Documentation: https://unofficial-tabdeal-api.readthedocs.io/en/latest/
.. _Code of Conduct: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CODE_OF_CONDUCT.md
.. _Contributor Guide: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CONTRIBUTING.md
.. _MIT License: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/LICENSE.txt
