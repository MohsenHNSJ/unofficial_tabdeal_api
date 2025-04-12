=================
Contributor Guide
=================

Thank you for your interest in improving this project.
This project is open-source under the `MIT License`_ and
welcomes contributions in the form of bug reports, feature requests, and pull requests.

Here is a list of important resources for contributors:

* `Source Code`_
* Documentation_
* `Issue Tracker`_
* `Code of Conduct`_

How to report a bug
-------------------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

How to request a feature
------------------------

Request features on the `Issue Tracker`_.

How to set up your development environment
------------------------------------------

Use `VS Code`_ `Dev Containers`_ extension and clone this repository.

Requirements will be installed automatically

Install pre-commit hooks using :code:`pre-commit install`

Possible issues you may encounter
---------------------------------

If you encounter an error about not setting user.name and user.email for committing with git:

* Run the following commands on your local machine terminal to set-up your git connection

.. code-block:: sh

    git config --global user.name "YOUR_USER_NAME"

    git config --global user.email "YOUR_EMAIL"


* Rebuild the container

If you encounter an error about not having the permission to .git/object for committing with git:
:code:`insufficient permission for adding an object to repository database .git/objects`

* Run the following commands on dev container terminal:

.. code-block:: sh

    sudo chmod -R a+rwX .

    sudo find . -type d -exec chmod g+s '{}' +

* Check the output of shared repository:

.. code-block:: sh

    git config core.sharedRepository

* If the output of last command is empty or does not include :code:`group` , :code:`true` or :code:`1`, run the following:

.. code-block:: sh

    git config core.sharedRepository group

* Finally, fix the root cause by following the answer from stackoverflow_.

How to test the project
-----------------------

Run the full test suite:

.. code-block:: sh

    nox -t test

Lint using Ruff_:

.. code-block:: sh

    nox -t fix

Typecheck using MyPy_:

.. code-block:: sh

    nox -t type

Build and live-preview documentation:

.. code-block:: sh

    nox -t preview

Run pre-commit_ hooks:

.. code-block:: sh

    nox -t pre-commit

List the available Nox_ sessions:

.. code-block:: sh

    nox --list

Unit tests are located in the *tests* directory,
and are written using the pytest_ testing framework.

How to submit changes
---------------------

Open a `pull request`_ to submit changes to this project.

Your pull request needs to meet the following guidelines for acceptance:

- The Nox test suite must pass without errors and warnings.
- Include unit tests. This project maintains high code coverage.
- If your changes add functionality, update the documentation accordingly.

Feel free to submit early, though—we can always iterate on this.

It is recommended to open an issue before starting work on anything.
This will allow a chance to talk it over with the owners and validate your approach.

..
    Links
.. _Source Code: https://github.com/MohsenHNSJ/unofficial_tabdeal_api
.. _Issue Tracker: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues
.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/en/stable/index.html
.. _stackoverflow: https://stackoverflow.com/a/6448326
.. _pytest: https://docs.pytest.org/en/stable/
.. _CodSpeed: https://codspeed.io/MohsenHNSJ/unofficial_tabdeal_api
.. _VS Code: https://code.visualstudio.com/
.. _Dev Containers : https://containers.dev/
.. _Ruff: https://docs.astral.sh/ruff/
.. _MyPy: https://www.mypy-lang.org/
.. _pre-commit: https://pre-commit.com/
.. _pull request: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/pulls

..
    Ignore-in-readthedocs
.. _Documentation: https://unofficial-tabdeal-api.readthedocs.io/en/latest/index.html
.. _MIT License: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/LICENSE
.. _Code of Conduct: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CODE_OF_CONDUCT.rst
