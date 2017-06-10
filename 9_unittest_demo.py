#! /usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'cent'

'''
a demo shows how to use unittest module
write unit test for dict class
'''

import unittest

# all the test function must named with prefix 'test', otherwise it will not be run
class TestDict(unittest.TestCase):
    # override special function setUp(), run before every test function
    def setUp(self):
        print('setUp: Begin')

    # override special function tearDown(), run after every test function
    def tearDown(self):
        print('tearDown: End')

    # unit test function named with prefix test
    def test_init(self):
        d = dict(a=1, b='test')
        self.assertIsInstance(d, dict)
        self.assertTrue('a' in d)
        self.assertTrue('b' in d)
        self.assertEqual(d['a'], 1)
        self.assertEqual(d['b'], 'test')

    def test_key(self):
        d = dict()
        d['key'] = 'value'
        self.assertTrue('key' in d)

    def test_value(self):
        d = dict()
        d['key'] = 'value'
        self.assertEqual(d['key'], 'value')

    def test_key_error(self):
        d = dict()
        self.assertFalse('key' in d)

        # assert to raise exception
        with self.assertRaises(KeyError):
            value = d['key']


# testing to run all unit-test function
if __name__ == '__main__':
    unittest.main()