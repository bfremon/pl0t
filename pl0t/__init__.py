#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

palette = 'deep'

def hist(*datas, labels=None,  palette=palette):
    d = {}
    i = 0
    for v in datas:
        d[i] = v
        i += 1
    df = pd.DataFrame(d)
    if labels:
        df.columns = labels
    else:
        df.columns = [i for i in range(1, len(datas) + 1)]
    long_df = df.melt()
    sns.histplot(data=long_df, x='value', hue='variable',
                  palette=palette)

    
def vline(x):
    '''Plot a vertical line'''
    plt.axvline(x)

    
def shw():
    plt.show()

    
def cls():
    plt.close()

    
if __name__ == '__main__':
    import numpy as np
    x1 = np.random.normal(10, 1, 10**5)
    x2 = np.random.normal(12, 2, 10**5)
    x3 = np.random.normal(14, 4, 10**5)
    x4 = np.random.normal(16, 6, 10**5)
#    hist(x1, x2, x3, x4)
    hist(x1, x2, x3, x4)
    ps()
