"""
This is a prototype to see if you can map the BPOLY table to Bcal table in CASA
It copies an existing table and update the values


The next step will be to contruct a table that works
"""

import os, sys

from tasks import *
from taskinit import *
import casa

import numpy as np


def metaref(bpolytable):
    """
    Extract info from reference Measurement Set

    @param bpolytable string : CARACal table name (*.P?)

    @return msfile string    : Name of reference MS file
    @return nrows int        : Nr of rows in Bcal table
    @return Xpol_idx int     : Index of XX pol correlator data
    @return Ypol_idx int     : Index of YY pol correlator data
    @return freq_range Array : Observation Frequency range [Hz]
    """

    # get nr of rows for new table
    tb.open(bpolytable)
    nrows = tb.nrows()
    tb.close()

    # get the ms file you're gonna need it
    tb.open(bpolytable+"/CAL_DESC")
    msfile=tb.getcol('MS_NAME')[0]
    tb.close()

    # Data: Complex value for each of 4 correlations per spectral channel
    # IDs correspond to values RR (5), RL (6), LR (7), LL (8), XX (9), XY (10), YX (11), and YY (12)
    corr_prods_id = {5: 'RR', 6: 'RL', 7: 'LR', 8: 'LL',
                     9: 'XX', 10: 'XY', 11: 'YX', 12: 'YY'}
    tb.open(msfile+'/POLARIZATION')
    ncorr_prods = int(tb.getcol("NUM_CORR"))
    corr_prods = tb.getcol("CORR_TYPE").squeeze()
    # associate corr prod with 4 tuple indices
    lin_prods = np.array([corr_prods_id[prod] for prod in corr_prods])
    Xpol_idx = np.nonzero(lin_prods == 'XX')[0][0]  # H pol
    Ypol_idx = np.nonzero(lin_prods == 'YY')[0][0]  # V pol
    tb.close()
    # H = XX
    print('H pol {} index in corr products'.format(Xpol_idx))
    # V = YY
    print('V pol {} index in corr products'.format(Ypol_idx))

    tb.open(msfile+"/SPECTRAL_WINDOW")
    freq_range = tb.getcol("CHAN_FREQ")
    tb.close()

    return msfile, nrows, Xpol_idx, Ypol_idx, freq_range


def create_empty_B(bpolytable, template_bcal, nrows=1):
    """
    Create an empty B cal table from BPOLY cal table

    @param bpolytable string    : CARACal table name (*.P?)
    @param template_bcal string : Empty Bcal table name (*.B)
    @param nrows int            : [Optional] Number of rows in table

    @return btable string    : Name of empty CASA B table name
    """
    # output MS assuming BCAL table
    [filename, ext] = os.path.splitext(os.path.basename(bpolytable))
    btable="{}.B{}".format(filename, ext[-1])

    # get old table schema by reading empty templage MS: "",
    print("Creating BCAL table {}".format(btable))
    tb.open(template_btable)
    tb.copy(btable, deep=True)
    tb.close()

    # add the rows _before_ filling the columns.
    tb.open(btable, nomodify=False)
    tb.addrows(nrows-1)
    tb.close()

    return btable


def addsubtables(msname, btable):
    # note which MS you used
    tb.open(btable, nomodify=False)
    fieldnames=tb.getkeywords()
    tb.putkeyword("MSName", msname)
    tb.flush()
    tb.close()

    # get list of subtables to create
    subtable_list = []
    for name, value in fieldnames.iteritems():
        if "table" in str(value).lower():
            subtable_list.append([name, value.split()[-1].strip()])

    # subtables are just copies from MS subtables
    for name, path in subtable_list:
        if name == 'HISTORY':
            continue
        tb.open(msname+'/'+name)
        tb.copyrows(btable+'/'+name, startrowout=0)
        tb.close()


def readcolumn(bpolytable, bp_field=None):
    """
    Read column data from BPOLY cal table

    @param bpolytable string : CARACal table name (*.P?)
    @param bp_field string   : Name of BPOLY column to read

    @return values Array     : BPOLY column values 
    """
    tb.open(bpolytable)
    # check if column has values
    values = None
    try:
        if tb.iscelldefined(bp_field):
            # read values
            values = tb.getcol(bp_field)
    except RuntimeError:
        pass
    tb.close()
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

    @param bpolytable string        : CARACal table name (*.P?)

    @return scaleFactor NDArray     : Amplitude scale factor
    @return antennasBP NDArray      : Antenna IDs
    @return frequencyLimits NDArray : Domain to use. The interval [domain[0], domain[1]]
    @return frequenciesGHz NDArray  : Poly eval x points
    @return nPolyAmp NDArray        : Amplitude poly fit degree
    @return nPolyPhase NDArray      : Phase poly fit degree
    @return polynomialAmplitude NDArray : Amplitude fit Chebyshev coefficients
    @return polynomialPhase NDArray : Phase fit Chebyshev coefficients
    """

    tb.open(bpolytable)

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

    # poly fit degrees
    nPolyAmp = tb.getcol('N_POLY_AMP')
    degamp = int(np.unique(nPolyAmp))
    nPolyPhase = tb.getcol('N_POLY_PHASE')
    degphase = int(np.unique(nPolyPhase))
    print("BPOLY fit using AMP order %d and PHASE order %d" % (degamp, degphase))
    # amplitude coefficients for antenna
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

    return scaleFactor, antennasBP, frequencyLimits, nPolyAmp, nPolyPhase, polynomialAmplitude, polynomialPhase


def bpolyfit(bpolytable, freq_range):
    """
    Calculate gain solutions from BPOLY table

    @param bpolytable string : CARACal table name (*.P?)
    @param freq_range Array  : Observation Frequency range [Hz]

    @return bcal_sol NDArray : Bcal solution from poly fit
    """
    # read caltable
    [scaleFactor,
     antennasBP,
     frequencyLimits,
     nPolyAmp,
     nPolyPhase,
     polynomialAmplitude,
     polynomialPhase] = readBPOLY(bpolytable)

    # display results
    print("The degphase ({}) and degamp ({}) parameters indicate the polynomial degree desired for the amplitude and phase solutions."
          .format(np.unique(nPolyPhase), np.unique(nPolyAmp)))
    bcal_sol = np.full([2, len(freq_range), len(antennasBP)], 0.+1j*0 ,dtype=np.complex128)
    for index in antennasBP:
        # start and end frequency (hz) defining valid frequency domain
        scaleFactor_ = scaleFactor[index]
        validDomain_ = [frequencyLimits[0,index], frequencyLimits[1,index]]
        freq_rangeHz_ = np.array(freq_range)
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
                                           freq_rangeHz_)
        amplitudeSolutionX += 1 - np.mean(amplitudeSolutionX)
        amplitudeSolutionY = np.real(scaleFactor_) \
                           + calcChebyshev(AmpCoeffY_,
                                           validDomain_,
                                           freq_rangeHz_)
        amplitudeSolutionY += 1 - np.mean(amplitudeSolutionY)
        phaseSolutionX = calcChebyshev(PhaseCoeffX_,
                                       validDomain_,
                                       freq_rangeHz_)  # rad
        phaseSolutionY = calcChebyshev(PhaseCoeffY_,
                                       validDomain_,
                                       freq_rangeHz_)  # rad

        antBX = np.array(amplitudeSolutionX*(np.cos(phaseSolutionX) + 1j*np.sin(phaseSolutionX)), dtype=np.complex128)
        antBY = np.array(amplitudeSolutionY*(np.cos(phaseSolutionY) + 1j*np.sin(phaseSolutionY)), dtype=np.complex128)
        antB = np.vstack([antBX.squeeze(), antBY.squeeze()])
        bcal_sol[:,:,index] = antB
    return bcal_sol


def map_main_tbl(
                 msfile,
                 bpolytable,
                 freq_range,
                 nrows=1,
                 ):
    """
    Populate Bcal main table column data

    @param msfile string     : Reference CASA MS name
    @param bpolytable string : CASA BPOLY table name
    @return freq_range Array : Observation Frequency range [Hz]
    @return nrows int        : [Optional] Nr of rows in Bcal table

    @return mail_tbl_dict Dict : Bcal table main table 
    """
    main_tbl_dict = {}
    # nrows [linux ts]
    main_tbl_dict["TIME"] = readcolumn(bpolytable, bp_field="TIME")
    # nrows [int]
    main_tbl_dict["FIELD_ID"] = readcolumn(bpolytable, bp_field="FIELD_ID")
    # nrows [int] ant index
    main_tbl_dict["ANTENNA1"] = readcolumn(bpolytable, bp_field="ANTENNA1")
    # nrows [int] ant index
    main_tbl_dict["ANTENNA2"] = readcolumn(bpolytable, bp_field="REF_ANT")
    # nrows [int]
    main_tbl_dict["INTERVAL"] = readcolumn(bpolytable, bp_field="INTERVAL")
    # nrows [int]
    main_tbl_dict["SCAN_NUMBER"] = readcolumn(bpolytable, bp_field="SCAN_NUMBER")
    # nrows [int]
    main_tbl_dict["OBSERVATION_ID"] = readcolumn(bpolytable, bp_field="OBSERVATION_ID")

    # nrows [int]
    spw_id = readcolumn(bpolytable+"/CAL_DESC", bp_field="SPECTRAL_WINDOW_ID")
    main_tbl_dict["SPECTRAL_WINDOW_ID"] = np.array(nrows*[int(spw_id)], dtype=np.int32)

    # 2 x nchans x nrows [complex] 
    main_tbl_dict["CPARAM"] = bpolyfit(bpolytable, freq_range)

    # default values for now
    nchans = len(freq_range)
    # 2 x nchans x nrows [bool] 
    main_tbl_dict['FLAG'] = np.full([2, nchans, nrows], 0., dtype=float)
    main_tbl_dict["PARAMERR"] = np.full([2, nchans, nrows], 0., dtype=float)
    main_tbl_dict["SNR"] = np.full([2, nchans, nrows], 0., dtype=float)

    # leave some columns empty for now
    main_tbl_dict["WEIGHT"] = np.empty([2, nchans, nrows], dtype=float)

    return main_tbl_dict


def Bpoly2B(bpolytable, template_btable):
    """
    Build a CASA B table from a CASA BPOLY table

    @param bpolytable string    : CARACal table name (*.P?)
    @param template_bcal string : Empty Bcal table name (*.B)

    @return btable string : CASA table name (*.B?)
    """
    # get various bits of metadata needed to extract and reconstruct information
    [msfile,
     nrows,
     Xpol_idx,
     Ypol_idx,
     freq_range] = metaref(bpolytable)

    # create empty BCAL table
    btable = create_empty_B(bpolytable, template_btable, nrows=nrows)

    # mapping of main table
    main_tbl_dict = map_main_tbl(
                                 msfile,
                                 bpolytable,
                                 freq_range,
                                 nrows=nrows,
                                 )

    # write info to Btable
    column_names = [
                    "TIME",
                    "FIELD_ID",
                    "SPECTRAL_WINDOW_ID",
                    "ANTENNA1",
                    "ANTENNA2",
                    "INTERVAL",
                    "SCAN_NUMBER",
                    "OBSERVATION_ID",
                    "CPARAM",
                    "PARAMERR",
                    "FLAG",
                    "SNR",
                    "WEIGHT",
                    ]

    tb.open(btable, nomodify=False)
    # force to release all locks
    tb.clearlocks()
    for col in column_names:
        tb.putcol(col, main_tbl_dict[col])
        tb.flush()
    tb.close()

    # copy relevant MS subtables over
    addsubtables(msfile, btable)

    return btable


if __name__ == '__main__':
    if (len(sys.argv)) < 3:
        print("Usage: {} <table_name.P> <template_name.B>".format(sys.argv[0]))
        sys.exit(0)

    bpolytable = sys.argv[1]
    template_btable = sys.argv[2]

    btable =  Bpoly2B(bpolytable, template_btable)

# -fin-
