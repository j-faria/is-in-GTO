import os
import pickle
import warnings
import numpy as np
_c = np.char
from astroquery.simbad import Simbad
Simbad.add_votable_fields('ids')


def get_GTO_targets():
    directory = os.path.dirname(os.path.abspath(__file__))
    file = 'P102_ESPRESSO-consortium_revised.csv'
    file = os.path.join(directory, file)
    GTOtargets = np.loadtxt(file, delimiter=',', usecols=(0, ), skiprows=5,
                            dtype=str)
    GTOtargets = _c.replace(GTOtargets, "_", "")
    # "special"
    GTOtargets = _c.replace(GTOtargets, "ProximaCen", "Proxima")
    GTOtargets = _c.replace(GTOtargets, "tauBoo", "tau Boo")
    return GTOtargets

def get_all_IDs(targets):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = Simbad.query_objects(targets)
    IDs = np.array(out['IDS']).astype(str)
    IDs = _c.replace(IDs, ' ', '')
    return IDs


def get_IDs():
    directory = os.path.dirname(os.path.abspath(__file__))
    picklefile = os.path.join(directory, 'IDs.pickle')
    if os.path.exists(picklefile):
        IDs = pickle.load(open(picklefile, 'rb'))
    else:
        print('querying Simbad, will take a bit of time...')
        GTOtargets = get_GTO_targets()
        IDs = get_all_IDs(GTOtargets)
        pickle.dump(IDs, open(picklefile, 'wb'), protocol=-1)
    return IDs


def is_in_GTO(targets, numpy=False):
    """ 
    Check if `targets` are in the ESPRESSO GTO list 

    Parameters
    ----------
    targets : str, iterable 
        Name(s) of the targets to check. If a string, should be a 
        comma-separated list of targets. If array-like (iterable), should be a 
        list of strings.
    numpy : bool, optional
        If True, return a numpy array, else a list. Default: False
    """

    IDs = get_IDs()
    if isinstance(targets, str):
        targets = targets.split(',')

    found = []
    for target in targets:
        index = None
        for i, ID in enumerate(IDs):
            if target in ID:
                index = i

        found.append(index is not None)

    if numpy:
        return np.array(found)
    else:
        return found