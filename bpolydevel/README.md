Adding BPOLY bandpass calibration option to CARACal bandpass calibration
All information accumulated in [Issue#1419](https://github.com/caracal-pipeline/caracal/issues/1419)

# Installations
## Setup
```
python3.7 -m venv venv3.7
source venv3.7/bin/activate
pip install -U pip setuptools wheel
```

## Software
Install devel version of CARACal and Stimela
```
git clone git@github.com:rubyvanrooyen/caracal.git
cd caracal
pip install -e .

git clone git@github.com:rubyvanrooyen/Stimela.git
cd Stimela
pip install -e .
```

```
pip cache purge
deactivate
```


-fin-
