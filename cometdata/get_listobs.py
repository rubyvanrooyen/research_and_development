from casatasks import listobs
import os, sys

msfile = sys.argv[1]
listfile = f'{os.path.splitext(msfile)[0]}.listobs'
listobs(vis=msfile, listfile=listfile)

# -fin-
