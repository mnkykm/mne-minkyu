# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time
import numpy as np

from mk_config import (shift, raw_path, epo_path, event_id_want,
                       freq_low, freq_high, base_interval, tmin, tmax, decim)
from mk_modules import get_subjects, initialize

print("*** Save Epochs from the data in %s ***" % raw_path)
init_time = time.time()

input_path, output_path = raw_path, epo_path
subjects = get_subjects(input_path)
initialize(subjects, input_path, output_path, input_type='raw', output_type='epo')

for subject in subjects:
    path_subj = os.path.join(raw_path, subject)
    bhv_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('.csv')]
    bhv_df = np.genfromtxt(bhv_list.pop(), dtype=float, delimiter=',', names=True)

    # Create a list of raw data and concatenate them into full_raw
    raw_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('.ds')]
    all_raws = list()
    for raw_file in raw_list:
        this_raw = mne.io.read_raw_ctf(raw_file, preload=True, system_clock='ignore')
        all_raws.append(this_raw)
    full_raw = mne.concatenate_raws(all_raws)

    # Find events from full raw data
    events = mne.find_events(full_raw)

    # Compare the target sequence from bhv data with the triggers in MEG data
    target_bhv = np.array(bhv_df)[:, 1]
    target_meg = events[np.where(np.in1d(events[:, 2], event_id_want.keys()))][:, 2]
                                # use np.isin instead of np.in1d if numpy >= 1.13.0
    if np.array_equal(map(lambda x: event_id_want[x],target_meg), target_bhv) is False:
        raise Exception('The events in behavorial data (.csv) and the events in MEG trigger are NOT consistent!')

    if shift:
        corrected_events = np.array(filter(lambda x: x[2] in event_id_want.keys(), events))
        corrected_events[:, 0] += (np.array(bhv_df['RT']) * 600).astype(int)
        events = corrected_events
    else:
        pass

    # Filter the raw data
    # raw.notch_filter(freq_notch)  # if needed
    full_raw.filter(l_freq=freq_low, h_freq=freq_high, fir_design='firwin',)

    # Epoch the raw data (configs are imported from mk_config.py)
    epochs = mne.Epochs(full_raw, events, event_id=event_id_want.keys(),
                       tmin=tmin, tmax=tmax, preload=True,
                       baseline=(tmin, tmin + base_interval))

    # Save the epochs into -epo.fif file
    epochs.save(os.path.join(output_path, subject, subject + '-epo.fif'))

print("Total %i seconds." % (time.time() - init_time))
