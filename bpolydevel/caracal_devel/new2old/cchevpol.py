# """
# This is a temporary hack to map the BPOLY table to Bcal table in CASA
# It copies an existing table and update the values
# """
# 
# import caracal
# import os
# import sys

import numpy as np

from casacore.tables import table
import casacore.fitting as fitting
# # import casacore.functionals as fun
# import casacore.fitting as nofun


def metaref(bpolytable):
    """
    Extract info from reference Measurement Set

    @param bpolytable string : CARACal BPOLY table name

    @return msfile string      : Name of reference MS file
    @return nrows int          : Nr of rows in Bcal table
    @return XXpol_idx int       : Index of XX pol correlator data
    @return YYpol_idx int       : Index of YY pol correlator data
    @return freq_range ndarray : Observation Frequency range [Hz]
    """

    # get nr of rows for new table
    nrows = table(bpolytable, ack=False).nrows()

    # get the ms file you're gonna need it
    msfile= table(bpolytable+"::CAL_DESC", ack=False).getcol('MS_NAME')[0]

    # Data: Complex value for each of 4 correlations per spectral channel
    # IDs correspond to values RR (5), RL (6), LR (7), LL (8), XX (9), XY (10), YX (11), and YY (12)
    corr_prods_id = {5: 'RR', 6: 'RL', 7: 'LR', 8: 'LL',
                     9: 'XX', 10: 'XY', 11: 'YX', 12: 'YY'}
    with table(msfile+'::POLARIZATION', ack=False) as tb:
        ncorr_prods = int(tb.getcol("NUM_CORR"))
        corr_prods = tb.getcol("CORR_TYPE").squeeze()
        tb.close()
    # associate corr prod with 4 tuple indices
    lin_prods = np.array([corr_prods_id[prod] for prod in corr_prods])
    XXpol_idx = np.nonzero(lin_prods == 'XX')[0][0]  # H pol
    XYpol_idx = np.nonzero(lin_prods == 'XY')[0][0]  # H pol
    YYpol_idx = np.nonzero(lin_prods == 'YY')[0][0]  # V pol
    YXpol_idx = np.nonzero(lin_prods == 'YX')[0][0]  # V pol
    print('Correlation products {}'.format(corr_prods))
    for prod in corr_prods:
        print('  {:2} : {}'.format(prod, corr_prods_id[prod]))
    # H = XX
    print(f'H pol {XXpol_idx} index in corr products')
    # V = YY
    print(f'V pol {YYpol_idx} index in corr products')

    freq_range = table(msfile+"::SPECTRAL_WINDOW", ack=False).getcol("CHAN_FREQ").squeeze()
    antennas = table(msfile+"::ANTENNA", ack=False).getcol("NAME")
    print('Antennas: {}'.format(antennas))

    # find passband from flags
    flags = table(msfile, ack=False).getcol("FLAG")
    [nrows, nchans, npols] = flags.shape
    flags=flags.sum(axis=0)/nrows
    flags = flags.sum(axis=1)/npols
    flag_mask = flags > 0.5

    return msfile, nrows, XXpol_idx, YYpol_idx, freq_range, antennas, flag_mask


def readcolumnasscalar(bpolytable, bp_field):
    """
    CASA varcol data / python dict column values flatten to np.ndarray

    @param bpolytable string : CARACal BPOLY table name
    @param bp_field string   : Name of BPOLY column to read

    @return colvalues ndarray : Column values as flat array
    """
    colvalues = readcolumn(bpolytable, bp_field)
    if isinstance(colvalues, dict):
        flatlist = []
        for key, value in colvalues.items():
            flatlist.append(value.squeeze())
        colvalues = np.array(flatlist)
    return colvalues


def readcolumn(btable, bp_field=None):
    """
    Read column data from BPOLY cal table

    @param btable string   : CARACal B table name
    @param bp_field string : Name of BPOLY column to read

    @return values ndarray   : BPOLY column values 
    """
    with table(btable, ack=False) as tb:
        if tb.isscalarcol(bp_field):
            values = tb.getcol(bp_field)
        elif tb.isvarcol(bp_field):
            values = tb.getvarcol(bp_field)
        else:
            values = tb.getcol(bp_field)
    return values


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

    values = np.polynomial.chebyshev.chebval(x, coeff)
    return values


def readBPOLY(bpolytable):
    """
    Extract polyfit coefficients from bpolytable

    @param bpolytable string        : CARACal BPOLY table name

    @return scaleFactor NDArray     : Amplitude scale factor
    @return antennasBP NDArray      : Antenna IDs
    @return frequencyLimits NDArray : Domain to use. The interval [domain[0], domain[1]]
    @return frequenciesGHz NDArray  : Poly eval x points
    @return nPolyAmp NDArray        : Amplitude poly fit degree
    @return nPolyPhase NDArray      : Phase poly fit degree
    @return polynomialAmplitude NDArray : Amplitude fit Chebyshev coefficients
    @return polynomialPhase NDArray : Phase fit Chebyshev coefficients
    """

    # output for user info
    polyMode = readcolumn(bpolytable, "POLY_MODE")
    print(f"This is a BPOLY solution = {polyMode[0]}")
    polyType = readcolumn(bpolytable, "POLY_TYPE")
    print(f"The 'BPOLY' solver fits ({np.unique(polyType)}) polynomials to the amplitude and phase of the calibrator visibilities as a function of frequency.")

    uniqueTimesBP = np.unique(readcolumn(bpolytable, "TIME"))
    nUniqueTimesBP = len(uniqueTimesBP)
    tsstring = f"There are {nUniqueTimesBP} unique times in the BPOLY solution: "
    for u in uniqueTimesBP:
        tsstring += '%.3f, ' % (u)
    print(tsstring)

    # table information needed for display
    scaleFactor = readcolumnasscalar(bpolytable, 'SCALE_FACTOR')
    antennasBP = readcolumnasscalar(bpolytable, 'ANTENNA1')
    frequencyLimits = readcolumnasscalar(bpolytable, 'VALID_DOMAIN')

     # poly fit degrees
    nPolyAmp = readcolumnasscalar(bpolytable, 'N_POLY_AMP')
    degamp = int(np.unique(nPolyAmp))
    nPolyPhase = readcolumnasscalar(bpolytable, 'N_POLY_PHASE')
    degphase = int(np.unique(nPolyPhase))
    print(f"BPOLY fit using AMP order {degamp} and PHASE order {degphase}")
    print(f"BPOLY fit using AMP order {degamp-1} and PHASE order {degphase-1}")

    # amplitude coefficients for antenna
    if (polyMode[0] == 'A&P' or polyMode[0] == 'A'):
        polynomialAmplitude = readcolumnasscalar(bpolytable, "POLY_COEFF_AMP")

    # phase coefficients for antenna
    if (polyMode[0] == 'A&P' or polyMode[0] == 'P'):
        polynomialPhase = readcolumnasscalar(bpolytable, "POLY_COEFF_PHASE")
    return scaleFactor, antennasBP, frequencyLimits, nPolyAmp, nPolyPhase, polynomialAmplitude, polynomialPhase


def bpolyfit(bpolytable, freq_range, antennas, flag_mask):

    # read caltable
    [scaleFactor,
     antennasBP,
     frequencyLimits,
     nPolyAmp,
     nPolyPhase,
     polynomialAmplitude,
     polynomialPhase] = readBPOLY(bpolytable)

    # display results
    PolyPhaseOrder = np.unique(nPolyPhase)[0]
    PolyAmpOrder = int(np.unique(nPolyAmp))
    print(PolyAmpOrder, type(PolyAmpOrder), nPolyAmp.shape)
    print(f"The degphase ({PolyPhaseOrder}) and degamp ({PolyAmpOrder}) parameters indicate the polynomial degree desired for the amplitude and phase solutions.")
    print(f"The degphase ({np.unique(nPolyPhase)-1}) and degamp ({np.unique(nPolyAmp)-1}) parameters indicate the polynomial degree desired for the amplitude and phase solutions.")
    bcal_sol = np.full([len(antennasBP), len(freq_range), 2], 0.+1j*0 ,dtype=np.complex128)
    freq_rangeHz_ = np.array(freq_range)
    for index in antennasBP:
        print(index, antennas[index])
        # start and end frequency (hz) defining valid frequency domain
        scaleFactor_ = scaleFactor[index]
        print(f"Scale factor {scaleFactor}")
        validDomain_ = [frequencyLimits[index,0], frequencyLimits[index,1]]
        print(f"xmin={validDomain_[0]}, xmax={validDomain_[1]}")
        # X pol coefficients
        AmpCoeffX_ = polynomialAmplitude[index, 0:nPolyAmp[index]]
        print(f"X amp coeffs {AmpCoeffX_}")
        # calculate CHEBYSHEV poly values
        bl=fitting.chebyshev(int(nPolyAmp[index])-1,
                             params=AmpCoeffX_,
                             xmin=frequencyLimits[index,0],
                             xmax=frequencyLimits[index,1])
        amplitudeSolutionX = bl.f(freq_range)
        amplitudeSolutionX = np.real(scaleFactor_) \
                           * amplitudeSolutionX \
                           + 1 - np.mean(amplitudeSolutionX[np.invert(flag_mask)])

        # calculate CHEBYSHEV poly values
        amplitudeSolutionX0 = np.real(scaleFactor_) \
                            * calcChebyshev(AmpCoeffX_,
                                            validDomain_,
                                            freq_rangeHz_)
        amplitudeSolutionX0 += 1 - np.mean(amplitudeSolutionX0[np.invert(flag_mask)])

        PhaseCoeffX_ = polynomialPhase[index, 0:nPolyPhase[index]]
        # calculate CHEBYSHEV poly values
        bl=fitting.chebyshev(int(nPolyPhase[index])-1,
                             params=PhaseCoeffX_,
                             xmin=frequencyLimits[index,0],
                             xmax=frequencyLimits[index,1])
        phaseSolutionX = bl.f(freq_range)
        phaseSolutionX = np.real(scaleFactor_) \
                       * phaseSolutionX \
                       - np.mean(phaseSolutionX[np.invert(flag_mask)])  # rad
#         phaseSolutionX = calcChebyshev(PhaseCoeffX_,
#                                        validDomain_,
#                                        freq_rangeHz_)  # rad

        # Y pol coefficients
        AmpCoeffY_ = polynomialAmplitude[index, nPolyAmp[index]:2*nPolyAmp[index]]
        print(f"Y amp coeffs {AmpCoeffY_}")
        # calculate CHEBYSHEV poly values
        bl=fitting.chebyshev(int(nPolyAmp[index])-1,
                             params=AmpCoeffY_,
                             xmin=frequencyLimits[index,0],
                             xmax=frequencyLimits[index,1])
        amplitudeSolutionY = bl.f(freq_range)
        amplitudeSolutionY = np.real(scaleFactor_) \
                           * amplitudeSolutionY \
                           + 1 - np.mean(amplitudeSolutionY[np.invert(flag_mask)])
        # calculate CHEBYSHEV poly values
        amplitudeSolutionY0 = np.real(scaleFactor_) \
                            * calcChebyshev(AmpCoeffY_,
                                            validDomain_,
                                            freq_rangeHz_)
        amplitudeSolutionY0 += 1 - np.mean(amplitudeSolutionY0[np.invert(flag_mask)])

        PhaseCoeffY_ = polynomialPhase[index, nPolyPhase[index]:2*nPolyPhase[index]]
        # freq_range=freq_range[:-1]
        # calculate CHEBYSHEV poly values
        bl=fitting.chebyshev(int(nPolyPhase[index])-1,
                             params=PhaseCoeffY_,
                             xmin=frequencyLimits[index,0],
                             xmax=frequencyLimits[index,1])
        phaseSolutionY = bl.f(freq_range)
        phaseSolutionY = np.real(scaleFactor_) \
                       * phaseSolutionY \
                       - np.mean(phaseSolutionY[np.invert(flag_mask)])  # rad
#         phaseSolutionY = calcChebyshev(PhaseCoeffY_,
#                                        validDomain_,
#                                        freq_rangeHz_)  # rad

        antBX = np.array(amplitudeSolutionX*(np.cos(phaseSolutionX) \
              + 1j*np.sin(phaseSolutionX)), dtype=np.complex128)
        antBY = np.array(amplitudeSolutionY*(np.cos(phaseSolutionY) \
              + 1j*np.sin(phaseSolutionY)), dtype=np.complex128)
#         antB = np.column_stack([antBX.squeeze(), antBY.squeeze()])
#         bcal_sol[index, :, :] = antB

        import matplotlib.pylab as plt
        plt.figure()
#         plt.plot(freq_range/1e9, amplitudeSolutionY, label='chebY')
#         plt.plot(freq_range/1e9, amplitudeSolutionX, label='chebX')
#         plt.plot(freq_range/1e9, amplitudeSolutionY0, "--", label='chebY')
#         plt.plot(freq_range/1e9, amplitudeSolutionX0, "--", label='chebX')
#         plt.plot(freq_range/1e9, np.degrees(phaseSolutionY), label='chebY')
#         plt.plot(freq_range/1e9, np.degrees(phaseSolutionX), label='chebX')
#         plt.plot(freq_range[np.invert(flag_mask)]/1e9, np.abs(antBX)[np.invert(flag_mask)], label='chebX')
#         plt.plot(freq_range[np.invert(flag_mask)]/1e9, np.abs(antBY)[np.invert(flag_mask)], label='chebY')
        plt.plot(freq_range[np.invert(flag_mask)]/1e9, np.degrees(np.angle(antBX)[np.invert(flag_mask)]), label='chebX')
        plt.plot(freq_range[np.invert(flag_mask)]/1e9, np.degrees(np.angle(antBY)[np.invert(flag_mask)]), label='chebY')
        plt.legend()
        plt.savefig(f"mygraph{antennas[index]}.png")




if __name__ == '__main__':

    bpolytable = "3C39_comet-1627186165_sdp_l0-1gc_primary.P1"

    print('Building a CASA B table from BPOLY table')
    # get various bits of metadata needed to extract and reconstruct information
    [msfile,
     nrows,
     XXpol_idx,
     YYpol_idx,
     freq_range,
     antennas,
     flag_mask] = metaref(bpolytable)

    bpolyfit(bpolytable, freq_range, antennas, flag_mask)

# -fin-
