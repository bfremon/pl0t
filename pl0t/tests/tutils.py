#!/usr/bin/env python3

from __future__ import annotations
import os
import sys
import pandas
import pl0t
import string
import random
import hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import unittest
import time
import shutil

tmp_path = os.path.join(os.getcwd(), 'pl0t', 'tests', 'tmp')
datum_path = os.path.join(os.getcwd(), 'pl0t', 'tests', 'datum')

def rnd_str(l: int = 8) -> str:
    ret = ''
    for i in range(l):
        ret += random.choice(string.ascii_letters)
    return ret


def gen_datum_labels(f_path: str, n_labs: int = 1000) -> None:
    ''' Generate n_labs random labels to
    be used as unmutable data for testing to be used for static testing'''
    out_buf = ''
    for i in range(n_labs):
        out_buf += rnd_str() + os.linesep
    with open(f_path, 'w+') as f_w:
        f_w.write(out_buf)

        
def gen_datum_data(f_path: str) -> None:
    plots_n = 20
    vals_n = 10**2
    mu = 20
    std = 5
    vals = [ gen_norm_vec(mu, std, vals_n)
                      for i in range(plots_n) ]
    hue_cat_labs = ['A', 'B', 'C', 'D', 'E']
    out = {'type': [], 'cat': [],
           'val': [], 'hue_cat': [] }
    for i in range(plots_n):
        cat = rnd_str(8)
        out['type'] += [ j for j in range(vals_n) ]
        out['cat'] += [ cat for j in range(vals_n) ]
        out['val'] += vals[i]
        hue_cat_len = int(plots_n * vals_n / len(hue_cat_labs))
    for c in hue_cat_labs:
        out['hue_cat'] += [ c for i in range(hue_cat_len) ]
    pandas.DataFrame(out).to_csv(f_path, sep = ';')

    
def read_datum_data(kind: str) -> Union[ pd.DataFrame]:
    ret = None
    if kind == 'df':
        ret = pandas.read_csv(os.path.join(datum_path, 'df.csv'), sep = ';')
    else:
        raise SyntaxError('Unknown datum type %s' % kind)
    return ret

    
def _gen_vals(self) -> dict:
    return ret 

            
def save(pfx: str, dest_path: str = None,
         rand_str_prefix: bool = True) -> None:
    if dest_path is None:
        # tmp dir is in ../../tmp
        dest_path = tmp_path
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
    if rand_str_prefix: 
        pl0t.save(fname = os.path.join(dest_path, pfx + rnd_str()))
    else:
        pl0t.save(fname = os.path.join(dest_path, '%s.png' % pfx),
                  ext = 'png')
        
    
def gen_norm_vec(mu: float, std: float, n_vals: int) -> list:
    ret = []
    for i in range(n_vals):
        ret += [ random.normalvariate(mu, std) ]
    return ret


def _chksum(f_path: str, chunk_size: int = 8192) -> str:
    ''' Return checksum of file pointed by f_path '''
    ret = hashlib.md5()
    with open(f_path, 'rb') as f_r:
        chunk = f_r.read(chunk_size)
        while chunk:
            ret.update(chunk)
            chunk = f_r.read(chunk_size)
    ret = ret.hexdigest()
    return ret


def cmp_csum(ref_csum: str, f_path: str,
             dbg: bool = False) -> bool:
    ret = True
    target_csum = _chksum(f_path)
    if dbg:
        print('target csum: %s' % target_csum)
        print('ref_csum: %s' % ref_csum)
    if not target_csum == ref_csum:
        ret = False
    return ret


def get_im_csum(im_id: str, tested_im_path: str,
                ref_path: str = datum_path,  
                allowed_exts: list = ['png'] ) -> str:
    ''' Populate ref_csums with files starting by prefix
    if im_csums doesn't exist in globals(). If im_id doesn't exist,
    ask user to copy tested_im_path in datum path
    and update cache'''
    ret = None
    if not 'im_csums' in globals():
        global im_csums
        im_csums = {}
        pfx = im_id.split('_')[0]
        for f in os.listdir(ref_path):
            f_path = os.path.join(ref_path, f)
            bs = os.path.basename(f_path)
            fname = bs.split('.')[:-1][0]
            ext = bs.split('.')[-1]
            if ext in allowed_exts and pfx in fname:
                im_csums[fname] = _chksum(f_path)
                #  print('-> %s: % s' % (fname, im_csums[fname]))
    try:
        ret = im_csums[im_id]
    except KeyError:
        print('%s im_key not present: create datum image? (y/n)' % im_id)
        answer = input()
        if answer in ['y', 'Y', 'yes']:
            del im_csums
            datum_im_path = os.path.join(datum_path, '%s.png' % im_id)
            shutil.copy(tested_im_path, datum_im_path)
            ret = get_im_csum(im_id, tested_im_path)
#    print(im_csums)
    return ret


def eval_im(fig: matplotlib.figure, im_id: str,
            tmp_dir: str = tmp_path, 
            dpi: int = 100, inline: bool =  False, profile: bool = False) -> bool:
    ''' Compare matplotlib fig to the datum image pointed by im_id.
    temp copy of fig is written into tmp_dir with dpi set to dpi
    '''
    ret = True
    status = 'OK'
    out_pfx = 'Comparing %s' % im_id
    f_path = os.path.join(tmp_dir, '%s.png' % im_id)
    out_path = os.path.join(tmp_dir, '%s.png' % im_id)
    #    fig.savefig(out_path, dpi = dpi)
    if profile:
        start_t = time.time()
    save(im_id, dest_path = tmp_dir, rand_str_prefix = False)
    if profile:
        end_t = time.time()
        print('%1.2fs' % (end_t - start_t))
    ref_csum = get_im_csum(im_id, out_path)
    if not cmp_csum(ref_csum, f_path, dbg = False):
        status = 'N' + status
        ret = False
    if inline:
        sys.stdout.write('%s: %s%s' % (out_pfx, status, os.linesep))
    return ret

