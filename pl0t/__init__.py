#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import string
import random
import os

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
    sns.boxplot(data=datas)
    
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

def save(fname=None, dest_dir=None, dpi=300, ext='.png'):
    filename = ''
    destdir = os.getcwd()
    if not fname:
        for i in range(15):
            filename += random.choice(string.ascii_letters)
    else:
        filename = fname
    if dest_dir:
        destdir = destdir
    plt.savefig(os.path.join(destdir, filename + ext), dpi=dpi)

def _is_dict(k):
    if isinstance(k, dict):
        return True
    return False
    
def _parse_datas(*datas, labels=None, cat=None):
    '''
    Verify that *datas is either a DataFrame or 
    a series of 1D vectors (np.array() or lists).
    Return formatted input for plotting
    '''
    ret = None
    if len(datas) == 1:
        if isinstance(datas[0], pd.DataFrame):
            if not cat:
                raise SyntaxError('cat key needed')
            if not cat in datas[0].columns:
                raise SyntaxError('cat key not in DataFrame columns')
        if _is_dict(datas[0]):
            raise SyntaxError('Only 1D datatypes accepted (no dict)')
        return datas[0]
    else:
        for k in datas:
            if isinstance(datas, pd.Dataframe):
                raise SyntaxError('Only one DataFrame accepted')
            elif _is_dict(k):
                raise SyntaxError('Only 1D datatypes accepted (no dict)')
