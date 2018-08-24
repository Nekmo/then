SMS
###

:Component Type: Message
:Requirements: None
:Features: text

Send a SMS to a phone using Twilio.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A Twilio account: https://www.twilio.com/ (you need a valid phone).
* Get a Twilio phone for SMS (explained below)


Setup steps
-----------

#. Go to SMS Console: https://www.twilio.com/console/sms/getting-started/build
#. Click on "Account notifications".
#. Set a project name.
#. Optional: invite a teammate.
#. Click on "Get a number". You must complete the steps to obtain a phone.
#. On **request block** click on *"Show your Auth Token"*. you have here all the necessary information:
  * Your **personal phone**: ``--data-urlencode 'To=<your phone>'``
  * Your **Twilio phone**: ``--data-urlencode 'From=<twilio phone>'``
  * Your **account** and **auth token**: ``-u <account>:<token>``. For example:
    ``AC3z4xabc4867ddc2441acda6b1834xxxx:bcc8476384cc714h991dc56d1906xxxx``


**Optional:** you can set a **alpha sender id** for your phone on *SMS -> Messaging services*. Using an
*alpha sender id* you can **set a name** for the sender of the message.

.. warning:: Your free account is limited and you need to establish a payment method to send messages to other phones.



Config setup
------------

These are the **required** parameters:

* **account**: your Twilio **account** ID (``AC3z4xabc4867ddc2441acda6b1834xxxx``).
* **token**: secret **auth token** (``bcc8476384cc714h991dc56d1906xxxx``).
* **from_**: your **Twilio phone** (``<twilio phone>``).
* **to**: your **account** (``<your phone>``, or another phone if you have established your payment method).


These are the **optional** parameters:

* **timeout**: Connection timeout to send message. By default ``15 seconds``.


Message setup
-------------

These are the **required** parameters:

* **body**: Message body.


Disclaimer
----------
THEN Project is not related to Twilio. THEN is not responsible for the service offered by Twilio.


Instructions for developers
===========================

.. automodule:: then.components.sms
   :members: Sms,SmsMessage
   :noindex:

