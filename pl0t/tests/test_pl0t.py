#!/usr/bin/env python3

import unittest
import pl0t
import pandas as pd
import numpy as np

class test_pl0t(unittest.TestCase):
    def test_prep_data(self):
        # no empty data allowed
        self.assertRaises(SyntaxError, pl0t._prep_data, None)
        self.assertRaises(SyntaxError, pl0t._prep_data, '')
        self.assertRaises(SyntaxError, pl0t._prep_data, [])
        self.assertRaises(SyntaxError, pl0t._prep_data, {})
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame({}))
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.Series([], dtype='float64'))
        self.assertRaises(SyntaxError, pl0t._prep_data, np.array([]))

        # no 1D / nD (n >= 2) data mixing 
        d =  {'a': [1, 2, 3]}
        self.assertRaises(SyntaxError, pl0t._prep_data, [1, 2, 3], d)
        self.assertRaises(SyntaxError, pl0t._prep_data, [1, 2, 3], pd.DataFrame(d))
        self.assertRaises(SyntaxError, pl0t._prep_data, d, d)
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame(d), pd.DataFrame(d))
        self.assertRaises(SyntaxError, pl0t._prep_data, [1, 2, 3], d, pd.DataFrame(d))
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.Series([1, 2, 3]), d, pd.DataFrame(d))

        self.assertRaises(SyntaxError, pl0t._prep_data, np.array([1, 2, 3]), d)
        self.assertRaises(SyntaxError, pl0t._prep_data, np.array([1, 2, 3]), pd.DataFrame(d))
        self.assertRaises(SyntaxError, pl0t._prep_data, d, d)
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame(d), pd.DataFrame(d))
        self.assertRaises(SyntaxError, pl0t._prep_data, np.array([1, 2, 3]), d, pd.DataFrame(d))

        a = [1, 2, 3]
        b = [4, 5, 6]
        c = [7, 8, 9]
        d = {0: a, 1: b, 2: c}

        # cat needed for DataFrame
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame(d))
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame(d), cat='d')

        # val needed for DataFrame
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame(d), cat='a')
        self.assertRaises(SyntaxError, pl0t._prep_data, pd.DataFrame(d), cat='a', val='d')

        # aggregation testing
        r = pl0t._prep_data(a, b, c)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value']
            self.assertTrue(set(out_v) == set(d[cat]))

        r = pl0t._prep_data(pd.Series(a), pd.Series(b), c)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value']
            self.assertTrue(set(out_v) == set(d[cat]))
            
        d = {0: np.array(a), 1: np.array(b), 2: np.array(c)}
        r = pl0t._prep_data(a, b, c)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value'].to_list()
            self.assertTrue(set(out_v) == set(d[cat]))

        d = {0: pd.Series(a), 1: np.array(b), 2: c}
        r = pl0t._prep_data(a, b, c)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value'].to_list()
            self.assertTrue(set(out_v) == set(d[cat]))

        d = {0: a, 1: b, 2: c}
        r = pl0t._prep_data(d)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value'].to_list()
            in_v = d[cat]
            self.assertTrue(set(out_v) == set(in_v))

        d = {'xy': a, 'zz': b, 'dd': c}
        r = pl0t._prep_data(d, labels='asis')
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value'].to_list()
            in_v = d[cat]
            self.assertTrue(set(out_v) == set(in_v))

        l = ['c', 'd', 'e']
        d = {'c': a, 'd': b, 'e': c}
        r = pl0t._prep_data(d, labels=l)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value'].to_list()
            in_v = d[cat]
            self.assertTrue(set(out_v) == set(in_v))

        l = ['c', 'd', 'e']
        d = {'c': pd.Series(a), 'd': b, 'e': pd.Series(c)}
        r = pl0t._prep_data(d, labels=l)
        for cat in r['variable'].unique():
            out_v = r[r['variable'] == cat]['value'].to_list()
            in_v = d[cat]
            self.assertTrue(set(out_v) == set(in_v))
        
        
        # d = {'c': a, 'd': b, 'e': c}
        # r = pl0t._prep_data(pd.DataFrame(d), cat='c', labels='asis')
        # out_v = r[r['variable'] == 'c'].to_list()
        # in_v = d['c']
        # print(in_v, out_v)
        # self.assertTrue(set(out_v) == set(in_v))



            
    def test__prep_labels(self):
        # labels = None
        r = pl0t._prep_labels([1,2,3], [4, 5, 6], [7, 8, 9], found_nD_data=False,
                                                     data_cnt = 3,  labels=None)
        self.assertTrue([0, 1, 2] == r)

        r = pl0t._prep_labels(np.array([1,2,3]), np.array([4, 5, 6]), np.array([7, 8, 9]),
                              found_nD_data=False, data_cnt = 3,  labels=None)
        self.assertTrue([0, 1, 2] == r)

        d = {'a': [1, 2, 3],
             'b': [4, 5, 6],
             'c': [7, 8, 9]
        }
        r = pl0t._prep_labels(d, found_nD_data=True, data_cnt = len(d.keys()), labels=None)
        self.assertTrue([0, 1, 2] == r)

        df = pd.DataFrame(d)
        r = pl0t._prep_labels(df, found_nD_data=True, data_cnt = len(df['a'].unique()),
                              cat='a', labels=None)
        self.assertTrue([0, 1, 2] == r)

        # label = 'asis'

        self.assertRaises(SyntaxError, pl0t._prep_labels, [1,2,3], found_nD_data=False,
                          data_cnt=1, labels='asis')

        self.assertRaises(SyntaxError, pl0t._prep_labels, np.array([1,2,3]), found_nD_data=False,
                          data_cnt=1, labels='asis')

        r = pl0t._prep_labels(d, found_nD_data=True, data_cnt = len(d.keys()), labels='asis')
        self.assertTrue(['a', 'b', 'c'] == r)

        r = pl0t._prep_labels(df, found_nD_data=True, data_cnt = len(df['a'].unique()),
                              cat='a', labels='asis')
        self.assertTrue(['a', 'b', 'c'] == r)

        # labels == (...)
        self.assertRaises(SyntaxError, pl0t._prep_labels, [1, 2, 3], [4, 5, 6]
                          , np.array([7, 8, 9]), found_nD_data=False, data_cnt=3,
                          labels= ('a', 'b'))

        self.assertRaises(SyntaxError, pl0t._prep_labels, [1, 2, 3], pd.Series([4, 5, 6])
                          , np.array([7, 8, 9]), found_nD_data=False, data_cnt=3,
                          labels= ('a', 'b'))

        self.assertRaises(SyntaxError, pl0t._prep_labels, d, found_nD_data=True, data_cnt=1,
                          labels=('a', 'b'))

        self.assertRaises(SyntaxError, pl0t._prep_labels, pd.DataFrame(d), found_nD_data=True,
                          data_cnt=1, cat='a', labels= ('a', 'b'))
        
        
    def test_rot_axis_labs(self):
        g = pl0t.ind([1, 2, 3])
        self.assertRaises(SyntaxError, pl0t.rot_axis_labs, None, 40, 'z')
        self.assertRaises(SyntaxError, pl0t.rot_axis_labs, g, 40, 'z')
        self.assertRaises(SyntaxError, pl0t.rot_axis_labs, g, -40, 'x')
        self.assertRaises(SyntaxError, pl0t.rot_axis_labs, g, 200, 'x')
            
