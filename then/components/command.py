import subprocess
from typing import Union

from dataclasses import dataclass

from then.components.base import Component, Message
from then.exceptions import ExecuteError, ValidationError

EXECUTE_SHELL_PARAM = '-c'


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
    user: str = None
    cwd: str = None
    ssh: str = None

    _message_class = CommandMessage

