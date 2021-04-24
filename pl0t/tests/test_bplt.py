#!/usr/bin/env python3

import numpy as np
import scipy
import pandas as pd
import seaborn as sns
from pl0t import *
from . import tutils as tu

f_prefix = 'test_bplt-'

b_dat = []
plots_n = 20
vals_n = 10**2
mu = 20
std = 5

vals = [ scipy.stats.norm.rvs(mu * np.random.random(),
                              std * np.random.random(),
                              vals_n) for i in range(plots_n) ]

dat = {'type': [], 'cat': [], 'val': []}

for i in range(plots_n):
    cat = tu.rnd_str(8)
    dat['type'].extend([ j for j in range(vals_n) ])
    dat['cat'].extend([ cat for j in range(vals_n) ])
    dat['val'].extend(vals[i])
df = pd.DataFrame(dat)

title('Boxplot title')
bplt('cat', 'val', df)
tu.save(f_prefix)
#shw()
cls()
