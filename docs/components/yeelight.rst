Yeelight
########

:Component Type: Message
:Requirements: None
:Features: other

Control a local Xiaomi Yeelight bulb.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

* A Yeelight bulb in the same network.


Config setup
------------

These are the **optional** parameters:

* **ip**: Yeelight bulb IP.

A ip is not mandatory but it is recommended. THEN will detect the IP if you have only one light bulb in the network.
THEN will output the IP so that you can define it in your configuration (define the ip will avoid errors
and allows faster execution).

Some routers may not remember the IP for your Yeelight. Maybe you have to make some changes to your router (like
setting a static IP for your light bulb).


Message setup
-------------

These are the **optional** parameters:

* **state**: ``ON``, ``OFF`` or ``TOGGLE``. By default ``ON``.
* **brightness**: Change brightness. 0-100 value. Some *flow_transition* use this parameter. After animation, the
  default brightness is restored.
* **color**: Change color (only available on some devices). Hexadecimal color (``#00FF00``) or color name (140
  registered names).
* **temperature** (in Kelvin). Change color temperature. 1700-6500 value. 1700 is warmer and 6500 colder.
* **effect**: effect on ``ON``/``OFF`` change or ``TOGGLE``. Choices: ``smooth`` or ``sudden``. By default ``smooth``.
* **effect_duration**: It only has effect with smooth *effect*. In milliseconds. By default ``300``.
* **flow_transition**: Color animations included with THEN. Choices:
 * ``disco``
 * ``temp``
 * ``strobe``
 * ``pulse`` (color is required).
 * ``strobe_color`` (*brightness* parameter available).
 * ``alarm`` (*flow_duration* parameter available).
 * ``police`` (*flow_duration* and *brightness* parameter available).
 * ``police2`` (*flow_duration* and *brightness* parameter available).
 * ``lsd`` (*flow_duration* and *brightness* parameter available).
 * ``christmas`` (*flow_duration*, *brightness* and *flow_sleep* parameter available).
 * ``rgb`` (*flow_duration*, *brightness* and *flow_sleep* parameter available).
 * ``randomloop`` (*flow_duration* and *brightness*).
 * ``slowdown`` (*flow_duration* and *brightness*).
* **flow_count**: Times that the *flow_transition* is repeated.
* **flow_duration**: duration in milliseconds. Only available in marked *flow_transition*.
* **flow_sleep**: time in milliseconds. Only available in marked *flow_transition*.

The *flow transitions* are courtesy of
`Python Yeelight Project <https://yeelight.readthedocs.io/en/stable/index.html>`_. 


Instructions for developers
===========================

.. automodule:: then.components.yeelight
   :members: Yeelight,YeelightMessage
   :noindex:
