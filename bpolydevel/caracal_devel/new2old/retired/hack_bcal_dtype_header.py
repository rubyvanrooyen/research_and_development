"""
Script to extract table schema into ASCII files
"""

import os, sys

from tasks import *
from taskinit import *
import casa

import numpy as np

def get_schema(btable):
    print(btable)
    basename = os.path.splitext(btable)[0]
    asciifile=basename+'.dat'
    headerfile=basename+'.head'
    print(basename)
    tb.open(btable, nomodify=False)
    values = tb.getcol("CPARAM")
    fill_array = np.full(values.shape, 0., dtype=float)
    tb.putcol("WEIGHT", fill_array)
    tb.flush()
    tb.toasciifmt(asciifile=asciifile, headerfile=headerfile, sep=";")
    tb.close()
    return asciifile, headerfile


def var2scalar(headerfile):
    with open(headerfile, 'r') as fin:
        columns = fin.readline()
        dtypes = fin.readline()

    print(columns.strip())
    print(dtypes.strip())

    columns = columns.strip().split(';')
    dtypes = dtypes.strip().split(';')

    hacked_dtype = []
    for col, dtype in zip(columns, dtypes):
        tb.open(btable)
        values = tb.getcol(col)
        tb.close()
        if len(values.shape) > 1:
            [npol, nchan, nrow] = values.shape
            arr_size="{},{}".format(npol, nchan)
            hacked_dtype.append(dtype.replace("[]", arr_size))
        else:
            hacked_dtype.append(dtype)

    print(";".join(columns))
    print(";".join(hacked_dtype))

    with open(headerfile, 'w') as fout:
        fout.write(";".join(columns)+"\n")
        fout.write(";".join(hacked_dtype)+"\n")


if __name__ == '__main__':
    btable="BCAL_TEMPLATE.B"
    [asciifile, headerfile ] = get_schema(btable)
    print("Created ASCII schema file", headerfile, asciifile)
    make_scalar = False
    if make_scalar:
        var2scalar(headerfile)

# -fin-
