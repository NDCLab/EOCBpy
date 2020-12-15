#!/bin/env python

"""eocb-bidsify

Usage:
    eocb-bisify <input_path> <output_path> <metadata_filename>
"""

import os
import sys
import glob
from os import path as pt
from glob import glob
from docopt import docopt
from pprint import pprint as p

import yaml

import mne
from mne_bids import BIDSPath, write_raw_bids

from bids_validator import BIDSValidator


def main(args):
    input_path = args["<input_path>"]
    output_path = args["<output_path>"]
    metadata_path = args["<metadata_filename>"]

    # get list of all eeglab or brainvision files
    subjects = get_subjects(input_path)
    # import data using list of .set files
    subject_data = import_data(subjects, metadata_path)

    # write to bids dir
    for (i, data) in enumerate(subject_data):
        bids_path = BIDSPath(subject=str(i), datatype='eeg', root=output_path)
        write_raw_bids(data, bids_path=bids_path)

    # verify new bids dir
    if not bids_compliant:
        print("Not BIDS Compliant")
        exit(1)

    # temporary trace
    print("Succeeded")
    exit(0)


def get_subjects(path):
    paths = []

    if eeg_paths := glob(pt.join(path, "./*/*.vhdr")):
        paths = eeg_paths

    if set_paths := glob(pt.join(path, "./*/*.set")):
        if paths:  # Found both brainvision and eeglab
            # prefer one over the other
            print("Found both Brainvision and EEGLab datasets \
                    for the same subject")

        paths = set_paths

    return paths


def import_data(subjects, metadata_path):
    sd = []

    for path in subjects:
        path = pt.normpath(path)
        base_path = pt.dirname(path)
        ext = pt.splitext(path)[1]

        # Import data based on extension
        if ext == ".vhdr":
            data = mne.io.read_raw_brainvision(path)
        elif ext == ".set":
            data = mne.io.read_raw_eeglab(path)

        # Get metadata
        metadata = load_metadata_file(pt.join(base_path, metadata_path))

        # Update metadata
        for k in metadata.keys():
            data.info[k] = metadata[k]

        sd.append(data)

    return sd


def bids_compliant(path):
    failed_validation = []
    for e in glob(pt.join(path, "**/*")):
        e = pt.relpath(e, path)

        if not BIDSValidator().is_bids(e):
            failed_validation.append(e)

    if len(failed_validation) > 0:
        print("Some files do not match the BIDS specification")
        p(failed_validation)
        return False

    return True


def load_metadata_file(path):
    mdata = None
    with open(path, "r") as f:
        try:
            mdata = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)

    return mdata


if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
