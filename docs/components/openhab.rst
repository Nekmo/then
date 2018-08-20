OpenHab
#######

:Component Type: Event
:Requirements: None

Execute an OpenHab event using OpenHab API.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A OpenHab installation ( https://www.openhab.org/docs/ ).
* Create a OpenHab Item: https://www.openhab.org/docs/configuration/items.html


Config setup
------------

These are the **required** parameters:

* **url**: OpenHab address (ip or domain) with or without protocol and port (by default ``http``
  and ``8080``). Syntax: ``[<protocol>://]<server>[:<port>]``. For example: ``https://192.168.1.140:1234``.

These are the **optional** parameters:

* **timeout**: Connection timeout to send event.


Message setup
-------------

These are the **required** parameters:

* **item**: Your OpenHab item name.

More info about events in the openhab documentation:

* https://www.openhab.org/docs/configuration/items.html

These are the **optional** parameters:

* **state**: State to send. Options ``ON``/``OFF``. ``ON`` by default.


Instructions for developers
===========================

.. automodule:: then.components.openhab
   :members: OpenHab,OpenHabMessage
   :noindex:
