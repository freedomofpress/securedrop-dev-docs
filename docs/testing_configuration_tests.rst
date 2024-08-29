.. _config_tests:

Testing: Configuration Tests
============================

Testinfra_ tests verify the end state of a full SecureDrop server, whether on
physical hardware or in staging VMs. Any changes to the Ansible configuration
should have a corresponding test.

.. _Testinfra: https://testinfra.readthedocs.io/en/latest/

Installation
------------

.. code:: sh

    pip install --no-deps --require-hashes -r securedrop/requirements/python3/develop-requirements.txt


Running the Config Tests
------------------------

Testinfra tests are executed against a virtualized staging environment. To
provision the environment and run the tests, run the following commands:

.. code:: sh

    make build-debs
    make staging
    make testinfra

Test failure against any host will generate a report with informative output
about the specific test that triggered the error. Molecule
will also exit with a non-zero status code.


Updating the Config Tests
-------------------------

Changes to the Ansible config should result in failing config tests, but
only if an existing task was modified. If you add a new task, make
sure to add a corresponding spectest to validate that state after a
new provisioning run. Tests import variables from separate YAML files
than the Ansible playbooks: ::

    molecule/testinfra/staging/vars/
    ├── app-prod.yml
    ├── app-staging.yml
    ├── mon-prod.yml
    ├── mon-staging.yml
    └── staging.yml

Any variable changes in the Ansible config should have a corresponding
entry in these vars files. These vars are dynamically loaded for each
host via the ``molecule/testinfra/staging/conftest.py`` file. Make sure to add
your tests to the relevant location for the host you plan to test: ::

    molecule/testinfra/staging/app/
    ├── apache
    │   ├── test_apache_journalist_interface.py
    │   ├── test_apache_service.py
    │   ├── test_apache_source_interface.py
    │   └── test_apache_system_config.py
    ├── test_apparmor.py
    ├── test_appenv.py
    ├── test_network.py
    └── test_ossec.py

In the example above, to add a new test for the ``app-staging`` host,
add a new file to the ``testinfra/staging/app`` directory.

.. tip:: Read :ref:`updating_ossec_rules` to learn how to write tests for the
         OSSEC rules.

Config Test Layout
------------------

With some exceptions, the config tests are broken up according to platform definitions in the
Molecule configuration: ::

    molecule/testinfra/staging
    ├── app
    ├── app-code
    ├── common
    ├── mon
    ├── ossec
    └── vars

Ideally the config tests would be broken up according to roles,
mirroring the Ansible configuration. Prior to the reorganization of
the Ansible layout, the tests are rather tightly coupled to hosts. The
layout of config tests is therefore subject to change.

Running the CI Staging Environment
----------------------------------

The staging environment can also run via CI in Google Cloud (GCE). These tests are
run every night or if a member of the ``freedomofpress`` Github Organization
pushes to a branch that starts with ``stg-``. Please ask in your PR if you'd like
someone to run the tests for you.

The tests can also be run manually with a Google Cloud Platform account and Docker
installed locally:

Source the setup script using the following command:

.. code:: sh

    source ./devops/gce-nested/ci-env.sh

You will be prompted for the values of the required environment variables. There
are some defaults set that you may want to change. You will need to export
``GOOGLE_CREDENTIALS`` with `authentication details <https://cloud.google.com/docs/authentication/use-cases>`_
for your GCP account, which is outside the scope of this guide. Some parameters
are specific to FPF's GCE setup and may need adjusting if you are running elsewhere.

Then to run the tests locally:

.. code:: sh

    make ci-go

You can use ``./devops/gce-nested/ci-runner.sh`` to provision the remote hosts
while making changes, including rebuilding the Debian packages used in the
Staging environment. See :doc:`virtual_environments` for more information.
