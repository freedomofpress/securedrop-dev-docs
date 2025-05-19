Package repositories
====================

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
to enable developers to test integrated systems with code straight from `main`. Nightlies
are stored in a separate component: "nightlies" in apt, "fXX-nightlies" in yum.

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

How it works technically
------------------------

This is an overview of the workflow, for step-by-step instructions, see
the :doc:`server release management <release_management>` and
:doc:`workstation release management <workstation_release_management>` docs.

1. New packages are committed to the relevant Git LFS repository:

   * Nightlies: by GitHub Actions
   * Test/QA/Prod: by a maintainer

2. If this is a yum repository containing RPMs, the individual RPMs are signed:

   * Test: by GitHub Actions, using the low-security test key
   * QA/Prod: by a maintainer, using the offline SecureDrop release key

3. Repository metadata is updated, including generation of ``index.html``:

   * Test: by the ``.github/workflows/sign.yml`` GitHub Actions workflow
   * QA/Prod: by a maintainer, by running ``./tools/publish`` locally (this script
     is a misnomer as it doesn't actually publish the packages)

4. If this is an apt repository, the ``Release`` files are signed:

   * Test: by the ``.github/workflows/sign.yml`` GitHub Actions workflow
   * QA/Prod: by a maintainer, using the offline SecureDrop release key

5. Once pushed to the correct branch, a GitHub Actions workflow publishes the
   "public" (yum) or "repo/public" (apt) folder to Cloudflare R2.

   We use rclone for this purpose, and in theory are entirely
   vendor neutral and can switch to any another S3-like service.
