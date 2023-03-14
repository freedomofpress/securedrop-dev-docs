Build metadata
==============

When we build packages to ship to users, we save and publish build metadata.
Currently this happens in the form of build logs and ``.buildinfo`` files, both
of which are published to the `build-logs <https://github.com/freedomofpress/build-logs>`__ repository.

Build logs
----------

When you build a package for release, you should should save your terminal output, including:

* Checking out the build tag and verifying that it is signed with the release key
* ``make build-debs`` (or equivalent) output
* SHA256 checksums of the built packages

These should be committed into the corresponding folder in the build-logs repository.

The goal with these build logs is to have a clear record of what happened during
the build process for the purpose of retrospectives. This can help us determine if
mistakes are made during the build (since some of the process is manual) and for
incident response.

buildinfo
---------

``.buildinfo`` files record information about the environment used to build the package
so that an external user can recreate that environment and reproduce the package. See
the `Debian documentation <https://wiki.debian.org/ReproducibleBuilds/BuildinfoFiles>`__ for more details.

When available, these should be committed into the ``buildinfo/`` folder. As these files
also contain SHA256 checksums of the packages, they can be omitted from the build log.

These are not yet `generated for RPM packages <https://github.com/freedomofpress/securedrop-builder/issues/418>`__.
