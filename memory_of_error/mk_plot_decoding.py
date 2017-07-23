import os, pandas
import numpy as np
import matplotlib.pyplot as plt
from jr.plot import share_clim

import seaborn as sns
sns.set_style("whitegrid")
np.seterr(divide='ignore', invalid='ignore')

from mk_config import res_path, plt_path, analyses
from mk_modules import initialize, get_subjects
from mk_plot_module import (times, plot, decod_stats, gat_stats)

print("*** Plot the decoding results in %s ***" % res_path)

input_path, output_path = res_path, plt_path
subjects = get_subjects(input_path)
initialize(subjects, input_path, output_path, input_type='res', output_type='plt')

plot_df = pandas.DataFrame(index=subjects, columns=analyses).fillna(0)

for analysis in analyses:
    all_scores, all_diag, all_patterns = [], [], []

    for subject in subjects:
        fname_score = os.path.join(input_path, subject) + '/scores_%s_%s.npy' % (subject, analysis)
        fname_pttrn = os.path.join(input_path, subject) + '/patterns_%s_%s.npy' % (subject, analysis)

        if not os.path.isfile(fname_score) or not os.path.isfile(fname_pttrn) :
            continue
        else:
            all_scores.append(np.load(fname_score))
            all_diag.append(np.diag(np.load(fname_score)))
            all_patterns.append(np.load(fname_pttrn))
            plot_df[analysis][subject] = 1

    all_scores = np.array(all_scores)
    all_diag = np.array(all_diag)
    all_patterns = np.array(all_patterns)
    chance = 0
    if ('rot' in analysis) or ('targ' in analysis):
        chance = .5
    # XXX FIXME AUC are inverted with LR
    # all_scores = 1 - all_scores
    # all_diag = 1 - all_diag

    fname_image = [None]*6
    for i in range(6):
        fname_image[i] = output_path + '/plot%i_%s.jpg' % (i+1, analysis)


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
    if ('rot' in analysis) or ('targ' in analysis):
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
    plt.savefig(fname_image[0])

    # Plot mean subjects
    fig_mean, axes = plt.subplots()
    im_mean = plot(np.mean(all_scores, axis=0), axes, analysis=analysis)
    plt.colorbar(im_mean, ax=axes)
    sig = np.array(gat_p_values < 0.05)
    xx, yy = np.meshgrid(times, times, copy=False, indexing='xy')
    plt.contour(xx, yy, sig, colors='Gray', levels=[0],
                linestyles='solid')
    plt.savefig(fname_image[1])
    # im_stat = plot(gat_p_values < 0.05, axes[1])
    # plt.colorbar(im_stat, ax=axes[1])

    # plot individual subjects
    fig_all, axes = plt.subplots(3, 5)
    axes = np.reshape(axes, -1)
    for scores, ax in zip(all_scores, axes):
        im = plot(scores, ax, analysis=analysis)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlabel('Train Times', fontsize='small')
        ax.set_ylabel('Test Times', fontsize='small')
        ax.set_title('')
    share_clim(axes)

    plt.savefig(fname_image[2])


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
    axes.plot(times, all_diag[2], color='r')
    axes.plot(times, all_diag[3], color='c')
    axes.plot(times, all_diag[4], color='m')
    axes.plot(times, all_diag[5], color='y')
    axes.plot(times, all_diag[6], color='k')
    plt.savefig(fname_image[3])

    plt.close('all')
    print analysis + " Done"

# sem = np.std(all_diag, axis=0)/np.sqrt(len(subjects))
# axes.fill_between(times,
#                   np.array(np.mean(all_diag, axis=0))+(np.array(sem)),
#                   np.array(np.mean(all_diag, axis=0))-(np.array(sem)),
#                   color='0.5')
# axes.fill_between(times,
#                   np.array(np.mean(all_diag, axis=0))+(np.array(sem)),
#                   np.array(np.mean(all_diag, axis=0))-(np.array(sem)),
#                   where=sig, color='red')
