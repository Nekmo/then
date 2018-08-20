IFTTT
#####

:Component Type: Event
:Requirements: None

Execute an IFTTT event using IFTTT Webhooks.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* An IFTTT account.
* Create a Applet using Webhooks (explained below)


Setup steps
-----------

#. Connect to your IFTTT account in the browser.
#. Create a new applet using Webhook trigger: https://ifttt.com/create/if-maker_webhooks?sid=1 .
   You will have to define a **event name**.
#. Get your IFTTT Webhook **key**: https://ifttt.com/services/maker_webhooks/settings
   For example: ``c2BVn_A93kLvaa4ymExxxx``. The key can be in the url. For example:
   ``https://maker.ifttt.com/use/c2BVn_A93kLvaa4ymExxxx``.


Config setup
------------

These are the **required** parameters:

* **token**: Your secret Webhook token (``c2BVn_A93kLvaa4ymExxxx``).

These are the **optional** parameters:

* **timeout**: Connection timeout to send message.


Message setup
-------------

These are the **required** parameters:

* **event**: You define the event name when creating a Webhook applet.

You can define **extra parameters** (called ingredients in IFTTT).


Instructions for developers
===========================

.. automodule:: then.components.ifttt
   :members: Ifttt,IftttMessage
   :noindex:
