# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time, sys, warnings
import numpy as np

from mk_config import (epo_path, res_path, decode_decim, topo_times,
                       analyses, split_cond, split_targ, decode_next)
from mk_modules import get_dirs, initialize

# !!!!!!!!!!!!!!
split_targ = True

# Start process
print("*** Decode Motor Task from the epoched data in %s ***" % epo_path)
init_time = time.time()

# Get pathway information and list of subjects and create result directories
input_path, output_path = epo_path, res_path
subjects = get_dirs(input_path)
initialize(subjects, input_path, output_path, input_type='epo', output_type='res')

# subject = sys.argv[1]     # Use these lines when using swarm!
# if True:                  # Use these lines when using swarm!
for subject in subjects:    # Delete this line when using swarm!

    # Get pathway information for a specific subject
    input_path_subj = os.path.join(input_path, subject)
    output_path_subj = os.path.join(output_path, subject)

    # Get behavioral data. If successfully initialized, len(bhv_list) should be 1.
    bhv_list = get_dirs(input_path_subj, '.csv')
    bhv_file = bhv_list.pop()
    bhv_events = np.genfromtxt(bhv_file, dtype=float, delimiter=',', names=True)
    bhv_conds = np.genfromtxt(bhv_file, dtype=object, delimiter=',', names=True)['cond']
    bhv_targs = np.genfromtxt(bhv_file, dtype=object, delimiter=',', names=True)['targ']
    # Get the epoched data. If successfully initialized, len(epo_list) should be 1.
    epo_list = get_dirs(input_path_subj, 'epo.fif')
    epochs = mne.read_epochs(epo_list.pop())

    # Re-decimate and pick channels
    epochs.decimate(decim=decode_decim)
    epochs.pick_types(meg=True)

    # Get the names of variables
    # analyses = list(bhv_events.dtype.names)   # if you want to analyse all the variables

    for analysis in analyses:
        # Start decoding
        print("** Decoding %s of %s **" % (analysis, subject))
        start_time = time.time()

        from mne.decoding import GeneralizingEstimator, cross_val_multiscore, LinearModel, get_coef
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import KFold
        from sklearn.linear_model import LogisticRegression, Ridge
        from sklearn.metrics import make_scorer
        from jr.gat import scorer_spearman

        # If decoding for each condition
        if split_targ is False:
            targ_list = ['all']
        else:
            targ_list = ['1', '2']

        # If decoding for each condition
        if split_cond is False:
            cond_list = ['all']
        else:
            cond_list = [bhv_conds[0], bhv_conds[150]]

        for cond in cond_list:
            for targ in targ_list:
                # Make a pipeline
                cv = KFold(5, shuffle=True)
                scores, patterns, filters = [], [], []

                all_y = np.array(bhv_events[analysis])
                epochs_inst1 = epochs.copy()
                epochs_inst2 = epochs.copy()

                mask = np.isfinite(all_y)

                # Stop process if NaN values exceed 25% of the data
                if np.sum(mask) < len(all_y) * 0.75:
                    continue

                # Split conditions
                if cond is not 'all':
                    mask1 = np.array(bhv_conds == cond)
                    mask2 = np.array(([False] * 25 + [True] * 100 + [False] * 25) * 2)
                    mask = np.logical_and(mask, np.logical_and(mask1, mask2))

                mask_targ1 = np.logical_and(mask, np.array(bhv_targs == '1'))
                mask_targ2 = np.logical_and(mask, np.array(bhv_targs == '2'))

                # Decoding nth trial or (n+1)th trial for nth variable?
                if decode_next is True:
                    all_y.pop(-1)
                    mask.pop(-1)
                    epochs_inst1.drop(0)
                    epochs_inst2.drop(0)

                # Make X and y for machine learning
                y1 = all_y[np.where(mask_targ1)]
                X1 = epochs_inst1.drop(np.invert(mask_targ1))._data
                y2 = all_y[np.where(mask_targ2)]
                X2 = epochs_inst2.drop(np.invert(mask_targ2))._data

                #
                if len(set(y1)) == 1 or len(set(y2)) == 1:
                    continue

                # Select a model
                if 'rot' in analysis:
                    y1[np.where((y1 == -40) | (y1 == +40))] = 1
                    y2[np.where((y2 == -40) | (y2 == +40))] = 1
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

                # Use GeneralizingEstimator
                clf = make_pipeline(scaler, model)
                gat = GeneralizingEstimator(clf, **kwargs)
                del scaler, model, kwargs

                # Do machine learning, get scores
                for train, test in cv.split(X1, y1):
                    try:
                        gat.fit(X1[train], y1[train])
                        scores.append(gat.score(X2[test], y2[test]))
                    except:
                        warnings.warn("Oops! Try again.")
                        continue
                    patterns.append(get_coef(gat, 'patterns_', inverse_transform=True))
                    filters.append(get_coef(gat, 'filters_', inverse_transform=True))

                # Get the mean value of scores, patterns, evoked
                scores, patterns, filters = map(lambda x: np.mean(x, axis=0), (scores, patterns, filters))
                evoked_p = mne.EvokedArray(patterns, epochs_inst1.info, tmin=epochs_inst1.tmin)
                evoked_f = mne.EvokedArray(filters, epochs_inst1.info, tmin=epochs_inst1.tmin)

                # Make filenames of scores, patterns, evoked
                fname_score = output_path_subj + '/scores_%s_%s_%s_%s.npy' % (subject, analysis, cond, str(targ))
                fname_pttrn = output_path_subj + '/patterns_%s_%s_%s_%s.npy' % (subject, analysis, cond, str(targ))
                fname_evokp = output_path_subj + '/evoked_patterns_%s_%s_%s_%s-ave.fif' % (subject, analysis, cond, str(targ))
                fname_evokf = output_path_subj + '/evoked_filters_%s_%s_%s_%s-ave.fif' % (subject, analysis, cond, str(targ))

                # Save scores, patterns, evoked
                np.save(fname_score, scores)
                np.save(fname_pttrn, patterns)
                evoked_p.save(fname_evokp)
                evoked_f.save(fname_evokf)

                del y1, X1, y2, X2, clf, gat, cv, epochs_inst1, epochs_inst2, mask, scores, patterns, evoked_p, evoked_f
                print("Done: %s of %s, %i seconds " % (analysis, subject, time.time() - start_time))

print("Total %i seconds." % (time.time() - init_time))
