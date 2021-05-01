#!/usr/bin/env python3

import numpy as np
import pandas as pd
import os
import sys
from pl0t import *
from . import tutils as tu
f_prefix = 'test_ind-'

x1 = np.random.normal(10, 1, 10**2)
x2 = np.random.normal(12, 2, 10**2)
x3 = np.random.normal(14, 4, 10**2)
x4 = np.random.normal(16, 6, 10**2)
#    hist(x1, x2, x3, x4)
ind(x1, x2, x3, x4)
title('Test title')
tu.save(f_prefix)
cls()

d = {'a': x1,
     'b': x2,
     'c': x3,
     'd': x4
     }
df = pd.DataFrame(d).melt()
df.columns = ('cat', 'val')
f_prefix += 'dataframe-'
ind(df, cat='cat', val='val')
tu.save(f_prefix)
cls()
