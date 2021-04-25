#!/usr/bin/python3.7

import numpy as np
import scipy
import pandas as pd
import seaborn as sns
from pl0t import *
from . import tutils as tu

f_prefix = 'test_fill-in'

x = np.linspace(0, 1, 100)
ub = x + 0.05
lb = x - 0.05

lplt(x, x)
fill_in(x, lb, ub)
tu.save(f_prefix)

# cls()


