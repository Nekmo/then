Log
###

:Component Type: Other
:Requirements: None

Log to a file or/and screen.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

There are no prerequisites. You only need to know the log destination file if you want log to a file.

Config setup
------------

These are the **optional** parameters:

* **file**: destination file path. If the file does not exist, it will be created.
* **console**: True or False. log to screen. By default False.
* **formatter**: By default ``%(asctime)s - %(name)s - %(levelname)-7s - %(message)s``.
  See: https://docs.python.org/3/library/logging.html#logrecord-attributes

If you do not set file or console, sending the message will have no effect.


Message setup
-------------

These are the **required** parameters:

* **body**: message body.
* **level**: by default ``INFO``. Options: ``CRITICAL``, ``ERROR``, ``WARNING``, ``INFO`` & ``DEBUG``.


Instructions for developers
===========================

.. automodule:: then.components.log
   :members: Log,LogMessage
   :noindex:
