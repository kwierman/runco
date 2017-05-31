#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_runco
----------------------------------
Tests for `runco` module.
"""

import pytest
import unittest
import sys
from contextlib import contextmanager
from click.testing import CliRunner
import logging

from runco import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    def test_get_config(self):
        c = config.Config()
        assert(c is not None)

    def test_config_has_content(self):
        c = config.Config()
        assert(c.data['slowcontrols'] is not None)
        assert(c.data['ecl'] is not None)