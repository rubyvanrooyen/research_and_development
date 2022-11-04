import os, sys

from tasks import *
from taskinit import *
import casa

import numpy as np

class MainTable:
    def __init__(self, path='.'):
        self.desc = {
        'ANTENNA1': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'option': 5, 'valueType': 'int'},
        'ANTENNA2': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'option': 5, 'valueType': 'int'},
        'CPARAM': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'ndim': -1, 'option': 0, 'valueType': 'complex'},
        'FIELD_ID': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'option': 5, 'valueType': 'int'},
        'FLAG': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'ndim': -1, 'option': 0, 'valueType': 'boolean'},
        'INTERVAL': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan',
                     'keywords': {'QuantumUnits': np.array(['s'], dtype='|S2')},
                     'maxlen': 0, 'option': 5, 'valueType': 'double'},
        'OBSERVATION_ID': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'option': 5, 'valueType': 'int'},
        'PARAMERR': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'ndim': -1, 'option': 0, 'valueType': 'float'},
        'SCAN_NUMBER': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'option': 5, 'valueType': 'int'},
        'SNR': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'ndim': -1, 'option': 0, 'valueType': 'float'},
        'SPECTRAL_WINDOW_ID': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'option': 5, 'valueType': 'int'},
        'TIME': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan',
                 'keywords': {'MEASINFO': {'Ref': 'UTC', 'type': 'epoch'}, 'QuantumUnits': np.array(['s'], dtype='|S2')},
                 'maxlen': 0, 'option': 5, 'valueType': 'double'},
        'WEIGHT': {'comment': '', 'dataManagerGroup': 'MSMTAB', 'dataManagerType': 'StandardStMan', 'keywords': {}, 'maxlen': 0, 'ndim': -1, 'option': 0, 'valueType': 'float'},
        '_define_hypercolumn_': {},
        '_keywords_': {'ANTENNA': 'Table: {}/ANTENNA'.format(path),
                       'CASA_Version': '5.8.0-109',
                       'FIELD': 'Table: {}/FIELD'.format(path),
                       'HISTORY': 'Table: {}/HISTORY'.format(path),
                       'MSName': 'dummyname.ms',
                       'OBSERVATION': 'Table: {}/OBSERVATION'.format(path),
                       'ParType': 'Complex',
                       'PolBasis': 'unknown',
                       'SPECTRAL_WINDOW': 'Table: {}/SPECTRAL_WINDOW'.format(path),
                       'VisCal': 'B Jones'},
        '_private_keywords_': {}}

        self.dminfo = {
                '*1':{'COLUMNS': np.array(['ANTENNA1', 'ANTENNA2', 'CPARAM', 'FIELD_ID', 'FLAG', 'INTERVAL', 'OBSERVATION_ID', 'PARAMERR', 'SCAN_NUMBER', 'SNR', 'SPECTRAL_WINDOW_ID', 'TIME', 'WEIGHT'],
                                          dtype='|S19'),
               'NAME': 'MSMTAB',
               'SEQNR': 0,
               'SPEC': {'BUCKETSIZE': 2560, 'IndexLength': 126, 'MaxCacheSize': 2, 'PERSCACHESIZE': 2},
               'TYPE': 'StandardStMan'}}

        self.columnnames=["TIME","FIELD_ID","SPECTRAL_WINDOW_ID","ANTENNA1","ANTENNA2","INTERVAL","SCAN_NUMBER","OBSERVATION_ID","CPARAM","PARAMERR","FLAG","SNR","WEIGHT"]
        self.datatypes=["D","I","I","I","I","D","I","I","X[]","R[]","B[]","R[]","R[]"]


class SpecWinTable:
    def __init__(self):
        self.desc = {
        'REF_FREQUENCY': {'comment': 'The reference frequency', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                          'keywords': {'QuantumUnits': np.array(['Hz'], dtype='|S3'),
                                       'MEASINFO': {'TabRefTypes': np.array(['REST', 'LSRK', 'LSRD', 'BARY', 'GEO', 'TOPO', 'GALACTO', 'LGROUP', 'CMB', 'Undefined'], dtype='|S10'),
                                       'type': 'frequency',
                                       'TabRefCodes': np.array([ 0,  1,  2,  3,  4,  5,  6,  7,  8, 64], dtype=np.uint32),
                                       'VarRefCol': 'MEAS_FREQ_REF'}},
                          'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'MEAS_FREQ_REF': {'comment': 'Frequency Measure reference', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'IF_CONV_CHAIN': {'comment': 'The IF conversion chain number', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'EFFECTIVE_BW': {'comment': 'Effective noise bandwidth of each channel', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                         'keywords': {'QuantumUnits': np.array(['Hz'], dtype='|S3')},
                         'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'FREQ_GROUP': {'comment': 'Frequency group', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'TOTAL_BANDWIDTH': {'comment': 'The total bandwidth for this window', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                            'keywords': {'QuantumUnits': np.array(['Hz'], dtype='|S3')},
                            'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'CHAN_WIDTH': {'comment': 'Channel width for each channel', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                       'keywords': {'QuantumUnits': np.array(['Hz'], dtype='|S3')},
                       'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'NUM_CHAN': {'comment': 'Number of spectral channels', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'CHAN_FREQ': {'comment': 'Center frequencies for each channel in the data matrix', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                      'keywords': {'QuantumUnits': np.array(['Hz'], dtype='|S3'),
                                   'MEASINFO': {'TabRefTypes': np.array(['REST', 'LSRK', 'LSRD', 'BARY', 'GEO', 'TOPO', 'GALACTO', 'LGROUP', 'CMB', 'Undefined'], dtype='|S10'),
                                   'type': 'frequency',
                                   'TabRefCodes': np.array([ 0,  1,  2,  3,  4,  5,  6,  7,  8, 64], dtype=np.uint32),
                                   'VarRefCol': 'MEAS_FREQ_REF'}},
                      'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'NAME': {'comment': 'Spectral window name', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'NET_SIDEBAND': {'comment': 'Net sideband', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'FREQ_GROUP_NAME': {'comment': 'Frequency group name', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'RESOLUTION': {'comment': 'The effective noise bandwidth for each channel', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                       'keywords': {'QuantumUnits': np.array(['Hz'], dtype='|S3')},
                       'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'FLAG_ROW': {'comment': 'Row flag', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'boolean'},
        '_define_hypercolumn_': {},
        '_keywords_': {},
        '_private_keywords_': {},
        }

        self.dminfo = {
                '*1': {'TYPE': 'StandardStMan', 'SEQNR': 0, 'NAME': 'MSMTAB',
                       'COLUMNS': np.array(['CHAN_FREQ', 'CHAN_WIDTH', 'EFFECTIVE_BW', 'FLAG_ROW', 'FREQ_GROUP', 'FREQ_GROUP_NAME', 'IF_CONV_CHAIN', 'MEAS_FREQ_REF', 'NAME', 'NET_SIDEBAND', 'NUM_CHAN', 'REF_FREQUENCY', 'RESOLUTION', 'TOTAL_BANDWIDTH'], dtype='|S16'),
                       'SPEC': {'MaxCacheSize': 2, 'PERSCACHESIZE': 2, 'IndexLength': 126, 'BUCKETSIZE': 2948}}}

        self.columnnames=["TIME","FIELD_ID","SPECTRAL_WINDOW_ID","ANTENNA1","ANTENNA2","INTERVAL","SCAN_NUMBER","OBSERVATION_ID","CPARAM","PARAMERR","FLAG","SNR","WEIGHT"]
        self.datatypes=["D","I","I","I","I","D","I","I","X[]","R[]","B[]","R[]","R[]"]

class ObsTable:
    def __init__(self):
        self.desc = {
        'TELESCOPE_NAME': {'comment': 'Telescope Name (e.g. WSRT, VLBA)', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'LOG': {'comment': 'Observing log', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'OBSERVER': {'comment': 'Name of observer(s)', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'SCHEDULE': {'comment': 'Observing schedule', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'RELEASE_DATE': {'comment': 'Release date when data becomes public', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                         'keywords': {'QuantumUnits': np.array(['s'], dtype='|S2'), 'MEASINFO': {'type': 'epoch', 'Ref': 'UTC'}},
                         'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'SCHEDULE_TYPE': {'comment': 'Observing schedule type', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'PROJECT': {'comment': 'Project identification string', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'TIME_RANGE': {'comment': 'Start and end of observation', 'ndim': 1, 'option': 5, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'shape': np.array([2], dtype=np.int32),
                       'keywords': {'QuantumUnits': np.array(['s'], dtype='|S2'), 'MEASINFO': {'type': 'epoch', 'Ref': 'UTC'}},
                       'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'FLAG_ROW': {'comment': 'Row flag', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'boolean'},
        '_keywords_': {},
        '_private_keywords_': {},
        '_define_hypercolumn_': {},
        }
        self.dminfo = {
                '*1': {'TYPE': 'StandardStMan', 'SEQNR': 0, 'NAME': 'MSMTAB',
                    'COLUMNS': np.array(['FLAG_ROW', 'LOG', 'OBSERVER', 'PROJECT', 'RELEASE_DATE', 'SCHEDULE', 'SCHEDULE_TYPE', 'TELESCOPE_NAME', 'TIME_RANGE'], dtype='|S15'),
                    'SPEC': {'MaxCacheSize': 2, 'PERSCACHESIZE': 2, 'IndexLength': 126, 'BUCKETSIZE': 3076}}}

class AntennaTable:
    def __init__(self):
        self.desc = {
        'NAME': {'comment': 'Antenna name, e.g. VLA22, CA03', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'MOUNT': {'comment': 'Mount type e.g. alt-az, equatorial, etc.', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'DISH_DIAMETER': {'comment': 'Physical diameter of dish', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                           'keywords': {'QuantumUnits': np.array(['m'], dtype='|S2')},
                           'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'STATION': {'comment': 'Station (antenna pad) name', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'OFFSET': {'comment': 'Axes offset of mount to FEED REFERENCE point', 'ndim': 1, 'option': 5, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'shape': np.array([3], dtype=np.int32),
                   'keywords': {'QuantumUnits': np.array(['m', 'm', 'm'], dtype='|S2'),
                                'MEASINFO': {'type': 'position', 'Ref': 'ITRF'}},
                   'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'POSITION': {'comment': 'Antenna X,Y,Z phase reference position', 'ndim': 1, 'option': 5, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'shape': np.array([3], dtype=np.int32),
                     'keywords': {'QuantumUnits': np.array(['m', 'm', 'm'], dtype='|S2'),
                                  'MEASINFO': {'type': 'position', 'Ref': 'ITRF'}},
                     'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'TYPE': {'comment': 'Antenna type (e.g. SPACE-BASED)', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'FLAG_ROW': {'comment': 'Flag for this row', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'boolean'},
        '_define_hypercolumn_': {},
        '_keywords_': {},
        '_private_keywords_': {},
        }
        self.dminfo = {
                '*1': {'TYPE': 'StandardStMan', 'SEQNR': 0, 'NAME': 'MSMTAB',
                       'COLUMNS': np.array(['DISH_DIAMETER', 'FLAG_ROW', 'MOUNT', 'NAME', 'OFFSET', 'POSITION', 'STATION', 'TYPE'], dtype='|S14'),
                       'SPEC': {'MaxCacheSize': 2, 'PERSCACHESIZE': 2, 'IndexLength': 126, 'BUCKETSIZE': 3332}}}


class FieldTable:
    def __init__(self):
        self.desc = {
        'REFERENCE_DIR': {'comment': 'Direction of REFERENCE center (e.g. RA, DEC).as polynomial in time.', 'ndim': 2, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                          'keywords': {'QuantumUnits': np.array(['rad', 'rad'], dtype='|S4'), 'MEASINFO': {'type': 'direction', 'Ref': 'J2000'}},
                          'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'CODE': {'comment': 'Special characteristics of field, e.g. Bandpass calibrator', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'NAME': {'comment': 'Name of this field', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'PHASE_DIR': {'comment': 'Direction of phase center (e.g. RA, DEC).', 'ndim': 2, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                      'keywords': {'QuantumUnits': np.array(['rad', 'rad'], dtype='|S4'), 'MEASINFO': {'type': 'direction', 'Ref': 'J2000'}},
                      'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'DELAY_DIR': {'comment': 'Direction of delay center (e.g. RA, DEC)as polynomial in time.', 'ndim': 2, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                      'keywords': {'QuantumUnits': np.array(['rad', 'rad'], dtype='|S4'), 'MEASINFO': {'type': 'direction', 'Ref': 'J2000'}},
                      'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'TIME': {'comment': 'Time origin for direction and rate', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                 'keywords': {'QuantumUnits': np.array(['s'], dtype='|S2'), 'MEASINFO': {'type': 'epoch', 'Ref': 'UTC'}},
                 'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'SOURCE_ID': {'comment': 'Source id', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'NUM_POLY': {'comment': 'Polynomial order of _DIR columns', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'FLAG_ROW': {'comment': 'Row Flag', 'option': 0, 'dataManagerGroup': 'MSMTA B', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'boolean'},
        '_private_keywords_': {},
        '_keywords_': {},
        '_define_hypercolumn_': {},
        }
        self.dminfo = {
            '*1': {'TYPE': 'StandardStMan', 'SEQNR': 0, 'NAME': 'MSMTAB',
                   'COLUMNS': np.array(['CODE', 'DELAY_DIR', 'FLAG_ROW', 'NAME', 'NUM_POLY', 'PHASE_DIR', 'REFERENCE_DIR', 'SOURCE_ID', 'TIME'], dtype='|S14'),
                   'SPEC': {'MaxCacheSize': 2, 'PERSCACHESIZE': 2, 'IndexLength': 126, 'BUCKETSIZE': 2052}}}

class HistoryTable:
    def __init__(self):
        self.desc = {
        'ORIGIN': {'comment': '(Source code) origin from which message originated', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'APP_PARAMS': {'comment': 'Application parameters', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'OBSERVATION_ID': {'comment': 'Observation id (index in OBSERVATION table)', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'TIME': {'comment': 'Timestamp of message', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0,
                 'keywords': {'QuantumUnits': np.array(['s'], dtype='|S2'), 'MEASINFO': {'type': 'epoch', 'Ref': 'UTC'}},
                 'dataManagerType': 'StandardStMan', 'valueType': 'double'},
        'OBJECT_ID': {'comment': 'Originating ObjectID', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'int'},
        'PRIORITY': {'comment': 'Message priority', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'APPLICATION': {'comment': 'Application name', 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'CLI_COMMAND': {'comment': 'CLI command sequence', 'ndim': 1, 'option': 0, 'dataManagerGroup': 'MSMTAB', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        'MESSAGE': {'comment': 'Log message', 'option': 0, 'dataManagerGroup': 'MSMTAB ', 'maxlen': 0, 'keywords': {}, 'dataManagerType': 'StandardStMan', 'valueType': 'string'},
        '_keywords_': {},
        '_private_keywords_': {},
        '_define_hypercolumn_': {}}
        self.dminfo = {
                '*1': {'TYPE': 'StandardStMan', 'SEQNR': 0, 'NAME': 'MSMTAB',
                       'COLUMNS': np.array(['APPLICATION', 'APP_PARAMS', 'CLI_COMMAND', 'MESSAGE', 'OBJECT_ID', 'OBSERVATION_ID', 'ORIGIN', 'PRIORITY', 'TIME'], dtype='|S15'),
                       'SPEC': {'MaxCacheSize': 2, 'PERSCACHESIZE': 2, 'IndexLength': 118, 'BUCKETSIZE': 2816}}}



type_mapping = {"D": np.float64,
                "I": np.int32,
                "R": np.float32,
                "B": bool,
                "X": np.complex128,
                }


ANTENNA.head
DISH_DIAMETER;FLAG_ROW;MOUNT;NAME;OFFSET;POSITION;STATION;TYPE
D;B;A;A;D[3];D[3];A;A
FIELD.head
CODE;DELAY_DIR;FLAG_ROW;NAME;NUM_POLY;PHASE_DIR;REFERENCE_DIR;SOURCE_ID;TIME
A;D[];B;A;I;D[];D[];I;D
HISTORY.head
APPLICATION;APP_PARAMS;CLI_COMMAND;MESSAGE;OBJECT_ID;OBSERVATION_ID;ORIGIN;PRIORITY;TIME
A;A[];A[];A;I;I;A;A;D
OBSERVATION.head
FLAG_ROW;LOG;OBSERVER;PROJECT;RELEASE_DATE;SCHEDULE;SCHEDULE_TYPE;TELESCOPE_NAME;TIME_RANGE
B;A[];A;A;D;A[];A;A;D[2]
SPECTRAL_WINDOW.head
CHAN_FREQ;CHAN_WIDTH;EFFECTIVE_BW;FLAG_ROW;FREQ_GROUP;FREQ_GROUP_NAME;IF_CONV_CHAIN;MEAS_FREQ_REF;NAME;NET_SIDEBAND;NUM_CHAN;REF_FREQUENCY;RESOLUTION;TOTAL_BANDWIDTH
D[];D[];D[];B;I;A;I;I;A;I;I;D;D[];D

def populate_table(btable, columnnames, datatypes, nchans, npol=2, nrows=1):
    tb.open(btable, nomodify=False)
    tb.addrows()
    for col, dtype in zip(columnnames, datatypes):
        print(col, dtype, tb.getcoldesc(columnname=col)['valueType'])
        if "[]" in dtype:
            print('varcol', dtype[:-2], type_mapping[dtype[:-2]])
            values = {'r1': np.full([npol, nchans, nrows], 0., dtype=type_mapping[dtype[:-2]])}
            print(values)
            tb.putvarcol(columnname=col, value=values)
            tb.flush()
        else:
            values = tb.getcol(col)
            print('scalar col', values, values.shape)
            values = np.full([nrows], 0, dtype=values.dtype)
            tb.putcol(columnname=col, value=values)
            tb.flush()
            print('scalar col', tb.getcol(col))
    tb.close()


if __name__ == '__main__':
    npol = 2
    nchans = 4096

    btable = "TEST_TEMP.B"
    abs_path = os.getcwd()
    tb.create(tablename=btable, tabledesc=MainTable(os.path.join(abs_path,btable)).desc, dminfo=MainTable().dminfo)
    populate_table(btable, MainTable().columnnames, MainTable().datatypes, nchans, npol=npol, nrows=1)

    tb.create(tablename=btable+"/ANTENNA", tabledesc=AntennaTable().desc, dminfo=AntennaTable().dminfo)
    tb.open(btable+"/ANTENNA", nomodify=False)
    tb.addrows()
    tb.close()
    tb.create(tablename=btable+"/FIELD", tabledesc=FieldTable().desc, dminfo=FieldTable().dminfo)
    tb.open(btable+"/FIELD", nomodify=False)
    tb.addrows()
    tb.close()
    tb.create(tablename=btable+"/HISTORY", tabledesc=HistoryTable().desc, dminfo=HistoryTable().dminfo)
    tb.open(btable+"/HISTORY", nomodify=False)
    tb.addrows()
    tb.close()
    tb.create(tablename=btable+"/OBSERVATION", tabledesc=ObsTable().desc, dminfo=ObsTable().dminfo)
    tb.open(btable+"/OBSERVATION", nomodify=False)
    tb.addrows()
    tb.close()
    tb.create(tablename=btable+"/SPECTRAL_WINDOW", tabledesc=SpecWinTable().desc, dminfo=SpecWinTable().dminfo)
    tb.open(btable+"/SPECTRAL_WINDOW", nomodify=False)
    tb.addrows()
    tb.close()


# -fin-
