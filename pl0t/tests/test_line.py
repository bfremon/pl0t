#!/usr/bin/env python3

import numpy as np
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'pl0t'))
from pl0t import *

x1 = np.random.normal(10, 1, 10**5)

hist(x1)
title('Vertical yellow line at x = 15')
vline(15, color='y')
xtitle('blah blah')
save()
cls()

hist(x1)
title('Vertical dashed red line at x = 15')
xtitle('blah blah')
vline(15, color='r', ls='dashed')
xtitle('blah blah')
ytitle('blih blih')
save()
cls()

title('Horizontal line at y = 2')
hline(2)
save()
cls()
