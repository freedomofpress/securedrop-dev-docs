Policy on Supported Languages
=============================

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Version
     - Approved
   * - 5 `(internal link) <https://github.com/freedomofpress/securedrop-engineering/issues/6>`_
     - 8 March 2023


Definitions
-----------

.. note::
   The key words *MUST*, *MUST NOT*, *REQUIRED*, *SHALL*, *SHALL NOT*, *SHOULD*,
   *SHOULD NOT*, *RECOMMENDED*,  *MAY*, and *OPTIONAL* in this document are to be
   interpreted as described in `RFC 2119`_.

.. glossary::

   translation freeze

      The deadline for translations to be reviewed and merged in order to be
      included in a given release.  For SecureDrop, this is :ref:`release day
      <release_day>`.


Thresholds for Translation and Review Coverage
----------------------------------------------

.. list-table::
   :widths: 30 30 30
   :header-rows: 1
   :stub-columns: 1

   * -
     - Translation Coverage
     - Review Coverage [#review_coverage]_
   * - To grant support
     - 100%
     - 100%
   * - To maintain support
     - 80%
     - 100%

In addition to these thresholds, the SecureDrop team will:

#. always prioritize the translation of source-facing strings, given their
   importance for sources' security; and

#. inform Localization Lab when particular strings should be prioritized or
   even considered blocking for a given release.

Granting Support for a Language
-------------------------------

Granting support for a new language consists of adding an entry in the
``supported_locales`` object in ``securedrop``'s ``i18n.json`` and/or in the
"Localization" section in ``securedrop-client``'s ``MANIFEST.in``.  Other steps,
such as communication, are at the discretion of the Localization Manager.

#. A language *L* that reaches coverage in time for a release
   version *V*'s :term:`translation freeze` SHOULD be nominated for support in
   version *V*.

#. The Localization Manager SHOULD ask Localization Lab whether they
   believe *L*'s `language team`_ is likely to be able to maintain coverage for
   the foreseeable future.

        #. If so, the Localization Manager SHOULD grant support for *L*.

        #. If not, the Localization Manager MUST NOT grant support for *L*.

Revoking Support for a Language
-------------------------------

Revoking support for a currently-supported language consists of removing the
language's entries in ``i18n.json`` and/or ``MANIFEST.in``.  Other steps, such
as communication, are at the discretion of the Localization Manager.

Consider an expected release timeline as follows:

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :stub-columns: 1

   * - Version
     - :term:`Translation Freeze`
   * - V1
     - January 1
   * - V2
     - March 1
   * - V3
     - May 1

Then:

#. A language *L* that misses coverage for a release version *V1*'s
   :term:`translation freeze` MUST be considered on probation for up to the next
   two releases *V2* and *V3*.  While on probation, a language is still
   considered supported until it has missed coverage for a total of 3
   consecutive translation freezes.

        #. In consultation with Localization Lab, the Localization
           Manager MAY consult the `language census`_ (internal link) and reach out to
           administrators who may be able to contribute to translation and
           review.

#. If *L* misses coverage again for *V2*'s translation freeze and does not
   regain coverage for *V3*'s translation freeze, then the Localization Manager
   SHOULD revoke support for *L* for *V3*.

        #. In consultation with Localization Lab and the Release
           Manager, the Localization Manager MAY extend *L*’s probationary
           period, for example if the `language census`_ indicates that revoking
           support for *L* would jeopardize the default locale for many
           instances, for especially high-traffic or high-profile instances,
           etc.
           
Adding a New Language for Translation
-------------------------------------

Translators MUST ask Localization Lab to add a new language for translation in
Weblate.

.. rubric:: Footnotes

.. [#review_coverage] Machine translation (e.g., Google Translate) MAY be used
   to close gaps in review coverage for an otherwise well-supported language.
   (It MAY NOT be used to close gaps in translation coverage.)  Because of the
   risk of low-quality machine translations especially from minority languages,
   machine translation SHOULD be considered a last resort, on a case-by-case
   basis in consultation with Localization Lab.

.. _`RFC 2119`: https://datatracker.ietf.org/doc/html/rfc2119
.. _`language census`: https://github.com/freedomofpress/i18n_scan
.. _`language team`: https://wiki.localizationlab.org/index.php/Category:Language_Teams
