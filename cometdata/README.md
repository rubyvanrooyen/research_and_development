Extracting comet data from SARAO database, some issues with comet as target.
This may be a versioning issue, so starting a fresh install

Create development enviroment and update pip tools for newest versions
```
python -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
```
Versions installed: `Successfully installed pip-23.0 setuptools-67.2.0 wheel-0.38.4`    
Python version: `Python 3.8.10`

Standard install and check that the script works
```
pip install python-casacore
pip install katdal
mvftoms.py -h
```
Versions installed: `Successfully installed python-casacore-3.5.2 katdal-0.20.1`

Clean up after yourself
```
pip cache purge
```

Extracting the data
```
mvftoms.py -a -f <katdaltoken> (this seem to be working)
mvftoms.py -a -f --flags cam <katdaltoken>
```

Check the data files
```
pip install casadata
pip install casatasks
pip cache purge
```

Silly script because I don't want to start casa
```
from casatasks import listobs
import os, sys

msfile = sys.argv[1]
listfile = f'{os.path.splitext(msfile)[0]}.listobs'
listobs(vis=msfile, listfile=listfile)
```

Put in a bash command and run through the files: `python get_listobs.py <msfile>`

-fin-
