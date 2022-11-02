"""
This script makes a template BCAL CASA table from an existing BCAL table
"""

import os, sys
from tasks import *
from taskinit import *
import casa

import numpy as np

if __name__ == '__main__':
    if (len(sys.argv)) < 2:
        print("Usage: {} <table_name.B>".format(sys.argv[0]))
        sys.exit(0)

    btable = sys.argv[1]
    template_btable='BCAL_TEMPLATE.B'

    # get old table schema by reading input CAL table
    print("Creating BCAL table template {} from {}".format(template_btable, btable))
    tb.open(btable)
    tb.copy(template_btable, deep=True)
    tb.close()

    tb.open(template_btable, nomodify=False)
    fieldnames=tb.getkeywords()
    tb.putkeyword("MSName", "dummyname.ms")
    tb.flush()
    tb.close()

    # get list of subtables
    subtable_list = []
    for name, value in fieldnames.iteritems():
        if "table" in str(value).lower():
            subtable_list.append([name, value.split()[-1].strip()])

    # subtable stubs
    for name, path in subtable_list:
        if name == 'HISTORY':
            continue
        tb.open(template_btable+'/'+name, nomodify=False)
        nrows = tb.nrows()
        tb.removerows(rownrs=range(1,nrows))
        tb.close()

    # main table stub
    tb.open(template_btable, nomodify=False)
    nrows = tb.nrows()
    tb.removerows(rownrs=range(1,nrows))
    colnames = tb.colnames()
    for idx, col in enumerate(colnames):
        print(col)
        if tb.isscalarcol(col):
            values = tb.getcol(col)
            print('scalar col', values.shape, values, values.dtype)
            if len(values.shape) > 1:
                values = np.full(values.shape, 0, dtype=values.dtype)
        elif tb.isvarcol(col):
            values = tb.getvarcol(col)
            keys = values.keys()
            for key in keys:
                if not isinstance(values[key], np.ndarray):
                    continue  # ignore empty columns
                print('variable col', key, values[key].dtype, values[key].shape)
                values[key] = np.full(values[key].shape, 0, dtype=values[key].dtype)
                tb.putvarcol(columnname=col, value=values)
                tb.flush()
        tb.clearlocks()
    tb.close()

    # force to release all locks
    tb.open(template_btable, nomodify=False)
    tb.clearlocks()
    tb.close()

# -fin-
