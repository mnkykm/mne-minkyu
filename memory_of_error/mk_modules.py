# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import numpy as np
from mk_plot_module import *

def get_dirs(input_path, suffix=None):
    if suffix is None:
        return [file for file in os.listdir(input_path)
                if not file.startswith('.') and not file.startswith('_')]
    else:
        return [os.path.join(input_path, file) for file in os.listdir(input_path)
                if not file.startswith('.') and not file.startswith('_') and file.endswith(suffix)]

def initialize(subjects, input_path, output_path, input_type='raw', output_type='epo'):
    if len(subjects) is 0:
        raise Exception("No subject directory in %s!" % input_path)

    for subject in subjects:
        path_subj = os.path.join(input_path, subject)

        if input_type is 'raw':
            raw_list = [os.path.join(path_subj, file) for file in get_dirs(path_subj)
                        if file.endswith('.ds')]
            # There should be at least one .ds file in the directory.
            if len(raw_list):
                pass
            else:
                raise Exception("No raw data (.ds) in %s!" % subject)

            bhv_list = [os.path.join(path_subj, file) for file in get_dirs(path_subj)
                        if file.endswith('.csv')]
            # There should be one and only .csv file in the directory.
            if len(bhv_list) is 1:
                pass
            elif len(bhv_list) is 0:
                raise Exception("No behavorial data (.csv) in %s!" % subject)
            else:
                raise Exception("Multiple data files (.csv) in %s!" % subject)

        elif input_type is 'epo':
            epo_list = [os.path.join(path_subj, file) for file in get_dirs(path_subj)
                        if file.endswith('epo.fif')]
            # There should be one and only -epo.fif file in the directory.
            if len(epo_list) is 1:
                pass
            elif len(epo_list) is 0:
                raise Exception("No epoched data (-epo.fif) in %s!" % subject)
            else:
                raise Exception("Multiple epoched files (-epo.fif) in %s!" % subject)

            bhv_list = [os.path.join(path_subj, file) for file in get_dirs(path_subj)
                        if file.endswith('.csv')]

            # There should be one and only .csv file in the directory.
            if len(bhv_list) is 1:
                pass
            elif len(bhv_list) is 0:
                raise Exception("No behavorial data (.csv) in %s!" % subject)
            else:
                raise Exception("Multiple data files (.csv) in %s!" % subject)

        elif input_type is 'res':
            npy_list = [os.path.join(path_subj, file) for file in get_dirs(path_subj)
                        if file.endswith('.npy')]
            # There should be at least one .npy file in the directory.
            if len(npy_list):
                pass
            else:
                raise RuntimeWarning("No decoding results (scores...npy) in %s!" % subject)

    # Create a directory for result files
    try:
        os.makedirs(output_path)
    except OSError:
        if not os.path.isdir(output_path): raise

    if output_type in ['epo', 'res']:
        for subject in subjects:
            try:
                os.makedirs(os.path.join(output_path, subject))
            except OSError:
                if not os.path.isdir(os.path.join(output_path, subject)): raise
        try:
            os.makedirs(os.path.join(output_path, '_average'))
        except OSError:
            if not os.path.isdir(os.path.join(output_path, '_average')): raise
    elif output_type is 'plt':
        pass
    else:
        pass

    return 0

def compare_events(events, bhv_df, event_id_want):
    target_bhv = np.array(bhv_df['targ'])
    target_meg = events[np.where(np.in1d(events[:, 2], event_id_want.keys()))][:, 2]
                                # use np.isin instead of np.in1d if numpy >= 1.13.0
    if np.array_equal(map(lambda x: event_id_want[x], target_meg), target_bhv) is False:
        raise Exception('The events in behavorial data (.csv) and the events in MEG trigger are NOT consistent!')
