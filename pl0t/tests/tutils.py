#!/usr/bin/env python3

from __future__ import annotations
import os
import sys
import pl0t
import string
import random
import hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import unittest

tmp_im_path = os.path.join(os.getcwd(), 'tmp_im')
ref_im_path = os.path.join(os.getcwd(), 'ref_im')

def rnd_str(l: int = 8) -> str:
    ret = ''
    for i in range(l):
        ret += random.choice(string.ascii_letters)
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


def cmp_csum(ref_csum: str, f_path: str) -> bool:
    ret = True
    target_csum = _chksum(f_path)
    if not target_csum == ref_csum:
        ret = False
    return ret


def get_im_csum(im_id: str, ref_path: str = ref_im_path,  
                allowed_exts: list = ['png'] ) -> str:
    ''' Populate ref_csums with files starting by prefix
    if im_csums doesn't exist in globals() '''
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
                im_csums[im_id] = _chksum(f_path)
    try:
        ret = im_csums[im_id]
    except IndexError:
           raise IndexError('%s not in im_csums' % im_id)
    return ret


def eval_im(fig: matplotlib.figure, im_id: str,
            tmp_dir: str = tmp_im_path, 
            dpi: int = 100 ) -> bool:
    ret = True
    status = 'OK'
    out_pfx = 'Comparing %s' % im_id
    f_path = os.path.join(tmp_dir, '%s.png' % im_id)
    out_path = os.path.join(tmp_dir, '%s.png' % im_id)
    #    fig.savefig(out_path, dpi = dpi)
    save(im_id, dest_path = tmp_dir, rand_str_prefix = False)
    ref_csum = get_im_csum(im_id)
    if not cmp_csum(ref_csum, f_path):
        status = 'N' + status
        ret = False
    sys.stdout.write('%s: %s%s' % (out_pfx, status, os.linesep))
    return ret


if __name__ == '__main__':
    class test_tutils(unittest.TestCase):
        def test_cmpsum(self):
            ref_csum = _chksum(__file__)
            self.assertTrue(cmp_csum(ref_csum, __file__))
            self.assertFalse(cmp_csum(ref_csum,
                                      os.path.join(os.getcwd(), '__init__.py')))

        def test_eval_im(self):
            fig, ax = plt.subplots()
            plt_data = [ i for i in range(10) ]
            pl0t.scat(x = plt_data, y = plt_data)
            ref_im_id = 'tutils_eval_im'
            save(ref_im_id, dest_path = ref_im_path,
                 rand_str_prefix = False)
            self.assertTrue(eval_im(fig, ref_im_id))
            plt.close()

            fig, ax = plt.subplots()
            plt_data = [ 0 for i in range(10) ]
            pl0t.scat(x = plt_data, y = plt_data)
            ref_im_id = 'tutils_eval_im'
            self.assertFalse(eval_im(fig, ref_im_id))
            plt.close()

            
    unittest.main()

