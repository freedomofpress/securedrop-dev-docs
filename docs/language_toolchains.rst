Language toolchains
===================

Python
------

In nearly all cases we use the OS-provided version of Python, whether it's Ubuntu,
Debian or Fedora. In some cases we may also install Python dependencies using OS
packages, typically when it's something that's hard to build from scratch (e.g.
Python Qt or GTK bindings).

We rely on the OS for security updates, so we only upgrade major versions when we
upgrade OS versions.

With Python, we use a mix of ``pip``, ``poetry`` and ``uv`` for package management.
Older projects may still use ``pip-tools``.

Rust
----

Unlike Python, which we get from Debian packages, we manage our own Rust toolchain
in the SecureDrop server dev environment and package builder.

Rust releases new versions every 6 weeks. We aim to stay within 2-3 versions of the
latest stable release, which allows us to update (at minimum) every 3-5 months.

Upgrading
^^^^^^^^^

The Rust version is specified in a number of files, including:

* ``rust-toolchain.toml``
* Package builder's ``Dockerfile``
* Dev environment's ``Dockerfile``
* CI manifests

It is recommended to grep for the old version string to find any other places
it might also be used.

As of this writing, Rust code is used by Sequoia-PGP ``redwood`` bridge and ``cryptography``
dependency. The following test plan can be used for smoke testing those:

.. code:: markdown

    * [ ] CI passes, including deb building and staging build
    * [ ] Build new debs, deploy on a staging/prod instance:
       * [ ] Create a new source, upload a file.
       * [ ] Create new journalist, log in as them.
       * [ ] As the journalist, download the file and successfully decrypt it.


Node.js
-------

Currently our primary usage of Node.js is with Electron in the
SecureDrop App (still under development). Electron ships its own
version of Node.js, so we match that version in CI and elsewhere.

For package management, we are using `pnpm <https://pnpm.io/>`__ largely for its
better control over build scripts, and because it's generally faster than npm.
