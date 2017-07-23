# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

# pathway information
raw_folder = 'mk_raw_epoch_decim15'
epo_folder = 'mk_raw_epoch_decim15'
res_folder = 'mk_results_epoch_decim15'
plt_folder = 'mk_plots_epoch_decim15'
cur_path = os.getcwd()
raw_path = os.path.join(cur_path, raw_folder)
epo_path = os.path.join(cur_path, epo_folder)
res_path = os.path.join(cur_path, res_folder)
plt_path = os.path.join(cur_path, plt_folder)

# List of analysis
analyses = ['rot', 'targ', 'cond', 'iMoveOn',
            'falsestart', 'Vp', 'iVp', 'Vmd', 'tVp', 'tVp_rel',
            'Vinit100', 'Vinit200', 'pathlength',
            'MT', 'RT', 'NJ', 'RMSE', 'RMSE_proj',
            'sec_submv_N', 'sec_submv_N_Vmin', 'sec_submv_N_ddir',
            'iSubMoveOn', 'iSMO_Vmin', 'iSMO_Ddir',
            'prime_disp', 'sec_disp', 'prime_dist', 'sec_dist', 'p2s_dist_ratio',
            'prime_MT', 'sec_MT', 'p2s_MT_ratio', 'prime_Vmd', 'sec_Vmd', 'prime_DEmd', 'sec_DEmd',
            'IDE100', 'IDB100', 'IDE200', 'IDB200',
            'VpDE', 'VpDB', 'IDEdist', 'IDBdist', 'IDE100signed', 'IDB100signed',
            'VpDEsigned', 'VpDBsigned', 'IDEdist_signed', 'IDBdist_signed', 'IDE200signed', 'IDB200signed']

# Event id's we want to see
event_list = [2, 3]
targ_list  = [1, 2]
event_id_want = dict(zip(event_list, targ_list))

# Epoch parameters
freq_notch = 60
freq_low   = 0.1
freq_high  = 30
tmin = -0.2
tmax = 3.0
base_interval = 0.2
decim = 15
