#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import seaborn
from pl0t import *

normx = np.random.normal(10, 3, 1000)

hist(normx)
xtitle('x title')
save()
cls()

hist(normx)
ytitle('y title')
save()
cls()

hist(normx)
xtitle('x title')
ytitle('y title')
save()
cls()

hist(normx)
set_titles('Main', 'x title', 'y title')
save()
cls()

hist(normx)
set_titles('Main', y_title='y title')
save()
cls()

hist(normx)
set_titles(y_title='y title')
save()
cls()

hist(normx)
set_titles(x_title='x title', y_title='y title')
save()
cls()

