import os
import random
import subprocess
from pathlib import Path
from typing import Union

from dataclasses import dataclass

from then.components.base import Component, Message
from then.exceptions import ExecuteError, ValidationError, ConfigError

EXECUTE_SHELL_PARAM = '-c'


"""Command component service
"""



def get_shell(name='bash'):
    """Absolute path to command

    :param str name: command
    :return: command args
    :rtype: list
    """
    if name.startswith('/'):
        return [name]
    return ['/usr/bin/env', name]


def get_execute_command(cmd, shell='bash'):
    if isinstance(cmd, (tuple, list)):
        return cmd
    return get_shell(shell) + [EXECUTE_SHELL_PARAM, ' '.join(cmd)]


def run_as_cmd(cmd, user, shell=None):
    """Get the arguments to execute a command as a user

    :param str cmd: command to execute
    :param user: User for use
    :param shell: Bash, zsh, etc.
    :return: arguments
    :rtype: list
    """
    shell = shell or 'bash'
    if not user:
        return get_execute_command(cmd, shell)
    return ['sudo', '-s', '--set-home', '-u', user] + get_execute_command(cmd, shell)


def execute_cmd(cmd, cwd=None, timeout=5):
    """Excecute command on thread

    :param cmd: Command to execute
    :param cwd: current working directory
    :return: None
    """
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        p.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    else:
        stdout, stderr = p.stdout.read(), p.stderr.read()
        stdout, stderr = stdout.decode('utf-8', errors='ignore'), stderr.decode('utf-8', errors='ignore')
        if p.returncode:
            raise ExecuteError('Error running command {}: The error code {} has returned. Stderr: {}'.format(
                ' '.join(cmd), p.returncode, stderr
            ))
        else:
            return stdout, stderr


def execute_over_ssh(cmd, ssh, cwd=None, shell='bash'):
    """Excecute command on remote machine using SSH

    :param cmd: Command to execute
    :param ssh: Server to connect. Port is optional
    :param cwd: current working directory
    :return: None
    """
    port = None
    parts = ssh.split(':', 1)
    if len(parts) > 1:
        port = parts[1]
    quoted_cmd = ' '.join([x.replace("'", """'"'"'""") for x in cmd.split(' ')])
    remote_cmd = ' '.join([
        ' '.join(get_shell(shell)), # /usr/bin/env bash
        ' '.join([EXECUTE_SHELL_PARAM, "'", ' '.join((['cd', cwd, ';'] if cwd else []) + [quoted_cmd]), "'"])],
    )
    return ['ssh', parts[0]] + (['-p', port] if port else []) + ['-C'] + [remote_cmd]


class CommandMessageBase(Message):
    cmd: Union[str, list] = None
    component: 'Command' = None

    def send(self):
        if self.component.ssh:
            cmd = execute_over_ssh(self.get_cmd(), self.component.ssh, self.component.cwd)
            output = execute_cmd(cmd)
        else:
            cmd = run_as_cmd(self.get_cmd(), self.component.user)
            output = execute_cmd(cmd, self.component.cwd)
        if output:
            return output[0]

    def get_cmd(self):
        return self.cmd


@dataclass
class CommandMessage(CommandMessageBase):
    """:class:`CommandMessage` instance created by :class:`Command` component. Create It using::

        from then.components import Command

        message = Command().message(cmd=['ls', '-l'])
        message.send()

    :arg cmd: System Command to execute. List or string
    """
    cmd: Union[str, list]
    component: 'Command' = None


class CommandBase(Component):
    user: str = None
    cwd: str = None
    ssh: str = None

    def __post_init__(self):
        parts = (self.ssh or '').split(':', 1)
        if len(parts) > 1 and not parts[1].isdigit():
            raise ValidationError('Invalid port number on ssh config: {}'.format(parts[1]))


@dataclass
class Command(CommandBase):
    """Create a Command instance to execute a system command::

        from then.components import Command

        Command(user='myuser', cwd='/home/myuser/Desktop')\\
            .send(cmd='ls -l')

    :param user: System user to use. Only available on local system
    :param cwd: Current directory
    :param ssh: Execute command over ssh. Syntax: ``<user>@<machine>[:<port>]``
    """
    user: str = None
    cwd: str = None
    ssh: str = None

    _message_class = CommandMessage


class PathBase(Component):
    action: str = 'ordered'
    pattern: str = '*'
    on_end: str = 'repeat'
    _actions = ['ordered', 'shuffle']
    _on_ends = ['stop', 'repeat']

    def __post_init__(self):
        self._action = self.get_action()
        self._on_end = self.get_on_end()

    def _availables(self, value, name, availables):
        new_action = value.lower()
        if new_action not in availables:
            raise ConfigError('Invalid {} in {}: {}. Availables: {}'.format(
                name, self.__class__.__name__, value, ', '.join(availables)
            ))
        return new_action

    def get_action(self):
        return self._availables(self.action, 'action', self._actions)

    def get_on_end(self):
        return self._availables(self.on_end, 'on_end', self._on_ends)


class PathMessageBase(Message):
    path: str
    component: PathBase = None
    _files = None

    def get_files(self):
        if not os.path.lexists(self.path):
            raise ConfigError('{} path does not exists.'.format(self.path))
        if os.path.isfile(self.path):
            return [self.path]
        elif self.component._action == 'ordered':
            return sorted(self.list_directory())
        elif self.component._action == 'shuffle':
            files = self.list_directory()
            random.shuffle(files)
            return files


    def get_next(self, on_end=None):
        if self._files is None:
            self._files = self.get_files()
        on_end = on_end or self.component._on_end
        try:
            return self._files.pop(0)
        except IndexError:
            if on_end == 'stop':
                raise StopIteration
            elif on_end == 'repeat':
                self._files = None
                return self.get_next('stop')

    def list_directory(self):
        return [str(path.resolve()) for path
                in Path(self.path).glob(self.component.pattern) if path.is_file()]
