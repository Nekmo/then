Google Chat
###########

:Component Type: Message
:Requirements: None
:Features: text

Send a Google Chat group message using Webhooks. This component does not work
for GTalk/Hangouts. You need to use the xmpp component.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A Google Chat account (GSuit required).
* Get **to**, **key** and **token** from Webhook url (explained below).


Setup steps
-----------

#. Go to https://chat.google.com/ (GSuit required).
#. Create or go to a group.
#. Click on *members count menu -> Configure webhooks*.
#. Add a Webhook and copy Webhook Url. For example:
   ``https://chat.googleapis.com/v1/spaces/AAAAqkJxxxx/messages?key=AIzaSfDdI7hChtE6zyS6Mm-WefRa3Cpzqlqxxxx&token
   =IWccInfAQhPSrkOVgVSzh07W9hBzp9eCqjQzTB_xxxxxxx``.
#. The url has 3 configuration parameters: To (``AAAAqkJxxxx``), key (``AIzaSfDdI7hChtE6zyS6Mm-WefRa3Cpzqlqxxxx``)
   and Token (``IWccInfAQhPSrkOVgVSzh07W9hBzp9eCqjQzTB_xxxxxxx``).


Config setup
------------

These are the **required** parameters:

* **to**: the space id for your organization (``AAAAqkJxxxx``).
* **key**: Webhook Key Id (``AIzaSfDdI7hChtE6zyS6Mm-WefRa3Cpzqlqxxxx``).
* **token**: Webhook Token (``IWccInfAQhPSrkOVgVSzh07W9hBzp9eCqjQzTB_xxxxxxx``).

These are the **optional** parameters:

* **timeout**: Connection timeout to send message. By default ``15 seconds``.


Message setup
-------------

These are the **required** parameters:

* **body**: Message body.


Instructions for developers
===========================

.. automodule:: then.components.googlechat
   :members: GoogleChat,GoogleChatMessage
   :noindex:
