# path_data = '/Users/quentinra/Desktop/MEGdata/WM1/'
# path_data = '/raids/hcpsraid4/quentinra/MEGdata/WM1/'
# path_data = '/Volumes/Samsung_T1/MEGdata/WM1/'
# path_data = '/media/DATA/Pro/Projects/NewYork/romain_wm/data'
import os
import os.path as op

path_data = op.join(os.getcwd(),'RAW_DATA')
subjects = [f for f in os.listdir(path_data) if not f.startswith('.')]
