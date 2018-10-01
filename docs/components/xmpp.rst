XMPP
####

:Component Type: Message
:Requirements: slekxmpp
:Features: text

Send an XMPP/Gtalk/Hangouts message using a Jabber/XMPP account. If you use *Google Chat*
(only available for GSuit) you need to use the googlechat component.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A Jabber/XMPP recipient account (for example a Gmail account).
* Other Jabber/XMPP account to send the message

Some servers and services may apply restrictions. For example, users may need to be friends.
First try writing a message between the accounts using a chat program (for example Gmail for
GTalk/Hangouts). This is not mandatory but it is highly recommended.


Config setup
------------

These are the **required** parameters:

* **from_**: Jabber ID Account (JID).
* **password**: Password for *from_* account.
* **to**: destination JID.

These are the **optional** parameters:

* **server**: server for *from_* account.

THEN will attempt to get the server (DNS SRV XMPP). This may not work if the server is misconfigured.
If you have issues and you use Google Suit, you must use this server: ``talk.google.com:5222``. This
is not required if you use an account ``<user>@gmail``.



Message setup
-------------

These are the **required** parameters:

* **body**: Message body.


Instructions for developers
===========================

.. automodule:: then.components.xmpp
   :members: Xmpp,XmppMessage
   :noindex:
