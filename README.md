# mne-minkyu
Analyzing MEG data with MNE-python, and their extensions

![dataflow](screenshot.png)

^ This is the dataflow of overall process. Please note.

## How to use

1. Place all your raw files in the same directory where python codes are.
    * Naming convention: `xx_RAW/` where xx is your initial. (e.g. `mk_RAW/`)
    * Raw file directory should have sub-directories for each subject (e.g. `mk_RAW/ABCDEFGH`)
    * Each sub-directory should have one bevioral data file (.csv) and one or more MEG data files (.ds)

2. Change your configuration at __mk_config.py__
    * set `shift_onset` as `True` if you want movement onset results
    * set `split_cond` as `True` if you want to decode by each condition
    * set `decode_next` as `True` if you want to decode (n+1)th trial
    * set filter parameters and epoch parameters
    * set directory names for epoched, results, and plots directories.
    * Naming convention: `xx_yyyyyy_zzdecim/`

3. Run __mk_save_epochs.py__
    * This will create `xx_epoched_zzdecim/` and sub-directories.
    * Epoched data (-epo.fif) will be generated per subject.
    * Behavioral data (.csv) will be copied per subject.
    
4. Run __mk_decode_motor_task.py__
    * This will create `xx_results_zzdecim/` and sub-directories.
    * Evoked data (-ave.fif) of filters and patterns will be generated per analysis per subject.
    * Data-only numpy array (.npy) of filters, patterns and scores will be generated per analysis per subject.
    * `xx_results_zzdecim/_average/` will be created also and the average data across subjects are stored.

5. Run __mk_make_topomap.py__
    * Topomaps of patterns and filters will be created per analysis per subject
    * Topomaps of average across subjects will be created in `xx_results_zzdecim/_average/`

6. Run __mk_plot_decoding.py__
    * This will create `xx_plots_zzdecim/` with no sub-directory.
    * Four plots will be generated from the decoding results per analysis.
