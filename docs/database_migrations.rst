Database Migrations
===================

SecureDrop uses Alembic_ for database schema migrations. This guide is not a complete explanation of
what ``alembic`` is or how it is used, so the original documentation should be read.

.. _Alembic: https://alembic.sqlalchemy.org/en/latest/

Migration Files
---------------

In the ``securedrop/`` directory, the file ``alembic.ini`` contains the configuration needed to run
``alembic`` commands, and the directory ``alembic/`` contains the Python code that executes
migrations.

The directory looks like this.

.. code-block:: none

    .
    ├── alembic
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    │       ├── 15ac9509fc68_init.py
    │       └── faac8092c123_enable_security_pragmas.py
    └── alembic.ini

The subdirectory ``versions/`` individual migrations that are generated by ``alembic``. In the
example above, there are two migrations. ``alembic`` orders these migrations based off of values in
the Python files, not off any sort of lexicographic ordering. The file
``faac8092c123_enable_security_pragmas.py`` has a module-level documentation string that specifies
that it comes after ``15ac9509fc68_init.py`` as well as variables used by alembic that specify the
ordering of migrations.

Deployment
----------

Database migrations are automatically applied to production instances via the command
``alembic upgrade head`` in the ``postinst`` script in the ``securedrop-app-code`` Debian package.
You do not need to worry about when or how these migrations are applied.

Developer Workflow
------------------

Updating the Models
~~~~~~~~~~~~~~~~~~~

When you want to modify the database schema, you need to add adjust the models in the file
``models.py``. All indices, constraints, or other metadata about the scheme needs to be in this
file. The development server creates tables directly from the subclasses of ``db.Model`` so that
they are available for manual and automated testing.

Creating Migrations
~~~~~~~~~~~~~~~~~~~

Once you are satisfied with your new model, ``alembic`` can auto-generate migrations using
SQLAlchemy metadata and comparing it to the schema of an up-to-date SQLite database. To generate a
new migration use the following steps.

.. code-block:: none

    cd securedrop/
    ./bin/dev-shell
    source bin/dev-deps
    maybe_create_config_py
    ./bin/new-migration 'my migration message'

This will output a new migration into ``alembic/versions/``. You will need to verify that this
migration produced the desired output. While still in the ``dev-shell``, you can run the following
command to see an output of the SQL that will be generated.

.. code-block:: none

    alembic upgrade head --sql

Unit Testing Migrations
~~~~~~~~~~~~~~~~~~~~~~~

The test suite already comes with a test runner (``test_alembic.py``) that runs a series of checks
to ensure migration's upgrade and downgrade commands are idempotent and don't break the database.
The test runner uses dynamic module import to iterate through all the migrations. You will need to
create a python module in the ``tests/migrations/`` directory. You module **MUST** be named
``migration_<revision identifier>.py``. For example, if your revision is named
``15ac9509fc68_init.py``, your test module will be named ``migration_15ac9509fc68.py``.
Example modules for the first two revisions are shown below.

.. code-block:: none

    tests/migrations/
    ├── __init__.py
    ├── migration_15ac9509fc68.py
    └── migration_faac8092c123.py


Your module **MUST** contain the following classes with the following attributes.

.. code:: python

    class UpgradeTester:

        def __init__(self, config):
            '''This function MUST accept an argument named `config`.
               You will likely want to save a reference to the config in your
               class so you can access the database later.
            '''
            self.config = config

        def load_data(self):
            '''This function loads data into the database and filesystem. It is
               executed before the upgrade.
            '''
            pass

        def check_upgrade(self):
            '''This function is run after the upgrade and verifies the state
               of the database or filesystem. It MUST raise an exception if the
               check fails.
            '''
            pass


    class DowngradeTester:

        def __init__(self, config):
            '''This function MUST accept an argument named `config`.
               You will likely want to save a reference to the config in your
               class so you can access the database later.
            '''
            self.config = config

        def load_data(self):
            '''This function loads data into the database and filesystem. It is
               executed before the downgrade.
            '''
            pass

        def check_downgrade(self):
            '''This function is run after the downgrade and verifies the state
               of the database or filesystem. It MUST raise an exception if the
               check fails.
            '''
            pass

Your migration test needs to load data that covers all edge cases such as potentially broken foreign
keys or columns with unexpected content.

Additionally, your test **MUST NOT** import anything from the ``models`` module as this will not
accurately test your migration, and it will likely break during future code changes. In fact, you
should use as few dependencies as possible in your test including other ``securedrop`` code as well
as external packages. This may be a rather annoying requirement, but it will make the tests more
robust against future code changes.

Release Testing Migrations
~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to ensure that migrations between from the previous to current version of SecureDrop apply
cleanly in production-like instances, we have a helper script that is designed to load
semi-randomized data into the database. You will need to modify the script ``loaddata.py`` to
include sample data. This sample data should intentionally include edge cases that might behave
strangely such as data whose nullability is only enforced by the application or missing files.

During QA, the release manager should follow these steps to test the migrations.

1. Checkout the previous SecureDrop release
2. Build Debian packages locally
3. Provision staging VMs
4. ``vagrant ssh app-staging``
5. ``sudo -u www-data bash``
6. ``cd /var/www/securedrop && ./loaddata.py``
7. Checkout the release candidate
8. Re-provision the staging VMs
9. Check that nothing went horribly wrong
