Linux kernel maintenance
========================

We build and publish our own Linux kernels with additional
`grsecurity hardening patches`_.
The `kernel-builder`_ repository contains scripts that fetch upstream
kernel tarballs plus grsecurity patches and produces Debian packages.

Testing a new kernel
--------------------

The following steps should be performed for all of the `recommended hardware`_:

#. Install the new kernel packages on your *Monitor Server*, then reboot. Verify with ``uname -r`` that you are using the new kernel.
#. If it doesn't boot, see the `Troubleshooting Kernel Updates`_ documentation.
#. Verify ``paxtest`` doesn't return any errors nor warnings.
#. Verify the `spectre-meltdown-checker`_ doesn't return any errors nor warnings.
#. Upgrade your *Application Server* to the new kernel and reboot.
#. Run basic smoke tests of SecureDrop by verifying you can send a submission and a journalist can reply.

.. _`grsecurity hardening patches`: https://grsecurity.net/`
.. _`kernel-builder`: https://github.com/freedomofpress/kernel-builder/
.. _`recommended hardware`: https://docs.securedrop.org/en/stable/hardware.html#application-and-monitor-servers
.. _`Troubleshooting Kernel Updates`: https://docs.securedrop.org/en/stable/kernel_troubleshooting.html
.. _`spectre-meltdown-checker`: https://github.com/speed47/spectre-meltdown-checker/
