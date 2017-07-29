# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time
import numpy as np

from mk_config import (epo_path, res_path, topo_times, analyses, split_cond)
from mk_modules import get_dirs, initialize

# Start process
print("*** Decode Motor Task from the epoched data in %s ***" % epo_path)
init_time = time.time()

# Get pathway information and list of subjects and create result directories
input_path, output_path = epo_path, res_path
subjects = get_dirs(input_path)

# Do not use swarm!
for subject in subjects:
    # Get pathway information for a specific subject
    input_path_subj = os.path.join(input_path, subject)
    output_path_subj = os.path.join(output_path, subject)

    # Get the names of variables
    # analyses = list(bhv_events.dtype.names)   # if you want to analyse all the variables

    for analysis in analyses:
        # If decoding for each condition
        if split_cond is False:
            cond_list = ['all']
        else:
            cond_list = ['rand', 'const']

        for cond in cond_list:
            fname_evokp = output_path_subj + '/evoked_patterns_%s_%s_%s.npy' % (subject, analysis, cond)
            fname_evokf = output_path_subj + '/evoked_filters_%s_%s_%s.npy' % (subject, analysis, cond)
            evoked_p = mne.Evoked(fname_evokp)
            evoked_f = mne.Evoked(fname_evokf)

            topo_title = '%s, %s, %s' % (subject, analysis, cond)
            topo_p = evoked_p.plot_topomap(title=topo_title, show=False, times=topo_times)
            topo_f = evoked_f.plot_topomap(title=topo_title, show=False, times=topo_times)

            fname_topop = output_path_subj + '/patterns_%s_%s_%s.jpg' % (subject, analysis, cond)
            fname_topof = output_path_subj + '/filters_%s_%s_%s.jpg' % (subject, analysis, cond)
            topo_p.savefig(fname_topop)
            topo_f.savefig(fname_topof)

evp_dict, evf_dict = dict(), dict()
for subject in subjects:
    input_path_subj = os.path.join(output_path, subject)
    evk_list = get_dirs(input_path_subj, 'fif')
    for file in evk_list:
        filename = file.split('/')[-1].rstrip('-ave.fif')
        evok_type, analysis = filename.split('_')[1], filename.split('_')[3]

        if analysis not in evp_dict.keys():
            evp_dict[analysis] = list()
        if analysis not in evf_dict.keys():
            evf_dict[analysis] = list()

        if evok_type == 'patterns':
            evp_dict[analysis].append(file)
        elif evok_type == 'filters':
            evf_dict[analysis].append(file)

for analysis in evp_dict.keys():
    evp_files = evp_dict[analysis]
    evp_list = list()
    for file in evp_files:
        evoked_p = mne.Evoked(file)
        evp_list.append(evoked_p.data)
        evp_info = evoked_p.info
    evp_ave = mne.EvokedArray(np.mean(evp_list, axis=0), evp_info)
    evp_ave.save(os.path.join(output_path, '_average', 'evoked_patterns_%s-ave.fif' % (analysis)))
    topo_ave = evp_ave.plot_topomap(title='%s, n=%i' % (analysis, len(evp_list)), show=False, times=topo_times)
    topo_ave.savefig(os.path.join(output_path, '_average', 'patterns_%s.jpg' % (analysis)))

for analysis in evf_dict.keys():
    evf_files = evf_dict[analysis]
    evf_list = list()
    for file in evf_files:
        evoked_f = mne.Evoked(file)
        evf_list.append(evoked_f.data)
        evf_info = evoked_f.info
    evf_ave = mne.EvokedArray(np.mean(evf_list, axis=0), evf_info)
    evf_ave.save(os.path.join(output_path, '_average', 'evoked_patterns_%s-ave.fif' % (analysis)))
    topo_ave = evf_ave.plot_topomap(title='%s, n=%i' % (analysis, len(evf_list)), show=False, times=topo_times)
    topo_ave.savefig(os.path.join(output_path, '_average', 'filters_%s.jpg' % (analysis)))

print("Total %i seconds." % (time.time() - init_time))
