#!/usr/bin/python3

from __future__ import annotations
import os
from pl0t import *
from . import tutils
import pandas as pd
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
            ref_im_id = 'tutils_eval_im'
            ref_im_path = os.path.join(tutils.datum_path,
                                   '%s.png' % ref_im_id)
            if os.path.exists(ref_im_path):
                    os.unlink(ref_im_path)

            fig, ax = plt.subplots()
            plt_data = [ i for i in range(10) ]
            scat(x = plt_data, y = plt_data)
            # Idempotent: fig is saved and compared to itself
            tutils.save(ref_im_id, dest_path = tutils.datum_path,
                 rand_str_prefix = False)
            self.assertTrue(tutils.eval_im(fig, ref_im_id, profile = False))
            plt.close()

           
            fig, ax = plt.subplots()
            # 0 not i in plt_data!
            plt_data = [ 0 for i in range(10) ]
            scat(x = plt_data, y = plt_data)
            ref_im_id = 'tutils_eval_im'
            # fig is compared to datum
            self.assertFalse(tutils.eval_im(fig, ref_im_id, profile = False))
            plt.close()
            
            fig, ax = plt.subplots()
            plt_data = [ 0 for i in range(100) ]
            scat(x = plt_data, y = plt_data)
            ref_im_id = 'tutils_eval_im'
            # fig is compared to datum
            self.assertFalse(tutils.eval_im(fig, ref_im_id, profile = False))
            plt.close()
            
            ref_im_id = 'tutils_eval_im_create'
            self.assertTrue(tutils.eval_im(fig, ref_im_id, profile = False))
            plt.close()
                

        def test_gen_datum_labels(self):
            out_path = os.path.join(tutils.tmp_path,
                                                'test_gen_rand_labels.txt')
            n_labels = 10
            tutils.gen_datum_labels(out_path, n_labels)
            line_cnt = 0
            with open(out_path, 'r') as f_r:
                for l in f_r.readlines():
                    self.assertTrue(len(l) == 9)
                    line_cnt += 1
            self.assertTrue(line_cnt == n_labels)


        def test_gen_datum_data(self):
            out_path = os.path.join(tutils.tmp_path,
                                    'test_datum_data.csv')
            tutils.gen_datum_data(out_path)
            out_data = pd.read_csv(out_path, sep = ';', index_col = [0])
            self.assertTrue(list(out_data.columns) == ['type', 'cat', 'val', 'hue_cat'])


        def test_read_datum_data(self):
                self.assertTrue(isinstance(tutils.read_datum_data('df'), pd.DataFrame))
                self.assertTrue(isinstance(tutils.read_datum_data('series'), pd.Series))
                self.assertRaises(SyntaxError, tutils.read_datum_data, 'prout')

                
        def tearDown(self):
            for f in os.listdir(tutils.tmp_path):
                os.unlink(os.path.join(tutils.tmp_path, f))
