#!/usr/bin/env python3

import unittest
import pl0t
import pandas as pd
import numpy as np

class test_pl0t(unittest.TestCase):
    def test__parse_datas(self):
        d = {}
        s1 = [4, 5, 6]
        s2 = [1, 3, 4]
        self.assertRaises(SyntaxError, pl0t._parse_datas, d)
        df = pd.DataFrame(d)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df)
        d1 = {'foo': [1,]}
        df1 = pd.DataFrame(d1)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df1)
        d2 = {'foo': s1, 'cat': s2}
        df2 = pd.DataFrame(d2)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df2)
        r = pl0t._parse_datas(df2, cat='cat')
        self.assertTrue(df2.equals(r))
        self.assertRaises(SyntaxError, pl0t._parse_datas, df2, [1, 2, 4])
        self.assertRaises(SyntaxError, pl0t._parse_datas, df2, {})
        self.assertRaises(SyntaxError, pl0t._parse_datas,
                          s1, s2, labels=('a',))
        r = pl0t._parse_datas(s1, s2, labels=('foo', 'cat'))
        self.assertTrue(r.equals(df2))
        r = pl0t._parse_datas(s1, s2)
        self.assertTrue(r.equals(pd.DataFrame({1: s1, 2: s2})))
