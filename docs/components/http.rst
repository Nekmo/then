HTTP
####

:Component Type: Other
:Requirements: None

Execute a HTTP service or WebHook. You can use this component to execute any service not supported by THEN.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

There are no prerequisites. You only need to know the url to execute and required options.


Config setup
------------

These are the **required** parameters:

* **url**: complete URL. Syntax: ``<protocol>://<server>[:<port>]``.

These are the **optional** parameters:

* **method**: HTTP method. By default ``GET``.
* **headers**: Headers to send to the server. ``content_type`` will be overwritten if it is defined later.
* **content_type**: HTTP Content-Type Header on request. For example: ``text/plain``. THEN includes some aliases:
  ``form = application/x-www-form-urlencoded``. ``json = application/json``. ``plain = text/plain``. If body is
  defined, default is ``json``.
* **auth**: HTTP Basic Auth. Syntax: ``<user>:<password>``.
* **max_body_read**: Maximum size to read from the server. By default ``102400 bytes``.
* **timeout**: Connection timeout to send message. By default ``15 seconds``.


Message setup
-------------

These are the **optional** parameters:

* **body**: Request payload. Only if the method is ``POST``/``PUT``/``PATCH``.


Instructions for developers
===========================

.. automodule:: then.components.http
   :members: Http,HttpMessage
   :noindex:
