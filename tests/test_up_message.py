#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `microparcel` package."""


import unittest

from microparcel import microparcel as up


class TestMicroparcelMessage(unittest.TestCase):
    """Tests for `microparcel` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_8bits(self):
        """Test access to 8 bits messages."""
        # full nibble, off 0
        msg = up.Message(size=4)

        msg.data[0] = 0xF
        b = msg.get(0, 4)
        self.assertTrue(b == 0xF)
        b = msg.get(4, 4)
        self.assertTrue(b == 0x0)
        msg.data[0] = 0x0


        # full nibble, off 8
        msg.data[1] = 0xF
        b = msg.get(8, 4)
        self.assertTrue(b == 0xF)
        b = msg.get(12, 4)
        self.assertTrue(b == 0x0)
        msg.data[1] = 0x0

        # full nibble, off 6
        msg.data[0] = 0b11000000
        msg.data[1] = 0b00000011
        b = msg.get(0, 6)
        self.assertTrue(b == 0x0)
        b = msg.get(10, 6)
        self.assertTrue(b == 0x0)
        b = msg.get(6, 4)
        self.assertTrue(b == 0xF)
        msg.data[1] = 0x0
        msg.data[0] = 0x0

        # full byte, off 0
        msg.data[0] = 0xFF
        b = msg.get(0, 8)
        self.assertTrue(b == 0xFF)
        b = msg.get(8, 8)
        self.assertTrue(b == 0x0)
        msg.data[0] = 0x0


        # full byte, off 4
        msg.data[0] = 0b11110000
        msg.data[1] = 0b00001111
        b = msg.get(0, 4)
        self.assertTrue(b == 0x0)
        b = msg.get(12, 4)
        self.assertTrue(b == 0x0)
        b = msg.get(4, 8)
        self.assertTrue(b == 0xFF)
        msg.data[1] = 0x0
        msg.data[0] = 0x0


        # 6bits, off 6
        msg.data[0] = 0b11000000
        msg.data[1] = 0b00001001
        b = msg.get(0, 6)
        self.assertTrue(b == 0x0)
        b = msg.get(12, 4)
        self.assertTrue(b == 0x0)
        b = msg.get(6, 6)
        self.assertTrue(b == 0b100111)
        msg.data[1] = 0x0
        msg.data[0] = 0x0



    def test_set_8bits(self):
        """Test write to 8 bits messages."""
        msg = up.Message(size=4)

        msg.set(0, 4, 0xF)
        self.assertTrue(msg.data[0] == 0xF) 
        msg.data[0] = 0x0

        msg.set(0, 8, 0xFF)
        self.assertTrue(msg.data[0] == 0xFF) 
        msg.data[0] = 0x0

        msg.set(4, 4, 0xF)
        self.assertTrue(msg.data[0] == (0xF<<4)) 
        msg.data[0] = 0x0

        msg.set(2, 4, 0xF)
        self.assertTrue(msg.data[0] == (0xF<<2)) 
        msg.data[0] = 0x0

        msg.set(6, 4, 0xF)
        self.assertTrue(msg.data[0] == (0x3<<6)) 
        self.assertTrue(msg.data[1] == (0x3)) 
        msg.data[0] = 0x0
        msg.data[1] = 0x0

        msg.set(6, 8, 0xFF)
        self.assertTrue(msg.data[0] == (0x3<<6)) 
        self.assertTrue(msg.data[1] == (0x3F)) 
        msg.data[0] = 0x0
        msg.data[1] = 0x0

