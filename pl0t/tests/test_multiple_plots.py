#!/usr/bin/python3

import random
import numpy as np
import pandas as pd
from . import tutils as tu
import pl0t

def rnd_title(l=50, min_word_len=2, max_word_len=8):
    ret = ''
    i = 0
    while i <= l:
        j = random.randint(min_word_len, max_word_len)
        i += j
        ret += tu.rnd_str(j) + ' '
    return ret

def gen_norm_series(series_nb, datas_nb=200,  x_min=-50,
                    x_max=50, y_min=-50, y_max=50):
    dat = []
    #datas.to_csv('/home/ben/multiple.csv', sep=';')
    for i in range(series_nb):
        title = rnd_title(20)
        for j in range(datas_nb):
            dat.append([title, random.uniform(x_min, x_max),
                    random.uniform(y_min, y_max)])
    ret = pd.DataFrame(dat)
    ret.columns = ('cat', 'x', 'y')
    return ret

def gen_sin_series(series_nb, datas_nb=200,  x_min=0,
                    x_max=2 * np.pi, max_shift=5.0, max_offset=5.0):
    dat = []
    for i in range(series_nb):
        title = rnd_title(20)
        x = np.linspace(x_min, x_max, datas_nb)
        mul = random.uniform(0, 1) * max_shift
        offset = random.uniform(0, 1) * max_offset
        y = np.sin(mul * x + offset)
        for i in range(datas_nb):
            dat.append([title, x[i], y[i]])
    ret = pd.DataFrame(dat)
    ret.columns = ('cat', 'x', 'y')
    return ret

f_prefix = 'test_multiple-'

def test__panel(graphs_nb=10):
    d = gen_norm_series(graphs_nb)
    pl0t.__panel('cat', d, yval='y', xval='x')
    tu.save(f_prefix + 'scat-' + str(graphs_nb))


#test__panel()
#test__panel(50)

def test_scat_panel(graphs_nb=10):
    d = gen_norm_series(graphs_nb)
    pl0t.scat_panel('cat', d, ylab='y', xlab='x')
    tu.save(f_prefix + 'scat_panel-' + str(graphs_nb))

test_scat_panel()

def test_scat_lplot(graphs_nb=10):
    d = gen_sin_series(graphs_nb)
    pl0t.lplot_panel('cat', d, ylab='y', xlab='x')
    tu.save(f_prefix + 'scat_lplot-' + str(graphs_nb))

test_scat_lplot()
