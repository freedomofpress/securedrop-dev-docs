SecureDrop Workstation Release Management
=========================================

SecureDrop Workstation code spans across several repositories:

-  https://github.com/freedomofpress/securedrop-client (Debian packaged)
-  https://github.com/freedomofpress/securedrop-export (Debian packaged)
-  https://github.com/freedomofpress/securedrop-log (Debian packaged)
-  https://github.com/freedomofpress/securedrop-proxy (Debian packaged)
-  https://github.com/freedomofpress/securedrop-sdk (Python packaged,
   brought in as a dependency of ``securedrop-client``)
-  https://github.com/freedomofpress/securedrop-workstation (RPM
   packaged)
- `securedrop-workstation-config <https://github.com/freedomofpress/securedrop-builder/tree/main/securedrop-workstation-config>`__ (Debian packaged)
- `securedrop-workstation-viewer <https://github.com/freedomofpress/securedrop-builder/tree/main/securedrop-workstation-viewer>`__ (Debian packaged)

Each SecureDrop Workstation component can be released independently. It’s worth noting that in general ``securedrop-sdk`` releases are accompanied with a ``securedrop-client`` release, as ``securedrop-sdk`` is a Python dependency of the ``securedrop-client`` code, so any change in the SDK the client wants to use will necessitate a release of the client also.

Release a Debian package
========================

Releasing a Debian package can take some time because it entails at least two package builds, multiple deployments to our different apt repositories, quality assurance testing, two signing ceremonies, and stakeholder communications.

Releasing a release candidate (rc) package is the first step before you begin QA or any signing ceremonies. Even when you are releasing a hotfix, it is recommended to start with an rc package to defer needing the Securedrop release key until the day of release when you are ready to deploy the package to production.

On release day (usually at least a couple weeks after releasing your first rc package), you, or another maintainer, will need to have access to the SecureDrop release key to sign both a new release tag and an updated Debian Release file for the production apt repository. You will also need at least one other maintainer to review your PRs and perform the final QA checks once the package lands on https://apt-qa.freedom.press and later on https://apt.freedom.press. Before you begin, it is recommended to review the steps below and to create a Release Github Issue titled ``Release <package name> <version>`` for the package being released with a test plan and assignees for release management, QA, and stakeholder communications.

Step 1: Create a release candidate (rc) tag
-------------------------------------------

1. Create a release branch (eg. ``release/1.2.3``) in the repo of the component you want to release.
2. Update the component version to the intended release version (not the RC!) using the ``update_version.sh`` script.
3. Update the changelog to include changes since the last release.
4. Commit and push the version and changelog update.
5. Push an rc tag in the format ``<major>.<minor>.<patch>-rcN`` on your new commit. We will be building from this tag in the next step.

Step 2: Build and deploy the package to ``apt-test``
----------------------------------------------------

1. Open a terminal in your ``sd-dev-dvm`` builder DispVM (see :ref:`How to create the DispVM for building packages`), and prepare to record terminal output- either by using a utility like ``script``, or just by making sure you have infinite scrollback enabled to allow for cut/pasting later.
2. Clone the the ``build-logs`` and ``securedrop-apt-test`` repos.

3. Clone ``securedrop-builder`` and install its dependencies (https://github.com/freedomofpress/securedrop-builder/tree/HEAD/workstation-bootstrap/wheels):

  .. code-block:: sh

   git clone git@github.com:freedomofpress/securedrop-builder.git
   cd securedrop-builder
   make install-deps  # This also confifgures the git-lfs repo used to store SecureDrop Workstation dependencies

4. Create a Debian changelog entry for the new version of the package you are about to build, using the format ``x.y.z~rcN`` - note the ``~``, as this differs from the git tag format.

  .. code-block:: sh

   PKG_VERSION=x.y.z~rcN ./scripts/update-changelog securedrop-foobar

5. Build the package.

  .. code-block:: sh

   PKG_GITREF=x.y.z-rcN make securedrop-foobar

6. Generate build artifact hashes for the build log.

  .. code-block:: sh

   sha256sum build/debbuild/packaging/securedrop-foobar_x.y.z~rc1*

7. Exit ``script`` if running, and save and publish :doc:`build metadata <build_metadata>` via a commit and push to the ``build-logs`` repo's ``main`` branch.

8. Open a PR to https://github.com/freedomofpress/securedrop-apt-test with the package you want to deploy. Remember to link to your build logs commit in the PR's test plan. Once your PR is merged, the package will be deployed to https://apt-test.freedom.press.

Step 3: Step through QA and apply bugfixes
------------------------------------------

You can start the QA process on the RC package that you deployed to https://apt-test.freedom.press. Typically this involves:

1. copying the SecureDrop test key to the TemplateVM where the package should be installed and installing the key via ``apt-key add``
2. updating ``apt``'s config to use ``apt-test.freedom.press`` instead of ``apt.freedom.press``
3. installing or upgradinf the RC package.

If a bug is found requiring a source fix:

1. Apply the fix in the component's ``main`` branch
2. Backport the fix via a PR into the ``release/x.y.z`` branch

Once all fixes found in a QA round are applied:

1. create an incremented RC tag against the head of the ``release/x.y.z`` branch.
2. repeat the build process above for the new RC tag.

Once an rc package has been approved, you are ready to move on to the next step.

Step 4: Create a release tag
----------------------------

Begin this step on the day you want to release the package. It's best to start this process early in the day to ensure there is enough time for final QA checks, signing ceremonies, and stakeholder communications.

In a fresh ``sd-dev-dvm`` environment:

1. Clone the component repo and check out the ``release/x.y.x`` branch.
2. Create a release tag ``x.y.z`` on the commit tagged with the approved rc tag QA.
3. :ref:`Sign the tag with the SecureDrop release key` (or ask another maintainer to do this).
4. Push the signed tag to the origin.

Step 5: Build and deploy the package to ``apt-qa``
--------------------------------------------------

In this step, you will build a production version of the package to be deployed first to ``apt-qa`` for pre-flight checks, and then later to ``apt-prod``. Since this package is reproducibly built, you will also confirm that it matches the hash of the rc package that was approved during QA.

1. Start a fresh ``sd-dev-dvm`` builder DispVM (see :ref:`How to create the DispVM for building packages`), open a terminal, and prepare to record terminal output- either by using a utility like ``script``, or just by making sure you have infinite scrollback enabled to allow for cut/pasting later.

2. Clone the the ``build-logs`` and ``securedrop-apt-test`` repos.

3. Clone ``securedrop-builder`` and install its dependencies (https://github.com/freedomofpress/securedrop-builder/tree/HEAD/workstation-bootstrap/wheels):

  .. code-block:: sh

   git clone git@github.com:freedomofpress/securedrop-builder.git
   cd securedrop-builder
   make install-deps  # This also confifgures the git-lfs repo used to store SecureDrop Workstation dependencies

4. Create a Debian changelog entry for the release version of the package you are about to build, using the format ``x.y.z``

  .. code-block:: sh

   PKG_VERSION=x.y.z ./scripts/update-changelog securedrop-foobar

5. Build the package from the release tag that was signed with the SecureDrop release key.

  .. code-block:: sh

   PKG_GITREF=x.y.z make securedrop-foobar

6. Ouput the package hash so that you can verify that it matches the hash of the rc package that was approved during QA.

  .. code-block:: sh

   sha256sum build/debbuild/packaging/securedrop-foobar_x.y.z*.deb

7. Save and publish :doc:`build metadata <build_metadata>`.
8. Add your package to a new branch called ``release`` in the ``securedrop-apt-prod`` repo, and commit the change
9. Update the apt repo distribution files by running ``./tools/publish`` and commit those changes to the ``release`` branch as well.
10. Generate a ``Release.gpg`` signature for the ``Release`` file of the distribution being targeted for the package (currently ``bullseye``), using the production release key. If you don't have the key, ask a maintainer who does. Commit the ``Release.gpg`` file as well.
11. Open a draft PR to merge the ``release`` branch into ``main``. This will make the package available on for preflight-checks via ``https://apt-qa.freedom.press``.

Step 6: Perform the ``apt-qa`` preflight check
----------------------------------------------

Ensure you are able to update and install the package directly in the package's Template VM by updating the apt sources file to point to https://apt-qa.freedom.press. Test basic functionality.

Step 7: Deploy the package to ``apt-prod`` and perform post-release tasks.
--------------------------------------------------------------------------

1. Flip the PR above from draft to "ready for review". Once approved, merge the ``release`` branch into ``main`` to deploy your package to https://apt.freedom.press.
2. Once you see the package land on https://apt.freedom.press, run the updater to install it in a production environment and ensure that it works as expected.
3. In the ``securedrop-builder`` repo, commit the debian changelog change from earlier and create a PR to merge it into the repo's ``main`` branch.
4. In the component repo (ie, ``securedrop-foobar`` in the examples above), backport the version and component changelog updates via a PR into the ``main`` branch.

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


.. _How to create the DispVM for building packages:

How to create the DispVM for building packages
==============================================

To avoid inadvertently contaminating a build environment with development changes, we'll use a DispVM for building SecureDrop Workstation packages. To do this, we'll create a VM hierarchy with a Debian 11 TemplateVM (for customizing system packages), an AppVM based on that TemplateVM (to customize home directory), and finally a DispVM that reuses that AppVM image and deletes customizations on each run.

In dom0, run:

.. code-block:: sh

    qvm-clone debian-11 t-sd-dev  # Templates default to no NetVM
    qvm-volume resize t-sd-dev:root 20G
    qvm-create t-sd-dev-dvm --label blue --template t-sd-dev  # This creates an AppVM, which will default to having network access
    qvm-prefs t-sd-dev-dvm template_for_dispvms True  # And now we configure our AppVM to be a template for creating our named DispVM
    qvm-features t-sd-dev-dvm appmenus-dispvm 1
    qvm-create sd-dev-dvm --label blue --template t-sd-dev-dvm --class DispVM  # Create the actual named DispVM

A couple pointers:
  * You may wish to customize the ``t-sd-dev-dvm`` home directory to contain personal dotfiles, containing your git config and setting ``QUBES_GPG_DOMAIN``.
  * You can save time by installing the dependencies for ``securedrop-builder`` inside ``t-sd-dev`` (which doesn't have a network) by installing these dependencies directly: https://github.com/freedomofpress/securedrop-builder/blob/c0167ee9f73feab10bf73d1dd1706309eddf4591/scripts/install-deps#L5-L22
