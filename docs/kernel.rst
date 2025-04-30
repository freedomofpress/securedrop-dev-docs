Linux kernel maintenance
========================

We build and publish our own Linux kernels with additional `grsecurity hardening
patches`_.  This process is automated in the `kernel-builder`_ repository.

#. Follow the instructions in `kernel-builder`_ for building and uploading new
   kernel packages.
#. Once the new packages have been reviewed and merged in the
   `securedrop-apt-test`_ repository, they will be `automatically tested`_
   on the hardware we maintain in our kernel test farm.
#. Wait for ``sdcibot`` to file a ``New Linux kernel`` ticket (`example`_) in
   the `securedrop`_ repository with its test results.
#. The packages can then be promoted to `securedrop-apt-prod`_.


Testing a new kernel manually
-----------------------------

These are the steps ``sdcibot`` performs in its `automatic testing`_ of new
kernel packages on all of our `recommended hardware`_:

#. Install the new kernel packages on your *Monitor Server* using unattended-upgrades,
   e.g. ``sudo apt update && sudo unattended-upgrades --debug`` or wait for the automatic
   nightly upgrade.
#. Reboot. Verify with ``uname -r`` that you are using the new kernel.
#. If it doesn't boot, see the `Troubleshooting Kernel Updates`_ documentation.
#. Install the ``paxtest`` package, run with ``sudo paxtest blackhat``, and verify it doesn't
   return any new errors nor warnings.
#. Install `spectre-meltdown-checker`_ and the ``binutils`` package, run with
   ``sudo ./meltdown-checker``, and verify it doesn't return any errors nor warnings.
#. Upgrade your *Application Server* to the new kernel and reboot.

You may optionally also:

7. Run basic smoke tests of SecureDrop by verifying you can send a submission and a journalist can reply.

.. _`grsecurity hardening patches`: https://grsecurity.net/
.. _`kernel-builder`: https://github.com/freedomofpress/kernel-builder/
.. _`recommended hardware`: https://docs.securedrop.org/en/stable/hardware.html#application-and-monitor-servers
.. _`Troubleshooting Kernel Updates`: https://docs.securedrop.org/en/stable/kernel_troubleshooting.html
.. _`spectre-meltdown-checker`: https://github.com/speed47/spectre-meltdown-checker/
.. _`securedrop-apt-test`: https://github.com/freedomofpress/securedrop-apt-test
.. _`automatically tested`: https://github.com/freedomofpress/securedrop/blob/kernel-test/install_files/ansible-base/roles/kernel-test/files/kernel-auto-test.py
.. _`securedrop`: https://github.com/freedomofpress/securedrop
.. _`example`: https://github.com/freedomofpress/securedrop/issues/7482
.. _`securedrop-apt-prod`: https://github.com/freedomofpress/securedrop-apt-prod
.. _`automatic testing`: https://github.com/freedomofpress/securedrop/blob/kernel-test/install_files/ansible-base/roles/kernel-test/files/kernel-auto-test.py
