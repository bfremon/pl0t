#!/usr/bin/env python3

import numpy as np
import scipy
import pandas as pd
import seaborn as sns
from pl0t import *
from . import tutils as tu

f_prefix = 'test_rot_ax_labs-'

mu = 20
std = 5
    
d = {'aazfa': (1, 2, 3),
     'afrebet': (4, 5, 6),
     'ergeebheheh': (7, 8, 9)
}

title('x labels rotated at 45°')
g = ind(d, labels='asis')
rot_axis_labs(g, 45)
tu.save(f_prefix)
#shw()
cls()
    
title('x labels rotated at -45°')
g = ind(d)
rot_axis_labs(g, 90 + 45)
tu.save(f_prefix)
#shw()
cls()


