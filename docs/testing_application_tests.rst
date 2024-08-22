.. _app_tests:

Testing: Application Tests
==========================

The application test suite uses pytest_, selenium_, and other Python tools
to comprehensively test the SecureDrop server.

The application tests consist of unit tests for the Python application code
and functional tests that verify the functionality of the application code
from the perspective of the user through a web browser.

.. _pytest: https://docs.pytest.org/en/latest/
.. _selenium: https://www.selenium.dev/documentation/

Running the Application Tests
-----------------------------

The tests are written to be run inside the development container:

.. code:: sh

    make test

If you just want to run the functional tests, you can use:

.. code:: sh

    make test-functional

Similarly, if you want to run a single test, you can specify it through the
file, class, and test name:

.. code:: sh

    securedrop/bin/dev-shell bin/run-test \
        tests/test_journalist.py::TestJournalistApp::test_invalid_credentials

Page Layout Tests
~~~~~~~~~~~~~~~~~

You can check the rendering of the layout of each page in each translated
language using the page layout tests. These will generate screenshots of
each page and can be used for example to update the SecureDrop user guides
when modifications are made to the UI.

To run just these tests:

.. code:: sh

    make test-pageslayout


Updating the Application Tests
------------------------------

Unit tests are stored in the ``securedrop/tests/`` directory and functional
tests are stored in the functional test directory::

    securedrop/tests/
    ├── functional
    │   ├── test_admin_interface.py
    │   ├── test_submit_and_retrieve_file.py
    │   │               ...
    │   └── submission_not_in_memory.py
    ├── utils
    │   ├── db_helper.py
    │   ├── env.py
    │   └── asynchronous.py
    ├── test_journalist.py
    ├── test_source.py
    │        ...
    └── test_store.py

``securedrop/tests/utils`` contains helper functions for writing tests.
If you want to add a test, you should see if there is an existing file
appropriate for the kind of test, e.g. a new unit testing ``manage.py``
should go in ``test_manage.py``.
