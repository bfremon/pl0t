#!/usr/bin/env python3

import numpy as np
import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'pl0t'))
from pl0t import *

x1 = np.random.normal(10, 1, 10**5)

hist(x1)
vline(15, color='y')
save()
cls()

hist(x1)
vline(15, color='r', ls='dashed')
save()
cls()

hline(2)
save()
cls()
