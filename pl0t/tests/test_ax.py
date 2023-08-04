#!/usr/bin/env python3

import unittest
import pl0t
import matplotlib.pyplot as plt
#from . import tutils as tu

x = [ i for i in range(10) ]
y = x

class test_ax(unittest.TestCase):
    def test_input(self):
        fig, ax = plt.subplots(nrows = 1, ncols = 2)

        def ___ix_raise_err(arg):
            self.assertRaises(SyntaxError, pl0t.scat, x, y , ix = arg)


        def __ix_valid_ret(arg, out):
            self.assertTrue(pl0t.scat(x, y, ix = arg) == out)
            
        ___ix_raise_err(ax[1])
        ___ix_raise_err('a')
        ___ix_raise_err((1, 2, 3))
        ___ix_raise_err(('a', 2))
        ___ix_raise_err(('a', 'b'))

        __ix_valid_ret(1, ax[1])
        __ix_valid_ret(0, ax[0])
        #        __ix_valid_ret('1', ax[1])
