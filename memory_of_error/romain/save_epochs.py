import os
import os.path as op
import numpy as np
import mne
from mne.io import read_raw_ctf
from mne import Epochs
from pandas import DataFrame as df
from Levenshtein import editops
import warnings

def int_to_unicode(array):
    return ''.join([str(chr(int(ii))) for ii in array])

path_data = op.join(os.getcwd(),'RAW_DATA')
subjects = [f for f in os.listdir(path_data) if not f.startswith('.')]

# Read behavioral data
for subject in subjects:
    fname_behavior = op.join(path_data, subject, subject + '.csv')
    events = np.genfromtxt(fname_behavior, dtype=float,
                           delimiter=',', names=True)
    labels = ('rotation', 'target', 'IDEat100ms', 'IDEat200ms', 'IDEatVp')
    event_data = list()
    for event in events:
        event_dict = {key: value for (key, value) in zip(event, labels)}
        event_data.append(event_dict)
    events_behavior = df(events)

    # Read raw to extract MEG event triggers
    run = list()
    files = os.listdir(op.join(path_data, subject))
    run.extend(([op.join(
                path_data, subject + '/') + f for f in files if '.ds' in f]))
    fname_raw = op.join(path_data, run[0])
    print(fname_raw)
    # get raw and events from raw file
    raw = read_raw_ctf(fname_raw, preload=True, system_clock='ignore')
    events = mne.find_events(raw)


    # Compare events_behavior and events
    target_meg = (events[np.where
                         ((events[:, 2] == 2) | (events[:, 2] == 3))][:, 2]) - 1
    target_bhv = np.array(events_behavior)[:, 1]
    changes = editops(int_to_unicode(target_meg),
                      int_to_unicode(target_bhv))
    if len(changes) != 0:
        warnings.warn('events in .cvs and events in meg trigger are different')

    raw.filter(0.1, 30)

    event_id = [2, 3]
    tmin = -0.2
    tmax = 3

    epochs = Epochs(raw, events, event_id=event_id,
                    tmin=tmin, tmax=tmax, preload=True,
                    baseline=(tmin, tmin+0.2), decim=15)
    epochs.pick_types(meg=True)
    epochs.save(op.join(path_data, subject, subject+'-epo.fif'))
