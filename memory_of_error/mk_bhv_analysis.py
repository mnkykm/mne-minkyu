# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, pandas, time, shutil
import numpy as np

from mk_config import bhv_path
from mk_modules import get_dirs
from itertools import groupby

print("*** Analyzing behavoiral data in %s ***" % bhv_path)
init_time = time.time()

bhv_list = [os.path.join(bhv_path, file) for file in get_dirs(bhv_path) if file.endswith('.csv')]

def task(rot, cond):
    if cond == 'const' and rot == 0:
        return 'CZ'
    elif cond == 'const' and rot == -40:
        return 'CN'
    elif cond == 'const' and rot == +40:
        return 'CP'
    elif cond == 'rand' and rot == 0:
        return 'RZ'
    elif cond == 'rand' and abs(rot) == 40:
        return 'RP'
    else:
        return 0

for bhv_file in bhv_list:
    bhv_df = pandas.read_csv(bhv_file, delimiter=',')
    tasklist = [task(bhv_df['rot'][i], bhv_df['cond'][i]) for i in range(len(bhv_df))]
    print bhv_file.split("/")[-1].split("_")[0] + "," + bhv_file.split("/")[-1].split("_")[1] + ", " \
          + ','.join([' '.join([str(k), str(len(list(g)))]) for k, g in groupby(tasklist)])
