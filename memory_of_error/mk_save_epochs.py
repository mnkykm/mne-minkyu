# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time, shutil
import numpy as np

from mk_config import (Epochs_params, filter_params, filter_notch_freq,
                       shift_onset, raw_path, epo_path, event_id_want)
from mk_modules import get_dirs, initialize, compare_events

# Start process
print("*** Save Epochs from the data in %s ***" % raw_path)
init_time = time.time()

# Get pathway information and list of subjects and create result directories
input_path, output_path = raw_path, epo_path
subjects = get_dirs(input_path)
initialize(subjects, input_path, output_path, input_type='raw', output_type='epo')

# subject = sys.argv[1]     # Use these lines when using swarm!
# if True:                  # Use these lines when using swarm!
for subject in subjects:    # Delete this line when using swarm!

    # Get pathway information for a specific subject
    input_path_subj = os.path.join(input_path, subject)
    output_path_subj = os.path.join(output_path, subject)

    # Get behavioral data. If successfully initialized, len(bhv_list) should be 1.
    bhv_list = get_dirs(input_path_subj, '.csv')
    bhv_file = bhv_list.pop()

    # Copy csv file to result folder and read
    shutil.copy2(bhv_file, output_path_subj)
    bhv_df = pandas.read_csv(bhv_file, delimiter=',')

    # Create a list of raw data and concatenate them into full_raw
    raw_list = [mne.io.read_raw_ctf(raw_file, preload=True, system_clock='ignore')
                for raw_file in get_dirs(input_path_subj, '.ds')]
    raw_full = mne.concatenate_raws(raw_list)

    # Find events from the raw data and compare with the behavioral data
    events = mne.find_events(raw_full)
    compare_events(events, bhv_df, event_id_want)

    # If shifting the onset to movement onset instead of target appearance:
    if shift_onset:
        events = np.array(filter(lambda x: x[2] in event_id_want.keys(), events))
        events[:, 0] += (np.array(bhv_df['RT']) * 600).astype(int)

    # Filter the raw data
    # raw.notch_filter(filter_notch_freq)   # if needed!
    raw_full.filter(**filter_params)

    # Epoch the raw data (configs are imported from mk_config.py)
    epochs = mne.Epochs(raw_full, events, event_id=event_id_want.keys(), **Epochs_params)

    # Save the epochs into -epo.fif file
    epochs.save(os.path.join(output_path_subj, subject + '-epo.fif'))

print("Total %i seconds." % (time.time() - init_time))
