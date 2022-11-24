

Create symbolic links to relevant caltables for evaluation:    
```
1627186165_sdp_l0-3c39-corr.ms -> ../../../../../data_processing/3c39/caracal_model/msdir-3c39-bpoly/1627186165_sdp_l0-3c39-corr.ms
1627186165_sdp_l0-cal.ms -> ../../../../../data_processing/3c39/caracal_model/msdir-3c39-bpoly/1627186165_sdp_l0-cal.ms
3C39_comet-1627186165_sdp_l0-1gc_primary.B1 -> ../../../../../data_processing/3c39/caracal_model/output-3c39-bpoly/caltables/3C39_comet-1627186165_sdp_l0-1gc_primary.B1
3C39_comet-1627186165_sdp_l0-1gc_primary.G1 -> ../../../../../data_processing/3c39/caracal_model/output-3c39-bpoly/caltables/3C39_comet-1627186165_sdp_l0-1gc_primary.G1/
3C39_comet-1627186165_sdp_l0-1gc_primary.K1 -> ../../../../../data_processing/3c39/caracal_model/output-3c39-bpoly/caltables/3C39_comet-1627186165_sdp_l0-1gc_primary.K1
3C39_comet-1627186165_sdp_l0-1gc_secondary.F0 -> ../../../../../data_processing/3c39/caracal_model/output-3c39-bpoly/caltables/3C39_comet-1627186165_sdp_l0-1gc_secondary.F0/
3C39_comet-1627186165_sdp_l0-1gc_secondary.K1 -> ../../../../../data_processing/3c39/caracal_model/output-3c39-bpoly/caltables/3C39_comet-1627186165_sdp_l0-1gc_secondary.K1/
```

Create Bcal from BPOLY and move here, and create appropriate link to BPOLY table
```
3C39_comet-1627186165_sdp_l0-1gc_primary.P1
3C39_comet-1627186165_sdp_l0-1gc_primary_bpoly.P1 -> ../../../../../data_processing/3c39/caracal_model/output-3c39-bpoly/caltables/3C39_comet-1627186165_sdp_l0-1gc_primary.P1
```

Basic tests of conversions from Jira[CAR-60](https://ruby-van-rooyen.atlassian.net/browse/CAR-60)
```
btable="3C39_comet-1627186165_sdp_l0-1gc_primary_bpoly.P1"
btable="3C39_comet-1627186165_sdp_l0-1gc_primary.P1"

browsetable(btable)
plotms(vis=btable, xaxis='freq', yaxis='amp', coloraxis='baseline')

msfile="1627186165_sdp_l0-cal.ms"
clearcal(msfile)
gtable="3C39_comet-1627186165_sdp_l0-1gc_primary.G1"
btable="3C39_comet-1627186165_sdp_l0-1gc_primary.P1"
ktable="3C39_comet-1627186165_sdp_l0-1gc_primary.K1"
applycal(vis=msfile, field='J0408-6545', gaintable=[gtable,btable,ktable], gainfield=['J0408-6545','J0408-6545','J0408-6545'], interp=['nearest', 'nearest', 'nearest'])
ftable="3C39_comet-1627186165_sdp_l0-1gc_secondary.F0"
btable="3C39_comet-1627186165_sdp_l0-1gc_primary.P1"
ktable="3C39_comet-1627186165_sdp_l0-1gc_secondary.K1"
applycal(vis=msfile, field='J0108+0134', gaintable=[ftable,btable,ktable], gainfield=['J0108+0134','J0408-6545','J0108+0134'], interp=['nearest', 'nearest', 'nearest'])
plotms(vis=msfile, xaxis='chan', yaxis='amp', correlation='XX,YY', ydatacolumn='corrected', avgtime='5200', averagedata=True, avgscan=True, avgbaseline=True, coloraxis='field')
plotms(vis=msfile, xaxis='chan', yaxis='phase', correlation='XX,YY', ydatacolumn='corrected', avgtime='5200', averagedata=True, avgscan=True, avgbaseline=True, coloraxis='field')

# Output show unexpected solutions, this needs to be corrected in the calculations, but the Bcal transformation seem to work




```


