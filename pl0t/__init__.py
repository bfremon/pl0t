#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import string
import random
import os
from Log import *

set_dbg_lvl(True)

palette = 'deep'

def hist(*data, labels=None, stat='count', palette=palette, **kwargs):
    dat = _prepare_data(*data, labels=labels)
    sns.histplot(data=dat, x='value', hue='variable',
                  stat=stat, palette=palette, **kwargs)

    
def ind(*data, labels=None, palette=palette, **kwargs):
    dat = _prepare_data(*data, labels=labels)
    ret = sns.catplot(data=dat, y='value', x='variable',
                palette=palette, jitter=True, **kwargs)
    return ret

    
def bplt(cat, val, *data, labels=None, **kwargs):
    dat = _prepare_data(*data, cat=cat, val=val, labels=labels)
    sns.boxplot(data=dat, y='variable', x='value')

    
def vline(x, color='r', **kwargs):
    '''Plot a vertical line going through x
    color: matplotlib color of line
    **kwargs: other axvline() params
    '''
    if color:
        plt.axvline(x, color=color, **kwargs)
    else:
        plt.axvline(x, **kwargs)

        
def hline(y, color='b', **kwargs):
    '''Plot an horizontal line going through y
    color: matplotlib color of line
    *args: other axvline() params
    '''
    if color:
        plt.axhline(y, color=color, **kwargs)
    else:
        plt.axhline(y, **kwargs)

        
def scat(x, y, **kwargs):
    '''
    Plot a scatter plot
    '''
    x_val = _prepare_data(x)
    y_val = _prepare_data(y)
    sns.scatterplot(x=x_val['value'], y=y_val['value'], **kwargs)

    
def lplt(*data, cat=None, labels=None, **kwargs):
    '''
    Plot a lineplot
    '''
    dat = _prepare_data(data, cat=cat, labels=labels)
    sns.scatterplot(*data, **kwargs)

    
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

    
def rot_axis_labs(graph, angle=30, ax='x'):
    if not graph:
        raise SyntaxError('Graph reference needed')
    if ax != 'x' and ax != 'y':
        raise SyntaxError('axis must be set either to x or y')
    if not 0 <= angle <= 180:
        raise SyntaxError('angle must be between 0 and 180°')
    if ax == 'x':
        graph.set_xticklabels(rotation=angle)
    else:
        graph.set_yticklabels(rotation=angle)

        
def rot_ylab(graph, angle=30):
    rot_axis_labs(graph=graph, angle=angle, ax='y')

    
def rot_xlab(graph, angle=30):
    rot_axis_labs(graph=graph, angle=angle, ax='x')

    
def fill_in():
    pass


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

    
def _prep_labels(*data, found_nD_data, data_cnt, cat=None, labels=None):
    ret = None
    if labels:
        if labels == "asis":
            if not found_nD_data:
                raise SyntaxError("labels=\'as is\' only allowed for dict or DataFrame")
            try:
                ret = list(data[0].keys())
            except KeyError:
                ret = data[0][cat].unique()
        else:
            if not found_nD_data:
                if len(labels) != len(data):
                    raise SyntaxError('As many labels needed as 1D vectors')
            elif _is_dict(data[0]):
                if len(labels) != len(data[0]):
                    raise SyntaxError('As many labels needed as dict keys')
            elif _is_df(data[0]):
                if len(labels) != len(data[0][cat].unique()):
                    raise SyntaxError('As many labels needed as categories')
            ret = labels
    else:
        ret = [i for i in range(data_cnt)]
    assert len(ret) != None
    return ret

    
def _prepare_data(*data, cat=None, val=None, labels=None):
    '''
    Sanitize input for plotting:
    *data: to be plotted - can be either:
    - 1D vectors (simple lists, 1D numpy arrays or pandas.Series)
    - a dict
    - a pandas.Dataframe with cat specifying the column holding the 
    sorting keys
    labels: can be either:
    - 'asis': cat or dict keys used for labels,
    -  list of strings
    - set to None: incremental ints as labels
    Return a long pandas.DataFrame for plotting
    '''
    ret = {}
    labs = None
    found_nD_data = False # bool set to True if dict or DataFrame found
    data_cnt = 0
    for v in data:
        data_cnt += 1

        # Only 1D or nD data allowed (not at the same time) 
        if _is_df(v) or _is_dict(v):
            if not found_nD_data:
                found_nD_data = True
        if data_cnt > 1 and found_nD_data:
            raise SyntaxError('1D and nD data mixing not allowed')

        # Only non null data allowed
        if _is_df(v):
            if v.empty: 
                raise SyntaxError('%s: no data to parse' % v)
        elif isinstance(v, np.ndarray):
            if len(v) == 0:
                raise SyntaxError('%s: no data to parse' % v)
        elif not v or str(v) == '' or v == {}:
                raise SyntaxError('%s: no data to parse' % v)

    # looking for cat / val param
    if found_nD_data:
        if _is_df(data[0]):
            if not cat:
                raise SyntaxError('categorical key needed for DataFrame')
            if not cat in data[0]:
                raise SyntaxError('%s column not found in Dataframe' % cat)
            if not val: 
                raise SyntaxError('value key needed for DataFrame')
            if not val in data[0]:
                raise SyntaxError('%s column not found in DataFrame')
            
    # labels parsing
    if found_nD_data:
        if _is_dict(data[0]):
            data_cnt = len(data[0].keys())
        else:
            data_cnt = len(data[0][cat].unique())
    labs = _prep_labels(*data, found_nD_data=found_nD_data,
                        data_cnt=data_cnt, cat=cat, labels=labels)

    # data aggregation    
    if found_nD_data:
        if _is_dict(data[0]):
            assert len(labs) == len(data[0].keys())
            i = 0
            for k in data[0]:
                ret[labs[i]] = data[0][k]
                i += 1
        else:
            assert len(labs) == len(data[0][cat].unique())
            # data[0][val] = data[0][val].astype('float64')
            # data[0][cat] = data[0][cat].astype('category')
            ret = data[0][[cat, val]]
            ret.columns = ('variable', 'value')
            return ret
    else:
        assert len(data) == len(labs)
        for i in range(len(data)):
            ret[labs[i]] = data[i]
            
    return pd.DataFrame(ret).melt()


def _is_dict(d):
    ret = True
    if not isinstance(d, dict):
        ret = False
    return ret


def _is_df(df):
    ret = True
    if not isinstance(df, pd.DataFrame):
        ret = False
    return ret
