Email
#####

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
* **server**: Email server used to send the email. By default *localhost*
* **password**: Authenticate using the password. This may be required on the server/account.
* **tls**: Start TLS mode on connect. This is recommended and mandatory on many servers.
* **mode**: HTML or text. By default *text/plain*.


.. note:: If you do not have a local mail server you need to configure the server.
          THEN includes configurations for some common services.


Pre-configured servers
^^^^^^^^^^^^^^^^^^^^^^

THEN includes default settings for these services:

* Gmail
* Yahoo!
* Outlook/Hotmail

You do not need to set the server and tls options in these services.


**Gmail** includes extra security measures. You may need to enable access from less secure applications
or generate an application password. More info:

https://security.google.com/settings/security/apppasswords
https://myaccount.google.com/lesssecureapps


Message setup
-------------

These are the **optional** parameters:

* **subject**: Message subject.
* **Body**: Message body.

.. note:: It is advisable to set the title and the message to avoid that the email is sent to the spam tray.


Instructions for developers
===========================

.. automodule:: then.components.email
   :members: Email,EmailMessage
   :noindex:
