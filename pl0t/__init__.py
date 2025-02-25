#!/usr/bin/env python3

from __future__ import annotations
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import string
import random
import os

palette = 'deep'
out_dpi = 1200
boxplot_orientation = 'vertical'
default_cat_name = 'no cat_' # '_' prohibited

def hist(*data, stat='count', palette=palette, **kwargs):
    '''
    Wrapper for seaborn histplot func:
    *data: 1D vectors to be plotted
    stat: can be either count, frequency, density or probability
    palette: eponymous
    **kwargs: any complementary options passed to histplot
    '''
    # TODO: palette option ?
    dat = _prep_data(*data)
    ret = sns.histplot(data=dat, x='val', hue='cat',
                  stat=stat, palette=palette, **kwargs)
    return ret

    
def ind(*data, cat=None, val=None, palette=palette, **kwargs):
    '''
    Wrapper for seaborn catplot func:
    *data: 1D vectors to be plotted
    palette: eponymous
    **kwargs: any complementary options passed to catplot
    '''
    # TODO: ret ? 
    dat = _prep_data(*data, cat=cat, val=val)
    if not 'hue' in kwargs:
        ret = sns.stripplot(data=dat, y='cat', x='val',
                            jitter=True, **kwargs)
    else:
        ret = sns.stripplot(data=dat, y='cat', x='val',
                            palette=palette, jitter=True, **kwargs)
    return ret


def bplt(*data: list, cat:str = None, val:str = None, **kwargs) -> matplotlib.Axes:
    '''
    Wrapper for seaborn boxplot func:
    cat: category column to be used
    val: value column
    *data: data dict or DataFrame 
    **kwargs: any complementary options passed to catplot
    '''
    ret = None
    dat = _prep_data(*data, cat = cat, val = val)
    ret = sns.boxplot(data = dat, y = 'cat', x = 'val', **kwargs)
    return ret


def scat_panel(cat, *data, ylab, xlab, col_nb=3, **kwargs):
    '''
    *data: data to be plotted
    cat: category column to be used
    ylab: y-axis variable column label
    xlab: x-axis variable column label (scatterplot)
    col_nb: number of columns (default to 3)
    **kwargs: any complementary options passed to gtype func
    '''
    ret = __panel(cat, *data, ylab=ylab, xlab=xlab, gtype='scat', col_nb=col_nb,  **kwargs)
    return ret


def lplot_panel(cat, *data, ylab, xlab, col_nb=3, **kwargs):
    '''
    *data: data to be plotted
    cat: category column to be used
    ylab: y-axis variable column label
    xlab: x-axis variable column label (scatterplot)
    col_nb: number of columns (default to 3)
    **kwargs: any complementary options passed to gtype func
    '''
    ret = __panel(cat, *data, ylab=ylab, xlab=xlab, gtype='lplot', col_nb=col_nb,  **kwargs)
    return ret


def __panel(cat, *data, ylab, xlab=None, gtype='scat', col_nb=3, **kwargs):
    '''
    Wrapper to plot graphs panels:
    gtype: graphe type (scatterplot or individual plot)
    cat: category column to be used
    *data: data to be plotted
    ylab: y-axis variable column label
    xlab: x-axis variable column label (scatterplot)
    col_nb: number of columns (default to 3)
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
        print('WARN: only one line will be plotted')
    ret = sns.FacetGrid(dat, col=cat, col_wrap=col_nb)
    if not 'hue' in kwargs:
        ret.map_dataframe(gfunc, data=dat, x=xlab, y=ylab)
    else:
        ret.map_dataframe(gfunc, data=dat, x=xlab, y=ylab, palette = palette, hue = kwargs['hue'])
    return ret


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

        
def scat(x, y, ix = None, **kwargs):
    '''
    Plot a scatter plot
    x_val: 1D vector 
    y_val: 1D vector
    **kwargs: any complementary options of seaborn.scatterplot
    '''
    x_val = _prep_data(x)
    y_val = _prep_data(y)
    if ix is not None:
        ax  = get_ax_dim(ix, kwargs)
    ret = sns.scatterplot(x=x_val['val'], y=y_val['val'], **kwargs)
    return ret


def lplt(x, y, **kwargs):
    '''
    Plot a line plot
    x_val: 1D vector 
    y_val: 1D vector
    **kwargs: any complementary options of seaborn.lineplot
    '''
    x_val = _prep_data(x)
    y_val = _prep_data(y)
    ret = sns.lineplot(x=x_val['val'], y=y_val['val'], **kwargs)
    return ret


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

    
def clr():
    '''
    To clear matplotlib memory (to be confirmed)
    '''
    plt.close('all')
    plt.cla()
    plt.clf()

    
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

        
def xlim(start, end,  ax =  None):
    if ax is not None:
        ax[ax].set_xlim(start, end)
    else:
        set_xlim(start, end)

        
def ylim(start, end,  ax =  None):
    if ax is not None:
        ax[ax].set_xlim(start, end)
    else:
         set_xlim(start, end)

        
def _isint(ax, type_msg):
    ret = True
    try:
        int(ax)
    except TypeError:
        ret = False
        raise SyntaxError(type_msg)
    except ValueError:
        ret  = False
        raise SyntaxError(type_msg)

        
def get_ax_dim(ix, kwargs):
    ''' 
    get Axes (assumed to be named ax) indixes
    from ix passed by plotting functions
    ix must not be passed in kwargs from calling functions
    Can be only one positive, non integer or a 
    tuple of 2 non-null positives integers
    '''
    # NOT WORKING 
    if 'ax' in kwargs:
        raise SyntaxError('Only ax = ... or ix = ... allowed')
    for k in locals():
        print(k)
    # if not 'ax' in locals():
    #     raise SyntaxError('target Axes ax needed')
    ret = None
    input_err_msg = 'ix can be only a non-null integer or a  tuple of 2 non null integers'
    try:
        len(ix)
    except TypeError:
        _isint(ix, input_err_msg)
    else:        
        if len(ix) == 2:
            for tok in ix:
                _isint(tok, input_err_msg)
            ret = ax[ ix[0] ][ ix[1] ] 
        elif len(ix) > 2:
            raise SyntaxError(input_err_msg)
        elif len(ix) == 1:
            _isint(ix, input_err_msg)
            ret = ax[ix] 
        else:
            raise SyntaxError(input_err_msg)
#    print(ix, ret)
    return None
    #    return ret

        
def save(fname=None, dest_dir=None, dpi=out_dpi, ext='svg', transparent=False):
    ''' 
    Save current graph in ext format with fname name in dest_dir
    dpi: pixels per inch
    transparent: background set or not to transparent
    '''
    filename = ''
    dest_path = ''
    if not fname:
        for i in range(15):
            filename += random.choice(string.ascii_letters)
        filename += '.' + ext
    else:
        fname_toks = os.path.basename(fname).split('.')
        if len(fname_toks) == 1:
            if ext is None:
                # should never happen as ext = 'svg' by default
                raise SyntaxError('''No extension provided for filename 
                (% given) and no extension provided''' % (fname))
            else:
                filename = fname + '.' + ext
        else:
            fname_ext = fname_toks[-1]
            if ext and ext != fname_ext:
                raise SyntaxError('''Provided ext (%s) is different from
                filename extension (%s)''' % (ext, fname_ext))
            filename = fname
    if dest_dir is None:
        dest_path = os.path.join(os.getcwd(), filename)
    else:
        dest_path = os.path.join(dest_dir, filename)
    plt.tight_layout()
    if transparent:
        plt.savefig(dest_path, dpi=dpi, transparent=True)
    else:
        plt.savefig(dest_path, dpi=dpi, transparent=False)     

def _val_arg_ignored(data_type):
    pass


def _is_list_of_scalars(lst):
    ''' 
    Return True if lst is a list of lists composed only of 
    scalars
    '''
    ret = True
    for l in lst:
        if l is None:
            ret = False
            break
        try:
            pd.Series(l, dtype = 'float')
        except ValueError:
            ret = False
            break
    return ret


def _get_var_name(var: str, dbg: bool = False) -> str:
    '''
    Return litteral name of var from globals when cat is not specified
    '''
    ret = None
    globals_dict = globals()
    for k in globals_dict:
        if var is globals_dict[k]:
            ret = str(k)
            break
    if dbg:
        print('%sDBG: _get_var_name() - key %s, value %s'
              % (os.linesep, k, globals_dict[k]))
    return ret


def _is_1D_vec(vec):
    ret = True
    try:
        pd.Series(vec, dtype = 'float')
    except TypeError:
        ret = False
    except ValueError:
        ret  = False
    return ret


def _set_no_cat_arg(dat): 
    ''' Set series_name when cat arg is None'''
    if default_cat_name:
        ret = default_cat_name
    else:
        ret = _get_var_name(dat)
    print('WARN: using %s as default cat' % ret)
    return ret


def _prep_data(*data, cat:str = None, val:str = None, dbg: bool = True) -> pd.DataFrame:
    '''*data must hold only 1D scalars arrays'''
    dat_idx = 0
    only_1D_scalars_msg = 'Only multiple 1D args are allowed'
    ret = {}
    if len(data) > 1:
        max_len = 0
        for dat in data:
            if  not _is_1D_vec(dat) or _is_dict(dat) or _is_df(dat):
                raise SyntaxError(only_1D_scalars_msg)
            if len(dat) > max_len:
                max_len = len(dat)
        if cat:
            if len(cat) != len(data):
                raise SyntaxError('Same lenght required for 1D data and cat')
        cat_idx = 0
        concat_data  = {}
        for dat in data:
            if cat is None:
                series_name = _set_no_cat_arg(dat)
            else:
                series_name = cat[cat_idx]
            if dbg:
                print('DBG: _prep_data(): series_name %s (cat_idx %i)'
                      % (series_name, cat_idx))
            if len(dat) < max_len:
                pad_len = max_len - len(dat)
                padded_dat = dat  + [ np.nan for i in range(pad_len) ]
            else:
                padded_dat = dat
            if not series_name in concat_data:
                concat_data[series_name] = padded_dat
            else:
                concat_data[series_name + str(cat_idx)] = padded_dat
            cat_idx += 1
        ret = __prep_data(concat_data, cat = cat, val = val)
    else:
        ret  = __prep_data(data[0], cat = cat, val = val)
    if dbg:
        print('DBG: _prep_data() ret:%s%s' % (os.linesep, ret))
    return ret 


def __prep_data(data:Union[ ...], cat: str = None, val:str = None, dbg:bool = True) -> pd.DataFrame:
    '''
    Format data __singleton__ for plotting using for input such as:
    - A dictionnary of lists (padded with Nan if necessary) with keys as categories (val & cat args  ignored
    with warning), Each list must composed of scalars.
    - A pandas dataframe in short form, using columns names as categories and column content 
    for plotting (val ignored with warning), 
    - A pandas dataframe in pseudo-long form using column name as categories and val as variable
    data,
    - A list of of lists (padded with NaN if necessary) with columns provided by the cat arg as 
    categories (val ignored with warning). 
    Return a long form DataFrame (val column for variable data, cat column for cat,
    and possibly with other columns for hue plotting)
    '''
    # lol axis = 0 or axis = 1 / prep_data public ou privé, val comme indicaeur ??
    ret = {}
    empty_msg = 'Empty data or scalar'
    cat_missing_msg = 'Category column needed (cat != None)'
    val_missing_msg = 'Variable column needed (val != None)'
    try:
        len(data)
    except TypeError:
        raise TypeError(empty_msg)
    if len(data) < 1 or data is None:
        raise TypeError(empty_msg)
    if _is_dict(data):
        if cat is not None or val is not None:
            print('WARN: cat and args values ignored for dict')
        ret = _prep_dict(data, cat = cat, val = val)
    elif _is_df(data):
        if cat is not None and val is not None:
            ret = _prep_long_df(data, cat = cat, val = val)
        elif cat is None and val is None:
            ret = _prep_short_df(data, cat = cat, val = val)
    elif _is_1D_vec(data):
        if cat is None:
            series_name = _set_no_cat_arg(data)
        else:
            series_name = cat
        if dbg:
            print('DBG: __prep_data(): 1D vec series_name %s' % series_name)
        ret = pd.Series(data, dtype = 'float', name = series_name)
        ret = pd.DataFrame(ret).melt()
        ret.rename(columns = {'value': 'val', 'variable': 'cat'},
                   inplace = True)
    else:
        # list of lists
        if not _is_list_of_scalars(data):
            raise SyntaxError('data should be only composed of scalar lists')
        if (cat is not None) and (len(data) != len(cat)):
            raise SyntaxError('cat must have an equal lengh to data for list of lists')
        if val is not None:
            print('WARN: val is not used for list of lists')
        ret  = _prep_listoflists(data, cat = cat, val = val)
    return ret


def _prep_dict(data, cat, val):
    max_len = 0
    ret = {}
    for k in data:
        try:
            pd.Series(data[k], dtype = 'float')
        except ValueError:
            raise ValueError('Only scalar lists allowed for dict as data')
        if len(data[k]) > max_len:
            max_len = len(data[k])
    for k in data:
        if len(data[k]) < max_len:
            pad_len = max_len - len(data[k])
            padded_list = data[k] + [ np.nan for i in range(pad_len) ]
            ret[k] = padded_list
        else:
            ret[k] = data[k]
    ret = pd.DataFrame(ret).melt()
    ret.rename(columns = {'variable': 'cat', 'value': 'val'},
            inplace = True)
    return ret

    
def _prep_long_df(data, cat, val):
    ret = data.copy()
    ret = ret[ [cat, val] ]
    ret.rename(columns = { cat: 'cat', val: 'val'},
               inplace = True)
    return ret


def _prep_short_df(data, cat, val):
    ret = data.copy()
    ret = ret.melt()
    ret.rename(columns = { 'variable': 'cat', 'value': 'val'},
               inplace = True)
    return ret    


def _prep_listoflists(data, cat, val):
    ret = {}
    if cat is None:
        print('WARN: no cat provided, using monotonic labels instead')
        cat = [str(i) for i in range(len(data)) ]
    print('WARN: list of lists: cat data used to label lists with no guaranteed order')
    max_len = 0
    for l in data:
        try:
            len(l)
        except TypeError:
            # l can be a scalar
            l = [ l ]
        if len(l) > max_len:
            max_len = len(l)
    for i in range(len(data)):
        cur_cat = cat[i]                   
        if cur_cat in ret:
            raise ValueError('duplicate %s category' % cur_cat)
        if len(data[i]) < max_len:
            pad_len = max_len - len(data[i])
            padded_list = data[i] + [ np.nan for n in range(pad_len) ]
            ret[cur_cat]  = padded_list
        else:
            ret[cur_cat] = data[i]
    ret = pd.DataFrame(ret).melt()
    ret.rename(columns = {'variable': 'cat', 'value': 'val'},
               inplace = True)
    return ret

        
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

