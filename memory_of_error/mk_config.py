# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

raw_folder  = 'RAW_DATA'
resultsdir  = os.path.join(os.getcwd(), 'mk_results')
path_data   = os.path.join(os.getcwd(), raw_folder)
subjects    = [f for f in os.listdir(path_data) if not f.startswith('.')]

event_id_want = {2: 1, 3: 2}

# Epoch parameters
freq_notch = 60
freq_low  = 0.1
freq_high = 30

tmin = -0.2
tmax = 3.0

base_interval = 0.2
decim = 15

# Evoked plot parameters
evokplot_times = [0, 0.1, 0.3, 0.6, 0.9, 1.3, 1.5, 1.8, 2.5]

# Below are dump codes! Never mind!
