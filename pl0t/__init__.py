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
    '''
    Wrapper for seaborn histplot func:
    *data: 1D vectors to be plotted
    labels: alternate labels for each 1D vector
    stat: can be either count, frequency, density or probability
    palette: eponymous
    **kwargs: any complementary options passed to histplot
    '''
    # TODO: palette option ?
    dat = _prep_data(*data, labels=labels)
    sns.histplot(data=dat, x='value', hue='variable',
                  stat=stat, palette=palette, **kwargs)

    
def ind(*data, cat=None, val=None, labels=None, palette=palette, **kwargs):
    '''
    Wrapper for seaborn catplot func:
    *data: 1D vectors to be plotted
    labels: alternate labels for each 1D vector
    palette: eponymous
    **kwargs: any complementary options passed to catplot
    '''
    # TODO: ret ? 
    dat = _prep_data(*data, cat=cat, val=val, labels=labels)
    ret = sns.stripplot(data=dat, y='variable', x='value',
                palette=palette, jitter=True, **kwargs)
    return ret
    
def bplt(cat, val, *data, labels=None, **kwargs):
    '''
    Wrapper for seaborn boxplot func:
    cat: category column to be used
    val: value column
    *data: data dict or DataFrame 
    labels: alternate labels for each 1D vector
    **kwargs: any complementary options passed to catplot
    '''
    dat = _prep_data(*data, cat=cat, val=val, labels=labels)
    sns.boxplot(data=dat, y='variable', x='value', **kwargs)

def scat_panel(cat, *data, ylab, xlab, col_nb=3, labels=None, **kwargs):
    '''
    *data: data to be plotted
    cat: category column to be used
    ylab: y-axis variable column label
    xlab: x-axis variable column label (scatterplot)
    col_nb: number of columns (default to 3)
    labels: alternate labels for each 1D vector
    **kwargs: any complementary options passed to gtype func
    '''
    __panel(cat, *data, ylab=ylab, xlab=xlab, gtype='scat', col_nb=col_nb, labels=None, **kwargs)

def lplot_panel(cat, *data, ylab, xlab, col_nb=3, labels=None, **kwargs):
    '''
    *data: data to be plotted
    cat: category column to be used
    ylab: y-axis variable column label
    xlab: x-axis variable column label (scatterplot)
    col_nb: number of columns (default to 3)
    labels: alternate labels for each 1D vector
    **kwargs: any complementary options passed to gtype func
    '''
    __panel(cat, *data, ylab=ylab, xlab=xlab, gtype='lplot', col_nb=col_nb, labels=None, **kwargs)
    
def __panel(cat, *data, ylab, xlab=None, gtype='scat', col_nb=3, labels=None, **kwargs):
    '''
    Wrapper to plot graphs panels:
    gtype: graphe type (scatterplot or individual plot)
    cat: category column to be used
    *data: data to be plotted
    ylab: y-axis variable column label
    xlab: x-axis variable column label (scatterplot)
    col_nb: number of columns (default to 3)
    labels: alternate labels for each 1D vector
    **kwargs: any complementary options passed to gtype func
    '''
    allowed_graphs = ['scat', 'lplot']
    if not gtype in allowed_graphs:
        raise SyntaxError('%s: graph type not supported' % gtype)
    else:
        if gtype == 'scat':
            gfunc = sns.scatterplot
        elif gtype == 'lplot':
            gfunc = sns.lineplot
    #    dat = _prep_data(*data, cat=cat, labels=labels
    dat = data[0]
    if not ylab in dat.columns:
        raise SyntaxError('Invalid y axis label')
    if not cat in dat.columns:
        raise SyntaxError('Invalid categorical label')
    if len(dat[cat].unique()) < 2:
        raise SyntaxError('Not enough categories to create panel (>= 2 needed)')
    if col_nb > len(dat[cat].unique()):
        warn('Only one line will be plotted')
    g = sns.FacetGrid(dat, col=cat, col_wrap=col_nb)
    g.map_dataframe(gfunc, data=dat, x=xlab, y=ylab, palette=palette)
    
def vline(x, color='r', **kwargs):
    '''
    Plot a vertical line going through x
    color: matplotlib color of line (default: red)
    **kwargs: other axvline() params
    '''
    if 'ax' in kwargs:
        local_kwargs = kwargs.copy()
        del local_kwargs['ax']
        if color:
            kwargs['ax'].axvline(x, color=color, **local_kwargs)
        else:
            kwargs['ax'].axvline(x, **local_kwargs)
        return
    if color:
        plt.axvline(x, color=color, **kwargs)
    else:
        plt.axvline(x, **kwargs)

        
def hline(y, color='b', **kwargs):
    '''
    Plot an horizontal line going through y
    color: matplotlib color of line (default: blue)
    *kwargs: other axvline() params
    '''
    if 'ax' in kwargs:
        local_kwargs = kwargs.copy()
        del local_kwargs['ax']
        if color:
            kwargs['ax'].axhline(y, color=color, **local_kwargs)
        else:
            kwargs['ax'].axhline(y, **local_kwargs)
        return

    if color:
        plt.axhline(y, color=color, **kwargs)
    else:
        plt.axhline(y, **kwargs)

        
def scat(x, y, **kwargs):
    '''
    Plot a scatter plot
    x_val: 1D vector 
    y_val: 1D vector
    **kwargs: any complementary options of seaborn.scatterplot
    '''
    x_val = _prep_data(x)
    y_val = _prep_data(y)
    sns.scatterplot(x=x_val['value'], y=y_val['value'], **kwargs)

    
def lplt(x, y, **kwargs):
    '''
    Plot a line plot
    x_val: 1D vector 
    y_val: 1D vector
    **kwargs: any complementary options of seaborn.lineplot
    '''
    x_val = _prep_data(x)
    y_val = _prep_data(y)
    sns.lineplot(x=x_val['value'], y=y_val['value'], **kwargs)

    
def shw():
    ''' 
    To display current graph
    '''
    plt.show()

    
def cls():
    '''
    To close current graph
    '''
    plt.close()

    
def title(t):
    '''
    Set main graph title
    '''
    plt.title(t)

    
def xtitle(t):
    ''' 
    Set x axis title
    '''
    plt.xlabel(t)

    
def ytitle(t):
    ''' 
    Set y axis title
    '''
    plt.ylabel(t)

    
def rot_axis_labs(graph, angle=30, axis='x'):
    '''
    Rotate x or y axis labels by angle °
    graph: pointer to current graph
    angle: rotation angle between 0 and 180°
    ax: x or y axis
    '''
    if not graph:
        raise SyntaxError('Graph reference needed')
    if axis != 'x' and axis != 'y':
        raise SyntaxError('axis must be set either to x or y')
    if not 0 <= angle <= 180:
        raise SyntaxError('angle must be between 0 and 180°')
    if axis == 'x':
        labels = graph.get_xticklabels()
        graph.set_xticklabels(labels=labels, rotation=angle)
    else:
        labels = graph.get_yticklabels()
        graph.set_yticklabels(labels=labels, rotation=angle)

        
def rot_ylab(graph, angle=30):
    '''
    Rotate y axis labels of plot 'graph' by angle °
    '''
    rot_axis_labs(graph=graph, angle=angle, ax='y')

    
def rot_xlab(graph, angle=30):
    '''
    Rotate x axis labels of plot 'graph' by angle °
    '''
    rot_axis_labs(graph=graph, angle=angle, ax='x')

    
def fill_in(x, lbound, ubound, color='lightgreen', alpha=0.5, **kwargs):
    '''
    Fill y zone between lbound and ubound with color and alpha transparency
    '''
    plt.fill_between(x, lbound, ubound, color=color, alpha=0.5)

    
def set_titles(main=None, x_title=None, y_title=None):
    ''' 
    Set graphs titles with eponymous options
    '''
    if main:
        title(main)
    if xtitle:
        xtitle(x_title)
    if ytitle:
        ytitle(y_title)

        
def save(fname=None, dest_dir=None, dpi=1200, ext='.svg', transparent=True):
    ''' 
    Save current graph in ext format with fname name in dest_dir
    dpi: pixels per inch
    transparent: background set or not to transparent
    '''
    filename = ''
    destdir = os.getcwd()
    if not fname:
        for i in range(15):
            filename += random.choice(string.ascii_letters)
    else:
        filename = fname
    if dest_dir:
        destdir = destdir
    plt.tight_layout()
    if transparent:
        plt.savefig(os.path.join(destdir, filename + ext), dpi=dpi, transparent=True)
    else:
        plt.savefig(os.path.join(destdir, filename + ext), dpi=dpi, transparent=False)

        
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


def _prep_data(*data, cat=None, val=None, labels=None):
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
        elif isinstance(v, pd.Series):
            if v.empty:
                raise SyntaxError('%s: no data to parse' % v)
        elif v == None  or str(v) == '' or v == {} or v == [] :
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
