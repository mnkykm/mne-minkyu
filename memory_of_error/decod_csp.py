import os
import os.path as op
import scipy.io as sio
import numpy as np
# from base import ScoringAUC
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
from pandas import DataFrame as df
from jr.gat import (AngularRegression, scorer_spearman,
                    scorer_angle)
import matplotlib.pyplot as plt
from mne import EvokedArray
from mne.decoding import CSP, SPoC, cross_val_multiscore
from sklearn.preprocessing import LabelEncoder


def _rolling_decoder(clf, epochs, y, scoring):
    """Roll a decoder over a window of time and return a cross val score"""
    # Prepare rolling windows
    window_spacing = .050
    n_cycles = 4.
    centered_w_times = np.arange(-.200, 1.2, window_spacing)[1:]

    # Infer window spacing from the max freq and number of cycles to avoid gaps
    tmin, tmax = epochs.times[[0, -1]]
    w_size = n_cycles / ((fmax + fmin) / 2.)  # in seconds

    # Roll covariance, csp and lda over time
    scores = list()
    for w_time in centered_w_times:
        w_tmin = np.where(epochs.times > (w_time - w_size / 2.))[0]
        w_tmax = np.where(epochs.times > (w_time + w_size / 2.))[0]
        if len(w_tmax) == 0:
            continue

        X = epochs._data[..., w_tmin[0]:w_tmax[0]]

        # Save mean scores over folds for each frequency and time window
        score = cross_val_multiscore(estimator=clf, X=X, y=y,
                                     cv=5, n_jobs=-1, scoring=scoring)
        scores.append(score.mean())
    return np.array(scores)


# path_data = op.join(op.dirname(__file__), 'RAW_DATA')
path_data = op.join(os.getcwd(), 'memory_of_error','RAW_DATA')
subjects = [f for f in os.listdir(path_data) if not f.startswith('.')]

analyses = ['rotation', 'target', 'IDEat100ms', 'IDEat200ms', 'IDEatVp']
analyses = ['target', 'IDEat100ms']

for subject in subjects:
    print subject + '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    all_scores = df([dict(fmin=None, fmax=None,
                     analysis=None, score=None)])
    # Read behavioral data
    fname_behavior = op.join(path_data, subject, subject + '.csv')
    events = np.genfromtxt(fname_behavior, dtype=float,
                           delimiter=',', names=True)
    labels = ('rotation', 'target', 'IDEat100ms', 'IDEat200ms', 'IDEatVp')
    event_data = list()
    for event in events:
        event_dict = {key: value for (key, value) in zip(event, labels)}
        event_data.append(event_dict)
    events_behavior = df(events)
    # Read raw data
    run = list()
    files = os.listdir(op.join(path_data, subject))
    run.extend(([op.join(
                path_data, subject + '/') + f for f in files if '.ds' in f]))
    fname_raw = op.join(path_data, run[0])
    raw = read_raw_ctf(fname_raw, preload=True, system_clock='ignore')
    events = mne.find_events(raw)
    event_id = [2, 3]
    tmin = -0.2
    tmax = 2

    results_folder = op.join(path_data + 'results/' + subject)
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    fname_score = results_folder +\
        '/scores_cov%s.npy' % (subject)
    # Loop across freqs
    freqs = [4., 8., 12., 20.]
    for freq, (fmin, fmax) in enumerate(zip(freqs, freqs[1:])):
        # Apply each analysis on a particular frequency band
        raw.filter(l_freq=fmin, h_freq=fmax, n_jobs=-1, fir_design='firwin2')
        epochs = Epochs(raw, events, event_id=event_id,
                        tmin=tmin, tmax=tmax, preload=True,
                        baseline=(tmin, tmin+0.2), decim=15)
        epochs.save(op.join(path_data, subject, 'epochs_%s_%s.fif' % (fmin, fmax)))
        epochs.pick_types(meg=True)
        for analysis in analyses:
            y = np.array(events_behavior[analysis])
            if 'target' in analysis:
                clf = make_pipeline(
                    CSP(n_components=10, reg='oas', log=True),
                    LogisticRegression(C=1))
                y = LabelEncoder().fit_transform(y)
                scoring = 'roc_auc'
            elif 'IDEat100ms' in analysis:
                clf = make_pipeline(
                    SPoC(10), Ridge(alpha=1))
                y = np.array(y, dtype=float)
                sel = np.where(~np.isnan(y))[0]
                scoring = make_scorer(scorer_spearman)
            # main decoding function
            score = _rolling_decoder(clf, epochs, y, scoring)  # noqa
            all_scores = all_scores.append([
                dict(analysis=analysis,  # noqa
                fmin=fmin, fmax=fmax, score=score)])  # noqa
    all_scores.to_csv(results_folder + '/scores_cov_%s.csv' % subject)
