import subprocess

from dataclasses import dataclass

from then.components.base import Component, Message
from then.exceptions import ExecuteError, ValidationError

EXECUTE_SHELL_PARAM = '-c'


def get_shell(name):
    """Absolute path to command

    :param str name: command
    :return: command args
    :rtype: list
    """
    if name.startswith('/'):
        return [name]
    return ['/usr/bin/env', name]


def run_as_cmd(cmd, user, shell='bash'):
    """Get the arguments to execute a command as a user

    :param str cmd: command to execute
    :param user: User for use
    :param shell: Bash, zsh, etc.
    :return: arguments
    :rtype: list
    """
    return ['sudo', '-s', '--set-home', '-u', user] + get_shell(shell) + [EXECUTE_SHELL_PARAM, cmd]


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


@dataclass
class CommandMessage(Message):
    cmd: str
    component: 'Command' = None

    def send(self):
        if self.component.ssh:
            cmd = execute_over_ssh(self.cmd, self.component.ssh, self.component.cwd)
            output = execute_cmd(cmd)
        else:
            cmd = run_as_cmd(self.cmd, self.component.user)
            output = execute_cmd(cmd, self.component.cwd)
        if output:
            return output[0]


@dataclass
class Command(Component):
    ssh: str
    user: str
    cwd: str

    _message_class = CommandMessage

    def __post_init__(self):
        parts = self.ssh.split(':', 1)
        if len(parts) > 1 and not parts[1].isdigit():
            raise ValidationError('Invalid port number on ssh config: {}'.format(parts[1]))
