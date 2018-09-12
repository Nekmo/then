Line
####

:Component Type: Message
:Requirements: None
:Features: text, sticker

Send a Line message using notify api.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A LINE account created in your mobile.
* Email & password in your LINE account (explained below)
* Notify Bot Token (explained below)


Setup steps
-----------

#. Establish an email and password for your Line account on your mobile.
   Go to ``Config -> Account -> Your email`` and set your email & password.
#. Log in https://notify-bot.line.me/my/ using your email & password.
#. Create a token and select a *target* (1-on-1 sends messages to your account).
   **Token** example: ``iJGhOHToGD5jCvawpigcKB7qpYAK6WRXTMWZYR3xxxx``


Config setup
------------

These are the **required** parameters:

* **token**: Third param from Webhook (``iJGhOHToGD5jCvawpigcKB7qpYAK6WRXTMWZYR3xxxx``).

These are the **optional** parameters:

* **timeout**: Connection timeout to send message. By default ``15 seconds``.


Message setup
-------------

These are the **required** parameters:

* **body**: Message body.

These are the **optional** parameters:

* **sticker_id**: Sticker id to send. *package_id* is required for this parameter.
* **package_id**: Package id for sticker id. *sticker_id* is required for this parameter.


Instructions for developers
===========================

.. automodule:: then.components.line
   :members: Line,LineMessage
   :noindex:
