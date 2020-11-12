#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

palette = 'deep'

def hist(*datas, labels=None, stat='count', palette=palette):
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
                  stat=stat, palette=palette)

    
def vline(x, color='r', **args):
    '''Plot a vertical line
    color: matplotlib color of vertical line
    *args: other axvline() params
    '''
    
    if color:
        plt.axvline(x, color=color, **args)
    else:
        plt.axvline(x, **args)

        
def shw():
    ''' To display current graph'''
    plt.show()

    
def cls():
    '''To close current graph'''
    plt.close()
