Email
#######

:Component Type: Message
:Requirements: None
:Features: text

Send an email using an email account on a local or remote server.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* An email account and server to send the email
* A destination email account


Config setup
------------

These are the **required** parameters:

* **to**: Destination email.

These are the **optional** parameters:

* **from_**: Account used to send the email. By default *noreply@localhost*.
* **server**: Email server sed to send the email. By default *localhost*
* **mode**: HTML or text. By default *text/plain*.


.. note:: If you do not have a local mail server you need to configure the server.


Message setup
-------------

These are the **optional** parameters:

* **subject**: Message subject.
* **Body**: Message body.

.. note:: It is advisable to set the title and the message to avoid that the email is sent to the spam tray.


Instructions for developers
===========================

.. autoattribute:: then.components.command.Email.user

.. automodule:: then.components.email
   :members: Email,EmailMessage
   :noindex:
