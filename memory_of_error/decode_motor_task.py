import os
import os.path as op
import scipy.io as sio
import numpy as np
from base import ScoringAUC
import mne
from mne.io import read_raw_ctf
from mne import Epochs
from mne.decoding import GeneralizingEstimator, cross_val_multiscore, LinearModel, get_coef
from sklearn.pipeline import make_pipeline
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import make_scorer
import pandas
from pandas import DataFrame as df
from jr.gat import (AngularRegression, scorer_spearman,
                    scorer_angle)
import matplotlib.pyplot as plt
from mne import EvokedArray

path_data = '/Users/minkyu/AnacondaProjects/nih_summer/memory_of_error/minkyu/'
subjects = ['sub01', 'sub02']
analyses = ['rotation', 'target', 'IDEat100ms', 'IDEat200ms',
            'IDEatVp', 'MoveDir100ms']
analyses = ['target', 'IDEat100ms', 'MoveDir100ms', 'err_sens']
for subject in subjects:
    epochs = mne.read_epochs(op.join(path_data, subject, 'epochs.fif'))
    epochs.pick_types(meg=True)
    epochs.plot()

    fname_behavior = op.join(path_data, subject, subject + '.csv')
    events = np.genfromtxt(fname_behavior, dtype=float,
                           delimiter=',', names=True)
    labels = ('rotation', 'target', 'IDEat100ms', 'IDEat200ms',
              'IDEatVp', 'MoveDir100ms')
    event_data = list()
    for event in events:
        event_dict = {key: value for (key, value) in zip(event, labels)}
        event_data.append(event_dict)
    events_behavior = df(events)

    for analysis in analyses:
        results_folder = op.join(path_data + 'results/' + subject)
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)
        fname_score = results_folder +\
            '/scores_%s_%s.npy' % (subject, analysis)
        fname_pattern = results_folder +\
            '/patterns_%s_%s.npy' % (subject, analysis)

        if 'rotation' in analysis:
            y = np.array(events[analysis])
            a = np.where((y == -40) | (y == +40))
            y[a] = 1
            # ------------- LogisticRegression --------------------
            clf = make_pipeline(StandardScaler(),
                                LinearModel(LogisticRegression()))
            kwargs = dict()
            gat = GeneralizingEstimator(clf, scoring='roc_auc',
                                        n_jobs=-1, **kwargs)
        elif 'target' in analysis:
            y = np.array(events[analysis])
            # ------------- LogisticRegression --------------------
            clf = make_pipeline(StandardScaler(),
                                LinearModel(LogisticRegression()))
            kwargs = dict()
            gat = GeneralizingEstimator(clf, scoring='roc_auc',
                                        n_jobs=-1, **kwargs)
        elif 'err_sens' in analysis:
            mov_eth = np.array(events['MoveDir100ms'])
            err = np.array(events['IDEat100ms'])
            ch_mov_eth = np.array([y - x for x, y in zip(mov_eth, mov_eth[1:])])
            err_sens_eth = ch_mov_eth/err[:299]
            err_sens_eth = np.insert(err_sens_eth, 0, 0)
            y = err_sens_eth
            #  ------------ Spearman corr ----------------
            clf = make_pipeline(StandardScaler(),
                                LinearModel(Ridge()))
            scorer = scorer_spearman
            kwargs = dict()
            gat = GeneralizingEstimator(clf, scoring=make_scorer(scorer),
                                        n_jobs=-1, **kwargs)
        else:
            y = np.array(events[analysis])
            #  ------------ Spearman corr ----------------
            clf = make_pipeline(StandardScaler(),
                                LinearModel(Ridge()))
            scorer = scorer_spearman
            kwargs = dict()
            gat = GeneralizingEstimator(clf, scoring=make_scorer(scorer),
                                        n_jobs=-1, **kwargs)

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
        np.save(fname_pattern, np.array(patterns))
        evoked = EvokedArray(patterns, epochs.info, tmin=epochs.tmin)
        evoked.plot_topomap(title='XXX', times=[0, 0.1, 0.3, 0.6, 0.9, 1.3, 1.5, 1.8, 2.5])

        # gat.fit(epochs._data, y)
        # scores = cross_val_multiscore(gat, epochs._data,
        #                               y, cv=5)
        # scores = scores.mean(axis=0)
        # np.save(fname, np.array(scores))
# ------------- Angular reg ----------------
# clf = AngularRegression(make_pipeline(StandardScaler(),
#                                       LinearModel(Ridge())),
#                         independent=False)
# scorer = scorer_angle
# kwargs = dict()
# gat = GeneralizingEstimator(clf, scoring=make_scorer(scorer),
#                             n_jobs=1, **kwargs)

# Plot coef
