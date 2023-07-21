SecureDrop package repositories
===============================

SecureDrop publishes .deb and .rpm packages via apt and yum repositories, respectively.

Each package repository is hosted on a dedicated virtual server and corresponds to a specific Git LFS repository.
The Git repository contains the .deb and .rpm files and in some cases, the repository metadata too. When a new commit
is pushed, a webhook instructs the server to pull new changes. A fallback cron job to git pull the repository also
runs every 15 minutes.

There are three levels of package repositories, which correspond to different stages
of the development process.

Test repositories
-----------------

* apt: apt-test.freedom.press, via securedrop-apt-test
* yum: yum-test.securedrop.org, via securedrop-yum-test

Test repositories serve two primary functions. First, during the release process,
release candidate packages are published here to enable developers to perform QA,
including testing upgrades.

Second, nightly package builds are automatically pushed to test repositories by CI
to enable developers to test integrated systems with code straight from `main`.

Packages pushed to test repositories are automatically signed with a lower-security
"test repository" key.

QA repositories
---------------

* apt: apt-qa.freedom.press, via securedrop-apt-prod's release branch
* yum: yum-qa.securedrop.org, via securedrop-yum-prod's release branch

QA repositories are used as the final QA step before a new version is fully released.
Developers upload candidate packages (using a non-release candidate version) to the
`release` branch, and sign the repository using the high-security SecureDrop signing key.

Once the new packages have been QA'd and approved, the `release` branch is merged into `main`,
which publishes the packages on the production repositories.

Production repositories
-----------------------

* apt: apt.freedom.press, via securedrop-apt-prod's main branch
* yum: yum.securedrop.org, via securedrop-yum-prod's main branch

Production repositories are used by real deployments of SecureDrop. SecureDrop server
is configured to automatically fetch and install updates every 24 hours while SecureDrop Workstation
requires a manual updater run.
