# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time
import numpy as np

from mk_config import (epo_path, res_path, decode_decim, topo_times,
                       analyses, split_cond, decode_next)
from mk_modules import get_dirs, initialize

# Start process
print("*** Decode Motor Task from the epoched data in %s ***" % epo_path)
init_time = time.time()

# Get pathway information and list of subjects and create result directories
input_path, output_path = epo_path, res_path + "_SPoC"
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

        from mne.decoding import CSP, SPoC, cross_val_multiscore
        from sklearn.pipeline import make_pipeline
        from sklearn.model_selection import KFold
        from sklearn.linear_model import LogisticRegression, Ridge
        from sklearn.metrics import make_scorer
        from sklearn.preprocessing import LabelEncoder
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
                continue
            elif 'targ' in analysis:
                # LogisticRegression
                scaler, model = CSP(n_components=10, reg='oas', log=True), LogisticRegression(C=1)
                kwargs = dict(scoring='roc_auc', n_jobs=-1)
                y = LabelEncoder().fit_transform(y)
            else:
                # Spearman Corr.
                scaler, model = SPoC(10), Ridge(alpha=1)
                kwargs = dict(scoring=make_scorer(scorer_spearman), n_jobs=-1)

            # Do machine learning, get scores
            clf = make_pipeline(scaler, model)
            score = cross_val_multiscore(estimator=clf, X=X, y=y, cv=5, **kwargs)
            scores.append(score.mean())

            # Save scores
            scores = np.mean(scores, axis=0)
            fname_score = output_path_subj + '/scores_%s_%s_%s.npy' % (subject, analysis, cond)
            np.save(fname_score, scores)

            del y, X, clf, cv, epochs_inst, mask, scores
            print("Done: %s of %s, %i seconds " % (analysis, subject, time.time() - start_time))

print("Total %i seconds." % (time.time() - init_time))

# ??
# def _rolling_decoder(clf, epochs, y, scoring):
#     """Roll a decoder over a window of time and return a cross val score"""
#     # Prepare rolling windows
#     window_spacing = .050
#     n_cycles = 4.
#     centered_w_times = np.arange(-.200, 1.2, window_spacing)[1:]
#
#     # Infer window spacing from the max freq and number of cycles to avoid gaps
#     tmin, tmax = epochs.times[[0, -1]]
#     w_size = n_cycles / ((fmax + fmin) / 2.)  # in seconds
#
#     # Roll covariance, csp and lda over time
#     scores = list()
#     for w_time in centered_w_times:
#         w_tmin = np.where(epochs.times > (w_time - w_size / 2.))[0]
#         w_tmax = np.where(epochs.times > (w_time + w_size / 2.))[0]
#         if len(w_tmax) == 0:
#             continue
#
#         X = epochs._data[..., w_tmin[0]:w_tmax[0]]
#
#         # Save mean scores over folds for each frequency and time window
#         score = cross_val_multiscore(estimator=clf, X=X, y=y,
#                                      cv=5, n_jobs=-1, scoring=scoring)
#         scores.append(score.mean())
#     return np.array(scores)
