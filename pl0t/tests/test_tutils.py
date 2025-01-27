#!/usr/bin/python3

from __future__ import annotations
from pl0t import *
from . import tutils
import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class test_tutils(unittest.TestCase):
        def test_cmpsum(self):
            ref_csum = tutils._chksum(__file__)
            self.assertTrue(tutils.cmp_csum(ref_csum, __file__))
            self.assertFalse(tutils.cmp_csum(ref_csum,
                                      os.path.join(os.getcwd(), 'pl0t',
                                                   'tests', '__init__.py')))

        def test_eval_im(self):
            fig, ax = plt.subplots()
            plt_data = [ i for i in range(10) ]
            scat(x = plt_data, y = plt_data)
            ref_im_id = 'tutils_eval_im'
            tutils.save(ref_im_id, dest_path = tutils.ref_im_path,
                 rand_str_prefix = False)
            self.assertTrue(tutils.eval_im(fig, ref_im_id))
            plt.close()

            fig, ax = plt.subplots()
            plt_data = [ 0 for i in range(10) ]
            scat(x = plt_data, y = plt_data)
            ref_im_id = 'tutils_eval_im'
            self.assertFalse(tutils.eval_im(fig, ref_im_id))
            plt.close()
