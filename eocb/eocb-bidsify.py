#!/bin/env python

"""eocb-bidsify

Usage:
    eocb-bisify <input_path> <output_path>

"""

import os
import sys
import glob
from os import path as pt
from glob import glob
from docopt import docopt
from pprint import pprint

import mne
from mne_bids import BIDSPath, write_raw_bids

from bids_validator import BIDSValidator

def main(args):
    input_path = args["<input_path>"]
    output_path = args["<output_path>"]

    # get list of all eeglab or brainvision files
    subjects = get_subjects(input_path)
    # import subjects using list of .set files
    subj_data = get_subject_data(subjects)
    for path in subjects:
        subj_data.append(get_subject_data(path))
    pprint(subj_data)
    exit()
    # write to raw bids dir
    # for data in subj_data:
        # bids_path = BIDSPath(subject=data[0], session='01', run='05', datatype='eeg',
                # bids_root=output_path)
        # write_raw_bids(data[1], bids_path=bids_path)
    # verify new bids dir
    if not BIDSValidator().is_bids(output_path):
        # temporary trace
        print("failed")
        exit(1)

    # temporary trace
    print("succeeded")
    exit(0)

def get_subjects(path):
    paths = []

    if eeg_paths := glob(pt.join(path, "./*/*.eeg")):
        paths = eeg_paths

    if set_paths := glob(pt.join(path, "./*/*.set")):
        if paths: # Found both brainvision and eeglab
            # prefer one over the other
            print("Found both Brainvision and EEGLab datasets for the same subject")

        paths = set_paths

    return paths

def get_subject_data(path):
    pass

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
