#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

f = open('list-utf.xls', 'r')
fo = open('list-conv.txt', 'w')

for line in f:
    line = line.decode('utf8')
    al = line.split('\t')
    # al contain quoted values, we need to dequote them
    bl = []
    btok = ''
    for tok in al:
        if tok[0:1] == '"':
            tok = tok[1:len(tok) - 1]
        tok = tok.replace('""', '"')
        tok = tok.replace('""', '"')
        bl.append(tok)

    for x in bl:
        fo.write(x.encode('utf8') + '\t')
    fo.write('\n')

f.close()
fo.close()
