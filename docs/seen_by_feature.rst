"Seen By" Feature Implementation
==================================

The "seen by" feature tracks which journalists are aware of items associated with a source in SecureDrop's shared inbox model. This document describes the technical implementation and behavior across different SecureDrop interfaces.

Overview
--------

**Definitions**

- **Item**: A source message, submitted file, or journalist reply
- **Seen**: An item has been viewed by at least one journalist 
- **Shared inbox model**: Only source content appears as "new" until any journalist has viewed it

**Purpose**

The feature supports multi-journalist review of content by providing visibility into which team members have viewed specific items. This enables coordination and prevents duplicate work.

Current Implementation
----------------------

Web Interface Behavior
~~~~~~~~~~~~~~~~~~~~~~~

In the web-based Journalist Interface:

- **Trigger**: Item status is set to "seen" when downloaded by a journalist
- **Granularity**: Per-item basis as downloaded
- **Source List UI**: Sources with unseen items are styled bold in the source list
- **Per-Item UI**: Individual items styled as bold (unseen) or normal (seen) with closed/opened envelope icons
- **Limitation**: Does not display which specific journalists have seen items

SecureDrop Client Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the legacy SecureDrop Client:

- **Trigger**: All source items marked "seen" when conversation is viewed
- **Granularity**: All items in a conversation marked seen simultaneously  
- **Source List UI**: Sources with unseen items are styled bold in the source list
- **Per-Item UI**: Journalist names displayed as tooltips on checkmarks for each item
- **Enhancement**: Shows specific journalist names who have seen each item

State Flow Diagrams
-------------------

Web Interface State Flow
~~~~~~~~~~~~~~~~~~~~~~~~

[PLACEHOLDER: PNG conversion of Mermaid chart from issue comment showing web interface state transitions]

SecureDrop Client State Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

[PLACEHOLDER: PNG conversion of Mermaid chart from issue comment showing SecureDrop Client state transitions]

API Integration
---------------

The feature integrates with the ``/api/v1/seen`` endpoint:

**Marking Items Seen**

.. code-block:: sh

    POST /api/v1/seen

with the request body:

.. code-block:: json

    {
      "files": ["uuid1", "uuid2"],
      "messages": ["uuid3"], 
      "replies": ["uuid4"]
    }

**Response Data**

Items marked as seen include the journalist UUID in the ``seen_by`` field:

.. code-block:: json

    {
      "seen_by": [
        "1c914871-a335-44ba-b2ae-da878cbc3630"
      ]
    }

Implementation Considerations
-----------------------------

**Special Cases**

- **Offline Mode**: SecureDrop Client displays "seen by" information but does not record new views
- **Deleted Users**: Displayed as "deleted" in SecureDrop Client tooltips
- **Own Replies**: Journalist's own replies are immediately marked as seen by the sending journalist

**Security Properties**

- Only tracks journalist viewing actions, never source actions
- Does not record file opening, only message/reply viewing
- Viewing status is shared across all journalists (not private per-user)

**Behavioral Comparison**

+-------------------+---------------------------+-----------------------------------+
| Aspect            | Web Interface             | SecureDrop Client                 |
+===================+===========================+===================================+
| **Trigger**       | File download             | Source click (viewing             |
|                   |                           | conversation)                     |
+-------------------+---------------------------+-----------------------------------+
| **Granularity**   | Per-item as downloaded    | All source items at once          |
+-------------------+---------------------------+-----------------------------------+
| **Name Display**  | Not implemented           | Tooltip on checkmark per item     |
+-------------------+---------------------------+-----------------------------------+
| **Source Styling**| Bold for sources with     | Bold for sources with unseen      |
|                   | unseen items              | items                             |
+-------------------+---------------------------+-----------------------------------+

Future Considerations
---------------------

The new SecureDrop App implementation may incorporate improvements to address:

- Consistency between interfaces
- Clearer visual indicators for new vs. personally unseen content
- Enhanced tooltip clarity and messaging

For the current API specification, see :doc:`journalist_api` section on marking items seen.