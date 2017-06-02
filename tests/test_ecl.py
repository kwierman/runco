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
from runco import ecl, config


class TestECL(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.config = config.Config()

    def tearDown(self):
        self.config = None

    def test_setup(self):
        conn = ecl.ConfiguredECLConnection(self.config.data['ecl'])
        assert(conn is not None)

    def test_list(self):
        conn = ecl.ConfiguredECLConnection(self.config.data['ecl'])
        l = conn.list()
        assert(l is not None)
        assert(len(l)>0)
