#!/usr/bin/env python3

import numpy as np
import os
import sys
from pl0t import *
from . import tutils as tu
f_prefix = 'test_hist-'

x1 = np.random.normal(10, 1, 10**2)
x2 = np.random.normal(12, 2, 10**2)
x3 = np.random.normal(14, 4, 10**2)
x4 = np.random.normal(16, 6, 10**2)
#    hist(x1, x2, x3, x4)
hist(x1, x2, x3, x4, stat='probability')
title('Test title')
tu.save(f_prefix)
cls()
