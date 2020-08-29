import unittest

from framework import Dict


class TestDict(unittest.TestCase):

    def test_key(self):
        d = Dict()
        d.a.b.c = 2
        self.assertEqual(d['a']['b']['c'], 2)

    def test_deep(self):
        origin_value = {
            'a': {
                'b': {
                    'c': 4
                }
            }
        }
        value = Dict.create(origin_value)
        self.assertEqual(value.a.b.c, 4)
        self.assertIsNotNone(value.a.b.c.d)
