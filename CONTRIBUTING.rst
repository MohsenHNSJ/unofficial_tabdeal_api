=================
Contributor Guide
=================

.. contents::
   :local:
   :depth: 2

Thank you for your interest in improving this project.

Contributions are welcome, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

This project is open-source under the `MIT License`_.

You can contribute in many ways:

* :ref:`Report Bugs<Report Bugs>`
* :ref:`Fix Bugs<Fix Bugs>`
* :ref:`Request Features<Request Features>`
* :ref:`Implement Features<Implement Features>`
* :ref:`Write Documentation<Write Documentation>`
* :ref:`Submit Feedback<Submit Feedback>`

Ready to start? Check out the guidelines:

* :ref:`How to set up your development environment<Dev Environment>`
* :ref:`Possible issues you may encounter<Possible Issues>`
* :ref:`Documenting your code<Documenting>`
* :ref:`How to test the project<Testing>`
* :ref:`Coding Style<Coding Style>`
* :ref:`How to submit changes<Submitting Changes>`

Here is a list of important resources for contributors:

* `Source Code`_
* Documentation_
* `Issue Tracker`_
* `Code of Conduct`_

----

.. _Report Bugs:

Report Bugs
-----------

Report bugs on the `Issue Tracker`_.

When filing an issue, make sure to answer these questions:

- Which operating system and Python version are you using?
- Which version of this project are you using?
- What did you do?
- What did you expect to see?
- What did you see instead?
- Any details about your local setup that might be helpful in troubleshooting

The best way to get your bug fixed is to provide a test case,
and/or steps to reproduce the issue.

.. _Fix Bugs:

Fix Bugs
--------

Look through the `GitHub issues`_ for bugs.
Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

.. _Request Features:

Request Features
----------------

Request features on the `Issue Tracker`_.

If you are proposing a new feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

.. _Implement Features:

Implement Features
------------------

Look through the `GitHub issues`_ for features.
Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

.. _Write Documentation:

Write Documentation
-------------------

Unofficial Tabdeal API could always use more documentation, whether as part of the `official docs`_, in docstrings, or even on the web in blog posts, articles, and such.

.. _Submit Feedback:

Submit Feedback
---------------

The best way to send feedback is to file an issue at `Issue Tracker`_

----

.. _Dev Environment:

How to set up your development environment
------------------------------------------

Ready to contribute? Here's how to set up `Unofficial Tabdeal API`_ for local development.

Use `VS Code`_ `Dev Containers`_ extension and clone this repository.

Requirements will be installed automatically

We use Poetry_ for managing virtual environments and dependencies.

For managing linters, static-analysis, and other tools, we use pre-commit_

Install pre-commit_ hooks after cloning, run:

.. code-block:: sh

    pre-commit install

Using pre-commit_ ensures PRs match the linting requirements of the codebase.

.. _Possible Issues:

Possible issues you may encounter
---------------------------------

If you encounter an error about not setting user.name and user.email for committing with git:

* Run the following commands on your **local machine** terminal to set-up your git connection

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

.. _Documenting:

Documenting your code
---------------------

Whenever possible, please add docstrings to your code!

We use `google-style docstrings`_.

To confirm docstrings are valid, build the docs by running :code:`nox -t docs`

Good docstrings include information like:

1. If not immediately obvious, what is the intended use-case? When should this function be used?
2. What happens during errors/edge-cases.
3. When dealing with physical values, include units.

.. _Testing:

How to test the project
-----------------------

We use the pytest_ framework for unit testing.

Ideally, all new code is paired with new unit tests to exercise that code.

If fixing a bug, consider writing the test first to confirm the existence of the bug, and to confirm that the new code fixes it.

Unit tests should only test a single concise body of code.

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

.. _Coding Style:

Coding Style
------------

In an attempt to keep consistency and maintainability in the code-base,
here are some high-level guidelines for code that might not be enforced by linters:

* Use f-strings.
* Keep/cast path variables as :code:`pathlib.Path` objects. Do not use :code:`os.path`.
  For public-facing functions, cast path arguments immediately to :code:`Path`.
* Avoid deeply nested code. Techniques like returning early and breaking up a complicated function into multiple functions results in easier-to-read and test code.
* Consider if you are double-name-spacing and how modules are meant to be imported.
  E.g. it might be better to name a function :code:`read` instead of :code:`image_read` in the module :code:`my_package/image.py`.
  Consider the module name-space and whether or not it's flattened in :code:`__init__.py`.

.. _Submitting Changes:

How to submit changes
---------------------

Open a `pull request`_ and target the ``dev`` branch to submit changes to this project.

DO NOT target the ``main`` branch, as it is reserved for releases.

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
.. _GitHub Issues: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/issues
.. _Poetry: https://python-poetry.org/
.. _Nox: https://nox.thea.codes/en/stable/index.html
.. _stackoverflow: https://stackoverflow.com/questions/6448242/git-push-error-insufficient-permission-for-adding-an-object-to-repository-datab/6448326#6448326
.. _pytest: https://docs.pytest.org/en/stable/
.. _CodSpeed: https://codspeed.io/MohsenHNSJ/unofficial_tabdeal_api
.. _VS Code: https://code.visualstudio.com/
.. _Dev Containers : https://containers.dev/
.. _Ruff: https://docs.astral.sh/ruff/
.. _MyPy: https://www.mypy-lang.org/
.. _pre-commit: https://pre-commit.com/
.. _pull request: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/pulls
.. _Unofficial Tabdeal API: https://pypi.org/project/unofficial-tabdeal-api/
.. _google-style docstrings: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/#google-vs-numpy

..
    Ignore-in-readthedocs
.. _Documentation: https://unofficial-tabdeal-api.readthedocs.io/en/latest/index.html
.. _official docs: https://unofficial-tabdeal-api.readthedocs.io/en/latest/index.html
.. _MIT License: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/LICENSE
.. _Code of Conduct: https://github.com/MohsenHNSJ/unofficial_tabdeal_api/blob/main/CODE_OF_CONDUCT.rst
