Discord
#######

:Component Type: Message
:Requirements: None
:Features: text

Send an Discord message using a application.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* An Discord account and server to send the message (you need to have permissions on the server).
* Create a Application (explained below)
* Create a bot (explained below)
* Get your channel id (explained below)


Setup steps
-----------

#. Connect to your Discord account in the browser.
#. Go to: https://discordapp.com/developers/applications/
#. Create a application and get your client ID. For example: ``47874976890709XXXX``.
#. Create a bot in your application (left panel) and get reveal secret token. For example:
   ``NDF4NGQ5GzY6OTF3MAk2vDc1.D1xvWv.nMarFQh3UdjaDLXZZggL1xxxxxx``.
#. Authorize your bot to send messages. Edit this url and paste It in your browser:
   ``https://discordapp.com/oauth2/authorize?&client_id=47874976890709XXXX&scope=bot&permissions=8``.
   Replace ``47874976890709XXXX`` with your client ID. You can change ``permissions`` (8) with your
   needed permissions. Get your permissions integer using the bottom section on Bot tab.
#. Get your channel ID. Go to the channel in your browser and get the second id in url. For example:
   ``https://discordapp.com/channels/48014601482xxxxxx/48014601482xxxx01``
   (channel id: ``48014601482xxxx01``).


Config setup
------------

These are the **required** parameters:

* **token**: Your secret bot token (``NDF4NGQ5GzY6OTF3MAk2vDc1.D1xvWv.nMarFQh3UdjaDLXZZggL1xxxxxx``).
* **to**: Channel id (``47874976890709XXXX``)

These are the **optional** parameters:

* **bot_token**: True or False. Token is the bot token. By default True.
* **timeout**: Connection timeout to send message. By default ``15 seconds``.


Message setup
-------------

These are the **required** parameters:

* **body**: Message body.
* **tts**: True or False. Use text to speach. By default false.


Instructions for developers
===========================

.. automodule:: then.components.discord
   :members: Discord,DiscordMessage
   :noindex:
