# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

# decode next trial?
decode_next = False

# shift event time?
shift_onset = True

# split by cond?
split_cond = False

# pathway information
raw_folder = 'mk_RAW'
epo_folder = 'mk_epoched_nodecim'
res_folder = 'mk_results_15decim_next'
plt_folder = 'mk_plots_15decim_next'
bhv_folder = 'mk_bhv'

if shift_onset:
    epo_folder += '_SHIFT'
    res_folder += '_SHIFT'
    plt_folder += '_SHIFT'
else:
    pass

if split_cond:
    res_folder += '_SPLIT'
    plt_folder += '_SPLIT'
else:
    pass

cur_path = os.getcwd()
raw_path = os.path.join(cur_path, raw_folder)
epo_path = os.path.join(cur_path, epo_folder)
res_path = os.path.join(cur_path, res_folder)
plt_path = os.path.join(cur_path, plt_folder)
bhv_path = os.path.join(cur_path, bhv_folder)

# List of analysis
analyses = ['targ', 'RMSE', 'IDE100signed', 'VpDEsigned', 'IDEdist_signed', 'IDE200signed']

# Event id's we want to see
event_list = [2, 3]
targ_list  = [1, 2]
event_id_want = dict(zip(event_list, targ_list))

topo_times = [0, 0.1, 0.3, 0.6, 0.9, 1.3, 1.5, 1.8, 2.5]

# Epoch parameters
filter_params = dict(
    l_freq=0.1,
    h_freq=30,
    fir_design='firwin'
)

Epochs_params = dict(
    tmin = -0.2,
    tmax = 3.0,
    base_interval = 0.2,
    decim = 1
)
decode_decim = 15
