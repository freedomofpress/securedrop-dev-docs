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

Step 1: Create a release candidate (rc) tag
-------------------------------------------

1. Create a release branch named ``release/<major>.<minor>.<patch>``.
2. Push a commit adding a new changelog entry and incrementing the version.
3. Push an rc tag in the format ``<major>.<minor>.<patch>~rcN`` on your new commit. We will be building from this tag in the next step.

Step 2: Build and deploy the package to ``apt-test``
----------------------------------------------------

1. Clone ``securedrop-client`` and ``securedrop-builder``.

  .. code-block:: sh

   git clone git@github.com:freedomofpress/securedrop-client.git
   git clone git@github.com:freedomofpress/securedrop-builder.git

2. Check out the newly pushed tag and then build the packages.

  .. code-block:: sh

   cd securedrop-client
   git checkout ``<major>.<minor>.<patch>~rcN``
   make build-debs

3. Save and publish :doc:`build metadata <build_metadata>`.
4. Open a PR to https://github.com/freedomofpress/securedrop-apt-test with the packages you want to deploy.
   Once merged, the packages will be deployed to https://apt-test.freedom.press.

Step 3: Begin QA
----------------

You can now start the QA process! If a bug is found, a fix should be developed, merged into the main branch and
cherry-picked into the release branch. If desired, release another RC package for further testing.

Once QA testers are satisfied with the package, you are ready to move on to the next step.

Step 4: Create a release tag
----------------------------

1. Update the changelog and version.
2. Generate a release tag named``<major>.<minor>.<patch>`` (same as the previous tags, without the ``~rcN`` part).
3. :ref:`Sign the tag with the SecureDrop release key` or ask another maintainer to do this and push the signed tag

Step 5: Build and deploy the package to ``apt-qa``
--------------------------------------------------

1. Clone ``securedrop-client`` and ``securedrop-builder``.

  .. code-block:: sh

   git clone git@github.com:freedomofpress/securedrop-client.git
   git clone git@github.com:freedomofpress/securedrop-builder.git

2. Check out the newly pushed tag and then build the packages.

  .. code-block:: sh

   cd securedrop-client
   git checkout ``<major>.<minor>.<patch>``
   make build-debs

3. Save and publish :doc:`build metadata <build_metadata>`.
4. Add your package to a new branch called ``release`` in https://github.com/freedomofpress/securedrop-apt-prod.
5. Update the apt repo distribution files by running ``./tools/publish`` and push those changes to the ``release`` branch as well.
6. :ref:`Regenerate and sign the apt release file` or ask another maintainer to do this. The package will now be installable from https://apt-qa.freedom.press.
7. Open a PR to merge the ``release`` branch into ``main``.
8. Another maintainer should also build the package (following the same steps as earlier) and verify their newly built packages
   are identical to those pushed to apt-qa.

Step 6: Perform the ``apt-qa`` preflight check
----------------------------------------------

1. Start the package's Template VM.
2. Edit the apt sources file to point to https://apt-qa.freedom.press.
3. Update the package system and install the new packages via ``apt update && apt upgrade -y``.
4. Open the Qube Manager and restart all VMs using the Template VM you just updated.
5. Start the Client application and verify that everything is working as expected. 

Step 7: Deploy the package to ``apt-prod``
------------------------------------------

1. Merge the ``release`` branch into ``main`` to deploy your package to https://apt.freedom.press.
2. Once you see the package land on https://apt.freedom.press, run the updater to install it in a production environment and ensure that it works as expected.

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
    ``securedrop-workstation`` you run ``make dom0-rpm`` to build the
    RPM.
4.  sha256sum the built template (and store hash in the build
    logs/commit message).
5.  Commit the (unsigned) version of this RPM to a branch in the
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
11. Commit the RPM in a second commit on the branch you began above in
    `securedrop-yum-prod <https://github.com/freedomofpress/securedrop-yum-prod>`__.
    Make a PR.
12. Upon merge to master, ensure that changes deploy to
    ``yum.securedrop.org`` without issue.

Release ``qubes-template-securedrop-workstation``
-------------------------------------------------

The SecureDrop workstation template is RPM packaged, and is first
deployed to ``yum-test.securedrop.org`` before being promoted to
production (``yum.securedrop.org``) using the following procedure:

1.  Verify the tag in the
    `qubes-template-securedrop-workstation <https://github.com/freedomofpress/qubes-template-securedrop-workstation>`__
    repository: ``git tag -v VERSION`` and ensure the tag is signed with
    the official release key.
2.  ``git checkout VERSION``
3.  Rebuild template following documentation in
    `qubes-template-securedrop-workstation <https://github.com/freedomofpress/qubes-template-securedrop-workstation>`__.
4.  sha256sum the built template (and store hash in the build
    logs/commit message).
5.  Commit unsigned template for historical purposes.
6.  Sign template RPM with test key (``rpm --resign``) (see Signing section
    below).
7.  Commit signed template.
8.  Push those two commits to a PR in
    `securedrop-yum-test <https://github.com/freedomofpress/securedrop-yum-test/>`__.
    Make the PR.
9.  Save and publish :doc:`build metadata <build_metadata>`.
10. Upon merge of the PR into
    `securedrop-yum-test <https://github.com/freedomofpress/securedrop-yum-test/>`__,
    the template will be deployed to ``yum-test.securedrop.org``.
11. Install the template in dom0 and test it. Provided you’ve run the Salt configurations, find the template via:
    ``sudo qubes-dom0-update --action=search qubes-template-securedrop-workstation``.
12. Once template is sufficiently tested, remove test sig:
    ``rpm --delsign <file>``.
13. Verify unsigned template sha256sum from build logs/commit message.
14. Sign template with prod key: ``rpm --resign <file>``
15. Push commit to a branch in the
    `securedrop-yum-prod <https://github.com/freedomofpress/securedrop-yum-prod/>`__
    repository. Make a PR.
16. Upon merge to master, ensure that changes deploy to
    ``yum.securedrop.org`` without issue.

Signing procedures
==================

.. _Sign the tag with the SecureDrop release key:

Sign the tag with the SecureDrop release key
--------------------------------------------

1. If the tag does not already exist, create a new release tag: ``git tag -a VERSION``.
2. Output the tag to a file: ``git cat-file tag VERSION > VERSION.tag``.
3. Copy the tag file into your signing environment and then verify the tag commit hash.
4. Sign the tag with the SecureDrop release key: ``gpg --armor --detach-sign VERSION.tag``.
5. Append ASCII-armored signature to tag file (ensure there are no blank lines): ``cat VERSION.tag.sig >> VERSION.tag``.
6. Move tag file with signature appended back to the release environment.
7. Delete old (unsigned) tag: ``git tag -d VERSION``.
8. Create new (signed) tag: ``git mktag < VERSION.tag > .git/refs/tags/VERSION``.
9. Verify the tag: ``git tag -v VERSION``.
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

   rpm --resign <rpm>.rpm  # --addsign would allow us to apply multiple signatures to the RPM
   rpm -qi<file.rpm>  # should now show that the file is signed
   rpm -Kv  # should contain NOKEY errors in the lines containing Signature
   # This is because the (public) key of the RPM signing key is not present,
   # and must be added to the RPM client config to verify the signature:
   sudo rpm --import <publicKey>.asc
   rpm -Kv  # Signature lines will now contain OK instead of NOKEY

You can then proceed with distributing the package, via the “test” or
“prod” repo, as appropriate.
