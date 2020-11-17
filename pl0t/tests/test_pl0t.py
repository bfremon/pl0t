#!/usr/bin/env python3

import unittest
import pl0t
import pandas as pd
import numpy as np

class test_pl0t(unittest.TestCase):
    def test__parse_datas(self):
        d = {}
        self.assertRaises(SyntaxError, pl0t._parse_datas, d)
        df = pd.DataFrame(d)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df)
        d1 = {'foo': [1,]}
        df1 = pd.DataFrame(d1)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df1)
        d2 = {'foo': [4, 5, 6], 'cat': [1, 3, 4]}
        df2 = pd.DataFrame(d2)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df2)
        r = pl0t._parse_datas(df2, cat='cat')
        self.assertTrue(df2.equals(r))
