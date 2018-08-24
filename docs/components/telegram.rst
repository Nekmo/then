Telegram
########

:Component Type: Message
:Requirements: None
:Features: text

Send an telegram message using Bots API.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* An Telegram account.
* Create a bot (explained below).
* Your user/group ID (explained below).


Setup steps
-----------

#. In Telegram, start a conversation with `@BotFather <https://t.me/botfather>`_ and execute ``/newbot``.
   Follow the steps and you will get the **bot token**. For example: ``520604247:ABF0EHnzZxDIQ15Re83iWZojuvja24Exxxx``.
#. Get the id of the recipient of the message. The steps are different if the recipient is a group or a user.


Send to user
^^^^^^^^^^^^

#. Get your **id** using `@get_id_bot <https://t.me/get_id_bot>`_ bot. For example: ``2379xxxx``.
#. For security, your bot can only send messages to users who have started a conversation with the bot.
   Start a conversation with your bot (``@<your_bot>``).


Send to group
^^^^^^^^^^^^^

#. For get your **group id**, add `@get_id_bot <https://t.me/get_id_bot>`_ to the group and execute
   ``/my_id@get_id_bot``. For example: ``-600503825xxxx``.
#. Add ``@<your_bot>`` to your group.


Config setup
------------

These are the **required** parameters:

* **token**: your secret **bot token**. For example: ``520604247:ABF0EHnzZxDIQ15Re83iWZojuvja24Exxxx``.
* **to**: the id of the user or the group. For example: ``2379xxxx`` (user) or ``-600503825xxxx`` (group,
  including negative symbol).


Message setup
-------------

These are the **required** parameters:

* **body**: Message body.


Instructions for developers
===========================

.. automodule:: then.components.telegram
   :members: Telegram,TelegramMessage
   :noindex:
