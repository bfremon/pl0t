#!/usr/bin/env python3

import unittest
import pl0t
import pandas as pd
import numpy as np
import os

class test_pl0t(unittest.TestCase):

    g_path = os.path.join(os.getcwd(), 'test-save')

    def setUp(self):
        if not os.path.exists(self.g_path):
            os.mkdir(self.g_path)
        elif len(os.listdir(self.g_path)) != 0:
            self._del_dir(self.g_path)

            
    def _del_dir(self, path):
        for f in os.listdir(self.g_path):
            f_path = os.path.join(self.g_path, f)
            os.unlink(f_path)

    def test_prep_data(self):

        def _raise_err(ex, *args, **kwds):
            self.assertRaises(ex, pl0t._prep_data, *args, **kwds)
        
        def _raise_syn_err(*args, **kwds):
            _raise_err(SyntaxError, *args, **kwds)
            
        def _raise_type_err(*args, **kwds):
            _raise_err(TypeError, *args, **kwds)

        def _raise_val_err(*args, **kwds):
            _raise_err(ValueError, *args, **kwds)

        # no empty data allowed

        emptys = [ None, '', [], {}, pd.DataFrame({}),
                       pd.Series([], dtype = 'float'), np.array([]) ]
        for s in emptys:
            _raise_type_err(s)
        
        # list of lists

        l = [1, 2]
        h = [1]
        # None can be tolerated as valid input as it is converted to NaN
        not_scalars = [ '', 'a', [], {}, pd.DataFrame({}),
                       pd.Series([], dtype = 'float'), np.array([]) ]
        for s in not_scalars:
            h += [ s ]
            self.assertFalse(pl0t._is_list_of_scalars(h))
            _raise_syn_err(h)
            h = [ l ]
            h += [ None ]
            self.assertFalse(pl0t._is_list_of_scalars(h))
            _raise_syn_err(h)
            h += [ [None] ]
            self.assertFalse(pl0t._is_list_of_scalars(h))
            _raise_syn_err(h)

        lol = [ l, [1] ]
        _raise_syn_err(lol,  None, None)
        cat =  ['a', 'b', 'c']
        _raise_syn_err(lol, {'cat': cat })
        cat = ['a', 'a']
        kwds = {'cat': cat }
        assert len(cat) == len(lol)
        _raise_syn_err(lol, kwds)
        cat = ['a', 'b']
        res = pl0t._prep_data(lol, cat = cat)
        self.assertTrue(list(res['cat'].unique()) == cat)
        #        self.assertRaises(SyntaxError, pl0t._prep_data, (lol, None, None))

        # dict
        
        d = {'a':  [1, 'b'] }
        _raise_val_err(d)
        d  = {'a': [1, 2], 'b': [3] }
        res = pl0t._prep_data(d)
        self.assertTrue(sorted(list(res['cat'].unique())) == sorted(d.keys()))
        
        # long df
        labs = ['a', 'a', 'b', 'b', 'c' , 'c']
        vls = [ 1, 2, 3, 4, 5, 6]
        df = pd.DataFrame({'a': labs,
                          't': vls,
                          'h': [7, 8, 9, 10, 11, 12 ] })
        res = pl0t._prep_data(df, cat = 'a', val = 't')
        self.assertTrue(sorted(res['cat']) == labs)
        self.assertTrue(sorted(res['val']) == vls)

        # short df
        s1 = [ 1, 2, 3, 4 ]
        s2 = [ 4, 5, 6, 7 ]
        s3 = [ 7, 8, 9, 10 ]
        df = pd.DataFrame({'a': s1,
                           'b': s2,
                           'c': s3})
        res = pl0t._prep_data(df)
        self.assertTrue(sorted(res['cat'].unique()) == ['a', 'b', 'c'])
        self.assertTrue(sorted(res['val']) == sorted(s1 + s2 + s3))
                        
        # mixed data

        l1 = [ 1, 2, 3 ]
        l2 = [4, 5, 6 ]
        l3 = [6, 7, 8 ]
        d = {'a' : l1, 'b': l1 }
        df = pd.DataFrame(d)

        _raise_syn_err(l1, d)
        _raise_syn_err(l1, df)
        _raise_syn_err(df, d)        

        res = pl0t._prep_data(l1, l2, l3)
        #        self.assertTrue(sorted(res['cat'].unique()) == ['l1', 'l2', 'l3'] )
        self.assertTrue(sorted(res['val'])== l1 + l2 + l3)
        
        res = pl0t._prep_data(l1, l2, l3, cat = ['l1', 'l2', 'l3'])
        self.assertTrue(sorted(res['cat'].unique()) == ['l1', 'l2', 'l3'] )
        self.assertTrue(sorted(res['val'])== l1 + l2 + l3)

        # 1D vec
        x = np.random.normal(10, 5, 100)
        res = pl0t._prep_data(x)
        #self.assertTrue(sorted(res['cat']).unique() == 'x')
        self.assertTrue(sorted(res['val']) == sorted(x))

        x = [1, 2, 3]
        res = pl0t._prep_data(x)
        print(res)
        self.assertTrue(sorted(res['val']) == sorted(x))

    def tearDown(self):
        if os.listdir(self.g_path) != '':
            self._del_dir(self.g_path)
            
