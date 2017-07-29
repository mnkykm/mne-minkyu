# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, mne, pandas, time
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from jr.plot import share_clim
import seaborn as sns
sns.set_style("whitegrid")
np.seterr(divide='ignore', invalid='ignore')

from mk_config import res_path, plt_path, analyses, shift_onset, split_cond
from mk_modules import (initialize, get_dirs,
                        ticks, times, plot, decod_stats, gat_stats)

# Start process
print("*** Plot the decoding results in %s ***" % res_path)
init_time = time.time()

# Get pathway information and list of subjects and create result directories
input_path, output_path = res_path, plt_path
subjects = get_dirs(input_path)
initialize(subjects, input_path, output_path, input_type='res', output_type='plt')

plot_df = pandas.DataFrame(index=subjects, columns=analyses).fillna(0)
print("List of anlyses: %s" % (', '.join(analyses)))

if split_cond == True:
    cond_list = ['rand', 'const']
else:
    cond_list = ['all']

if shift_onset:
    onset_name = 'movement'
else:
    onset_name = 'target'

# analysis = sys.argv[1]    # Use these lines when using swarm!
# if True:                  # Use these lines when using swarm!
for analysis in analyses:   # Delete this line when using swarm!

    for cond in cond_list:
        print("Plotting %s..." % (analysis))
        start_time = time.time()
        fname_image = [output_path + '/plot%i_%s_%s.jpg' % (i, analysis, cond) for i in range(1, 5)]

        all_scores, all_diag, all_patterns = [], [], []
        for subject in subjects:
            path_subj = os.path.join(input_path, subject)
            fname_score = path_subj + '/scores_%s_%s_%s.npy' % (subject, analysis, cond)
            fname_pttrn = path_subj + '/patterns_%s_%s_%s.npy' % (subject, analysis, cond)

            if not os.path.isfile(fname_score) or not os.path.isfile(fname_pttrn):
                continue
            else:
                all_scores.append(np.load(fname_score))
                all_diag.append(np.diag(np.load(fname_score)))
                all_patterns.append(np.load(fname_pttrn))
                plot_df[analysis][subject] = 1

        if not all_scores or not all_patterns:
            continue
        else:
            all_scores, all_diag, all_patterns = np.array(all_scores), np.array(all_diag), np.array(all_patterns)
            n = np.sum(plot_df[analysis])

        if ('rot' in analysis) or ('targ' in analysis):
            chance = .5
        else:
            chance = 0

        decod_p = decod_stats(np.array(all_diag) - chance, chance)
        gat_p = gat_stats(np.array(all_scores) - chance)

        decod_sig = decod_p < 0.05
        gat_sig = gat_p < 0.05

        # ----- Plot diagonal curve -----
        fig_diag, axes = plt.subplots()
        axes.set_title("%s (n=%i, onset=%s, cond=%s)" % (analysis, n, onset_name, cond))
        plt.xticks(ticks)

        axes.axhline(y=chance, linewidth=0.7, color='k', ls='dashed')
        axes.axvline(x=0, linewidth=0.7, color='k', ls='dashed')

        if ('rot' in analysis) or ('targ' in analysis):
            plt.xlabel('Time', fontsize='x-large')
            plt.ylabel('Decoding Performance (AUC)', fontsize='x-large')
            plt.text(0.8, 0.5, 'chance')
        else:
            plt.xlabel('Time', fontsize='x-large')
            plt.ylabel('Decoding Performance (r)', fontsize='x-large')
            plt.text(0.8, 0.0, 'chance')

        sem = np.std(all_diag, axis=0)/np.sqrt(len(subjects))
        axes.fill_between(times,
                          np.mean(all_diag, axis=0) + sem,
                          np.mean(all_diag, axis=0) - sem,
                          color='0.5')
        axes.fill_between(times,
                          np.mean(all_diag, axis=0) + sem,
                          np.mean(all_diag, axis=0) - sem,
                          where=decod_sig, color='red')
        plt.savefig(fname_image[0])

        # ----- Plot mean subjects -----
        fig_mean, axes = plt.subplots()
        plt.xticks(ticks)
        plt.yticks(ticks)
        im_mean = plot(np.mean(all_scores, axis=0), axes, analysis=analysis)
        plt.colorbar(im_mean, ax=axes)
        xx, yy = np.meshgrid(times, times, copy=False, indexing='xy')
        plt.contour(xx, yy, gat_sig, colors='Gray', levels=[0], linestyles='solid')
        axes.set_title("%s (n=%i, onset=%s, cond=%s)" % (analysis, n, onset_name, cond))
        plt.savefig(fname_image[1])

        # ----- Plot individual subjects -----
        fig_all, axes = plt.subplots(3, 5)
        axes = np.reshape(axes, -1)
        for idx, ax in enumerate(axes):
            if idx < n:
                im = plot(all_scores[idx], ax, analysis=analysis)
            else:
                im = plot(np.empty_like(all_scores[-1]), ax, analysis=analysis)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xlabel('Train Times', fontsize='small')
            ax.set_ylabel('Test Times', fontsize='small')
            ax.set_title(analysis, fontsize='small')
        share_clim(axes[:n])
        plt.tight_layout()
        plt.savefig(fname_image[2])

        # ----- Plot preliminary figure -----
        fig_diag, axes = plt.subplots()
        # Show the mean curve
        # im = axes.plot(times, np.mean(all_diag, axis=0), color='k')

        axes.set_title("%s (n=%i, onset=%s, cond=%s)" % (analysis, n, onset_name, cond))
        plt.xticks(ticks)
        axes.axhline(y=chance, linewidth=0.7, color='k', ls='dashed')
        axes.axvline(x=0, linewidth=0.7, color='k', ls='dashed')

        if ('rot' in analysis) or ('targ' in analysis):
            plt.xlabel('Time', fontsize='x-large')
            plt.ylabel('Decoding Performance (AUC)', fontsize='x-large')
            plt.text(0.8, 0.5, 'chance')
        else:
            plt.xlabel('Time', fontsize='x-large')
            plt.ylabel('Decoding Performance (r)', fontsize='x-large')
            plt.text(0.8, 0.0, 'chance')

        colors = cm.rainbow(np.linspace(0, 1, len(subjects)))
        for i in range(n):
            axes.plot(times, all_diag[i], color=colors[i])
        plt.savefig(fname_image[3])

        plt.close('all')
        print("Done: %s, %i results, %i seconds " % (analysis, n, time.time() - start_time))

plot_df.to_csv(os.path.join(output_path, 'plot.csv'))
print("Total %i seconds." % (time.time() - init_time))
