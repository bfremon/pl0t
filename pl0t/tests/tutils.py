#!/usr/bin/env python3

from __future__ import annotations
import os
import pl0t
import string
import random
import hashlib

def rnd_str(l: int =8) -> str:
    ret = ''
    for i in range(l):
        ret += random.choice(string.ascii_letters)
    return ret


def save(pfx: str, dest_path: str = None) -> None:
    if dest_path is None:
        # tmp dir is in ../../tmp
        dest_path = os.path.join(os.getcwd(), 'tmp')
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
    pl0t.save(fname = os.path.join(dest_path, pfx + rnd_str()))

    
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


if __name__ == '__main__':
    import unittest

    class test_tutils(unittest.TestCase):
        def test_cmpsum(self):
            ref_csum = _chksum(__file__)
            self.assertTrue(cmp_csum(ref_csum, __file__))
            self.assertFalse(cmp_csum(ref_csum,
                                      os.path.join(os.getcwd(), '__init__.py')))
    unittest.main()
