import os
import numpy as np
import matplotlib.pyplot as plt
from jr.plot import share_clim
from jr import OnlineReport
from mne.stats import spatio_temporal_cluster_1samp_test
from mne.stats import permutation_cluster_1samp_test
from scipy.stats import ttest_1samp
import seaborn as sns
sns.set_style("whitegrid")

from mk_config import raw_folder, resultsdir, path_data, subjects

np.seterr(divide='ignore', invalid='ignore')
report = OnlineReport()

# Create a directory for result files
for subject in subjects:
    try:
        os.makedirs(os.path.join(resultsdir, subject))
    except OSError:
        if not os.path.isdir(os.path.join(resultsdir, subject)): raise

analyses = ['targ', 'rot']

for analysis in analyses:
    all_scores = list()
    all_diag = list()
    all_patterns = list()
    for subject in subjects:
        fname_score = os.path.join(resultsdir, subject) + '/scores_%s_%s.npy' % (subject, analysis)
        fname_pttrn = os.path.join(resultsdir, subject) + '/patterns_%s_%s.npy' % (subject, analysis)
        scores = np.load(fname_score)
        diag = np.diag(scores)
        patterns = np.load(fname_pttrn)
        all_scores.append(scores)
        all_diag.append(diag)
        all_patterns.append(patterns)
    all_scores = np.array(all_scores)
    all_diag = np.array(all_diag)
    all_patterns = np.array(all_patterns)
    chance = 0
    if ('rot' in analysis) or ('targ' in analysis):
        chance = .5
    # XXX FIXME AUC are inverted with LR
    # all_scores = 1 - all_scores
    # all_diag = 1 - all_diag


    sfreq = 40
    tmin = -.2
    tmax = 3
    sample_times = np.linspace(0, (tmax-tmin)*sfreq, (tmax-tmin)*sfreq + 1)
    times = sample_times/sfreq + tmin

    def plot(scores, ax):
        im = ax.matshow(scores, origin='lower', cmap='RdBu_r',
                        extent=[tmin, tmax, tmin, tmax])
        # im = ax.matshow(scores, origin='lower', cmap='RdBu_r',
        #                  extent=[tmin, tmax, tmin, tmax], vmin=-0.15, vmax=0.15)

        ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8 ])
        ax.set_yticks([0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8 ])
        ax.set_xlabel('Train Times', fontsize='x-large')
        ax.set_ylabel('Test Times', fontsize='x-large')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_title(analysis)
        return im

    def decod_stats(X, chance):
        """Statistical test applied across subjects"""
        # check input
        X = np.array(X)
        # stats function report p_value for each cluster
        null = np.repeat(chance, len(times))
        # Non-corrected t-test...
        # T_obs, p_values_ = ttest_1samp(X, null, axis=0)
        T_obs_, clusters, p_values, _ = permutation_cluster_1samp_test(
            X, out_type='mask', n_permutations=2**12, n_jobs=-1,
            verbose=False)
        # format p_values to get same dimensionality as X
        p_values_ = np.ones_like(X[0]).T
        for cluster, pval in zip(clusters, p_values):
            p_values_[cluster] = pval

        return np.squeeze(p_values_)

    def gat_stats(X):
        """Statistical test applied across subjects"""
        # check input
        X = np.array(X)
        X = X[:, :, None] if X.ndim == 2 else X

        # stats function report p_value for each cluster
        T_obs_, clusters, p_values, _ = spatio_temporal_cluster_1samp_test(
            X, out_type='mask',
            n_permutations=2**12, n_jobs=-1, verbose=False)

        # format p_values to get same dimensionality as X
        p_values_ = np.ones_like(X[0]).T
        for cluster, pval in zip(clusters, p_values):
            p_values_[cluster.T] = pval

        return np.squeeze(p_values_).T

    decod_p_values = decod_stats(np.array(all_diag) - chance, chance)
    sig = decod_p_values < 0.05
    gat_p_values = gat_stats(np.array(all_scores) - chance)

    # Plot diagonal curve
    fig_diag, axes = plt.subplots()
    # Show the mean curve
    # im = axes.plot(times, np.mean(all_diag, axis=0), color='k')
    axes.set_title('analysis')
    plt.xticks([0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8 ])
    # plt.ylim(-0.04, 0.15)
    plt.xlabel('Time', fontsize='x-large')
    plt.ylabel('Decoding Performance (r)', fontsize='x-large')
    plt.text(0.8, 0, 'chance')
    if ('rotation' in analysis) or ('target' in analysis):
        plt.ylabel('Decoding Performance (AUC)', fontsize='x-large')
        plt.text(0.8, 0.5, 'chance')
    axes.axhline(y=chance, linewidth=0.7, color='k', ls='dashed')
    axes.axvline(x=0, linewidth=0.7, color='k', ls='dashed')
    sem = np.std(all_diag, axis=0)/np.sqrt(len(subjects))
    axes.fill_between(times,
                      np.array(np.mean(all_diag, axis=0))+(np.array(sem)),
                      np.array(np.mean(all_diag, axis=0))-(np.array(sem)),
                      color='0.5')
    axes.fill_between(times,
                      np.array(np.mean(all_diag, axis=0))+(np.array(sem)),
                      np.array(np.mean(all_diag, axis=0))-(np.array(sem)),
                      where=sig, color='red')

    # Plot mean subjects
    fig_mean, axes = plt.subplots()
    im_mean = plot(np.mean(all_scores, axis=0), axes)
    plt.colorbar(im_mean, ax=axes)
    sig = np.array(gat_p_values < 0.05)
    xx, yy = np.meshgrid(times, times, copy=False, indexing='xy')
    plt.contour(xx, yy, sig, colors='Gray', levels=[0],
                linestyles='solid')

    # im_stat = plot(gat_p_values < 0.05, axes[1])
    # plt.colorbar(im_stat, ax=axes[1])

    # plot individual subjects
    fig_all, axes = plt.subplots(1, 5)
    axes = np.reshape(axes, -1)
    for scores, ax in zip(all_scores, axes):
        im = plot(scores, ax)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title('')
    share_clim(axes)
#     report.add_figs_to_section([fig_mean, fig_diag, fig_all], ['mean', 'diag', 'all'],
#                                analysis)
# report.save()


# Plot preliminary figure
fig_diag, axes = plt.subplots()
# Show the mean curve
# im = axes.plot(times, np.mean(all_diag, axis=0), color='k')
axes.set_title('Decoding the Error', fontsize=20)
plt.xticks([0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8 ])
# plt.ylim(-0.04, 0.15)
plt.xlabel('Time', fontsize=14)
plt.ylabel('Decoding Performance (r)', fontsize=14)
plt.text(0.8, 0, 'chance')
axes.axhline(y=chance, linewidth=0.7, color='k', ls='dashed')
axes.axvline(x=0, linewidth=0.7, color='k', ls='dashed')
axes.plot(times, all_diag[0], color='b')
axes.plot(times, all_diag[1], color='g')
plt.show()
# axes.plot(times, all_diag[2], color='r')
# axes.plot(times, all_diag[3], color='c')
# sem = np.std(all_diag, axis=0)/np.sqrt(len(subjects))
# axes.fill_between(times,
#                   np.array(np.mean(all_diag, axis=0))+(np.array(sem)),
#                   np.array(np.mean(all_diag, axis=0))-(np.array(sem)),
#                   color='0.5')
# axes.fill_between(times,
#                   np.array(np.mean(all_diag, axis=0))+(np.array(sem)),
#                   np.array(np.mean(all_diag, axis=0))-(np.array(sem)),
#                   where=sig, color='red')
