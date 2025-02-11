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
        self.data = tu.read_datum_data(kind = 'df')

        
    def test_bplt_std(self) -> None: 
        im_id = 'bplt_std'
        fig, ax = plt.subplots()
        title('Boxplot title')
        bplt('cat', 'val', self.data)        
        self.assertTrue(tu.eval_im(fig, im_id))
