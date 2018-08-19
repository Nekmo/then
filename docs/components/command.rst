

Command
#######

:Component Type: Others
:Requirements: None

Excecute a local system command or execute It on a remote machine using SSH. This component allows you
to run programs (like a browser, Spotify...) on the local machine or a remote machine. It also allows
to execute bash commands and scripts.


Setup for users
===============

These instructions are for the users. For developer instructions, look below.


Prerequisites
-------------

There are no prerequisites. You only need to know the command to execute.


Config setup
------------

These are the **optional** parameters:

* **user**: System user that will execute the command. It only works on a local machine running the program as root.
* **cwd**: Directory in which the command is executed.
* **ssh**: It allows executing the command on a remote machine. The value of the ssh option must be the name/IP of
  the machine. You can also specify the port. For example: ``machine:2222``


Message setup
-------------

These are the **required** parameters:

* **cmd**: Command to execute. Arguments can be placed after the command.


Instructions for developers
===========================

.. autoattribute:: then.components.command.Command.user

.. automodule:: then.components.command
   :members: Command,CommandMessage
   :noindex:
