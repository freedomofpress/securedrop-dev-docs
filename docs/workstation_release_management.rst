Releasing SecureDrop Workstation and its Subprojects
====================================================

Release a subproject
--------------------

SecureDrop Workstation code spans across several repositories:

-  https://github.com/freedomofpress/securedrop-client (Debian packaged)
-  https://github.com/freedomofpress/securedrop-export (Debian packaged)
-  https://github.com/freedomofpress/securedrop-log (Debian packaged)
-  https://github.com/freedomofpress/securedrop-proxy (Debian packaged)
-  https://github.com/freedomofpress/securedrop-sdk (Python packaged,
   brought in as a dependency of ``securedrop-client``)
-  https://github.com/freedomofpress/securedrop-workstation (RPM
   packaged)

Some of these subprojects have a corresponding release guide in the
project’s README
(`example <https://github.com/freedomofpress/securedrop-client#making-a-release>`__
for ``securedrop-client``). The release process for each subproject is
generally:

1. Run that project’s update version script if it has one. Else, update
   version numbers manually. Update the changelog describing the changes
   in that release.
2. Commit those changes, and create a PR.
3. Once this PR is approved, add a tag (see below) that is signed with
   the official release key.

**Note:** Early tags in each subproject were not signed with the
official release key. Later releases, as the subprojects were prepared
for production, had their tags signed with the official release key.

In addition, we have the following (Debian) metapackages, which are
stored in the `securedrop-debian-packaging <https://github.com/freedomofpress/securedrop-debian-packaging>`__
repository:

- `securedrop-workstation-config <https://github.com/freedomofpress/securedrop-debian-packaging/tree/main/securedrop-workstation-config>`__
- `securedrop-workstation-viewer <https://github.com/freedomofpress/securedrop-debian-packaging/tree/main/securedrop-workstation-viewer>`__

The release process for a metapackage is generally to bump the version,
update the debian changelog, and then tag
``securedrop-debian-packaging`` (see below).

Each subcomponent can be released independently. It’s worth noting that
in general ``securedrop-sdk`` releases generally be accompanied with a
``securedrop-client`` release, as ``securedrop-sdk`` is a Python
dependency of the ``securedrop-client`` code, so any change in the SDK
the client wants to use will necessitate a release of the client also.
We’ll cover that below.

Tag a subproject
----------------

Once the release PR is merged, the procedure of adding signed tags is as
follows:

1.  Create tag: ``git tag -a VERSION``
2.  Output tag to file: ``git cat-file tag VERSION > VERSION.tag``
3.  Copy tag file to signing environment
4.  Verify tag integrity (commit hash)
5.  Sign tag with release key: ``gpg --armor --detach-sign VERSION.tag``
6.  Append ASCII-armored signature to tag file (ensure there are no
    blank lines): ``cat VERSION.tag.sig >> VERSION.tag``
7.  Move tag file with signature appended back to the release
    environment
8.  Delete old (unsigned) tag: ``git tag -d VERSION``
9.  Create new (signed) tag:
    ``git mktag < VERSION.tag > .git/refs/tags/VERSION``
10. Verify the tag: ``git tag -v VERSION``
11. Push the tag to the shared remote: ``git push origin VERSION``

Generate Tarballs
-----------------

Next, for the Debian-packaged projects **only**, one needs to generate
the source tarballs for use during packaging, as well as add the debian
changelog addition. This is done via a PR into
https://github.com/freedomofpress/securedrop-debian-packaging.

Follow the instructions described in `this
section <https://github.com/freedomofpress/securedrop-debian-packaging#build-a-package>`__,
stopping before the final step where the package itself is built. Save
the build logs from the tarball generation step (since the tarball
generation is not reproducible) and commit them
`here <https://github.com/freedomofpress/build-logs>`__. You should then
in a branch:

-  Add the tarball that is generated from that step to the
   ``./tarballs`` directory in that
   `securedrop-debian-packaging <https://github.com/freedomofpress/securedrop-debian-packaging>`__
   repository
-  Add a detached signature of that tarball also to the ``./tarballs``
   directory alongside the tarball above for ease of verification
-  Add the Debian changelog addition
-  Remove the tarball and corresponding signature from the previous
   release.

File that PR. Once it’s approved, move to the next step.

Tag code used to generate artifacts
-----------------------------------

In addition to the code repositories above, the following repositories
are used to create artifacts - the ``securedrop-workstation`` template
and the debian packages, respectively - used in the workstation:

-  https://github.com/freedomofpress/qubes-template-securedrop-workstation
-  https://github.com/freedomofpress/securedrop-debian-packaging

Next, if one of these projects is needed to generate an artifact for us
in a production environment, it will be released by adding a signed tag
before using the corresponding logic. You can do this following the same
steps as in the ``Tag a subproject`` section. For
``securedrop-debian-packaging``, we include in the tag annotation the
latest release for each subproject that is released using its logic. For
example the tag annotation for ``securedrop-debian-packaging 0.2.2``:

::

   securedrop-client 0.1.2
   securedrop-proxy 0.2.0
   securedrop-log 0.1.0
   securedrop-export 0.2.1
   securedrop-workstation-svs-disp 0.2.1
   securedrop-workstation-grsec 4.14.169
   securedrop-workstation-config 0.1.2

Final build for a subproject
----------------------------

Finally, perform the final build. You should follow one of the sections
below based on whether the subproject you are building is Debian or rpm
packaged.

Debian package
~~~~~~~~~~~~~~

In an environment sufficient for building production artifacts (if
unsure, check with a technical lead):

1. Clone the
   `securedrop-debian-packaging <https://github.com/freedomofpress/securedrop-debian-packaging>`__
   repository.
2. Determine which version of the packaging logic and tarballs you want
   to use. You probably created the tag in the previous step, else
   inspect the tag annotation to determine which is the right version.
3. ``git tag -v VERSION`` and ensure the tag is signed with the official
   release key.
4. ``git checkout VERSION``
5. Now you are ready to build. For good measure, you can also verify the
   signature of the tarball you want to use, although this will have
   been done by the reviewer of the PR adding the tarball.
6. Set ``PKG_DIR`` to point to the tarball you wish to package, and
   ``PKG_VERSION`` to the version you wish to package, then run the
   relevant makefile target in the
   `securedrop-debian-packaging <https://github.com/freedomofpress/securedrop-debian-packaging>`__
   repository. For example to build version 0.1.1 of the
   ``securedrop-client``:

``$ PKG_VERSION=0.1.1 PKG_PATH=tarballs/securedrop-client-0.1.1.tar.gz make securedrop-client``

6.  Upload build logs in the
    `build-logs <https://github.com/freedomofpress/build-logs>`__
    repository in the workstation directory. Ensure that the sha256sum
    of the built package is included in the build log.
7.  Next, add the package via PR to the private
    `securedrop-debian-packages-lfs <https://github.com/freedomofpress/securedrop-debian-packages-lfs>`__
    repository.
8.  Regenerate reprepro repository metadata using the script in that
    repository: ``./tools/publish``. When you inspect the diff, you’ll
    notice that the previous version of the subproject will no longer be
    served. This is expected.
9.  Copy the ``Release`` file to signing environment.
10. Verify integrity of ``Release`` file.
11. Sign the Release file
    ``gpg --armor --detach-sign --output Release.gpg Release``
12. Copy the detached signature into your working directory and commit
    along with the new package(s), and the modified repository metadata.
13. Open a PR for review.
14. Upon merge to master, ensure that changes deploy to
    ``apt.freedom.press`` without issue.

RPM package
~~~~~~~~~~~

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
    `securedrop-workstation-prod-rpm-packages-lfs <https://github.com/freedomofpress/securedrop-workstation-prod-rpm-packages-lfs>`__
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
10. Upload build logs directly to the
    `build-logs <https://github.com/freedomofpress/build-logs>`__
    repository in the workstation directory. Ensure that the sha256sum
    of the package before and after signing is included in the build
    log.
11. Commit the RPM in a second commit on the branch you began above in
    `securedrop-workstation-prod-rpm-packages-lfs <https://github.com/freedomofpress/securedrop-workstation-prod-rpm-packages-lfs>`__.
    Make a PR.
12. Upon merge to master, ensure that changes deploy to
    ``yum.securedrop.org`` without issue.

``qubes-template-securedrop-workstation`` release and promotion to production
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
6.  Sign template RPM with test key (rpm –resign ) (see Signing section
    below).
7.  Commit signed template.
8.  Push those two commits to a PR in
    `securedrop-workstation-dev-rpm-packages-lfs <https://github.com/freedomofpress/securedrop-workstation-dev-rpm-packages-lfs/>`__.
    Make the PR.
9.  Upload build logs directly to the
    `build-logs <https://github.com/freedomofpress/build-logs>`__
    repository in the workstation directory.
10. Upon merge of the PR into
    `securedrop-workstation-dev-rpm-packages-lfs <https://github.com/freedomofpress/securedrop-workstation-dev-rpm-packages-lfs/>`__,
    the template will be deployed to ``yum-test.securedrop.org``.
11. Test template.
12. Once template is sufficiently tested, remove test sig:
    ``rpm --delsign <file>``.
13. Verify unsigned template sha256sum from build logs/commit message.
14. Sign template with prod key: ``rpm --resign <file>``
15. Push commit to a branch in the
    `securedrop-workstation-prod-rpm-packages-lfs <https://github.com/freedomofpress/securedrop-workstation-prod-rpm-packages-lfs/>`__
    repository. Make a PR.
16. Upon merge to master, ensure that changes deploy to
    ``yum.securedrop.org`` without issue.

Signing binaries/packages
-------------------------

Debian packages
~~~~~~~~~~~~~~~

The apt repository Release file will be signed, containing checksums of
the debs.

RPM packages
~~~~~~~~~~~~

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
   # This is because the the (public) key of the RPM signing key is not present,
   # and must be added to the RPM client config to verify the signature:
   sudo rpm --import <publicKey>.asc
   rpm -Kv  # Signature lines will now contain OK instead of NOKEY

You can then proceed with distributing the package, via the “test” or
“prod” repo, as appropriate.

``~/.rpmmacros`` file
~~~~~~~~~~~~~~~~~~~~~

::

   %_signature gpg
   %_gpg_name 22245C81E3BAEB4138B36061310F561200F4AD77

Distributing packages
---------------------

For the Debian packages, see
https://github.com/freedomofpress/securedrop-debian-packaging/. For the
RPM packages, such as the ``securedrop-workstation`` TemplateVM package,
first build the package (e.g. ``make template``), then sign the RPM, as
outlined above.

To upload the package, submit a PR to
https://github.com/freedomofpress/securedrop-workstation-dev-rpm-packages-lfs/

The RPM will immediately be available in dom0. Provided you’ve run the
Salt configurations, find it via:

::

   sudo qubes-dom0-update --action=search qubes-template-securedrop-workstation

You can then install it directly.