#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

palette = 'deep'

def hist(*datas, labels=None, stat='count', palette=palette, **args):
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

def bplt(*datas):
    sns.boxplot(*datas)
    
def vline(x, color='r', **args):
    '''Plot a vertical line going through x
    color: matplotlib color of line
    *args: other axvline() params
    '''
    if color:
        plt.axvline(x, color=color, **args)
    else:
        plt.axvline(x, **args)

def hline(y, color='b', **args):
    '''Plot an horizontal line going through y
    color: matplotlib color of line
    *args: other axvline() params
    '''
    if color:
        plt.axhline(y, color=color, **args)
    else:
        plt.axhline(y, **args)

def scatter(*datas):
    sns.scatterplot(*datas, **args)

        
def shw():
    ''' To display current graph'''
    plt.show()

    
def cls():
    '''To close current graph'''
    plt.close()
