Home Assistant
##############

:Component Type: Event
:Requirements: None

Execute an Home Assistant event using Home Assistant API.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A Home Assistant installation ( https://www.home-assistant.io/getting-started/ ).


Config setup
------------

These are the **required** parameters:

* **url**: Home assistant address (ip or domain) with or without protocol and port (by default ``http``
  and ``8123``). Syntax: ``[<protocol>://]<server>[:<port>]``. For example: ``https://hassio.local:1234``.

These are the **optional** parameters:

* **access**: HomeAssistant password for API (``x-ha-access`` header).
* **timeout**: Connection timeout to send event.


Message setup
-------------

These are the **required** parameters:

* **event**: You can use any event name. Just use an event name in THEN and create an automation
  in Homeassistant for your event.

More info about events in the homeassistant documentation:

* https://www.home-assistant.io/docs/configuration/events/
* https://www.home-assistant.io/docs/automation/trigger/

These are the **optional** parameters:

* **body**: Event data to send (JSON).


Instructions for developers
===========================

.. automodule:: then.components.homeassistant
   :members: HomeAssistant,HomeAssistantMessage
   :noindex:
