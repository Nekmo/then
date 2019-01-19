####
THEN
####


.. image:: https://img.shields.io/travis/Nekmo/then.svg?style=flat-square&maxAge=2592000
  :target: https://travis-ci.org/Nekmo/then
  :alt: Latest Travis CI build status

.. image:: https://img.shields.io/pypi/v/then.svg?style=flat-square
  :target: https://pypi.org/project/then/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/then.svg?style=flat-square
  :target: https://pypi.org/project/then/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/maintainability/Nekmo/then.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/then
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/then/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/then
  :alt: Test coverage

.. image:: https://img.shields.io/requires/github/Nekmo/then.svg?style=flat-square
     :target: https://requires.io/github/Nekmo/then/requirements/?branch=master
     :alt: Requirements Status


A Python library for lazy developers who want actions in their projects. Send communications
and execute actions in remote services without needing to program them. Stop reinventing the
wheel! Send an email, a Telegram message or write to a log with the same API:

.. code-block:: python

    from then.components import Email  # 20 different components! All with the same API

    email = Email(to='nekmo@localhost')
    email.send(subject='[ERROR] HDD SATAIII Barracuda lifetime 10%',
               body="Hello Nekmo,\nThis is the latest monitoring result: ...")


THEN supports most services and methods:

* Telegram
* Email
* Slack
* Discord
* Log to file
* IFTTT
* Home Assistant
* OpenHab
* System command
* HTTP
* Play sound
* SMS
* LINE
* XMPP
* Google Chat
* BroadLink
* Xiaomi Yeelight


**This is embarrassing...** THEN is in development! It's not ready yet but you can subscribe to the project changes.
THEN is being programmed for the `Amazon-dash <https://github.com/Nekmo/amazon-dash>`_ project (with support from
2016 and 400+ stars).



To install then, run this command in your terminal:

.. code-block:: console

    $ sudo pip install then

This is the preferred method to install then, as it will always install the most recent stable release.


Features
========

* TODO

