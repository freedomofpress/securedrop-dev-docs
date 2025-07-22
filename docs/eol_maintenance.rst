End-of-Life Maintenance Guidelines
==================================

This document outlines the procedures for managing end-of-life (EOL) transitions for software components in the SecureDrop ecosystem, including both SecureDrop Server and SecureDrop Workstation environments.

Overview
--------

End-of-life maintenance is a critical aspect of SecureDrop's security posture. When software components reach their EOL dates, they no longer receive security updates. This document provides guidelines for:

- Tracking EOL dates and timelines
- Planning and implementing upgrades
- Coordinating community communication

This document focuses on operating system EOLs. For additional component upgrades, see:

- :doc:`updating_tor`
- :doc:`kernel`
- :doc:`dependency_updates`
- :doc:`release_management`
- :doc:`workstation_release_management`
- :doc:`package_repos` (relevant for EOL upgrades if new distributions have to be added)
- :doc:`dependency_updates`

`Guidelines regarding hardware end-of-life <https://docs.securedrop.org/en/stable/admin/installation/hardware.html#hardware-end-of-life>`_ are maintained in the documentation for SecureDrop administrators.


EOL Tracking and Monitoring
---------------------------

SecureDrop uses an automated EOL checker system located in the `securedrop-dev repository <https://github.com/freedomofpress/securedrop-dev>`_ to monitor component lifecycles.

Key Features:

- **Automated Issue Creation**: Opens GitHub issues at specified intervals before EOL dates
- **Calendar Integration**: Generates ICS files that developers can subscribe to for EOL date tracking
- **endoflife.date API**: Consumes data maintained by the https://endoflife.date/ community

.. note::
   The EOL checker requires manual updates for each new software release. Developers must update the YAML configuration when new versions are released to ensure proper monitoring.

SecureDrop Server Components
-----------------------------

Ubuntu Operating System
~~~~~~~~~~~~~~~~~~~~~~~~

The SecureDrop Server runs on Ubuntu LTS (Long Term Support) releases. The project follows a conservative upgrade strategy:

- **Upgrade Schedule**: Upgrade to every other LTS release (e.g., 16.04 → 20.04, skipping 18.04)
- **Timeline**: Plan upgrades well in advance of the current LTS reaching EOL
- **Testing**: Perform extensive testing in continuous integration and in developer-run staging environments.

Because newsroom admins typically have many other responsibilities besides SecureDrop, we want to keep the maintenance effort as low as possible. Starting with the Ubuntu 20.04 → 24.04 migration, we've pursued an in-place upgrade strategy.

Upgrade considerations include Python and Debian package compatibility across Ubuntu and Python versions, changes to configuration file formats, OS software components getting swapped out, and changes to the Ubuntu installer. This migration is therefore typically a heavy lift.

SecureDrop Workstation Components
----------------------------------
The SecureDrop Workstation (SDW) operates on Qubes OS and requires management of multiple operating systems used in virtual machine templates.

Qubes OS
~~~~~~~~

Qubes OS itself is updated on an irregular schedule:

- Qubes 4.0: March 2018
- Qubes 4.1: February 2022
- Qubes 4.2: December 2023

After each major release, the previous one is given 6 months until end-of-life. Given this short timeline, ideally, compatibility testing should begin no later than the first release candidate, after preliminary testing with nightly builds.

.. note::
   Because the exect dates are not known ahead of time, the Qubes OS EOL is not tracked automatically.

Template VMs
~~~~~~~~~~~~

**Debian Templates**

- **Usage**: Base template for all SDW virtual machines
- **Lifecycle**: Follow Debian stable release cycles (typically 2-year cycles) and availability of Qubes base template
- **Management**: Requires changes to SecureDrop Workstation provisioning logic. High-effort due to major package updates (e.g., Python version) that may require components to be rebuilt or upgraded, cause incompatibilities, etc.

**Fedora Templates**

- **Usage**: Base template for system VMs
- **Lifecycle**: Follow Fedora release schedule (typically 6-month cycles) and availability of Qubes base template
- **Management**: Requires updates to SecureDrop Workstation provisioning logic. Usually low-to-moderate effort. These templates are used by Qubes OS itself, so it is possible that future version of Qubes OS will provide more built-in automation here.

Communication Protocol
----------------------

Low-risk ugrades that are performed automatically without user action can be announced through the relevant release blog post. A simple tracking issue is sufficient to plan this work.

For moderate to high-risk upgrades, we typically at least want to give admins the option to trigger them manually, so they can troubleshoot any unexpected issues. This involves additional advance notice, typically through blog posts, social media, and our support portal.
