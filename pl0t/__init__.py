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

def scatter(*datas, cat=None, labels=None, **args):
    '''Plot a scatter plot'''
    sns.scatterplot(*datas, **args)
        
def shw():
    ''' To display current graph'''
    plt.show()
    
def cls():
    '''To close current graph'''
    plt.close()

def title(t):
    plt.title(t)

def xtitle(t):
    plt.xlabel(t)
    
def ytitle(t):
    plt.ylabel(t)

def set_titles(main=None, x_title=None, y_title=None):
    if main:
        title(main)
    if xtitle:
        xtitle(x_title)
    if ytitle:
        ytitle(y_title)
    
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

def _no_dict_allowed():
    raise SyntaxError('Only 1D datatypes accepted (no dict)')
    
def _parse_datas(*datas, labels=None, cat=None):
    '''
    Verify that *datas is either a DataFrame or 
    a series of 1D vectors (np.array() or lists).
    Return formatted input for plotting 
    using identifiers given by labels or randomly specified
    '''
    ret = None
    if len(datas) == 1:
        if isinstance(datas[0], pd.DataFrame):
            if not cat:
                raise SyntaxError('cat key needed')
            if not cat in datas[0].columns:
                raise SyntaxError('cat key not in DataFrame columns')
        if _is_dict(datas[0]):
            _no_dict_allowed()    
        ret = datas[0]
    else:
        for k in datas:
            if isinstance(k, pd.DataFrame):
                raise SyntaxError('Only one DataFrame accepted')
            elif _is_dict(k):
                _no_dict_allowed()
        if labels:
            labs = labels
            if len(labels) != len(datas):
                raise SyntaxError('%i labels given, %i needed'
                                  % (len(labels), len(datas)))
        else:
            labs = [ i for i in range(1, len(datas) + 1) ]
        r = {}
        i = 0
        for k in datas:
            r[labs[i]] = list(k)
            i += 1
        ret = pd.DataFrame(r)
    return ret
