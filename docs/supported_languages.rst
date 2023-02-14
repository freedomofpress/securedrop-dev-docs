Policy on Supported Languages
=============================

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Version
     - Approved
   * - `4 <https://github.com/freedomofpress/securedrop-engineering/issues/6>`_
     - 7 February 2023

.. note::
   The key words *MUST*, *MUST NOT*, *REQUIRED*, *SHALL*, *SHALL NOT*, *SHOULD*,
   *SHOULD NOT*, *RECOMMENDED*,  *MAY*, and *OPTIONAL* in this document are to be
   interpreted as described in `RFC 2119`_.

Thresholds for Translation and Review Coverage
----------------------------------------------

.. list-table::
   :widths: 30 30 30
   :header-rows: 1
   :stub-columns: 1

   * - Component
     - Translation Coverage (of Source Strings)
     - Review Coverage (of Translations) [#review_coverage]_
   * - Source Interface [#source_components]_
     - 100%
     - 100%
   * - Journalist Interface; SecureDrop Client [#journalist_components]_
     - 80%
     - 100%

The goals of these thresholds are to:

#. emphasize to **translators and reviewers** the importance of
   translating and reviewing source-facing strings;

#. emphasize to **code contributors and maintainers** the higher
   cost and risk involved in changing source (English) strings in source-facing
   components compared to others; and

#. maximize the correctness of the translations we ultimately ship.

Granting Support for a Language
-------------------------------

Granting support for a new language consists of adding an entry in the
``supported_locales`` object in ``securedrop``'s ``i18n.json`` and in the
"Localization" section in ``securedrop-client``'s ``MANIFEST.in``.  Other steps,
such as communication, are left to the discretion of the Localization Manager.

#. A language *L* that reaches coverage in time for a release
   version *V* SHOULD be nominated for support in version *V*.

#. The Localization Manager SHOULD ask Localization Lab whether they
   believe *L*'s `language team`_ is likely to be able to maintain coverage for
   the foreseeable future.

        #. If so, the Localization Manager SHOULD grant support for *L*.

        #. If not, the Localization Manager MUST NOT grant support for *L*.

.. rubric:: Footnotes

.. [#journalist_components] As of this writing, to include any future
   journalist-, admin, or otherwise *non*-source-facing components.

.. [#review_coverage] Machine translation (e.g., Google Translate) MAY be used
   to close gaps in review coverage for an otherwise well-supported language.
   (It MAY NOT be used to close gaps in translation coverage.)

.. [#source_components] As of this writing, to include any future source-facing
   components.

.. _`RFC 2119`: https://datatracker.ietf.org/doc/html/rfc2119
.. _`language team`: https://wiki.localizationlab.org/index.php/Category:Language_Teams
