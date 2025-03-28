SecureDrop Workstation Release Management
=========================================

SecureDrop Workstation code spans across two repositories:

-  https://github.com/freedomofpress/securedrop-client (Debian packages)
-  https://github.com/freedomofpress/securedrop-workstation (RPM
   package)

The components in the Debian packages are all released together, while the workstation RPM package is released independently.

Release a Debian package
========================

Releasing a release candidate (RC) package is the first step before you begin QA or any signing ceremonies. Even when you are
releasing a hotfix, RC packages are still recommended for QA purposes.

Production releases will require at least two maintainers, one of which will need access to the SecureDrop release key.

Step 0: Tracking issue
----------------------

Before beginning the release proces, create a tracking issue titled ``Release <package name> <version>``. It should contain
estimated timelines and assignees for release management, QA, and stakeholder communications. Pin the issue for ease of access
and visibility.

Step 1: Create a release candidate (RC) tag
-------------------------------------------

1. Create a release branch named ``release/<major>.<minor>.<patch>``.
2. Ensure that the version is set to the expected value; if not, increment it as needed using ``update_version.sh``.
3. Push a commit adding the changelog for this release.
4. Push an RC tag in the format ``<major>.<minor>.<patch>~rcN`` on your new commit. We will be building from this tag in the next step.
5. Unless this is a patch-level release, create a PR to bump the version on ``main``
   to ``<major>.<minor+1>.<patch>-rc1``. In other words, if you are in the process of
   releasing ``0.5.0``, ``main`` should be bumped to ``0.6.0-rc1``.

Step 2: Build and deploy the package to ``apt-test``
----------------------------------------------------

1. Clone ``securedrop-client`` and ``securedrop-builder``.

  .. code-block:: sh

   git clone git@github.com:freedomofpress/securedrop-client.git
   git clone git@github.com:freedomofpress/securedrop-builder.git

2. Check out the newly pushed tag and then build the packages.

  .. code-block:: sh

   cd securedrop-client
   git checkout <major>.<minor>.<patch>~rcN
   make build-debs

3. Save and publish :doc:`build metadata <build_metadata>`.
4. Open a PR to https://github.com/freedomofpress/securedrop-apt-test with the packages you want to deploy.
   Once merged, the packages will be deployed to https://apt-test.freedom.press.

Step 3: Begin QA
----------------

You can now start the QA process! If a bug is found, a fix should be developed, merged into the main branch and
cherry-picked into the release branch. If desired, release another RC set of packages for further testing.

Once QA testers are satisfied with the packages, you are ready to move on to the next step.

Step 4: Create a release tag
----------------------------

1. Update the changelog and version. Remove any references to the RC versions from the changelogs.
2. Generate a release tag named ``<major>.<minor>.<patch>`` (same as the previous tags, without the ``~rcN`` part).
3. :ref:`Sign the tag with the SecureDrop release key` or ask another maintainer to do this and push the signed tag

Step 5: Build and deploy the packages to ``apt-qa``
---------------------------------------------------

1. Clone ``securedrop-client`` and ``securedrop-builder``.

  .. code-block:: sh

   git clone git@github.com:freedomofpress/securedrop-client.git
   git clone git@github.com:freedomofpress/securedrop-builder.git

2. Check out the newly pushed tag and then build the packages.

  .. code-block:: sh

   cd securedrop-client
   git tag -v <major>.<minor>.<patch> # Signed by SecureDrop Release Key
   git checkout <major>.<minor>.<patch>
   make build-debs

3. Save and publish :doc:`build metadata <build_metadata>`.
4. Add your packages to a new branch called ``release`` in https://github.com/freedomofpress/securedrop-apt-prod. Include all .deb packages built by the client, including ``-dbgsym`` packages. ``-dbgsym`` packages belong in the ``main-debug`` component repo. See :ref:`Notes on dbgsym-packages <dbgsym-packages>` for more information.
5. Update the apt repo distribution files by running ``./tools/publish`` and push those changes to the ``release`` branch as well.
6. :ref:`Regenerate and sign the apt release file` or ask another maintainer to do this. The packages will now be installable from https://apt-qa.freedom.press.
7. Open a PR to merge the ``release`` branch into ``main``.
8. Another maintainer should also build the packages (following the same steps as earlier) and verify their newly built packages
   are `bit-for-bit identical <https://reproducible-builds.org/docs/definition/>`_ to those pushed to apt-qa.

Step 6: Perform the ``apt-qa`` preflight check
----------------------------------------------
First, provision a production workstation from the most recently-released
``securedrop-workstation-dom0-config`` production package. Ensure your machine
has been updated (either via Qubes native updater or SDW GUI updater).

At minimum, perform the full test. Additional QAers may perform smoketest to
save time if there is already full test coverage.

**Full test (includes updater)**

1. As root, edit ``/srv/salt/sd-default-config.yml`` so that the ``prod`` ``apt_repo_url`` points to ``https://apt-qa.freedom.press``.
2. Run the SDW GUI updater. To force an updater run, invoke the updater via ``/opt/securedrop/launcher/sdw-launcher.py --skip-delta 0``.
3. Start the Client application, and observe the updated version string, indicating the required packages were installed. Perform testing according to the test plan.

**Smoketest (no updater run)**

1. Start the Template VMs.
2. In each template VM, edit ``/etc/apt/sources.list.d/securedrop_workstation.list`` file to point to https://apt-qa.freedom.press.
3. Update the package system and install the new packages via ``apt update && apt upgrade -y``.
4. Verify that the updated packages were installed in the templates. Shut down template VMs and all VMs associated with SecureDrop Workstation.
5. Start the Client application and perform testing according to test plan.

Step 7: Deploy the package to ``apt-prod``
------------------------------------------

1. In ``securedrop-apt-prod``, merge the ``release`` branch into ``main`` to deploy your package to https://apt.freedom.press.
2. Once you see the package land on https://apt.freedom.press, run the updater to install it in a production environment and ensure that it works as expected.
3. In the source repository (e.g., ``securedrop-client``), port the changelog to the ``main`` branch.
   Ensure that the version number on ``main`` designates it as RC1 for the *next* release.

Release an RPM package
======================

Release ``securedrop-workstation-dom0-config``
----------------------------------------------

1.  Verify the tag of the project you wish to build:
    ``git tag -v VERSION`` and ensure the tag is signed with the
    official release key.
2.  ``git checkout VERSION``
3.  Now you are ready to build. Build RPMs following the documentation
    in an environment sufficient for building production artifacts. For
    ``securedrop-workstation`` you run ``make build-rpm`` to build the
    RPM.
4.  sha256sum the built RPM (and store hash in the build
    logs/commit message).
5.  Commit the (unsigned) version of this RPM to the ``release`` branch in the
    `securedrop-yum-prod <https://github.com/freedomofpress/securedrop-yum-prod>`__
    repository.
6.  Copy the RPM to the signing environment.
7.  Verify integrity of RPM prior to signing (use sha256sums to
    compare). **Note for reviewers:** Using ``rpm --delsign`` on a
    signed artifact (for example, a release candidate) in order to
    verify the checksum of the unsigned .rpm file must be done in the
    same type of build environment (Linux distribution and ``rpm``
    version) as the .rpm was built in, or the checksums may not match.
8.  Sign RPM in place (see Signing section below).
9.  Move the signed RPM back to the environment for committing to the
    lfs repository.
10. Save and publish :doc:`build metadata <build_metadata>`.
11. Commit the RPM in a second commit on the ``release`` branch in
    `securedrop-yum-prod <https://github.com/freedomofpress/securedrop-yum-prod>`__.
12. Run the `./tools/publish` script to update repository metadata and commit the result.
13. Create a PR to merge ``release`` into ``main``. At this point, the package will be
    available on `yum-qa.securedrop.org <https://yum-qa.securedrop.org>`__.
14. Once the PR is merged, the changes will be available on `yum.securedrop.org <https://yum.securedrop.org>`__.

Signing procedures
==================

.. _Sign the tag with the SecureDrop release key:

Sign the tag with the SecureDrop release key
--------------------------------------------

1. If the tag does not already exist, create a new annotated and unsigned tag: ``git tag -a VERSION``.
2. Output the tag to a file: ``git cat-file tag VERSION > VERSION.tag``.
3. Copy the tag file into your signing environment and then verify the tag commit hash.
4. Sign the tag with the SecureDrop release key: ``gpg --armor --detach-sign VERSION.tag``.
5. Append ASCII-armored signature to tag file (ensure there are no blank lines): ``cat VERSION.tag.sig >> VERSION.tag``.
6. Move tag file with signature appended back to the release environment.
7. Delete old unsigned tag: ``git tag -d VERSION``.
8. Create new signed tag: ``git mktag < VERSION.tag > .git/refs/tags/VERSION``.
9. Verify the tag's signature: ``git tag -v VERSION``.
10. Push the tag to the shared remote: ``git push origin VERSION``.

.. _Regenerate and sign the apt release file:

Regenerate and sign the apt release file
----------------------------------------

1. From the ``release`` branch containing the new package, update the apt repository distribution files.

  .. code-block:: sh

   git clone https://github.com/freedomofpress/securedrop-apt-prod
   cd securedrop-apt-prod
   git checkout -b release
   ./tools/publish

2. Copy the regenerated file called ``Release`` into your signing environment and then verify the hash to ensure the file transfer was successful.
3. Sign the ``Release`` file with the SecureDrop release key.

  .. code-block:: sh

   gpg --armor --detach-sign Release

4. Copy the ``Release.gpg`` file into your release environment and move it to ``repo/public/dists/<debian-codename>/`` on your ``release`` branch.
5. Verify that the release file was signed with the production key.

  .. code-block:: sh

   gpg --verify ./repo/public/dists/<debian-codename>/Release{.gpg,}

Sign the RPM package
--------------------

The entire RPM must be signed. This process also requires a Fedora
machine/VM on which the GPG signing key (either in GPG keyring or in
qubes-split-gpg) is setup. You will need to add the public key to RPM
for verification (see below).

``rpm -Kv`` indicates if digests and sigs are OK. Before signature it
should not return signature, and ``rpm -qi <file>.rpm`` will indicate an
empty Signature field. Set up your environment (for prod you can use the
``~/.rpmmacros`` example file at the bottom of this section):

::

   sudo dnf install rpm-build rpm-sign  # install required packages
   echo "vault" | sudo tee /rw/config/gpg-split-domain  # edit 'vault' as required
   cat << EOF > ~/.rpmmacros
   %_signature gpg
   %_gpg_name <gpg_key_id>
   %__gpg /usr/bin/qubes-gpg-client-wrapper
   %__gpg_sign_cmd %{__gpg} --no-verbose -u %{_gpg_name} --detach-sign %{__plaintext_filename} --output %{__signature_filename}
   EOF

Now we’ll sign the RPM:

::

   rpm --resign <name>.rpm  # --addsign would allow us to apply multiple signatures to the RPM
   rpm -qi <name>.rpm  # should now show that the file is signed
   rpm -Kv <name>.rpm # should contain NOKEY errors in the lines containing Signature
   # This is because the (public) key of the RPM signing key is not present,
   # and must be added to the RPM client config to verify the signature:
   sudo rpm --import <publicKey>.asc
   rpm -Kv <name>.rpm # Signature lines will now contain OK instead of NOKEY

You can then proceed with distributing the package, via the “test” or
“prod” repo, as appropriate.


Post-Release tasks
==================

1. Ensure release communications have been published.
2. Run the updater on a production setup once packages are live, and conduct a smoketest (successful updater run, and basic functionality if updating client packages).
3. Backport changelog commit(s) with ``git cherry-pick -x`` from the release branch into the main development branch, and sign the commit(s). In a separate commit, run the ``update_version.sh`` script to bump the version on main to the next minor version's rc1. Open a PR with these commits; this PR can close the release tracking issue.
