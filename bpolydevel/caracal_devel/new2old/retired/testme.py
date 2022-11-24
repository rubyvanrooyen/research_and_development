from casacore.tables import table, tablecolumn
import numpy as np

def readcolumn(btable, bp_field=None):
    """
    Read column data from BPOLY cal table

    @param btable string   : CARACal table name (*.B? or *.P?)
    @param bp_field string : Name of BPOLY column to read

    @return values ncolrows  : Number rows in column
    @return values ncoldtype : Column array type 
    @return values Array     : BPOLY column values 
    """
    tb = table(btable, ack=False)
    with tablecolumn(tb, bp_field) as tbcol:
        ncolrows = tbcol.nrows()
        coldtype = tbcol.datatype()
        if tb.isscalarcol(bp_field):
            values = tb.getcol(bp_field)
        elif tb.isvarcol(bp_field):
            values = tb.getvarcol(bp_field)
        else:
            values = tb.getcol(bp_field)
    return ncolrows, coldtype, values

def makecolumndata(values, arrsize=[], dtype=np.ndarray, varcol=False):
    # create dummy array for CASA
    if dtype == 'boolean': dtype='bool'
    # create empty array
    if values is None:
        values = np.empty(arrsize, dtype=eval(dtype))
    # create dummy array
    if not isinstance(values, (np.ndarray, np.generic)):
        values = np.full(arrsize, values, dtype=eval(dtype))
    if varcol:
        # make ndarray to dict
        valuedict = {}
        for rowcnt, valueline in enumerate(values):
            valuedict[f"r{rowcnt+1}"] = np.expand_dims(np.array(valueline), axis=0)
        values = valuedict
#     print(values)
    return values



bpolytable="3C39_comet-1627186165_sdp_l0-1gc_primary.P1"
btable="BCAL_TEMPLATE.B0"
nrows = table(bpolytable, ack=False).nrows()
# table(btable, ack=False, readonly=False).addrows(nrows-1)
nchans = 4096 # comes from len freq

# list col types
colnames = ['TIME', 'FIELD_ID', 'SPECTRAL_WINDOW_ID', 'ANTENNA1', 'ANTENNA2', 'INTERVAL', 'SCAN_NUMBER', 'OBSERVATION_ID', 'CPARAM', 'PARAMERR', 'FLAG', 'SNR', 'WEIGHT']
for colname in colnames:
    mystr = f"{colname}: "
    [_, coltype, bvals] = readcolumn(btable, colname)
    try:
        [ncolrows, _, polyvals] = readcolumn(bpolytable, colname)
    except RuntimeError:
        pass
    if isinstance(bvals, (np.ndarray, np.generic)):
        mystr += f"scalarcol {bvals.shape} "
    if isinstance(bvals, dict):
        mystr += f"varcol [{ncolrows}, {bvals['r1'].shape}] "
    print(f"{mystr} {coltype}")

# scalar columns
print("\nScalar columns")
colname = 'SPECTRAL_WINDOW_ID'
print(colname)
[_, coltype, bvals] = readcolumn(btable, colname)
polyvals = makecolumndata(1, arrsize=bvals.shape, dtype=coltype)
# table(btable, ack=True, readonly=False).putcol(colname, polyvals)
colname = 'ANTENNA2'
print(colname)
[_, coltype, bvals] = readcolumn(btable, colname)
polyvals = makecolumndata(21, arrsize=bvals.shape, dtype=coltype)
# table(btable, ack=True, readonly=False).putcol(colname, polyvals)
colnames = ['TIME', 'FIELD_ID', 'ANTENNA1', 'INTERVAL', 'SCAN_NUMBER', 'OBSERVATION_ID']
for colname in colnames:
    print(colname)
    [_, coltype, bvals] = readcolumn(btable, colname)
    [ncolrows, _, polyvals] = readcolumn(bpolytable, colname)

# variable columns
print("\nVariable columns")
colname = 'FLAG'
print(colname)
[_, coltype, bvals] = readcolumn(btable, colname)
polyvals = makecolumndata(False,
                          arrsize=[nrows, nchans, 2],
                          dtype=coltype,
                          varcol=True)
# table(btable, ack=True, readonly=False).putvarcol(colname, polyvals)
colname = 'SNR'
print(colname)
[_, coltype, bvals] = readcolumn(btable, colname)
polyvals = makecolumndata(0.,
                          arrsize=[nrows, nchans, 2],
                          dtype=coltype,
                          varcol=True)
# table(btable, ack=True, readonly=False).putvarcol(colname, polyvals)
colname = 'PARAMERR'
print(colname)
[_, coltype, bvals] = readcolumn(btable, colname)
polyvals = makecolumndata(0.,
                          arrsize=[nrows, nchans, 2],
                          dtype=coltype,
                          varcol=True)
# table(btable, ack=True, readonly=False).putvarcol(colname, polyvals)
colname = 'WEIGHT'
print(colname)
[_, coltype, bvals] = readcolumn(btable, colname)
polyvals = makecolumndata(None,
                          arrsize=[nrows, nchans, 2],
                          dtype=coltype,
                          varcol=True)
# table(btable, ack=True, readonly=False).putvarcol(colname, polyvals)

# colnames = 'CPARAM'
# for key, val in bvals.items():
#     if isinstance(bvals[key], np.ndarray):
#         print(key, bvals[key].shape, polyvals[key].shape)
#     else:
#         print(key, bvals[key], polyvals[key].shape)
