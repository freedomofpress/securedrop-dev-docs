Setting up the SecureDrop Workstation
=====================================
The SecureDrop Workstation based on `Qubes OS <https://www.qubes-os.org/>`_
is a project currently in the beta stages of software development which aims to
improve journalists' experience working with SecureDrop while retaining
the current security and privacy features SecureDrop provides.

Installing the project requires an up-to-date Qubes 4.2 installation
running on a machine with at least 16GB of RAM (32 GB recommended).

The project is currently in a closed beta, and we do not recommend
installing it for production purposes. Documentation for end users is
being developed `here <https://workstation.securedrop.org>`__. The
instructions below are intended for developers.

Install Qubes
-------------

Before trying to use this project, install `Qubes
4.2.1 <https://www.qubes-os.org/downloads/>`__ on your development
machine. Accept the default VM configuration during the install process.

After installing Qubes, you must update both dom0 and the base templates
to include the latest versions of apt packages. Open a terminal in
``dom0`` by clicking on the Qubes menu top-right of the screen and
left-clicking on Terminal Emulator and run:

::

   sudo qubes-dom0-update

After dom0 updates complete, reboot your computer to ensure the updates
have been properly applied. Finally, update all existing TemplateVMs:

::

   qubes-update-gui

Select all VMs marked as **updates available**, then click **Next**.
Once all updates have been applied, you’re ready to proceed. Choose the
environment that you wish to set up and then follow the applicable
instructions:

-  The staging environment uses the ``yum-test.securedrop.org`` and
   ``apt-test.freedom.press`` repositories, and is configured to use the
   ``main`` component for apt packages. It will typically install the
   most recent release candidate packages (which could be more recent
   than the production packages if a release is underway).

-  The development environment uses the ``yum-test.securedrop.org`` and
   ``apt-test.freedom.press`` repositories, and is configured to use the
   ``nightly`` component for apt package. It does not alter power
   management settings on your laptop to prevent suspension to disk (a
   security measure for production environments, which the staging
   environment preserves to be more faithful to prod-like settings).

-  The production environment uses ``yum.securedrop.org`` and
   ``apt.freedom.press`` repositories, verified using the production
   signing key. Its setup is not covered below; see our `production
   install
   docs <https://workstation.securedrop.org/en/stable/admin/install/overview.html>`__
   for details.

Development Environment
-----------------------

Download, Configure, Copy to ``dom0``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This repository contains the specification for an RPM package, which
contains the provisioning logic. By following the instructions below,
you will build this RPM package locally from a ``git`` checkout in your
development VM, copy it to ``dom0``, install it, and run the
provisioning code to set up a SecureDrop Workstation in the development
environment configuration.

Decide on a VM to use for development. We recommend creating a
standalone VM called ``sd-dev`` by following `these
instructions <https://developers.securedrop.org/en/latest/setup_development.html#qubes>`__.

Clone the `securedrop-workstation` repo to your preferred location on that VM.

Qubes provisioning is handled by Salt on ``dom0``, so this project must
be copied there from your development VM.

.. include:: includes/dom0-warning.txt

That process is a little tricky, but here’s one way to do it: assuming
this code is checked out in your ``sd-dev`` VM at
``/home/user/projects/securedrop-workstation``, run the following in
``dom0``:

::

   qvm-run --pass-io sd-dev 'tar -c -C /home/user/projects/ securedrop-workstation' | tar xvf -

(Be sure to include the space after ``/home/user/projects/``.) After
that initial manual step, the code in your development VM may be copied
into place on ``dom0`` by setting the ``SECUREDROP_DEV_VM`` and
``SECUREDROP_DEV_DIR`` environmental variables to reflect the VM and
directory to which you’ve cloned this repo, and running ``make clone``
from the root of the project on ``dom0``:

::

   [dom0]$ export SECUREDROP_DEV_VM=sd-dev    # set to your dev VM
   [dom0]$ export SECUREDROP_DEV_DIR=/home/user/projects/securedrop-workstation    # set to your working directory
   [dom0]$ cd ~/securedrop-workstation/
   [dom0]$ make clone    # build RPM package and copy repo to dom0

**NOTE:** The destination directory on ``dom0`` is not customizable; it
must be ``securedrop-workstation`` in your home directory.

If you plan to work on the `SecureDrop
Client <https://github.com/freedomofpress/securedrop-client>`__ code,
also run this command in ``dom0``:

::

   qvm-tags sd-dev add sd-client

Doing so will permit the ``sd-dev`` AppVM to make RPC calls with the
same privileges as the ``sd-app`` AppVM.


Run Development SecureDrop Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here, you will setup a development version of the SecureDrop server to
which your workstation will connect. Alternatively, you can setup
:doc:`virtualized staging environments on Qubes OS <virtual_environments>`,
which is slightly more involved.

- Setup a :doc:`SecureDrop (server) development environment <setup_development>` on Qubes.

.. note:: You will need to run the following step every time that you want
   to login on SecureDrop client.

- Start the securedrop server in ``sd-dev`` qube with use ``make dev-tor``


Configure the Workstation
~~~~~~~~~~~~~~~~~~~~~~~~~

In the output of the `make dev-tor` command ran in the previous section, there
should be a section that looks like this:

::

   {
      "submission_key_fpr": "65A1B5FF195B56353CC63DFFCC40EF1228271441",
      "hidserv": {
         "hostname": "jpweqok4r43xp4si5pattodglw2btdqlpz2utvn4mkwnx2iwbmp4v2id.onion",
         "key": "DAZHRYYKWHQCIRUMEVIRSOUZA4MKU4C7WPDWLIVB3TMZWZH2V5MA"
      },
      "environment": "prod",
      "vmsizes": {
         "sd_app": 10,
         "sd_log": 5
      }
   }

Save this text in the file ``securedrop-workstation/config.json``.

Next, set the default encryption key (for development purposes only):

::

   cd securedrop-workstation
   cp sd-journalist.sec.example sd-journalist.sec

Then, in ``dom0``, clone the workstation again, to obtain these new files:

::

   [dom0]$ cd ~/securedrop-workstation/
   [dom0]$ make clone


Provision the VMs
~~~~~~~~~~~~~~~~~

Once the configuration is done and this directory is copied to ``dom0``,
you must update existing Qubes templates and use ``make`` to handle all
provisioning and configuration by your unprivileged user. Before you do
so, you may wish to increase the scrollback in the dom0 terminal from
1000 (the default) to 100000 or unlimited, to ensure you can review any
errors in the verbose output.

Then run the following command to set up a development environment:

::

   make dev

Note that this target automatically sets the ``environment`` variable in
``config.json`` to ``dev``, regardless of its current value, before
provisioning. It identifies the latest RPM you have built (using
``scripts/prep-dev``), installs it, and runs the ``sdw-admin --apply``
command to provision the SecureDrop Workstation.

The build process takes quite a while. You will be presented with a
dialog asking how to connect to Tor: you should be able to select the
default option and continue. If you want to refer back to the
provisioning log for a given VM, go to
``/var/log/qubes/mgmt-<vm name>.log`` in ``dom0``. You can also monitor
logs as they’re being written via ``journalctl -ef``. This will display
logs across the entire system so it can be noisy. It’s best used when
you know what to look for, at least somewhat, or if you’re provisioning
one VM at a time.

When the installation process completes, a number of new VMs will be
available on your machine, all prefixed with ``sd-``.

Editing the configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

When developing on the Workstation, make sure to edit files in
``sd-dev``, then copy them to dom0 via ``make clone && make dev`` to
reinstall them. Any changes that you make to the
~/securedrop-workstation folder in dom0 will be overwritten during
``make clone``. Similarly, any changes you make to e.g. ``/srv/salt/``
in dom0 will be overwritten by ``make dev``.

Staging Environment
-------------------

Update ``dom0``, ``fedora-40-xfce``, ``whonix-gateway-17`` and ``whonix-workstation-17`` templates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates to these VMs will be performed by the installer and updater, but
updating them prior to install makes it easier to debug any errors.

Before proceeding to updates, we must ensure that ``sys-whonix`` can
bootstrap to the Tor network. In the Qubes menu, navigate to
``sys-whonix`` and click on ``Anon Connection Wizard`` and click
``Next`` and ensure the Tor Bootstrap process completes successfully.

In the Qubes Menu, select the cog icon to access the Settings submenu,
navigate to ``Qubes Tools`` and click on ``Qubes Update``. In the updater,
select all VMs in the list, then click  ``Next`` and wait for updates to complete.

Choose your installation method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can install the staging environment in two ways:

-  If you have an up-to-date clone of this repo with a valid
   configuration in ``dom0``, you can use the ``make staging`` target to
   provision a staging environment. Prior to provisioning,
   ``make staging`` will set your ``config.json`` environment to
   ``staging``.

-  If you want to download a specific version of the RPM, and follow a
   verification procedure similar to that used in a production install,
   follow the process in the following sections.

Download and install securedrop-workstation-dom0-config package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since ``dom0`` does not have network access, we will need to download
the ``securedrop-workstation-dom0-config`` package in a Fedora-based VM.
We can use the default Qubes-provisioned ``work`` VM. If you perform
these changes in the ``work`` VM or another AppVM, they won’t persist
across reboots (recommended).

In a terminal in ``work``, run the following commands:

1. Import the test signing key:

::

   [user@work ~]$ wget https://raw.githubusercontent.com/freedomofpress/securedrop-workstation/master/sd-workstation/apt-test-pubkey.asc
   [user@work ~]$ sudo rpmkeys --import apt-test-pubkey.asc

2. Configure the test repository

Populate ``/etc/yum.repos.d/securedrop-temp.repo`` with the following
contents:

::

   [securedrop-workstation-temporary]
   enabled=1
   baseurl=https://yum-test.securedrop.org/workstation/dom0/f37
   name=SecureDrop Workstation Qubes initial install bootstrap

3. Download the RPM package

::

   [user@work ~]$ dnf download securedrop-workstation-dom0-config

The RPM file will be downloaded to your current working directory.

4. Verify RPM package signature

::

   [user@work ~]$ rpm -Kv securedrop-workstation-dom0-config-x.y.z-1.fc37.noarch.rpm

The output should match the following, and return ``OK`` for all lines
as follows:

::

   securedrop-workstation-dom0-config-x.y.z-1.fc37.noarch.rpm:
       Header V4 RSA/SHA256 Signature, key ID 2211b03c: OK
       Header SHA1 digest: OK
       V4 RSA/SHA256 Signature, key ID 2211b03c: OK
       MD5 digest: OK

5. Transfer and install RPM package in ``dom0``

.. include:: includes/dom0-warning.txt

In ``dom0``, run the following commands (changing the version number to
its current value):

::

   [dom0]$ qvm-run --pass-io work 'cat /home/user/securedrop-workstation-dom0-config-x.y.z-1.fc37.noarch.rpm' > securedrop-workstation.rpm
   sudo dnf install securedrop-workstation.rpm

The provisioning scripts and tools should now be in place, and you can
proceed to the workstation configuration step.

Configure the Workstation
~~~~~~~~~~~~~~~~~~~~~~~~~

Your workstation configuration will reside in
``/usr/share/securedrop-workstation-dom0-config/`` and will contain
configuration information specific to your SecureDrop instance:

1. Populate ``config.json`` with your instance-specific variables. Set
   ``environment`` to ``staging``
2. Move your submission private key to ``sd-journalist.sec``

.. _provision-the-vms-1:

Provision the VMs
~~~~~~~~~~~~~~~~~

In a terminal in ``dom0``, run the following commands:

::

   [dom0]$ sdw-admin --apply
