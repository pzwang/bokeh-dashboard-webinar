"Step 0. Load data"

import pandas as pd

from os.path import dirname, join
DATA_DIR = './daily'

def load_ticker(name):
    fname = join(DATA_DIR, "table_%s.csv" % name.lower())
    data = pd.read_csv(fname, header=None, parse_dates=['date'],
                       names=['date', 'foo', 'o', 'h', 'l', 'c', 'v'])
    data = data.set_index('date')
    # For each tick symbol, compute the returns 
    return pd.DataFrame(
            { name            : data.c, 
              name+'_returns' : data.c.diff()/data.c })


