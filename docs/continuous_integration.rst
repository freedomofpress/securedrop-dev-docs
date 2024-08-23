.. _ci_tests:

Continuous Integration
===============================

The SecureDrop project uses `GitHub Actions <https://docs.github.com/en/actions>`_ for
running automated continuous integration on code changes. You can get an overview of what
each project does by reviewing the ``Makefile`` and files in the ``.github/workflows`` folder of the project's repository.

Basics
------

Our CI runs a mixture of linters, tests and build processes to validate code submissions.

Most tasks have a corresponding ``make`` target that will run the same command locally. Common
targets across all our projects include:

* ``make lint``: run linters
* ``make fix``: apply automated fixes from formatters and linters
* ``make test``: run automated tests

In CI, these are run in a container using the corresponding Linux distribution (e.g. Debian or Fedora),
which can also be used to reproduce CI results locally. Some projects, like ``securedrop`` (server) and
``securedrop-workstation``, automatically run commands in containers.

Pull requests
-------------

Most CI jobs are `triggered <https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows>`_ by both ``push`` and ``pull_request`` events. The former is run against
your branch, while the latter is run against your branch merged into ``main`` (or ``develop``).


Special branch prefixes
-----------------------

In the ``securedrop`` repository, some slower jobs are only triggered if a specific branch prefix
is used when creating the pull request. Currently these are:

* ``stg-*``: runs a staging build in Google Cloud, see :ref:`Configuration Tests<config_tests>`
* ``l10n-*``: runs localization tests across all 20+ supported languages

Nightlies
---------

For ``securedrop-workstation`` and ``securedrop-client``, packages are built for every merged
commit as well as every night. These packages are published to the test yum and apt repositories.

A "nightlies" workflow runs in each repository that builds the respective packages. The workflow
uses an authenticated token for the ``sdcibot`` GitHub account to push the packages and build metadata
to ``build-logs``, ``securedrop-apt-test`` and ``securedrop-yum-test``.

The ``securedrop-apt-test`` and ``securedrop-yum-test`` repositories have a workflow that automatically
prunes older packages, also using a token for ``sdcibot`` to push to themselves.

Workstation CI
--------------

For testing ``securedrop-workstation``, we run a special CI job that virtualizes Qubes OS inside
of VMWare. Documentation for this is available in the `securedrop-workstation-ci <https://github.com/freedomofpress/securedrop-workstation-ci>`_
repository.
