SecureDrop Workstation Release Management
=========================================

Communications Process
-----------------------
As with SecureDrop server releases, the release manager should work with the Communications Manager
assigned for the release to prepare announcements that will be shared on the SecureDrop
blog and on social media after the release is live.

Typically, the kick-off of the QA period is a good time to begin the process. Please note that review
by FPF's editorial team is required and should only be skipped in case of urgent release-specific
considerations, e.g., to get a hotfix release out as quickly as possible.

Once the release is live:

1. Make sure that release notes are written and posted on the SecureDrop blog.
2. Make sure that the release is announced on social media.
3. If the release warrants announcements beyond that (e.g., via Signal group), make them now.

Release an RPM package
-----------------------

Release ``securedrop-workstation-dom0-config``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~~~~

.. _Sign the tag with the SecureDrop release key:

Sign the tag with the SecureDrop release key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Sign the RPM package
~~~~~~~~~~~~~~~~~~~~

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

Now we'll sign the RPM:

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
------------------
1. If you've not done so already as part of the release, ensure release communications are published.
2. Run the updater on a production setup once packages are live, and conduct a smoketest (successful updater run, and basic functionality if updating client packages).
3. Backport changelog commit(s) with ``git cherry-pick -x`` from the release branch into the main development branch, and sign the commit(s). In a separate commit, run the ``update_version.sh`` script to bump the version on main to the next minor version's rc1. Open a PR with these commits; this PR can close the release tracking issue.
