SecureDrop Inbox Release Management
===================================

Development timeline
--------------------

The SecureDrop Team works on a 2-week sprint cycle. The schedule for a sprint that includes a release
should look like:

* Week 1: Development work
* Week 2: Release week

  * Monday: Major features list finalized by standup; start Comms draft and send to FPF Editorial
    by the end of the day.
  * Tuesday: All remaining PRs that will be included in the release are identified at standup. By
    the end of the day, bump the version to an RC to begin QA. Merges to ``main`` are temporarily
    blocked until the release is complete.
  * Wednesday: Finish QA by standup and discuss any potential blockers. If there are no blockers,
    proceed with the full release, otherwise work on fixes/reverts and repeat the QA cycle.
  * Thursday: backup release day in case we needed extra time because of extra RCs.

If a release takes longer than this, then it becomes an all-hands-on-deck situation to resolve whatever
is necessary. That could also include backing out the problematic change and retrying it in the next sprint.

Workflow
--------

Step 0: Tracking and planning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a tracking issue titled ``Release SecureDrop Inbox <version>``. It should contain assigned roles and estimated timelines.
Pin the issue for ease of access and visibility.

Review the in-flight issues and PRs, tagging them with the appropriate milestone. Ensure you explicitly communicate with other developers if you
are expecting to include their work in the upcoming release.

Step 1: Create a release candidate (RC) tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Increment the version using ``./update_version.sh <version>-rc1``, and update ``changelog.md``, opening a PR with your changes.
2. Once that PR is merged, create a tag with the version, e.g. ``git tag -s <version>-rc1`` and push it. The tag should be signed with your local developer key, not the SecureDrop Release Key.

Step 2: Build and deploy the package to ``apt-test``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   This step will largely be automated in the future.


1. Clone ``securedrop-client`` and ``securedrop-builder``.

   .. code-block:: sh

      git clone git@github.com:freedomofpress/securedrop-client.git
      git clone git@github.com:freedomofpress/securedrop-builder.git

2. Check out the newly pushed tag and then build the packages.

   .. code-block:: sh

      cd securedrop-client
      git checkout <version>-rc1
      make build-debs

3. Save and publish :doc:`build metadata <build_metadata>`.
4. Open a PR to https://github.com/freedomofpress/securedrop-apt-test with the packages you want to deploy.
   Once merged, the packages will be deployed to https://apt-test.freedom.press.

Step 3: Begin QA
~~~~~~~~~~~~~~~~

QA testers should begin working through the test plan, identifying any issues they run into. File issues for
any unexpected behavior, and determine if they should be fixed or can be deferred to a future release.

If fixes are needed, create and merge PRs into ``main``, issue another RC and repeat the QA process.

Once no fixes are needed, then you can begin preparing the production release.

Step 4: Create a production release tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Submit a PR that updates the changelog and version. Remove any references to the RC versions from the changelogs.
2. Generate a release tag named ``<version>`` (same as the previous tags, without the ``-rcN`` part).
3. :ref:`Sign the Inbox tag with the SecureDrop release key` or ask another maintainer to do this and push the signed tag
4. Ask another maintainer to verify the tag signature and that it points to the correct commit.

Step 5: Build and deploy the packages to ``apt-prod``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   This step will largely be automated in the future.

1. Clone ``securedrop-client`` and ``securedrop-builder``.

   .. code-block:: sh

     git clone git@github.com:freedomofpress/securedrop-client.git
     git clone git@github.com:freedomofpress/securedrop-builder.git

2. Check out the newly pushed tag and then build the packages.

   .. code-block:: sh

     cd securedrop-client
     git tag -v <version> # Signed by SecureDrop Release Key
     git checkout <major>.<minor>.<patch>
     make build-debs

3. Save and publish :doc:`build metadata <build_metadata>`.
4. Add your packages to a new branch called ``release`` in https://github.com/freedomofpress/securedrop-apt-prod. Include all built .deb packages, including ``-dbgsym`` packages. (``-dbgsym`` packages will be kept in the ``main-debug`` component. See :ref:`Notes on dbgsym-packages <dbgsym-packages>` for more information.)
5. Update the apt repo distribution files by running ``./tools/publish`` and push those changes to the ``release`` branch as well.
6. :ref:`Regenerate and sign the apt release file` or ask another maintainer to do this. The packages will now be installable from https://apt-qa.freedom.press.
7. Open a PR to merge the ``release`` branch into ``main``.
8. Another maintainer should also build the packages (following the same steps as earlier) and verify their newly built packages
   are `bit-for-bit identical <https://reproducible-builds.org/docs/definition/>`_ to those pushed to apt-qa.

Step 6: Perform the ``apt-qa`` preflight check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
First, provision a production workstation from the most recently-released
``securedrop-workstation-dom0-config`` production package. Ensure your machine
has been updated (either via Qubes native updater or SDW GUI updater).

At minimum, perform the full test. Additional QAers may perform smoketest to
save time if there is already full test coverage.

.. note::
   These instructions are out of date.

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

Step 7: Deploy to ``apt-prod``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. In ``securedrop-apt-prod``, merge the PR into ``main`` to deploy the new version to https://apt.freedom.press.
2. Once you see the packages land on https://apt.freedom.press, run the updater to install it in a production environment and ensure that it works as expected.

Step 8: Communications
~~~~~~~~~~~~~~~~~~~~~~

1. Publish a blog post for the release on securedrop.org and promote it on our social media accounts.
2. If appropriate, send a blast out to Signal groups announcing the new release and any notable features or bug fixes.

Step 9: Cleanup
~~~~~~~~~~~~~~~

1. In the ``securedrop-client`` repository, update the version to `<major>.<minor+1>.0-alpha` to prepare for the next development cycle.
2. Close the release issue and milestone.
3. Celebrate!

Using a release branch
----------------------

Historically each release was prepared on a separate ``release/<version>`` branch, with changes needing to be backported into
the release branch, and then commits forward-ported into ``main`` post-release. In mid-2026 we moved away from this being the default
workflow, however it remains an option for when a release takes longer than normal.

This can be implemented at the beginning of the release process, if we know that the release will take longer than normal and don't want to
keep ``main`` frozen for that entire time, or if it ends up taking longer than anticipated.

To use a release branch, create a new branch from wherever ``main`` is. All future version bump, changelog updates and tags will take place
on this branch. Any changes in main that should go into the release will need to manually be cherry-picked into the release branch.

Once the release is complete, review the release branch for any changes that were solely made in it, which should normally be just version bumps
and the changelog, and cherry-pick those back into main.

Signing procedures
------------------

.. _Sign the Inbox tag with the SecureDrop release key:

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

.. _Regenerate and sign the apt release file:

Regenerate and sign the apt release file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
