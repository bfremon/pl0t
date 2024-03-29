#!/usr/bin/env python3

import numpy as np
import os
import sys
from pl0t import *
from . import tutils as tu

f_prefix = 'test_scatter'

x1 = np.random.normal(10, 1, 10**5)
x2 = np.random.normal(12, 2, 10**5)
x3 = np.random.normal(14, 4, 10**5)
x4 = np.random.normal(16, 6, 10**5)
#    hist(x1, x2, x3, x4)
title('Scatter plot title')
scat(x=x1, y=x2)
tu.save(f_prefix)
cls()

r = scat(x=x2, y=x4)
r.set(xscale='log')
tu.save(f_prefix + 'ret_x_scale_log')
clr()
