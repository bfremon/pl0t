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

dat = {'type': [], 'cat': [], 'val': [], 'hue_cat': []}

for i in range(plots_n):
    cat = tu.rnd_str(8)
    dat['type'].extend([ j for j in range(vals_n) ])
    dat['cat'].extend([ cat for j in range(vals_n) ])
    dat['val'].extend(vals[i])
    
hue_cat_labs = ['A', 'B', 'C', 'D', 'E']
hue_cat_len = int(plots_n * vals_n / len(hue_cat_labs))
for c in hue_cat_labs:
    dat['hue_cat'].extend([ c for i in range(hue_cat_len) ])

df = pd.DataFrame(dat)

title('Boxplot title')
bplt('cat', 'val', df)
tu.save(f_prefix)
#shw()
cls()

r = bplt('cat', 'val', df)
r.set(xscale='log')
tu.save(f_prefix + 'ret_x_scale_log')
clr()

r = bplt('cat', 'val', df, hue = 'hue_cat')
r.set(xscale='log')
tu.save(f_prefix + 'ret_x_scale_log-hue')
clr()

