#!/usr/bin/env python3

import numpy as np
import os
import sys
from pl0t import *
sys.path.append(os.getcwd())
from . import tutils as tu
normx = np.random.normal(10, 3, 10**2)

f_prefix = 'test_x-title-'
hist(normx)
xtitle('x title')
tu.save(f_prefix)
cls()

f_prefix = 'test_y-title-'
hist(normx)
ytitle('y title')
tu.save(f_prefix)
cls()

f_prefix = 'test_x-y-title-'
hist(normx)
xtitle('x title')
ytitle('y title')
tu.save(f_prefix)
cls()

f_prefix = 'test_all-titles-'
hist(normx)
set_titles('Main', 'x title', 'y title')
tu.save(f_prefix)
cls()

f_prefix = 'test_y-main-titles-'
hist(normx)
set_titles('Main', y_title='y title')
tu.save(f_prefix)
cls()

f_prefix = 'test_x-y-titles2-'
hist(normx)
set_titles(x_title='x title', y_title='y title')
tu.save(f_prefix)
cls()

