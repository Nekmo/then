#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import subprocess
import unittest
from io import BytesIO
from unittest.mock import patch, Mock

from then.components.command import Command, execute_over_ssh, get_shell, get_execute_command
from then.exceptions import ExecuteError, ValidationError


class TestExecuteCmdFunction(unittest.TestCase):

    @patch.object(subprocess, 'Popen')
    def test_success(self, m):
        process_mock = Mock()
        process_mock.configure_mock(**{'returncode': 0, 'stdout': BytesIO(bytes('foo', 'utf-8'))})
        m.return_value = process_mock
        out = Command().send(cmd=['ls'])
        self.assertEqual(out, 'foo')

    @patch.object(subprocess, 'Popen')
    def test_success_without_list(self, m):
        process_mock = Mock()
        process_mock.configure_mock(**{'returncode': 0, 'stdout': BytesIO(bytes('foo', 'utf-8'))})
        m.return_value = process_mock
        out = Command().send(cmd='ls -l')
        self.assertEqual(out, 'foo')
        m.assert_called_once_with(get_execute_command('ls -l'), cwd=None, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

    @patch.object(subprocess, 'Popen')
    def test_error(self, m):
        process_mock = Mock()
        process_mock.configure_mock(**{'returncode': 1})
        m.return_value = process_mock
        with self.assertRaises(ExecuteError):
            Command().send(cmd=['ls'])

    @patch.object(subprocess, 'Popen')
    def test_timeout(self, m):
        def side_effect(timeout=None):
            raise subprocess.TimeoutExpired('', timeout)

        process_mock = Mock()
        process_mock.configure_mock(**{'wait.side_effect': side_effect})
        m.return_value = process_mock
        self.assertEqual(Command().send(cmd=['ls']), None)


class TestCommandSsh(unittest.TestCase):
    def test_invalid_port(self):
        with self.assertRaises(ValidationError):
            Command(ssh='machine:spam')

    def test_execute_without_port(self):
        cmd = execute_over_ssh('ls', 'machine')
        self.assertEqual(['ssh', 'machine', '-C', "/usr/bin/env bash -c ' ls '"], cmd)

    def test_execute_with_port(self):
        cmd = execute_over_ssh('ls', 'machine:222')
        self.assertEqual(['ssh', 'machine', '-p', '222', '-C', "/usr/bin/env bash -c ' ls '"], cmd)

    def test_execute_double_quotes(self):
        cmd = execute_over_ssh('"ls"', 'machine:222')
        self.assertEqual(['ssh', 'machine', '-p', '222', '-C', "/usr/bin/env bash -c ' \"ls\" '"], cmd)

    def test_execute_single_quotes(self):
        cmd = execute_over_ssh('\'ls\'', 'machine:222')
        self.assertEqual(['ssh', 'machine', '-p', '222', '-C', "/usr/bin/env bash -c ' '\"'\"'ls'\"'\"' '"], cmd)


class TestCommand(unittest.TestCase):
    subject = 'subject'
    body = 'body'

    @patch('subprocess.Popen', autospec=True)
    def test_execution_success(self, popen_mock):
        popen_mock.return_value = Mock()
        popen_mock_obj = popen_mock.return_value

        popen_mock_obj.communicate.return_value = ("OUT", "")
        popen_mock_obj.returncode = 0
        Command().send(cmd='ls')
        popen_mock.assert_called_once()

    @patch('subprocess.Popen', autospec=True)
    def test_execution_error(self, popen_mock):
        popen_mock.return_value = Mock()
        popen_mock_obj = popen_mock.return_value

        popen_mock_obj.communicate.return_value = ("OUT", "ERR")
        popen_mock_obj.returncode = 1
        with self.assertRaises(ExecuteError):
            Command().send(cmd='ls')

    @patch('then.components.command.execute_cmd')
    def test_ssh(self, mock):
        component = Command(ssh='foo@bar')
        with patch('then.components.command.execute_over_ssh') as execute_over_ssh_mock:
            component.send(cmd='ls')
            execute_over_ssh_mock.assert_called_once()
        mock.assert_called_once()

    def test_get_shell(self):
        self.assertEqual(get_shell('/usr/bin/command'), ['/usr/bin/command'])
        self.assertEqual(get_shell('command'), ['/usr/bin/env', 'command'])
