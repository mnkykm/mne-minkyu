# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time, sys
import numpy as np

from mk_config import (epo_path, res_path, decode_decim, topo_times,
                       analyses, split_cond, decode_next)
from mk_modules import get_dirs, initialize

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
        if split_cond is False:
            cond_list = ['all']
        else:
            cond_list = [bhv_conds[0], bhv_conds[150]]

        for cond in cond_list:
            # Make a pipeline
            cv = KFold(5, shuffle=True)
            scores, patterns, filters = [], [], []

            all_y = np.array(bhv_events[analysis])
            epochs_inst = epochs.copy()

            mask = np.isfinite(all_y)

            # Stop process if NaN values exceed 25% of the data
            if np.sum(mask) < len(all_y) * 0.75:
                continue

            # Split conditions
            if cond is not 'all':
                mask1 = np.array(bhv_conds == cond)
                mask2 = np.array(([False] * 25 + [True] * 100 + [False] * 25) * 2)
                mask = np.logical_and(mask, np.logical_and(mask1, mask2))

            # Decoding nth trial or (n+1)th trial for nth variable?
            if decode_next is True:
                all_y.pop(-1)
                mask.pop(-1)
                epochs.inst.drop(0)

            # Make X and y for machine learning
            y = all_y[np.where(mask)]
            X = epochs_inst.drop(np.invert(mask))._data

            # Select a model
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

            # Use GeneralizingEstimator
            clf = make_pipeline(scaler, model)
            gat = GeneralizingEstimator(clf, **kwargs)
            del scaler, model, kwargs

            # Do machine learning, get scores
            for train, test in cv.split(X, y):
                gat.fit(X[train], y[train])
                scores.append(gat.score(X[test], y[test]))
                patterns.append(get_coef(gat, 'patterns_', inverse_transform=True))
                filters.append(get_coef(gat, 'filters_', inverse_transform=True))

            # Get the mean value of scores, patterns, evoked
            scores, patterns, filters = map(lambda x: np.mean(x, axis=0), (scores, patterns, filters))
            evoked_p = mne.EvokedArray(patterns, epochs_inst.info, tmin=epochs_inst.tmin)
            evoked_f = mne.EvokedArray(filters, epochs_inst.info, tmin=epochs_inst.tmin)

            # Make filenames of scores, patterns, evoked
            fname_score = output_path_subj + '/scores_%s_%s_%s.npy' % (subject, analysis, cond)
            fname_pttrn = output_path_subj + '/patterns_%s_%s_%s.npy' % (subject, analysis, cond)
            fname_evokp = output_path_subj + '/evoked_patterns_%s_%s_%s-ave.fif' % (subject, analysis, cond)
            fname_evokf = output_path_subj + '/evoked_filters_%s_%s_%s-ave.fif' % (subject, analysis, cond)

            # Save scores, patterns, evoked
            np.save(fname_score, scores)
            np.save(fname_pttrn, patterns)
            evoked_p.save(fname_evokp)
            evoked_f.save(fname_evokf)

            del y, X, clf, gat, cv, epochs_inst, mask, scores, patterns, evoked_p, evoked_f
            print("Done: %s of %s, %i seconds " % (analysis, subject, time.time() - start_time))

print("Total %i seconds." % (time.time() - init_time))
