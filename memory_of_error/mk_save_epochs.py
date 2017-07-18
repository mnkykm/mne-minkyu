# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas
import numpy as np

from mk_config import raw_folder, path_data, subjects, event_id_want
from mk_config import freq_low, freq_high, base_interval, tmin, tmax, decim

print("*** Save Epochs from the data in %s ***" % raw_folder)

for subject in subjects:
    path_subj = os.path.join(path_data, subject)
    bhv_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('.csv')]
    raw_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('.ds')]

    # There should be one and only .csv file in the directory.
    if len(bhv_list) == 1:
        bhv_df = pandas.read_csv(bhv_list.pop())
    elif len(bhv_list) == 0:
        raise Exception("No behavorial data (.csv) in %s!" % subject)
    else:
        raise Exception("Multiple data files (.csv) in %s!" % subject)

    # Create a list of raw data and concatenate them into full_raw
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

    # Filter the raw data
    # raw.notch_filter(freq_notch)  # if needed
    raw.filter(freq_low, freq_high, fir_design='firwin')

    # Epoch the raw data (configs are imported from mk_config.py)
    epochs = mne.Epochs(full_raw, events, event_id=event_id_want.keys(),
                       tmin=tmin, tmax=tmax, preload=True,
                       baseline=(tmin, tmin + base_interval), decim=decim)

    # Save the epochs into -epo.fif file
    epochs.pick_types(meg=True)
    epochs.save(os.path.join(path_data, subject, subject + '-epo.fif'))
