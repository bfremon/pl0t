#!/usr/bin/env python3

import numpy as np
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'pl0t'))
from pl0t import *

x1 = np.random.normal(10, 1, 10**5)
x2 = np.random.normal(12, 2, 10**5)
x3 = np.random.normal(14, 4, 10**5)
x4 = np.random.normal(16, 6, 10**5)
#    hist(x1, x2, x3, x4)
hist(x1, x2, x3, x4, stat='probability')
title('Test title')
save()
cls()
