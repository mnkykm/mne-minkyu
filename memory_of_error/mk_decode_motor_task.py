# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, sklearn
import numpy as np

from mne.decoding import GeneralizingEstimator, cross_val_multiscore, LinearModel, get_coef
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import make_scorer
from jr.gat import scorer_spearman

from mk_config import raw_folder, resultsdir, path_data, subjects
from mk_config import evokplot_times

print("*** Decode Motor Task from the epoched data in %s ***" % raw_folder)

# Create a directory for result files
for subject in subjects:
    try:
        os.makedirs(os.path.join(resultsdir, subject))
    except OSError:
        if not os.path.isdir(os.path.join(resultsdir, subject)): raise

for subject in subjects:
    path_subj = os.path.join(path_data, subject)
    bhv_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('.csv')]
    epo_list = [os.path.join(path_subj, file) for file in os.listdir(path_subj)
                if file.endswith('epo.fif')]

    # There should be one and only .csv file in the directory.
    if len(bhv_list) == 1:
        bhv_events = np.genfromtxt(bhv_list.pop(), dtype=float, delimiter=',', names=True)
    elif len(bhv_list) == 0:
        raise Exception("No behavorial data (.csv) in %s!" % subject)
    else:
        raise Exception("Multiple data files (.csv) in %s!" % subject)

    # There should be one and only epoch file in the directory.
    if len(epo_list) == 1:
        epochs = mne.read_epochs(epo_list.pop())
    elif len(epo_list) == 0:
        raise Exception("No epoched data (-epo.fif) in %s!" % subject)
    else:
        raise Exception("Multiple epoched files (-epo.fif) in %s!" % subject)

    epochs.pick_types(meg=True)
    # epochs.plot()

    analyses = list(bhv_events.dtype.names)
    print(analyses)
    for analysis in analyses:
        fname_score = os.path.join(resultsdir, subject) + '/scores_%s_%s.npy' % (subject, analysis)
        fname_pttrn = os.path.join(resultsdir, subject) + '/patterns_%s_%s.npy' % (subject, analysis)
        fname_evokd = os.path.join(resultsdir, subject) + '/evoked_%s_%s-ave.fif' % (subject, analysis)
        fname_image = os.path.join(resultsdir, subject) + '/topomap_%s_%s.jpg' % (subject, analysis)

        if np.all(np.isnan(np.array(bhv_events[analysis]))) is True:
            continue
        elif 'rot' in analysis:
            y = np.array(bhv_events[analysis])
            a = np.where((y == -40) | (y == +40))
            y[a] = 1
            # ------------- LogisticRegression --------------------
            clf = make_pipeline(StandardScaler(),
                                LinearModel(LogisticRegression()))
            kwargs = dict()
            gat = GeneralizingEstimator(clf, scoring='roc_auc',
                                        n_jobs=-1, **kwargs)
        elif 'targ' in analysis:
            y = np.array(bhv_events[analysis])
            # ------------- LogisticRegression --------------------
            clf = make_pipeline(StandardScaler(),
                                LinearModel(LogisticRegression()))
            kwargs = dict()
            gat = GeneralizingEstimator(clf, scoring='roc_auc',
                                        n_jobs=-1, **kwargs)
        else:
            continue
            # y = np.array(bhv_events[analysis])
            # #  ------------ Spearman corr ----------------
            # clf = make_pipeline(StandardScaler(),
            #                     LinearModel(Ridge()))
            # scorer = scorer_spearman
            # kwargs = dict()
            # gat = GeneralizingEstimator(clf, scoring=make_scorer(scorer),
            #                             n_jobs=-1, **kwargs)

        cv = KFold(5)
        scores = list()
        patterns = list()

        for train, test in cv.split(epochs._data, y):
            gat.fit(epochs._data[train], y[train])
            score = gat.score(epochs._data[test], y[test])
            scores.append(score)
            patterns.append(get_coef(gat, 'patterns_', inverse_transform=True))

        # scores = cross_val_multiscore(gat, epochs._data[sel], y=y[sel])
        scores = np.mean(scores, axis=0)
        patterns = np.mean(patterns, axis=0)
        np.save(fname_score, np.array(scores))
        np.save(fname_pttrn, np.array(patterns))

        evoked = mne.EvokedArray(patterns, epochs.info, tmin=epochs.tmin)
        evoked.save(fname_evokd)
        evoked.plot_topomap(title='%s, %s' % (subject, analysis), times=evokplot_times, show=False).savefig(fname_image)
