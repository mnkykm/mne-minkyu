import os.path as op
import numpy as np
import matplotlib.pyplot as plt
from jr.plot import share_clim
from jr import OnlineReport
from mne.stats import spatio_temporal_cluster_1samp_test
from mne.stats import permutation_cluster_1samp_test
from scipy.stats import ttest_1samp
import pandas

report = OnlineReport()
path_data = '/Users/quentinra/Desktop/MEGdata/ethandata/'
subjects = ['ADGGGJAZ', 'BMFIUFUK', 'BRIENXLD', 'GXWWVBYG', 'NHRRSYHC']
analyses = ['target', 'IDEat100ms']
subjects = ['ADGGGJAZ']
all_scores = list()
for subject in subjects:
    results_folder = op.join(path_data + 'results/' + subject)
    fname_scores = results_folder +\
        '/scores_cov_%s.csv' % (subject)
    scores = dict(pandas.read_csv(fname_scores))
    scores = (scores['score'].values)
    scores = scores[1:]
    scores = float(scores)
    all_scores.append(scores)
all_scores = np.array(all_scores)
