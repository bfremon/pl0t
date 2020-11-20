#!/usr/bin/env python3

import numpy as np
import os
import sys
from pl0t import *
sys.path.append(os.getcwd())
from . import tutils as tu

f_prefix = 'test_line-'
x1 = np.random.normal(10, 1, 10**5)

hist(x1)
title('Vertical yellow line at x = 15')
vline(15, color='y')
xtitle('blah blah')
tu.save(f_prefix)
cls()

hist(x1)
title('Vertical dashed red line at x = 15')
xtitle('blah blah')
vline(15, color='r', ls='dashed')
xtitle('blah blah')
ytitle('blih blih')
tu.save(f_prefix)
cls()

title('Horizontal line at y = 2')
hline(2)
tu.save(f_prefix)
cls()
