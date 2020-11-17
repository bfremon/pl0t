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
        self.assertRaises(SyntaxError, pl0t._parse_datas, d)
        d = {'foo': [1,]}
        df = pd.DataFrame(d)
        self.assertRaises(SyntaxError, pl0t._parse_datas, df)
        d = {'foo': [4, 5, 6], 'cat': [1, 3, 4]}
        df = pd.DataFrame(d)
        self.assertRaises(SyntaxError, pl0t._parse_datas(), df)
        self.assertTrue(pl0t._parse_datas(df, cat='cat') == df)
