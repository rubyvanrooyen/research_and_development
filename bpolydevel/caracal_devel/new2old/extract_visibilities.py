from numpy import recarray
import numpy as np
import pyrap.tables as pt

import os

with pt.table("1627186165_sdp_l0-cal.ms/SPECTRAL_WINDOW") as tb:
    freq_range = tb.getcol("CHAN_FREQ").squeeze()
    print(freq_range.shape)

with pt.table("1627186165_sdp_l0-cal.ms") as tb:
    # per block dimension: nbls x nchans x ncorrs
    data = tb.getcol("DATA").squeeze()
    realavg = data.real.mean(axis=0)
    rxx = realavg[:,0]
    rxy = realavg[:,1]
    ryx = realavg[:,2]
    ryy = realavg[:,3]
    imagavg = data.imag.mean(axis=0)
    imxx = imagavg[:,0]
    imxy = imagavg[:,1]
    imyx = imagavg[:,2]
    imyy = imagavg[:,3]
    visxx = rxx + 1j*imxx
    visxy = rxy + 1j*imxy
    visyx = ryx + 1j*imyx
    visyy = ryy + 1j*imyy
    ampxx = np.abs(visxx)
    ampxy = np.abs(visxy)
    ampyx = np.abs(visyx)
    ampyy = np.abs(visyy)
    print(ampxx.shape)
    phasexx = np.unwrap(np.angle(visxx))
    phasexy = np.unwrap(np.angle(visxy))
    phaseyx = np.unwrap(np.angle(visyx))
    phaseyy = np.unwrap(np.angle(visyy))

import matplotlib.pylab as plt
plt.figure()
plt.subplot(211)
plt.plot(ampxx, 'r,', label='xx')
# plt.plot(ampxy, 'b,', label='xy')
# plt.plot(ampyx, 'g,', label='yx')
plt.plot(ampyy, 'k,', label='yy')
plt.legend()
plt.subplot(212)
plt.plot(phasexx, 'r,', label='xx')
# plt.plot(phasexy, 'b,', label='xy')
# plt.plot(phaseyx, 'g,', label='yx')
plt.plot(phaseyy, 'k,', label='yy')
plt.legend()
plt.savefig("mygraph.png")

# write to CSV file
filename = os.path.splitext("1627186165_sdp_l0-cal.ms")[0]+'.csv'
with open(filename, 'w') as fout:
    outline = 'chanfreq, ampXX, angXX, ampXY, angXY, ampYX, angYX, ampYY, angYY'
    fout.write('{}\n'.format(outline))
    for cfreq, campxx, cphasexx, campxy, cphasexy, campyx, cphaseyx, campyy, cphaseyy in zip(freq_range, ampxx, phasexx, ampxy, phasexy, ampyx, phaseyx, ampyy, phaseyy):
        outline = '{:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}, {:.10f}'.format(
                  cfreq,
                  campxx,
                  cphasexx,
                  campxy,
                  cphasexy,
                  campyx,
                  cphaseyx,
                  campyy,
                  cphaseyy,
                  )
        fout.write('{}\n'.format(outline))

# -fin-
