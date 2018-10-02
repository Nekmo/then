#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import unittest
from unittest.mock import patch, Mock

from then.components import Yeelight
from then.exceptions import ExecuteError


class TestListDevices(unittest.TestCase):
    def setUp(self):
        self.patch_logger = patch('then.components.yeelight.logger')
        self.logger_mock = self.patch_logger.start()

    def tearDown(self):
        self.patch_logger.stop()

    def test_two_bulbs(self):
        from then.components.yeelight import list_devices
        list_devices([{'ip': '1'}, {'ip': '2'}])
        self.assertEqual(self.logger_mock.info.call_count, 3)

    def test_no_bulbs(self):
        from then.components.yeelight import list_devices
        with self.assertRaises(ExecuteError):
            list_devices([])


class TestYeelight(unittest.TestCase):

    def setUp(self):
        self.patch_bulb = patch('yeelight.Bulb')
        self.patch_logger = patch('then.components.yeelight.logger')
        self.bulb_mock = self.patch_bulb.start()
        self.patch_logger.start()

    def tearDown(self):
        self.patch_bulb.stop()
        self.patch_logger.stop()

    def get_component(self, **kwargs):
        return Yeelight(**kwargs)

    def test_send(self):
        from yeelight import Bulb

        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]) as m:
            self.get_component().send()

    def test_toggle(self):
        from yeelight import Bulb
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.bulb_mock.return_value.get_properties = Mock(return_value={'power': 'on'})
            self.get_component().send(state='TOGGLE')
            self.bulb_mock.return_value.turn_off.assert_called_once()

    def test_on_off(self):
        from yeelight import Bulb
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(state='ON')
            self.bulb_mock.return_value.turn_on.assert_called_once()
            self.get_component().send(state='OFF')
            self.bulb_mock.return_value.turn_off.assert_called_once()

    def test_pulse_transition(self):
        from yeelight import Bulb
        patch_pulse = patch('yeelight.transitions.pulse')
        pulse_mock = patch_pulse.start()
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(flow_transition='pulse', color='red', flow_count=3)
            flow = self.bulb_mock.return_value.start_flow.call_args[0][0]
            self.assertEqual(flow.count, 3)
            pulse_mock.assert_called_once_with(255, 0, 0, 250, 100)
            self.bulb_mock.return_value.set_rgb.assert_not_called()
        patch_pulse.stop()

    def test_transition_no_params(self):
        from yeelight import Bulb
        patch_trans = patch('yeelight.transitions.strobe')
        trans_mock = patch_trans.start()
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(flow_transition='strobe', flow_duration=1000)
            trans_mock.assert_called_once_with()
        patch_trans.stop()

    def test_christmas_transition(self):
        from yeelight import Bulb
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(flow_transition='christmas', flow_duration=500,
                                      brightness=80, flow_sleep=600)
            flow = self.bulb_mock.return_value.start_flow.call_args[0][0]
            self.assertEqual(flow.transitions[0].brightness, 80)
            self.assertEqual(flow.transitions[0].duration, 500)
            self.assertEqual(flow.transitions[1].duration, 600)
            self.bulb_mock.return_value.set_brightness.assert_not_called()

    def test_color(self):
        from yeelight import Bulb
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(color='#FAEBD7')
            self.bulb_mock.return_value.set_rgb.assert_called_with(250, 235, 215)

    def test_brightness(self):
        from yeelight import Bulb
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(brightness=65)
            self.bulb_mock.return_value.set_brightness.assert_called_with(65)

    def test_temperature(self):
        from yeelight import Bulb
        with patch('yeelight.discover_bulbs', return_value=[Bulb('')]):
            self.get_component().send(temperature=17)
            self.bulb_mock.return_value.set_color_temp.assert_called_with(17)
