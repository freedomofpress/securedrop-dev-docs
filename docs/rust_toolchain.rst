Rust toolchain maintenance
==========================

Unlike Python, which we get from Debian packages, we manage our own Rust toolchain
in the SecureDrop server dev environment and package builder.

Rust releases new versions every 6 weeks. We aim to stay within 2-3 versions of the
latest stable release, which allows us to update (at minimum) every 3-5 months.

Upgrading the toolchain
-----------------------

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
