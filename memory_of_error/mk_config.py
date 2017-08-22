# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

# shift event time?
shift_onset = False

# shift event time to target contact?
contact_onset = True

# split by cond?
split_cond = False

# split by targ?
split_targ = True

# decode next trial?
decode_next = False

# Filter parameters
filter_low_freq = 0.1
filter_high_freq = 30
if_notch = False
filter_notch_freq = 60

# Epoch parameters
tmin = -3
tmax = 3.0
base_interval = 0.2
epoch_decim = 1
decode_decim = 5

# pathway information
raw_folder = 'mk_RAW'
epo_folder = 'mk_epoched_nodecim'
res_folder = 'mk_results_5decim'
plt_folder = 'mk_plots_5decim'
bhv_folder = 'mk_bhv'

if shift_onset:
    epo_folder += '_SHIFT'
    res_folder += '_SHIFT'
    plt_folder += '_SHIFT'

if contact_onset:
    epo_folder += '_CONTACT'
    res_folder += '_CONTACT'
    plt_folder += '_CONTACT'

if split_cond:
    res_folder += '_SPLITc'
    plt_folder += '_SPLITc'

if split_targ:
    res_folder += '_SPLITt'
    plt_folder += '_SPLITt'

cur_path = os.getcwd()
raw_path = os.path.join(cur_path, raw_folder)
epo_path = os.path.join(cur_path, epo_folder)
res_path = os.path.join(cur_path, res_folder)
plt_path = os.path.join(cur_path, plt_folder)
bhv_path = os.path.join(cur_path, bhv_folder)

# List of analysis
# analyses = ['targ', 'RMSE', 'IDE100signed', 'VpDEsigned', 'IDEdist_signed', 'IDE200signed']
analyses = ['rot', 'RMSE', 'IDE100', 'IDE100signed', 'IDE200', 'IDE200signed']
if split_targ and ('targ' in analyses): analyses.remove('targ')

# Event id's we want to see
event_list = [2, 3]     # numbers in MEG data
targ_list  = [1, 2]     # numbers in behavorial data
event_id_want = dict(zip(event_list, targ_list))

# plot parameters
topo_times = [0, 0.1, 0.3, 0.6, 0.9, 1.3, 1.5, 1.8, 2.5]

# Epoch parameters
filter_params = dict(
    l_freq=filter_low_freq,
    h_freq=filter_high_freq,
    fir_design='firwin'
)
Epochs_params = dict(
    tmin = tmin,
    tmax = tmax,
    baseline = (tmin, tmin+base_interval),
    decim = epoch_decim
)
