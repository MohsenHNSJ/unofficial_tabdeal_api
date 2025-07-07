======================
Unofficial Tabdeal API
======================
..
    Badges section

.. list-table::
    :stub-columns: 1

    * - Package
      - |version| |status| |supported-python-versions| |poetry| |release-to-pypi| |implementation| |wheel| |pydantic-badge|
    * - Quality Assurance
      - |sonar-quality-gate| |sonar-reliability| |sonar-maintainability| |sonar-technical-debt| |sonar-bugs| |sonar-code-smells|
    * - Stats
      - |contributors| |stars| |issues| |pull-requests| |sonar-lines-of-code| |repository-size|
    * - Tests
      - |nox| |codspeed| |pre-commit-ci| |types| |codecov| |scorecard|
    * - Security
      - |synk| |sonar-security| |sonar-vulnerabilities| |openssf|
    * - Linters
      - |ruff| |pre-commit| |megalinter| |mypy| |pylint|
    * - Activity
      - |maintenance| |commit-activity| |downloads|
    * - Misc
      - |contributor-covenant| |doi| |skeleton|
    * - Documentation
      - |documentation|
    * - License
      - |license|


🧭 Project overview
--------------------

Unofficial Tabdeal API is a modern, fully asynchronous Python wrapper for the Tabdeal_ cryptocurrency trading platform. Built from the ground up to replace the outdated and limited `official package`_, this library leverages Tabdeal's new backend API to offer safer and developer-friendly access to all available features.

This package supports both public and private endpoints ( such as placing orders, fetching balances, and managing trades ) and is designed with clarity, security, and performance in mind,
therefore, ideal for developers and algo traders who need reliable, complete, and secure access to Tabdeal's trading features.

✅ Key features
~~~~~~~~~~~~~~~~

* 🚀 Async-first: Designed to work efficiently in modern Python async environments.

* 🛡️ Safer interface: Raises clear, informative exceptions instead of vague errors.

* 🔧 Complete coverage: Aims to support all endpoints exposed by the new Tabdeal API.

* 🧪 Fully typed: Clean type hints across the codebase for better IDE support and readability.

* ✔️ Unit tested: Each function is tested to ensure reliability and correct behavior.

* 🧹 Linted and secure: Codebase follows modern Python best practices with multiple linters and security checks.


🛠️ Technical overview
----------------------

This package uses the website backend to communicate with the Tabdeal platform (``https://api-web.tabdeal.org``) rather than the original API at (``https://api1.tabdeal.org/api/v1``).

This enables more stable and reliable access to Tabdeal's features, as the new backend is designed to be more robust and feature-rich.

There are also exclusive features that aren't available in the original API, such as setting stop loss/take profit points and 60x margin leverage.

🧰 Tech stack
~~~~~~~~~~~~~~

* aiohttp_ 3.12.13

* pydantic_ 2.9.2

🏁 Getting started
-------------------

📋 Prerequisites
~~~~~~~~~~~~~~~~~

You need ``Authorization`` key and ``user-hash`` to use this package.

To obtain these credentials, follow these steps:

#. On a computer, open your internet browser and log-in to Tabdeal website

#. Navigate to settings page

#. Press F12 to open Developer tools

#. Navigate to Network panel

#. Refresh the website page and the network section should populate with many entries

#. Find the entry with ``wallet/`` name

#. Select it and in ``Headers`` section, under ``Request Headers``, you should find them

📦 Installation
~~~~~~~~~~~~~~~~

You can install *unofficial tabdeal api* via pip_ from PyPI_, requirements will be met automatically:

.. code-block:: sh

    pip install unofficial-tabdeal-api

⚙️ Usage
---------

#. Import ``TabdealClient`` from the package.

#. Initialize the ``TabdealClient`` with your ``Authorization`` key and ``user-hash`` information

#. Run your desired commands

.. code-block:: python

    # Import TabdealClient
    from unofficial_tabdeal_api import TabdealClient

    async def main():

        # Initialize a TabdealClient object
        my_client: TabdealClient = TabdealClient(USER_HASH, USER_AUTHORIZATION_KEY)

        # Run your desired commands, remember to `await` the methods as all of them (except a few) are asynchronous
        bomeusdt_asset_id = await my_client.get_margin_asset_id("BOMEUSDT")

Learn more in the Documentation_.

🐛 Issues
----------

If you encounter any problems,
please `file an issue`_ along with a detailed description.

⚖️ License
-----------

Distributed under the terms of the `MIT license`_, *unofficial tabdeal api* is free and open source software.

🤝 Contributing
----------------

Any contributions to this project are highly valued and appreciated. For detailed guidelines on how to contribute, please refer to the `Contributor Guide`_.

🌟 Credits
-----------

This project was created with the help of `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template and `@fpgmaas`_'s `Cookiecutter Poetry`_ template.

..
    Badges


.. |codecov| image:: https://codecov.io/gh/MohsenHNSJ/unofficial_tabdeal_api/graph/badge.svg?token=QWCOB4VHEP
    :target: CodeCov_
    :alt: Coverage status

.. |codspeed| image:: https://img.shields.io/endpoint?url=https://codspeed.io/badge.json
    :target: CodSpeed_
    :alt: CodSpeed

.. |commit-activity| image:: https://img.shields.io/github/commit-activity/m/MohsenHNSJ/unofficial_tabdeal_api?logo=git
    :target: `Commit Activity`_
    :alt: GitHub commit activity

.. |contributor-covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg?logo=contributorcovenant
    :target: `Code of Conduct`_
    :alt: Contributor Covenant

.. |contributors| image:: https://img.shields.io/github/contributors/MohsenHNSJ/unofficial_tabdeal_api.svg
    :target: Contributors_
    :alt: Contributors

.. |documentation| image:: https://readthedocs.org/projects/unofficial-tabdeal-api/badge/?version=latest
    :target: Read-The-Docs_
    :alt: Documentation Status

.. |doi| image:: https://zenodo.org/badge/917705429.svg
    :target: DOI_
    :alt: Digital Object Identifier

.. |downloads| image:: https://static.pepy.tech/badge/unofficial_tabdeal_api
    :target: `Total Downloads`_
    :alt: Total Downloads

.. |implementation| image:: https://img.shields.io/pypi/implementation/unofficial-tabdeal_api?logo=python
    :alt: PyPI - Implementation

.. |issues| image:: https://img.shields.io/github/issues/MohsenHNSJ/unofficial_tabdeal_api
    :target: Issues-link_
    :alt: GitHub Issues

.. |license| image:: https://img.shields.io/pypi/l/unofficial-tabdeal-api
    :target: `MIT License`_
    :alt: License

.. |maintenance| image:: https://img.shields.io/badge/Maintenance%20Intended-✔-green.svg
    :target: Unmaintained_
    :alt: Maintenance - intended

.. |megalinter| image:: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions/workflows/mega-linter.yml/badge.svg?branch=main
    :target: MegaLinter-Status_
    :alt: MegaLinter status

.. |mypy| image:: https://img.shields.io/badge/MyPy-Checked-blue
    :target: mypy-docs_
    :alt: Checked with MyPy

.. |nox| image:: https://img.shields.io/badge/%F0%9F%A6%8A-Nox-D85E00.svg
    :target: Nox_
    :alt: Nox

.. |openssf| image:: https://www.bestpractices.dev/projects/10685/badge
    :target: openssf-status_
    :alt: Open Source Security Foundation Best Practices Badge

.. |poetry| image:: https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json
    :target: poetry-website_
    :alt: Poetry

.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
    :target: Pre-commit_
    :alt: pre-commit

.. |pre-commit-ci| image:: https://results.pre-commit.ci/badge/github/MohsenHNSJ/unofficial_tabdeal_api/main.svg
    :target: Pre-commit-ci_
    :alt: pre-commit.ci status

.. |pull-requests| image:: https://img.shields.io/github/issues-pr/MohsenHNSJ/unofficial_tabdeal_api
    :target: `Pull Requests`_
    :alt: GitHub Pull Requests

.. |pydantic-badge| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json
    :target: pydantic_
    :alt: Pydantic

.. |pylint| image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: pylint-website_
    :alt: Linting with Pylint

.. |release-to-pypi| image:: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions/workflows/release-packge.yml/badge.svg
    :target: `Release to PyPI`_
    :alt: Release to PyPI status

.. |repository-size| image:: https://img.shields.io/github/repo-size/MohsenHNSJ/unofficial_tabdeal_api?color=BE81F7
    :alt: Repository Size

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square
    :target: Ruff_
    :alt: Ruff

.. |scorecard| image:: https://api.scorecard.dev/projects/github.com/MohsenHNSJ/unofficial_tabdeal_api/badge
    :target: scorecard-rating_
    :alt: OpenSSF Scorecard

.. |skeleton| image:: https://img.shields.io/badge/skeleton-2025-informational?color=000000
    :target: Skeleton_
    :alt: Skeleton

.. |sonar-bugs| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=bugs
    :target: sonar-qube-page_
    :alt: SonarQube Bugs

.. |sonar-code-smells| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=code_smells
    :target: sonar-qube-page_
    :alt: SonarQube Code Smells

.. |sonar-lines-of-code| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=ncloc
    :target: sonar-qube-page_
    :alt: SonarQube Lines of Code

.. |sonar-maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=sqale_rating
    :target: sonar-qube-page_
    :alt: SonarQube Maintainability Rating

.. |sonar-quality-gate| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=alert_status
    :target: sonar-qube-page_
    :alt: SonarQube Quality Gate

.. |sonar-qube| image:: https://sonarcloud.io/images/project_badges/sonarcloud-dark.svg
    :target: sonar-qube-page_
    :alt: SonarQube Cloud

.. |sonar-reliability| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=reliability_rating
    :target: sonar-qube-page_
    :alt: SonarQube Reliability Rating

.. |sonar-security| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=security_rating
    :target: sonar-qube-page_
    :alt: SonarQube Security Rating

.. |sonar-technical-debt| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=sqale_index
    :target: sonar-qube-page_
    :alt: SonarQube Technical Debt

.. |sonar-vulnerabilities| image:: https://sonarcloud.io/api/project_badges/measure?project=MohsenHNSJ_unofficial_tabdeal_api&metric=vulnerabilities
    :target: sonar-qube-page_
    :alt: SonarQube Vulnerabilities

.. |stars| image:: https://img.shields.io/github/stars/MohsenHNSJ/unofficial_tabdeal_api?style=social
    :target: Stars_
    :alt: Stars

.. |status| image:: https://img.shields.io/pypi/status/unofficial-tabdeal-api.svg
    :target: package-url_
    :alt: Status

.. |supported-python-versions| image:: https://img.shields.io/pypi/pyversions/unofficial-tabdeal-api?logo=python
    :target: package-url_
    :alt: Python Version

.. |synk| image:: https://img.shields.io/badge/Synk-white?logo=snyk&color=4C4A73
    :target: synk-website_
    :alt: Analyzed with Synk

.. |types| image:: https://img.shields.io/pypi/types/unofficial-tabdeal-api
    :alt: PyPI - Types

.. |version| image:: https://img.shields.io/pypi/v/unofficial-tabdeal-api.svg?logo=pypi
    :target: package-url_
    :alt: PyPI

.. |wheel| image:: https://img.shields.io/pypi/wheel/unofficial-tabdeal-api
    :alt: PyPI - Wheel


..
    Links
..
    Badges-links

.. _CodeCov: https://codecov.io/gh/MohsenHNSJ/unofficial_tabdeal_api
.. _CodSpeed: https://codspeed.io/MohsenHNSJ/unofficial_tabdeal_api
.. _Commit Activity: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/graphs/commit-activity
.. _Contributors: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/graphs/contributors
.. _DOI: https://doi.org/10.5281/zenodo.15035227
.. _Issues-link: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues
.. _MegaLinter-Status: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions?query=workflow%3AMegaLinter+branch%3Amain
.. _Nox: https://github.com/wntrblm/nox
.. _openssf-status: https://www.bestpractices.dev/projects/10685
.. _package-url: https://pypi.org/project/unofficial-tabdeal-api/
.. _poetry-website: https://python-poetry.org/
.. _Pre-commit: https://github.com/pre-commit/pre-commit
.. _Pre-commit-ci: https://results.pre-commit.ci/latest/github/MohsenHNSJ/unofficial_tabdeal_api/main
.. _Pull Requests: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/pulls
.. _pydantic: https://pydantic.dev
.. _pylint-website: https://github.com/pylint-dev/pylint
.. _Read-The-Docs: https://unofficial-tabdeal-api.readthedocs.io/en/latest/?badge=latest
.. _Release to PyPI: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/actions
.. _Ruff: https://github.com/astral-sh/ruff
.. _scorecard-rating: https://scorecard.dev/viewer/?uri=github.com/MohsenHNSJ/unofficial_tabdeal_api
.. _Skeleton: https://blog.jaraco.com/skeleton
.. _sonar-qube-page: https://sonarcloud.io/summary/new_code?id=MohsenHNSJ_unofficial_tabdeal_api
.. _Stars: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/stargazers
.. _synk-website: https://snyk.io/
.. _Total Downloads: https://pepy.tech/project/unofficial_tabdeal_api
.. _Unmaintained: http://unmaintained.tech/
.. _mypy-docs: https://mypy.readthedocs.io/en/stable/

..
    Project-overview-links

.. _official package: https://pypi.org/project/tabdeal-python/
.. _Tabdeal: https://tabdeal.org/

..
    Technical-overview-links

.. _aiohttp: https://docs.aiohttp.org/en/stable/

..
    Installation-links

.. _pip: https://pypi.org/project/pip/
.. _PyPI: https://pypi.org/

..
    Issues-links

.. _file an issue: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues/new

..
    Credits-links

.. _@cjolowicz: https://github.com/cjolowicz
.. _@fpgmaas: https://github.com/fpgmaas
.. _Cookiecutter Poetry: https://github.com/fpgmaas/cookiecutter-poetry
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python

..
    Ignore-in-readthedocs
.. _Code of Conduct: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CODE_OF_CONDUCT.rst
.. _Contributor Guide: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CONTRIBUTING.rst
.. _Documentation: https://unofficial-tabdeal-api.readthedocs.io/en/latest/
.. _MIT License: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/LICENSE
