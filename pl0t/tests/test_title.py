#!/usr/bin/env python3

import numpy as np
import os
import sys
from pl0t import *
sys.path.append(os.getcwd())
from . import tutils as tu
normx = np.random.normal(10, 3, 1000)
f_prefix = 'test_title-'

hist(normx)
xtitle('x title')
tu.save(f_prefix)
cls()

hist(normx)
ytitle('y title')
tu.save(f_prefix)
cls()

hist(normx)
xtitle('x title')
ytitle('y title')
tu.save(f_prefix)
cls()

hist(normx)
set_titles('Main', 'x title', 'y title')
tu.save(f_prefix)
cls()

hist(normx)
set_titles('Main', y_title='y title')
tu.save(f_prefix)
cls()

hist(normx)
set_titles(y_title='y title')
tu.save(f_prefix)
cls()

hist(normx)
set_titles(x_title='x title', y_title='y title')
tu.save(f_prefix)
cls()

