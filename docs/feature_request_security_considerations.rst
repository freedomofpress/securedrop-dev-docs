Security Considerations When Submitting a Feature Request
==========================================================

When submitting a feature request, it is best to consider the security implications of the 
requested feature. To this end, this document aims to provide some guidelines to identify
any security implications that might arise as a result of implementing the requested feature.

Things to Look Out For
-----------------------

Here we can go over some common security issues, and for each one list some simple questions that
can help ensure that we've [TODO]

Spoofing
~~~~~~~~~

*Note: most, if not all, of these options will rely on securely storing credentials*

Some questions we can ask ourselves to identify spoofing as a risk:

**Are there any remote requests or queries to non-public resources?**

If so, some of the following might be required:

* ensuring that no cleartext credentials are passed
* enabling CSRF mechanisms

**Does the feature need to performs actions as a different user?**

* ensure that 