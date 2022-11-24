Constructing a Bcal solution table from a BPOLY solution table

BPOLY solutions creates `*.P?` tables to distringuish them from Bcal solutions in CARACal

Use python venv running python3    
`source venv3.7/bin/activate`

Run from within CASA python environment

Plot bandpass solution from CARACAL bpoly table 3C39_comet-1627186165_sdp_l0-1gc_primary.P1  
`run plot_bpoly.py`

Create an empty B cal table from an existing `*.B` CASA table created by CARACal    
`run make_empty_bcal_table.py <input_table_name.B>`    
This will create the table `BCAL_TEMPLATE.B`

Construct a B cal table from a CARACal bpoly table    
`run casa_bpolytob.py <input_table_name.P> <input_template_name.B>`    

Running BPOLY to Bcal template in python    
`python3 bpolytob.py <table_name.P> <template_name.B>`

It will move the input table to a backup name and create a Bcal table with the same name as the input .P table
```
python3 bpolytob.py 3C39_comet-1627186165_sdp_l0-1gc_primary.P1 BCAL_TEMPLATE.B
```
Will move `3C39_comet-1627186165_sdp_l0-1gc_primary.P1` to `3C39_comet-1627186165_sdp_l0-1gc_primary_bpoly.P1`,
while creating `3C39_comet-1627186165_sdp_l0-1gc_primary.P1` from template `BCAL_TEMPLATE.B`

-fin-
