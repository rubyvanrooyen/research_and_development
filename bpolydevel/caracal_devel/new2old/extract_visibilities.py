from numpy import recarray
import numpy as np
import pyrap.tables as pt

import os


### Get visibilities per antenna (XX, YY) for auto correlation
ms_filename="1627186165_sdp_l0-cal.ms"
# Data: Complex value for each of 4 correlations per spectral channel
# IDs correspond to values RR (5), RL (6), LR (7), LL (8), XX (9), XY (10), YX (11), and YY (12)
corr_prods_id = {5: 'RR', 6: 'RL', 7: 'LR', 8: 'LL',
                 9: 'XX', 10: 'XY', 11: 'YX', 12: 'YY'}
with pt.table(ms_filename+'/POLARIZATION') as tb:
    corr_prods = tb.getcol("CORR_TYPE")[0]
    # associate corr prod with 4 tuple indices
    lin_prods = np.array([corr_prods_id[prod] for prod in corr_prods])
    Xidx = np.nonzero(lin_prods == 'XX')[0][0]  # H pol
    Yidx = np.nonzero(lin_prods == 'YY')[0][0]  # V pol
print('Correlation products {}'.format(corr_prods))
for prod in corr_prods:
    print('  {:2} : {}'.format(prod, corr_prods_id[prod]))
# H = XX
print('H pol {} indices in corr products'.format(Xidx))
# V = YY
print('V pol {} indices in corr products'.format(Yidx))

with pt.table(ms_filename+'/SPECTRAL_WINDOW') as tb:
    data = tb.getvarcol("NUM_CHAN")
    for spw in data.keys():
        n_chans = data[spw][0]
print('Number channels: {}'.format(n_chans))

with pt.table(ms_filename+'/ANTENNA') as tb:
    antennas = tb.getcol("NAME")
antennas = np.array(antennas)
n_ants = len(antennas)
print('Antennas: {}'.format(antennas))
print('Number antennas: {}'.format(n_ants))

# find unique timestamps indices
with pt.table(ms_filename) as tb:
    # extract baselines
    time = tb.getcol("TIME_CENTROID")

    bl_ant1_idx = tb.getcol("ANTENNA1")
    bl_ant2_idx = tb.getcol("ANTENNA2")

len_ = len(time)
uniquetime = list(set(time))
time = np.array(time)
uniquetime = np.sort(uniquetime)
bl_ant1 = antennas[np.array(bl_ant1_idx)]
bl_ant2 = antennas[np.array(bl_ant2_idx)]
baselines = list(set(np.char.add(bl_ant1, bl_ant2)))
n_bl = len(baselines)
print('Baseline indices: {}'.format(bl_ant1_idx))
print('Baseline indices: {}'.format(bl_ant2_idx))
print('Baseline antennas: {}'.format(bl_ant1))
print('Baseline antennas: {}'.format(bl_ant2))
print('{} timestamps with {} unique'.format(
    len(time), len(uniquetime)))
print('Number dumps: {}'.format(len(uniquetime)))
print('Number baselines: {}'.format(n_bl))


# per timestamps sum over auto and cross correlation baselines
n_ts = uniquetime.size
ts0 = np.min(time)
ant_bl_dict = {}
flagged_mask = np.ones([n_chans], dtype=bool)
# with pt.table(ms_filename) as tb:
# 
#     print('Reading flags from cross correlations')
#     for cnt, ts in enumerate(np.sort(time)):
#         ant1 = antennas[bl_ant1_idx][cnt]
#         ant2 = antennas[bl_ant2_idx][cnt]
# 
#         flag = tb.getcol("FLAG",
#                          startrow=cnt,
#                          nrow=1).squeeze()
# 
#         # ignore flags from lines that are mostly flagged out
#         if flag.sum()/flag.size < 0.8:
#             print(cnt, ant1, ant2, flag.size, np.sum(flag), flag.sum()/flag.size)
#             [nchans, npols] = flag.shape
#             flagged_region = np.array(flag.sum(axis=1)/npols, dtype=bool)
#             print('flag', flagged_mask.sum())
#             flagged_mask = np.logical_and(flagged_mask, flagged_region)
#             print('flag', flagged_mask.sum())
# 
# print(flagged_mask.shape, flagged_mask.sum())

#     for cnt, bl in enumerate(np.sort(baselines)):
#         ant1 = bl[:4]
#         ant2 = bl[4:]
# 
#         if ant1 == ant2:
#             # ant<x>h ant<x>h and ant<x>v ant<x>v
#             print('Reading power from autocorrelations')
#             Xamp = []
#             Yamp = []
#             # timestamps with ant1 in baselines
#             bl1_mask = (bl_ant1==ant1)
#             # timestamps with ant2 in baselines
#             bl2_mask = (bl_ant2==ant2)
#             print(cnt, ant1, ant2, '{}-{}'.format(
#                   np.unique(bl_ant1[bl1_mask])[0],
#                   np.unique(bl_ant2[bl2_mask])[0]))
#             # find timestamps for baseline
#             bl_mask = np.logical_and(bl1_mask, bl2_mask)
#             bl_ts_idx = np.nonzero(bl_mask)[0]
# 
#             for bl_ts in bl_ts_idx:
#                 idx = np.nonzero(uniquetime==time[bl_ts])[0][0]
#                 data = tb.getcol("DATA",
#                                  startrow=bl_ts,
#                                  nrow=1).squeeze()
#                 Xamp.append(np.abs(data[:,Xidx]))
#                 Yamp.append(np.abs(data[:,Yidx]))
#             # average over all timestamps to get passband spectrum
#             ant_bl_dict[ant1] = {
#                                  'Xamp': np.array(Xamp).mean(axis=0),
#                                  'Yamp': np.array(Yamp).mean(axis=0),
#                                  }
#         else:
#             print('Reading flags from cross correlations')
#             # timestamps with ant1 in baselines
#             bl1_mask = (bl_ant1==ant1)
#             # timestamps with ant2 in baselines
#             bl2_mask = (bl_ant2==ant2)
#             print(cnt, ant1, ant2, '{}-{}'.format(
#                   np.unique(bl_ant1[bl1_mask])[0],
#                   np.unique(bl_ant2[bl2_mask])[0]))
#             # find timestamps for baseline
#             bl_mask = np.logical_and(bl1_mask, bl2_mask)
#             bl_ts_idx = np.nonzero(bl_mask)[0]
#             for bl_ts in bl_ts_idx:
#                 flag = tb.getcol("FLAG",
#                                  startrow=bl_ts,
#                                  nrow=1).squeeze()
# #                 print(cnt, flag.size, np.sum(flag), flag.sum()/flag.size)
# #                 data = tb.getcol("DATA",
# #                                  startrow=bl_ts,
# #                                  nrow=1).squeeze()
# #                 print('shapes', data[:,Xidx].shape, flag[:,Xidx].shape, np.shape(range(n_chans)))
#                 # ignore flags from lines that are mostly flagged out
#                 if flag.sum()/flag.size < 0.8:
#                     print('flags', flag[:,0].sum(), flag[:,1].sum(), flag[:,2].sum(), flag[:,3].sum())
#                     [nchans, npols] = flag.shape
#                     flagged_region = np.array(flag.sum(axis=1)/npols, dtype=bool)
#                     print('flag', flagged_mask.sum())
#                     flagged_mask = np.logical_and(flagged_mask, flagged_region)
#                     print('flag', flagged_mask.sum())
# #                     unflagged_region = np.invert(np.array(flag.sum(axis=1)/npols, dtype=bool))
# #                     print(unflagged_region.shape)
# #                     import matplotlib.pylab as plt
# #                     plt.figure()
# #                     plt.plot(range(nchans), np.abs(data[:,Xidx]))
# #                     plt.plot(np.arange(nchans)[unflagged_region], np.abs(data[:,Xidx])[unflagged_region])
# #                     plt.savefig("mygraph.png")
#                     break
#             break

flags = pt.table(ms_filename).getcol("FLAG")
[nrows, nchans, npols] = flags.shape
flags=flags.sum(axis=0)/nrows
flags = flags.sum(axis=1)/npols
flag_mask = flags > 0.5
import matplotlib.pylab as plt
plt.figure()
plt.plot(range(nchans), flag_mask)
plt.savefig("mygraph.png")

# with pt.table("1627186165_sdp_l0-cal.ms/SPECTRAL_WINDOW") as tb:
#     freq_range = tb.getcol("CHAN_FREQ").squeeze()
#     print(freq_range.shape)
# 
# 
# import matplotlib.pylab as plt
# plt.figure()
# plt.subplot(211)
# plt.plot(ampxx, 'r,', label='xx')
# # plt.plot(ampxy, 'b,', label='xy')
# # plt.plot(ampyx, 'g,', label='yx')
# plt.plot(ampyy, 'k,', label='yy')
# plt.legend()
# plt.subplot(212)
# plt.plot(phasexx, 'r,', label='xx')
# # plt.plot(phasexy, 'b,', label='xy')
# # plt.plot(phaseyx, 'g,', label='yx')
# plt.plot(phaseyy, 'k,', label='yy')
# plt.legend()
# plt.savefig("mygraph.png")
# 
# write to CSV file
filename = os.path.splitext("1627186165_sdp_l0-cal.ms")[0]+'.csv'
print(filename)
# with open(filename, 'w') as fout:
Xamplitudes = []
Yamplitudes = []
for key, value in ant_bl_dict.items():
    print(key, value['Xamp'].shape, value['Yamp'].shape)
    Xamplitudes.append(value['Xamp'])
    Yamplitudes.append(value['Yamp'])

Xamplitudes = np.array(Xamplitudes)
print(Xamplitudes.shape)
np.save('Xamplitudes.npy', Xamplitudes)
Yamplitudes = np.array(Yamplitudes)
print(Yamplitudes.shape)
np.save('Yamplitudes.npy', Yamplitudes)

#     outline = 'chanfreq, ampXX, angXX, ampXY, angXY, ampYX, angYX, ampYY, angYY'
#     fout.write('{}\n'.format(outline))
#     for cfreq, campxx, cphasexx, campxy, cphasexy, campyx, cphaseyx, campyy, cphaseyy in zip(freq_range, ampxx, phasexx, ampxy, phasexy, ampyx, phaseyx, ampyy, phaseyy):
#         outline = '{:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}'.format(
#                   cfreq,
#                   campxx,
#                   cphasexx,
#                   campxy,
#                   cphasexy,
#                   campyx,
#                   cphaseyx,
#                   campyy,
#                   cphaseyy,
#                   )
#         fout.write('{}\n'.format(outline))

# -fin-
