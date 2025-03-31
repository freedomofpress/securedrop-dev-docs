Reproducible builds
===================

We have implemented `reproducible builds <https://reproducible-builds.org/docs/definition/>`_
for most of our projects (see the exceptions below).

Goals
-----

A developer should be able to build Debian and RPM packages and get bit-for-bit identical results
as another developer. This is primarily done at release time, to verify the packages were not altered
in some way.

We also want third-parties to be able to take our code and reproduce the output to verify we
are building from what we've published and not e.g. inserting secret backdoors.

We expect that any reproduction attempts will be done near the time of the release (on the scale of months).
While we are supportive of efforts to reproducibly rebuild packages from years ago, we are not explicitly
guaranteeing that.

Build environment
-----------------

Our primary strategy for having reproducible builds is using a containerized build environment (docker or podman).
By using containers, we ensure the build environment is:

* clean: no manual modifications have been made to it (aside from what is specified in a Dockerfile or equivalent)
* minimalist: only essential packages and build requirements are installed.
* up to date: all installed packages should be up to date and we should be able to verify this
* repeatable: it should be straightforward for another developer to set up an identical environment

Build metadata
--------------

We publish all the build metadata available to us, so that others have as much information as possible
when attempting to reproduce our builds. See :doc:`build metadata <build_metadata>` for more details.

Reproducible wheels
-------------------

Python packages with C or other native dependencies are often not reproducible because the build process happens
in a randomized temporary directory, which is then captured in the ``.so``. We build wheels ourselves in a fixed path to ensure they're reproducible,
see `securedrop-builder <https://github.com/freedomofpress/securedrop-builder>`_ for more details.


Not reproducible
----------------

Currently the ``securedrop-app-code`` package (`issue #5901 <https://github.com/freedomofpress/securedrop/issues/5901>`_)
and our Linux kernel builds (`issue #3 <https://github.com/freedomofpress/kernel-builder/issues/3>`_) are not reproducible.
