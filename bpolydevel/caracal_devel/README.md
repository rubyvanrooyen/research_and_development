# Workflow for CARACal using BPOLY calibration option

Since BPOLY caltable structure is not yet available in mstransform, the whole MS has to be used during calibration so that applycal can be applied before target extraction

Workflow
```
# setup work directory structure
caracal -c run-g330-32k-bpoly.yml -ew obsconf

# copy full ms
cp -r ms-orig/1625501782_sdp_l0.ms/ msdir-bpoly/
chmod -R +w 1625501782_sdp_l0.ms

# calibrate using BPOLY
caracal -c run-g330-32k-bpoly.yml -sw prep__calibrators -ew crosscal

# extract and prep target and do line processing
caracal -c run-g330-32k-bpoly.yml -sw transform__target -ew flag__target

# extract continuum data for cont sub
caracal -c run-g330-32k-bpoly.yml -sw transform__cont_target -ew 

```


