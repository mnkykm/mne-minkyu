# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time
import numpy as np

from mk_config import epo_path, res_path
from mk_modules import get_subjects, initialize

print("*** Decode Motor Task from the epoched data in %s ***" % epo_path)
init_time = time.time()

input_path, output_path = epo_path, res_path
subjects = get_subjects(input_path)
initialize(subjects, input_path, output_path, input_type='epo', output_type='res')

for subject in subjects:
    path_subj = os.path.join(input_path, subject)

    bhv_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('.csv')]
    bhv_events = np.genfromtxt(bhv_list.pop(), dtype=float, delimiter=',', names=True)

    epo_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('epo.fif')]
    epochs = mne.read_epochs(epo_list.pop())
    # epochs.decimate(decim=15)
    epochs.pick_types(meg=True)

    analyses = list(bhv_events.dtype.names)

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

        cv, scores, patterns = KFold(5), [], []

        y = np.array(bhv_events[analysis])
        mask = np.isfinite(y)
        y = y[np.where(mask)]

        epochs_instance = epochs.copy().drop(np.invert(mask))
        X = epochs_instance._data

        if np.sum(mask) < len(y) * 0.75:
            continue
        elif 'rot' in analysis:
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

        # Get scores, patterns, evoked, topomap
        scores   = np.mean(scores, axis=0)
        patterns = np.mean(patterns, axis=0)
        evoked   = mne.EvokedArray(patterns, epochs_instance.info, tmin=epochs_instance.tmin)
        topomap  = evoked.plot_topomap(title='%s, %s' % (subject, analysis), show=False,
                                       times=[0, 0.1, 0.3, 0.6, 0.9, 1.3, 1.5, 1.8, 2.5])

        # Save scores, patterns, evoked, topomap
        output_path_subj = os.path.join(output_path, subject)
        fname_score = output_path_subj + '/scores_%s_%s.npy' % (subject, analysis)
        fname_pttrn = output_path_subj + '/patterns_%s_%s.npy' % (subject, analysis)
        fname_evokd = output_path_subj + '/evoked_%s_%s-ave.fif' % (subject, analysis)
        fname_image = output_path_subj + '/topomap_%s_%s.jpg' % (subject, analysis)

        np.save(fname_score, scores)
        np.save(fname_pttrn, patterns)
        evoked.save(fname_evokd)
        topomap.savefig(fname_image)

        del y, X, clf, gat, cv, epochs_instance, mask, scores, patterns, evoked, topomap
        print("Done: %s of %s, %i seconds " % (analysis, subject, time.time() - start_time))

print("Total %i seconds." % (time.time() - init_time))
