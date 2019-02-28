#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `microparcel` package."""


import unittest

from microparcel import microparcel as up


class TestMicroparcelParser(unittest.TestCase):
    """Tests for `microparcel` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_encode(self):
        """Test Parser Encoding."""
        parser = up.make_parser_cls(4)()

        msg = up.Message(4)
        msg.data[0] = 0
        msg.data[1] = 1
        msg.data[2] = 2
        msg.data[3] = 3

        frame = parser.encode(msg)

        self.assertEqual(frame.SOF, 0xAA)
        self.assertEqual(frame.message.data[0], 0)
        self.assertEqual(frame.message.data[1], 1)
        self.assertEqual(frame.message.data[2], 2)
        self.assertEqual(frame.message.data[3], 3)
        self.assertEqual(frame.checksum, 0xAA + sum([0,1,2,3]))

    def test_decode(self):
        """Test Parser Decoding."""
        parser = up.make_parser_cls(4)()
        msg = up.Message()

        # valid message
        self.assertEqual(parser.parse(0xAA, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x0, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x1, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x2, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x3, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0xFF & (0xAA + 0 + 1 + 2 + 3), msg), parser.Status.Complete)

        self.assertEqual(msg.data[0], 0)
        self.assertEqual(msg.data[1], 1)
        self.assertEqual(msg.data[2], 2)
        self.assertEqual(msg.data[3], 3)


        # invalid CS
        self.assertEqual(parser.parse(0xAA, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x44, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x99, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0xB, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x4, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0xFF, msg), parser.Status.Error)

        # Invalid SOF
        self.assertEqual(parser.parse(0xDD, msg), parser.Status.Error)
        self.assertEqual(parser.parse(0xEE, msg), parser.Status.Error)
        self.assertEqual(parser.parse(0xBB, msg), parser.Status.Error)
        self.assertEqual(parser.parse(0xAA, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x4, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x5, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x6, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0x7, msg), parser.Status.NotComplete)
        self.assertEqual(parser.parse(0xFF & (0xAA + 4+5+6+7), msg), parser.Status.Complete)