Slack
#####

:Component Type: Message
:Requirements: None
:Features: text

Send an slack message using Webhooks to a channel o user.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* An slack account and server to send the message
* Create a Webhook (explained below)


Create a Webhook
----------------

#. Log in to the Slack server in your browser
#. Go to: https://slack.com/apps/A0F7XDUAZ-incoming-webhooks
#. Configure It and get your Webhook URL. For example:
   ``https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX``
#. The url has 3 configuration parameters: Team (``T00000000``), Bot (``B00000000``) and
   Token (``XXXXXXXXXXXXXXXXXXXXXXXX``).


Config setup
------------

These are the **required** parameters:

* **team**: First param from Webhook (``T00000000``).
* **bot**: Second param from Webhook (``B00000000``).
* **token**: Third param from Webhook (``XXXXXXXXXXXXXXXXXXXXXXXX``).

These are the **optional** parameters:

* **from_**: Bot username. By default *THEN*.
* **to**: Channel (``#other-channel``) or user (``@username``). By default configured channel.
* **icon**: Image URL or emoticon. By default *:robot_face:*.
* **timeout**: Connection timeout to send message.


Message setup
-------------

These are the **required** parameters:

* **body**: Message body.


Instructions for developers
===========================

.. automodule:: then.components.slack
   :members: Slack,SlackMessage
   :noindex:
