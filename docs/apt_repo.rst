SecureDrop apt Repository
=========================

This document contains brief descriptions of the Debian packages
hosted and maintained by Freedom of the Press Foundation in our apt
repository (`apt.freedom.press`_).

linux-image-\*-grsec
    This package contains the Linux kernel image, patched with grsecurity.
    Listed as a dependency of ``securedrop-grsec``.

`ossec-agent <https://github.com/ossec/ossec-hids>`_
    Installs the OSSEC agent, repackaged for Ubuntu.
    Listed as a dependency of ``securedrop-ossec-agent``.

`ossec-server <https://github.com/ossec/ossec-hids>`_
    Installs the OSSEC manager, repackaged for Ubuntu.
    Listed as a dependency of ``securedrop-ossec-server``.

securedrop-app-code
    Packages the SecureDrop application code, Python pip dependencies and
    AppArmor profiles.

securedrop-ossec-agent
    Installs the SecureDrop-specific OSSEC configuration for the *Application Server*.

securedrop-ossec-server
    Installs the SecureDrop-specific OSSEC configuration for the *Monitor Server*.

securedrop-grsec
    SecureDrop grsecurity kernel metapackage, depending on the latest version
    of ``linux-image-*-grsec``.

securedrop-keyring
    Packages the public signing key for this apt repository.
    Allows for managed key rotation via automatic updates, as implemented in
    `SecureDrop 0.3.10`_.

All `SecureDrop Client <https://github.com/freedomofpress/securedrop-client>`_ component packages.
    See :doc:`workstation_release_management` for more information.

.. note::
   The SecureDrop install process configures a custom Linux kernel hardened
   with the grsecurity patch set. Only binary images are hosted in the apt
   repo. For source packages, see the `Source Offer`_.

.. _SecureDrop 0.3.10: https://github.com/freedomofpress/securedrop/blob/c5b4220e04e3c81ad6f92d5e8a92798f07f0aca2/changelog.md
.. _apt.freedom.press: https://apt.freedom.press
.. _`Source Offer`: https://github.com/freedomofpress/securedrop/blob/develop/SOURCE_OFFER


.. _dbgsym-packages:

About dbgsym packages
---------------------

A
`debug symbols package <https://wiki.debian.org/DebugPackage>`_ is a Debian package
that includes static debug symbols and allows for generating a backtrace or other
diagnostic information in the event of a crash, for example
`with gdb <https://wiki.debian.org/HowToGetABacktrace/#Running_gdb>`_. These packages
have a ``-dbgsym.deb`` suffix on Debian, and a ``-dbgsym.ddeb`` suffix (which we 
`rename <https://github.com/freedomofpress/securedrop/blob/b7bda4fe7badd5267a829f5bfe243fd13db9178e/builder/build-debs-securedrop.sh#L35-L37>`_
to to ``-dbgsym.deb`` for consistency) on Ubuntu. These packages are generated
during the build process for components that include compiled binaries, such as
for SecureDrop components with Rust or C code, and they do not make any
other changes (i.e, they do not enable debug logs).

When building non-kernel production Debian packages, follow the relevant Release Management
documentation to commit the dbgsym packages along with the regular production
packages. These packages are automatically placed in a separate repo component (``main-debug``) in
`securedrop-apt-prod <https://github.com/freedomofpress/securedrop-apt-prod>`_.

Currently, we publish dbgsym packages for: ``securedrop-app-code`` (core),
``securedrop-client``, ``securedrop-proxy`` (workstation). Kernel builds also
generate dbgsym packages, but they are not published due to their prohibitive size.
