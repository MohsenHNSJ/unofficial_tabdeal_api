======================
Unofficial Tabdeal API
======================
..
    Badges section

.. list-table::
    :stub-columns: 1

    * - Package
      - |version| |status| |supported-python-versions| |poetry| |release-to-pypi| |implementation| |wheel| |maintenance|
    * - Documentation
      - |documentation|
    * - Tests
      - |nox| |codspeed| |pre-commit-ci| |types| |codecov| |synk| |scorecard| |sonar-quality-gate|
    * - Linters
      - |ruff| |pre-commit| |megalinter| |mypy| |pylint|
    * - License
      - |license|
    * - Stats
      - |contributors| |stars| |downloads| |issues| |pull-requests| |commit-activity| |sonar-lines-of-code| |sonar-reliability| |sonar-security| |sonar-maintainability| |sonar-technical-debt| |sonar-vulnerabilities| |sonar-bugs| |sonar-code-smells|
    * - Misc
      - |contributor-covenant| |doi| |skeleton| |openssf|


a Package to communicate with Tabdeal platform

Features
--------

* Transfer USDT to/from margin asset from/to account balance

* Get account USDT balance

* Get order state

* Get history of all orders

* Get all open orders

* Open margin order

* Set SL/TP for margin order

* Proper exception handling

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

First, obtain the ``Authorization`` key and ``user-hash``:

* On a computer, open your internet browser and log-in to Tabdeal website

* Navigate to settings page

* Press F12 to open Developer tools

* Navigate to Network panel

* Refresh the website page and the network section should populate with many entries

* Find the entry with ``wallet/`` name

* Select it and in ``Headers`` section, under ``Request Headers``, you should find them

Now initialize the ``TabdealClient`` with your information and do as you wish :)

.. code-block:: python

    # Import requirements and TabdealClient
    import aiohttp
    from unofficial_tabdeal_api import TabdealClient

    async def main():

        # Initialize aiohttp.ClientSession asynchronously
        async with aiohttp.ClientSession() as client_session:

            # Create a TabdealClient object inside the async wrap
            my_client: TabdealClient = TabdealClient(USER_HASH, USER_AUTHORIZATION_KEY, client_session)

            # Run your desired commands, remember to `await` the methods as all of them (except a few) are asynchronous
            bomeusdt_asset_id = await my_client.get_margin_asset_id("BOMEUSDT")

Learn more at the Documentation_.

Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.

TODO
----

* Improve documentation for setup and usage.

* Use python built-in TypeGuard_ (3.10+) as a pre-processor on server responses to mitigate Type issues. (`TypeGuard example`_) (`Type Narrowing`_)

* `Configure Sphinx`_ thoroughly.

License
-------

Distributed under the terms of the `MIT license`_, *unofficial tabdeal api* is free and open source software.

Contributing
------------

Contributions are welcome. To learn more, see the `Contributor Guide`_.

Credits
-------

This project was created with the help of `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template and `@fpgmaas`_'s `Cookiecutter Poetry`_ template.

..
    Badges

.. |version| image:: https://img.shields.io/pypi/v/unofficial-tabdeal-api.svg?logo=pypi
    :target: package-url_
    :alt: PyPI

.. |status| image:: https://img.shields.io/pypi/status/unofficial-tabdeal-api.svg
    :target: package-url_
    :alt: Status

.. |supported-python-versions| image:: https://img.shields.io/pypi/pyversions/unofficial-tabdeal-api?logo=python
    :target: package-url_
    :alt: Python Version

.. |license| image:: https://img.shields.io/pypi/l/unofficial-tabdeal-api
    :target: `MIT License`_
    :alt: License

.. |contributor-covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?logo=contributorcovenant
    :target: `Code of Conduct`_
    :alt: Contributor Covenant

.. |documentation| image:: https://readthedocs.org/projects/unofficial-tabdeal-api/badge/?version=latest
    :target: Read-The-Docs_
    :alt: Documentation Status

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square
    :target: Ruff_
    :alt: Ruff

.. |nox| image:: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
    :target: Nox_
    :alt: Nox

.. |poetry| image:: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
    :target: poetry-website_
    :alt: Poetry

.. |release-to-pypi| image:: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions/workflows/release-packge.yml/badge.svg
    :target: `Release to PyPI`_
    :alt: Release to PyPI status

.. |contributors| image:: https://img.shields.io/github/contributors/MohsenHNSJ/unofficial_tabdeal_api.svg
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

.. |codspeed| image:: https://img.shields.io/endpoint?url=https://codspeed.io/badge.json
    :target: CodSpeed_
    :alt: CodSpeed

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
    :target: Pre-commit_
    :alt: pre-commit

.. |pre-commit-ci| image:: https://results.pre-commit.ci/badge/github/MohsenHNSJ/unofficial_tabdeal_api/main.svg
    :target: Pre-commit-ci_
    :alt: pre-commit.ci status

.. |implementation| image:: https://img.shields.io/pypi/implementation/unofficial-tabdeal_api?logo=python
    :alt: PyPI - Implementation

.. |types| image:: https://img.shields.io/pypi/types/unofficial-tabdeal-api
    :alt: PyPI - Types

.. |wheel| image:: https://img.shields.io/pypi/wheel/unofficial-tabdeal-api
    :alt: PyPI - Wheel

.. |issues| image:: https://img.shields.io/github/issues/MohsenHNSJ/unofficial_tabdeal_api
    :target: Issues-link_
    :alt: GitHub Issues

.. |pull-requests| image:: https://img.shields.io/github/issues-pr/MohsenHNSJ/unofficial_tabdeal_api
    :target: `Pull Requests`_
    :alt: GitHub Pull Requests

.. |commit-activity| image:: https://img.shields.io/github/commit-activity/m/MohsenHNSJ/unofficial_tabdeal_api?logo=git
    :target: `Commit Activity`_
    :alt: GitHub commit activity

.. |codecov| image:: https://codecov.io/gh/MohsenHNSJ/unofficial_tabdeal_api/graph/badge.svg?token=QWCOB4VHEP
    :target: CodeCov_
    :alt: Coverage status

.. |skeleton| image:: https://img.shields.io/badge/skeleton-2025-informational?color=000000
    :target: Skeleton_
    :alt: Skeleton

.. |maintenance| image:: https://img.shields.io/badge/Maintenance%20Intended-✔-green.svg
    :target: Unmaintained_
    :alt: Maintenance - intended

.. |megalinter| image:: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions/workflows/mega-linter.yml/badge.svg?branch=main
    :target: MegaLinter-Status_
    :alt: MegaLinter status

.. |openssf| image:: https://www.bestpractices.dev/projects/10685/badge
    :target: openssf-status_
    :alt: Open Source Security Foundation Best Practices Badge

.. |mypy| image:: https://img.shields.io/badge/MyPy-Checked-blue
    :target: mypy-docs_
    :alt: Checked with MyPy

.. |synk| image:: https://img.shields.io/badge/Synk-white?logo=snyk&color=4C4A73
    :target: synk-website_
    :alt: Analyzed with Synk

.. |scorecard| image:: https://api.scorecard.dev/projects/github.com/MohsenHNSJ/unofficial_tabdeal_api/badge
    :target: scorecard-rating_
    :alt: OpenSSF Scorecard

.. |pylint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: pylint-website_
    :alt: Linting with Pylint

.. |sonar-qube| image:: https://sonarcloud.io/images/project_badges/sonarcloud-dark.svg
    :target: sonar-qube-page_
    :alt: SonarQube Cloud

.. |sonar-quality-gate| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=alert_status
    :target: sonar-qube-page_
    :alt: SonarQube Quality Gate

.. |sonar-bugs| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=bugs
    :target: sonar-qube-page_
    :alt: SonarQube Bugs

.. |sonar-code-smells| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=code_smells
    :target: sonar-qube-page_
    :alt: SonarQube Code Smells

.. |sonar-lines-of-code| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=ncloc
    :target: sonar-qube-page_
    :alt: SonarQube Lines of Code

.. |sonar-reliability| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=reliability_rating
    :target: sonar-qube-page_
    :alt: SonarQube Reliability Rating

.. |sonar-security| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=security_rating
    :target: sonar-qube-page_
    :alt: SonarQube Security Rating

.. |sonar-technical-debt| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=sqale_index
    :target: sonar-qube-page_
    :alt: SonarQube Technical Debt

.. |sonar-maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=sqale_rating
    :target: sonar-qube-page_
    :alt: SonarQube Maintainability Rating

.. |sonar-vulnerabilities| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=vulnerabilities
    :target: sonar-qube-page_
    :alt: SonarQube Vulnerabilities

..
    Links
..
    Badges-links
.. _package-url: https://pypi.org/project/unofficial-tabdeal-api/
.. _Read-The-Docs: https://unofficial-tabdeal-api.readthedocs.io/en/latest/?badge=latest
.. _Ruff: https://github.com/astral-sh/ruff
.. _Release to PyPI: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions
.. _Nox: https://github.com/wntrblm/nox
.. _Contributors: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/graphs/contributors
.. _Stars: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/stargazers
.. _DOI: https://doi.org/10.5281/zenodo.15035227
.. _Total Downloads: https://pepy.tech/project/unofficial_tabdeal_api
.. _CodSpeed: https://codspeed.io/MohsenHNSJ/unofficial_tabdeal_api
.. _Pre-commit: https://github.com/pre-commit/pre-commit
.. _Pre-commit-ci: https://results.pre-commit.ci/latest/github/MohsenHNSJ/unofficial_tabdeal_api/main
.. _Issues-link: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues
.. _Pull Requests: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/pulls
.. _Commit Activity: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/graphs/commit-activity
.. _CodeCov: https://codecov.io/gh/MohsenHNSJ/unofficial_tabdeal_api
.. _Skeleton: https://blog.jaraco.com/skeleton
.. _Unmaintained: http://unmaintained.tech/
.. _MegaLinter-Status: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions?query=workflow%3AMegaLinter+branch%3Amain
.. _openssf-status: https://www.bestpractices.dev/projects/10685
.. _scorecard-rating: https://scorecard.dev/viewer/?uri=github.com/MohsenHNSJ/unofficial_tabdeal_api
.. _synk-website: https://snyk.io/
.. _mypy-docs: https://mypy.readthedocs.io/en/stable/
.. _poetry-website: https://python-poetry.org/
.. _pylint-website: https://github.com/pylint-dev/pylint
.. _sonar-qube-page: https://sonarcloud.io/summary/new_code?id=MohsenHNSJ_unofficial_tabdeal_api
..
    Installation
.. _pip: https://pypi.org/project/pip/
.. _PyPI: https://pypi.org/

..
    Issues
.. _file an issue: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues/new

..
    TODO
.. _TypeGuard: https://typing.python.org/en/latest/spec/narrowing.html#typeguard
.. _TypeGuard example: https://www.slingacademy.com/article/using-typeguard-in-python-python-3-10/
.. _Type Narrowing: https://mypy.readthedocs.io/en/stable/type_narrowing.html
.. _Configure Sphinx: https://www.sphinx-doc.org/en/master/usage/configuration.html
.. _Pytest parallel benching: https://docs.codspeed.io/benchmarks/python#running-benchmarks-in-parallel-ci-jobs
.. _Github parallel benching: https://docs.codspeed.io/integrations/ci/github-actions#running-benchmarks-in-parallel-ci-jobs

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
