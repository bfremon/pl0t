#!/usr/bin/env python3

from __future__ import annotations
import unittest
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pl0t import *
from . import tutils as tu

class test_bplot(unittest.TestCase):
    def setUp(self) -> None:
        self.df_data = tu.read_datum_data(kind = 'df')
        self.ser_data = tu.read_datum_data(kind = 'series')
        self.listoflists_data = tu.read_datum_data(kind = 'listoflists')
        self.labels = tu.read_datum_data(kind = 'labels')
        
        
    def test_bplt_univariate(self) -> None:
        plt_data = self.df_data['val'].iloc[:10]
        im_id = 'bplt_univariate_list'
        fig, ax = plt.subplots()
        title('Univariate list, default label')
        bplt(list(plt_data))
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()

        
    def test_bplt_univariate_label(self) -> None:
        plt_data = self.df_data['val'].iloc[:10]
        im_id = 'bplt_univariate_list_label'
        fig, ax = plt.subplots()
        title('Univariate list with label lab')
        bplt(list(plt_data), cat = 'lab')
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()

        
    def test_bplt_univariate_Series(self) -> None:
        plt_data = self.ser_data
        im_id = 'bplt_univariate_series'
        fig, ax = plt.subplots()
        title('Univariate series - Series, default label')
        bplt(plt_data)
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()


    def test_bplt_univariate_Series_label(self) -> None:
        plt_data = self.ser_data
        im_id = 'bplt_univariate_series_label'
        fig, ax = plt.subplots()
        title('Univariate series - Series with label prat')
        bplt(plt_data, cat = 'prat')
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()

        
    def test_bplt_univariate_listoflists(self) -> None:
        plt_data = self.listoflists_data
        im_id = 'bplt_univariate_listofflist'
        fig, ax = plt.subplots()
        title('Univariate series - List of lists with default labels ?')
        bplt(plt_data)
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()


    def test_bplt_univariate_listoflists_label(self) -> None:
        plt_data = self.listoflists_data
        im_id = 'bplt_univariate_listofflist_label'
        fig, ax = plt.subplots()
        title('Univariate series - List of lists with label lab')
        self.assertRaises(SyntaxError, bplt, plt_data, cat = 'listoflists lab')
#        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()

        plt_data = self.listoflists_data
        im_id = 'bplt_univariate_listofflist_label'
        labs = [ self.labels[i] for i in range(len(plt_data)) ]
        fig, ax = plt.subplots()
        title('Univariate series - List of lists with true labels')
        bplt(plt_data, cat = labs)
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()
 
        
    def test_bplt_std(self) -> None: 
        im_id = 'bplt_std'
        plt_data = self.df_data
        fig, ax = plt.subplots()
        title('Standard dataframe')
        bplt(plt_data, cat = 'cat', val = 'val')        
        self.assertTrue(tu.eval_im(fig, im_id))
        plt.close()
