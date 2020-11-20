#!/usr/bin/env python3.7

import pl0t
import string
import random

def _rnd_str(l=15):
    ret = ''
    for i in range(l):
        ret += random.choice(string.ascii_letters)
    return ret

def save(pfx):
    pl0t.save(fname = pfx + _rnd_str())
