#!/usr/bin/env python3.7

import os
import pl0t
import string
import random

def rnd_str(l=8):
    ret = ''
    for i in range(l):
        ret += random.choice(string.ascii_letters)
    return ret


def save(pfx, dest_path = None):
    if dest_path is None:
        # tmp dir is in ../../tmp
        dest_path = os.path.join(os.getcwd(), 'tmp')
        if not os.path.exists(dest_path):
            os.mkdir(dest_path)
    pl0t.save(fname = os.path.join(dest_path, pfx + rnd_str()))

    
def gen_norm_vec(mu, std, n_vals):
    ret = []
    for i in range(n_vals):
        ret += [ random.normalvariate(mu, std) ]
    return ret

                 
