SecureDrop Workstation Development
==================================

This project’s development requires different workflows for working on
provisioning components and working on submission-handling scripts.

For developing salt states and other provisioning components, work is
done in a development VM and changes are made to individual state and
top files there. In the ``dom0`` copy of this project: - ``make clone``
is used to build a new version of the RPM and copy the contents of your
working directory (including the RPM) from your development VM to
``dom0`` - ``make <vm-name>`` can be used to rebuild an individual VM -
``make dev`` installs the latest locally present RPM and performs the
full installation.

Note that ``make clone`` requires two environment variables to be set:
``SECUREDROP_DEV_VM`` must be set to the name of the VM where you’ve
been working on the code, the ``SECUREDROP_DEV_DIR`` should be set to
the directory where the code is checked out on your development VM.

For work on components such as the SecureDrop Client, see their
respective repositories for developer documentation.

Testing
-------

Tests should cover two broad domains. First, we should assert that all
the expected VMs exist and are configured as we expect (with the correct
NetVM, with the expected files in the correct place). Second, we should
end-to-end test the document handling scripts, asserting that files
present in the ``sd-proxy`` VM correctly make their way to the
``sd-app`` AppVM, and are opened correctly in disposable VMs.

Configuration Tests
~~~~~~~~~~~~~~~~~~~

These tests assert that expected scripts and configuration files are in
the correct places across the VMs. These tests can be found in the
``tests/`` directory. They can be run from the project’s root directory
on ``dom0`` with:

::

   make test

Note that since tests confirm the states of provisioned VMs, they should
be run *after* all the VMs have been built with ``make dev``.

Individual tests can be run with ``make <test-name>``, where
``test-name`` is one of ``test-base``, ``test-app``, ``test-proxy``,
``test-whonix`` or ``test-gpg``.

Be aware that running tests *will* power down running SecureDrop VMs,
and may result in *data loss*. Only run tests in a development / testing
environment.

Automatic updates
-----------------

Double-clicking the “SecureDrop” desktop icon will launch a preflight
updater that applies any necessary updates to VMs, and may prompt a
reboot. In a development environment, this will install the latest
nightly packages, and the latest RPM published to ``yum-test``.

Manually updating dom0 code
---------------------------

To update code in ``dom0`` manually, e.g., to a specific branch or tag
of this repository, use the ``sd-dev`` AppVM that was created during the
install. For example, to build a specific tag, from your checkout
directory, run the following commands (replace ``<tag>`` with the tag of
the release you are working with):

::

   git fetch --tags
   git tag -v <tag>
   git checkout <tag>

In ``dom0``:

::

   make clone
   make dev

The ``make clone`` command will build a new version of the RPM package
that contains the provisioning logic in your development VM (e.g.,
``sd-dev``) and copy it to ``dom0``.

Building the Templates
----------------------

To build the base template, please follow the instructions in
https://github.com/freedomofpress/qubes-template-securedrop-workstation

Building workstation deb packages
---------------------------------

Debian packages for the SecureDrop Workstation components are maintained
in a separate repository:
https://github.com/freedomofpress/securedrop-builder/

Building workstation rpm packages
---------------------------------

::

   make dom0-rpm

The build assumes use of Debian Stable as the build environment. You can
install the necessary dependencies from system packages via the
``make install-deps`` target.
