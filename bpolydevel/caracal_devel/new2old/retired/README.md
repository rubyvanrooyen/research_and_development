Failed attempt to constuct Bcal from scratch
This leads to v1tov2 error, rather use the templates

Constructing a Bcal solution table from a BPOLY solution table

Run from within CASA python environment

Extract table from template
btable="BCAL_TEMPLATE.B"
tb.open(btable, nomodify=False)
fill_array = np.full([2, 4096, 1], 0., dtype=float)
tb.putcol("WEIGHT", fill_array)
tb.flush()
tb.toasciifmt(asciifile='BCAL_TEMPLATE.dat', headerfile='BCAL_TEMPLATE.head', sep=";")
tb.close()

Run auto-script to extract schema to ascii and fix sizes
`run hack_bcal_dtype_header.py 

Construct a B cal table
`run create_bcal_table.py`


tb.open(btable)
tb.toasciifmt(asciifile='BCAL_TEMPLATE.dat', headerfile='BCAL_TEMPLATE.head', sep=';')
tb.close()
tb.fromascii(tablename="TEST_TEMP.B", asciifile="BCAL_TEMPLATE.dat", headerfile="BCAL_TEMPLATE.head", sep=';')


tb.open(btable)
tb.getcoldesc("CPARAM")
tb.getcoldminfo("CPARAM")
tb.close()


TIME;FIELD_ID;SPECTRAL_WINDOW_ID;ANTENNA1;ANTENNA2;INTERVAL;SCAN_NUMBER;OBSERVATION_ID;CPARAM;PARAMERR;FLAG;SNR;WEIGHT
D;I;I;I;I;D;I;I;X2,4096;R2,4096;B2,4096;R2,4096;R2,4096
tb.fromascii(tablename="TEST_TEMP.B", asciifile="BCAL_TEMPLATE.dat", headerfile="BCAL_TEMPLATE.head", sep=';')


CASA <25>: for col in colnames:
      ...:     print(col)
      ...:     if tb.isscalarcol(col): print(col, 'scalar col')
      ...:     elif tb.isvarcol(col): print(col, 'variable col')
      ...:     else: print(col, 'not known')

tb.getvarcol("CPARAM")
tb.putvarcol(columnname="CPARAM", value=bla)
{'r1': array([[[ 0.+0.j],
         [ 0.+0.j],
         [ 0.+0.j],
         ...,
         [ 0.+0.j],
         [ 0.+0.j],
         [ 0.+0.j]],

        [[ 0.+0.j],
         [ 0.+0.j],
         [ 0.+0.j],
         ...,
         [ 0.+0.j],
         [ 0.+0.j],
         [ 0.+0.j]]])}

