Policy on Supported Languages
=============================

*Revision 4, approved 7 February 2023*

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

.. rubric:: Footnotes

.. [#journalist_components] As of this writing, to include any future
   journalist-, admin, or otherwise *non*-source-facing components.

.. [#review_coverage] Machine translation (e.g., Google Translate) MAY be used
   to close gaps in review coverage for an otherwise well-supported language.
   (It MAY NOT be used to close gaps in translation coverage.)

.. [#source_components] As of this writing, to include any future source-facing
   components.
