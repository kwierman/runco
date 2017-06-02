#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ecl
----------------------------------
Tests for `runco.ecl` module.
"""

import pytest
import unittest
import sys
import logging
from runco import sc, config


class TestSlowCon(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.config = config.Config()

    def tearDown(self):
        self.config = None

    def test_setup(self):
        slowcon = sc.ConfiguredSlowControls(self.config.data['slowcontrols'])
        assert(slowcon is not None)

    def test_last_day_data(self):
        slowcon = sc.ConfiguredSlowControls(self.config.data['slowcontrols'])
        ch = slowcon.channel_id_by_name['uB_Cryo_IFIX_1_0/PT102']
        logging.info("Channel: " + str(ch))
        slowcon.query_timebinned_data(ch,1, '2017-05-13 00:00:00', '2017-06-30 01:00:00')
        result = slowcon.cur.fetchall()
        assert(result is not None)
