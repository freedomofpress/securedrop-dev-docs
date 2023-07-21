Package repositories
====================

.. warning::
    This document describes some work that is still in progress and may not be 100% applicable yet.

SecureDrop publishes .deb and .rpm packages via apt and yum repositories, respectively.

Each package repository is maintained in a specific Git LFS repository that is published to `Cloudflare's R2
static hosting product <https://developers.cloudflare.com/r2/>`__. The Git repository contains the .deb and .rpm files, as well as the repository metadata.
When a new commit is pushed, GitHub Actions (GHA) publishes the contents of the "public" folder to Cloudflare.
We use `rclone <https://rclone.org/>`__ for this process to make it mostly vendor-neutral in case we
need to switch providers in the future.

For historical reasons, the apt repositories are on ``*.freedom.press`` while the yum respositories
are on ``*.securedrop.org``.

There are three levels of package repositories, which correspond to different stages
of the development process.

Test repositories
-----------------

* apt: `apt-test.freedom.press <https://apt-test.freedom.press>`__, via `securedrop-apt-test <https://github.com/freedomofpress/securedrop-apt-test>`__
* yum: `yum-test.securedrop.org <https://yum-test.securedrop.org>`__, via `securedrop-yum-test <https://github.com/freedomofpress/securedrop-yum-test>`__

Test repositories serve two primary functions. First, during the release process,
release candidate packages are published here to enable developers to perform QA,
including testing upgrades.

Second, nightly package builds are automatically pushed to test repositories by CI
to enable developers to test integrated systems with code straight from `main`.

The signing key for these test repositories is lower-security and stored in GHA. Packages
are automatically signed by a GHA workflow before being uploaded to Cloudflare.

QA repositories
---------------

* apt: `apt-qa.freedom.press <https://apt-qa.freedom.press>`__, via `securedrop-apt-prod's release branch <https://github.com/freedomofpress/securedrop-apt-prod/tree/release>`__
* yum: `yum-qa.securedrop.org <https://yum-qa.securedrop.org>`__, via `securedrop-yum-prod's release branch <https://github.com/freedomofpress/securedrop-yum-prod/tree/release>`__

QA repositories are used as the final QA step before a new version is fully released.
Developers upload candidate packages (using a non-release candidate version) to the
`release` branch, and sign the repository using the high-security, offline, SecureDrop signing key.

Once the new packages have been QA'd and approved, the `release` branch is merged into `main`,
which publishes the packages on the production repositories.

Production repositories
-----------------------

* apt: `apt.freedom.press <https://apt.freedom.press>`__, via `securedrop-apt-prod's main branch <https://github.com/freedomofpress/securedrop-apt-prod/tree/main>`__
* yum: `yum.securedrop.org <https://yum.securedrop.org>`__, via `securedrop-yum-prod's main branch <https://github.com/freedomofpress/securedrop-yum-prod/tree/main>`__

Production repositories are used by real deployments of SecureDrop. SecureDrop server
is configured to automatically fetch and install updates every 24 hours while SecureDrop Workstation
requires a manual updater run.

This repository is signed using the high-security, offline, SecureDrop signing key.

Historical setup
----------------

Historically each package repository was hosted on a dedicated virtual server, corresponding to the same Git LFS repositories.
The Git repository contained the .deb and .rpm files and in some cases, the repository metadata too. When a new commit
is pushed, a webhook instructed the server to pull new changes. A fallback cron job to git pull the repository also
ran every 15 minutes.
