#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `then` package."""
import unittest
from unittest.mock import patch


from then.components import Yeelight


class TestYeelight(unittest.TestCase):

    def setUp(self):
        self.patch_bulb = patch('yeelight.Bulb')
        self.patch_logger = patch('then.components.yeelight.logger')
        self.patch_bulb.start()
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
