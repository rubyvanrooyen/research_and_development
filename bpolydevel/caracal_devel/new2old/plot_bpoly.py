"""
Display bandpass solution by calculating the chebyshev polynomial from BPOLY coefficients
"""

import os
from os import F_OK

from tasks import *
from taskinit import *
import casac

### Hard coded definition of Btable structure ###

# """
# Mimic the plotms command in CASA to display BPOLY gain calibration results
# plotms(vis=bpoly_caltable, xaxis='freq', yaxis='phase', field=bpcal, coloraxis='corr')
# 
# Reference:
#     http://www.eso.org/~jagonzal/telcal/antenna_position/online-antenna-position/analysis_scripts/plotbandpass3.py
# """

import numpy as np
import matplotlib.pylab as plt


def calcChebyshev(coeff, validDomain, x):
    """
    Given a set of coefficients, evaluate a Chebyshev series at points x

    @param coeff NDArray    : Chebyshev polynomial coefficients
    @param validDomain List : Domain to use. The interval [domain[0], domain[1]]
    @param coeff NDArray    : Points to evaluate coefficients at

    @return values NDArray  : Chebyshev approximated values

    """
    xrange_ = validDomain[1] - validDomain[0]
    x = -1 + 2*(x-validDomain[0])/xrange_
    coeff[0] = 0

    values = np.polynomial.chebyshev.chebval(x,coeff)
    return values


def readBPOLY(caltable):
    """
    Extract polyfit coefficients from caltable

    @param caltable String          : CARACal table name (*.P?)

    @return scaleFactor NDArray     : Amplitude scale factor
    @return antennasBP NDArray      : Antenna IDs
    @return frequencyLimits NDArray : Domain to use. The interval [domain[0], domain[1]]
    @return frequenciesGHz NDArray  : Poly eval x points
    @return nPolyAmp NDArray        : Amplitude poly fit degree
    @return nPolyPhase NDArray      : Phase poly fit degree
    @return polynomialAmplitude NDArray : Amplitude fit Chebyshev coefficients
    @return polynomialPhase NDArray : Phase fit Chebyshev coefficients
    """

    tb.open(caltable)

    # output for user info
    polyMode = tb.getcol('POLY_MODE')
    print("This is a BPOLY solution = %s" % (polyMode[0]))
    polyType = tb.getcol('POLY_TYPE')
    print("The 'BPOLY' solver fits ({}) polynomials to the amplitude and phase of the calibrator visibilities as a function of frequency."
            .format(np.unique(polyType)))
    uniqueTimesBP = np.unique(tb.getcol('TIME'))
    nUniqueTimesBP = len(uniqueTimesBP)
    tsstring = "There are %d unique times in the BPOLY solution: " % nUniqueTimesBP
    for u in uniqueTimesBP:
        tsstring += '%.3f, ' % (u)
    print(tsstring)


    # table information needed for display
    scaleFactor = tb.getcol('SCALE_FACTOR')
    antennasBP = tb.getcol('ANTENNA1')
    frequencyLimits = tb.getcol('VALID_DOMAIN')

    frequenciesGHz = []
    increments = 0.001*(frequencyLimits[1,:]-frequencyLimits[0,:])
    for i in range(len(increments)):
        freqs = (1e-9)*np.arange(frequencyLimits[0,i],frequencyLimits[1,i],increments[i])
        frequenciesGHz.append(freqs)

    # poly fit degrees
    nPolyAmp = tb.getcol('N_POLY_AMP')
    degamp = int(np.unique(nPolyAmp))
    nPolyPhase = tb.getcol('N_POLY_PHASE')
    degphase = int(np.unique(nPolyPhase))
    print("BPOLY fit using AMP order %d and PHASE order %d" % (degamp, degphase))
    # amplitude coefficients for antenna
    print(polyMode.shape)
    polynomialAmplitude = []
    polynomialPhase = []
    for i in range(len(polyMode)):
        polynomialAmplitude.append([1])
        polynomialPhase.append([0])
        if (polyMode[i] == 'A&P' or polyMode[i] == 'A'):
            polynomialAmplitude[i]  = tb.getcell('POLY_COEFF_AMP',i)[0][0][0]
        if (polyMode[i] == 'A&P' or polyMode[i] == 'P'):
            polynomialPhase[i] = tb.getcell('POLY_COEFF_PHASE',i)[0][0][0]

    tb.close()

    return scaleFactor, antennasBP, frequencyLimits, frequenciesGHz, nPolyAmp, nPolyPhase, polynomialAmplitude, polynomialPhase


def main(caltable):
    """
    Read and plot gain solutions from BPOLY table

    @param caltable String : CARACal table name (*.P?)

    @return None
    """

    # read caltable
    [scaleFactor,
     antennasBP,
     frequencyLimits,
     frequenciesGHz,
     nPolyAmp,
     nPolyPhase,
     polynomialAmplitude,
     polynomialPhase] = readBPOLY(caltable)

    # display results
    print("The degphase ({}) and degamp ({}) parameters indicate the polynomial degree desired for the amplitude and phase solutions."
          .format(np.unique(nPolyPhase), np.unique(nPolyAmp)))
    for index in antennasBP:
        print('Antenna nr %d' % index)

        # start and end frequency (hz) defining valid frequency domain
        scaleFactor_ = scaleFactor[index]
        validDomain_ = [frequencyLimits[0,index], frequencyLimits[1,index]]
        freqRangeHz_ = np.array(frequenciesGHz[index], dtype=float)*1e+9
        # X pol coefficients
        AmpCoeffX_ = np.array(polynomialAmplitude[index][0:nPolyAmp[index]], dtype=float)
        PhaseCoeffX_ = np.array(polynomialPhase[index][0:nPolyPhase[index]], dtype=float)
        # Y pol coefficients
        AmpCoeffY_ = np.array(polynomialAmplitude[index][nPolyAmp[index]:2*nPolyAmp[index]], dtype=float)
        PhaseCoeffY_ = np.array(polynomialPhase[index][nPolyPhase[index]:2*nPolyPhase[index]], dtype=float)
        # calculate CHEBYSHEV poly values
        amplitudeSolutionX = np.real(scaleFactor_) \
                           + calcChebyshev(AmpCoeffX_,
                                           validDomain_,
                                           freqRangeHz_)
        amplitudeSolutionX += 1 - np.mean(amplitudeSolutionX)
        amplitudeSolutionY = np.real(scaleFactor_) \
                           + calcChebyshev(AmpCoeffY_,
                                           validDomain_,
                                           freqRangeHz_)
        amplitudeSolutionY += 1 - np.mean(amplitudeSolutionY)
        phaseSolutionX = calcChebyshev(PhaseCoeffX_,
                                       validDomain_,
                                       freqRangeHz_) * 180/np.pi
        phaseSolutionY = calcChebyshev(PhaseCoeffY_,
                                       validDomain_,
                                       freqRangeHz_) * 180/np.pi

        # plot amp and phase solutions
        plt.subplot(211)
        plt.plot(frequenciesGHz[index], amplitudeSolutionX, 'k-',
                 frequenciesGHz[index], amplitudeSolutionY, 'r-')
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Amplitude')
        plt.subplot(212)
        plt.plot(frequenciesGHz[index], phaseSolutionX, 'k-',
                 frequenciesGHz[index], phaseSolutionY, 'r-')
        plt.xlabel('Frequency (GHz)')
        plt.ylabel('Phase (deg)')

    plt.show()


if __name__ == '__main__':

    # CARACal BPOLY caltables are designated *.P?
    bpoly_caltable='3C39_comet-1627186165_sdp_l0-1gc_primary.P1'
    main(bpoly_caltable)

# -fin-

