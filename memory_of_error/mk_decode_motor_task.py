# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time
import numpy as np

from mk_config import epo_path, res_path, decode_decim, topo_times, analyses, split_cond, decode_next
from mk_modules import get_dirs, initialize

print("*** Decode Motor Task from the epoched data in %s ***" % epo_path)
init_time = time.time()

input_path, output_path = epo_path, res_path
subjects = get_dirs(input_path)
initialize(subjects, input_path, output_path, input_type='epo', output_type='res')

for subject in subjects:
    input_path_subj = os.path.join(input_path, subject)
    output_path_subj = os.path.join(output_path, subject)

    bhv_list = get_dirs(input_path_subj, '.csv')
    bhv_file = bhv_list.pop()
    bhv_events = np.genfromtxt(bhv_file, dtype=float, delimiter=',', names=True)
    bhv_conds = np.genfromtxt(bhv_file, dtype=object, delimiter=',', names=True)['cond']

    epo_list = get_dirs(input_path_subj, 'epo.fif')
    epochs = mne.read_epochs(epo_list.pop())
    epochs.decimate(decim=decode_decim)
    epochs.pick_types(meg=True)

    # analyses = list(bhv_events.dtype.names)

    for analysis in analyses:
        print("** Decoding %s of %s **" % (analysis, subject))
        start_time = time.time()

        from mne.decoding import GeneralizingEstimator, cross_val_multiscore, LinearModel, get_coef
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import KFold
        from sklearn.linear_model import LogisticRegression, Ridge
        from sklearn.metrics import make_scorer
        from jr.gat import scorer_spearman

        if split_cond is False:
            cond_list = ['all']
        else:
            cond_list = [bhv_conds[0], bhv_conds[150]]

        for cond in cond_list:
            cv = KFold(5)
            scores, patterns, filters = [], [], []

            all_y = np.array(bhv_events[analysis])
            epochs_inst = epochs.copy()

            mask = np.isfinite(all_y)

            if np.sum(mask) < len(all_y) * 0.75:
                continue

            if cond is not 'all':
                mask1 = np.array(bhv_conds == cond)
                mask2 = np.array((([False] * 25) + ([True] * 100) + ([False] * 25)) * 2)
                mask = np.logical_and(mask, np.logical_and(mask1, mask2))

            if decode_next is False:
                y = all_y[np.where(mask)]
                X = epochs_inst.drop(np.invert(mask))._data
            else:
                y = all_y[:-1][np.where(mask[:-1])]
                X = epochs_inst.drop(0).drop(np.invert(mask[:-1]))._data

            if 'rot' in analysis:
                y[np.where((y == -40) | (y == +40))] = 1
                # LogisticRegression
                scaler, model = StandardScaler(), LinearModel(LogisticRegression())
                kwargs = dict(scoring='roc_auc', n_jobs=-1)
            elif 'targ' in analysis:
                # LogisticRegression
                scaler, model = StandardScaler(), LinearModel(LogisticRegression())
                kwargs = dict(scoring='roc_auc', n_jobs=-1)
            else:
                # Spearman Corr.
                scaler, model = StandardScaler(), LinearModel(Ridge())
                kwargs = dict(scoring=make_scorer(scorer_spearman), n_jobs=-1)

            clf = make_pipeline(scaler, model)
            gat = GeneralizingEstimator(clf, **kwargs)
            del scaler, model, kwargs

            for train, test in cv.split(X, y):
                gat.fit(X[train], y[train])
                scores.append(gat.score(X[test], y[test]))
                patterns.append(get_coef(gat, 'patterns_', inverse_transform=True))
                filters.append(get_coef(gat, 'filters_', inverse_transform=True))

            # Get scores, patterns, evoked, topomap
            scores, patterns, filters = map(lambda x: np.mean(x, axis=0), (scores, patterns, filters))
            evoked_p = mne.EvokedArray(patterns, epochs_inst.info, tmin=epochs_inst.tmin)
            evoked_f = mne.EvokedArray(filters, epochs_inst.info, tmin=epochs_inst.tmin)
            topomapp = evoked_p.plot_topomap(title='%s, %s, %s' % (subject, analysis, cond), show=False, times=topo_times)
            topomapf = evoked_f.plot_topomap(title='%s, %s, %s' % (subject, analysis, cond), show=False, times=topo_times)

            # Save scores, patterns, evoked, topomap

            fname_score = output_path_subj + '/scores_%s_%s_%s.npy' % (subject, analysis, cond)
            fname_pttrn = output_path_subj + '/patterns_%s_%s_%s.npy' % (subject, analysis, cond)
            fname_evokp = output_path_subj + '/evoked_patterns_%s_%s_%s-ave.fif' % (subject, analysis, cond)
            fname_evokf = output_path_subj + '/evoked_filters_%s_%s_%s-ave.fif' % (subject, analysis, cond)
            fname_topop = output_path_subj + '/topomap1_%s_%s_%s.jpg' % (subject, analysis, cond)
            fname_topof = output_path_subj + '/topomap2_%s_%s_%s.jpg' % (subject, analysis, cond)

            np.save(fname_score, scores)
            np.save(fname_pttrn, patterns)
            evoked_p.save(fname_evokp)
            evoked_f.save(fname_evokf)
            topomapp.savefig(fname_topop)
            topomapf.savefig(fname_topof)

            del y, X, clf, gat, cv, epochs_inst, mask, scores, patterns, evoked_p, evoked_f, topomapp, topomapf
            print("Done: %s of %s, %i seconds " % (analysis, subject, time.time() - start_time))

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
