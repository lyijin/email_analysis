#!/usr/bin/env python3

"""
> plot.aranda.swarmplot.py <

Based on the parsed inbox file, plot a swarmplot to provide chronological
context to email volume from lab members.
"""
import csv
import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

KAUST_START_UNIX_TIME = 1367712000
LAB_MEMBERS = ['Manuel Aranda', 'Yong Li', 'Jit Ern Chen', 'Noura Zahran',
               'Guoxin Cui', 'Maha Czies. Olschowsky', 
               'Marcela Herrera Sarrias', 'Wang Xin']

def reformat_time(unix_time):
    """
    Converts UNIX time of email to a float that stores "years post-KAUST start".
    For example, an email sent exactly a year after my joining = 1.00
    """
    sec_in_year = 365.25 * 24 * 60 * 60
    unix_time = (int(unix_time) - KAUST_START_UNIX_TIME) / sec_in_year
    return round(unix_time, 4)

def get_weekend_bool(unix_time):
    """
    Converts UNIX time to whether day is a weekend (True) or a weekday (False).
    Note that weekend = ['Fri', 'Sat']!
    """
    d = datetime.date.fromtimestamp(unix_time)
    return d.strftime('%a') in ['Fri', 'Sat']

email_volume = {}

tsv_reader = csv.reader(open('inbox.parsed.tsv'), delimiter='\t')
# read the top 18 lines, ignore non-lab members
for x in range(18):
    row = next(tsv_reader)
    if row[0] not in LAB_MEMBERS: continue

    email_volume[row[0]] = [int(x) for x in row[1].split(', ')]

# create pandas table for seaborn plot
data = []
for x in sorted(email_volume, key=lambda x: len(email_volume[x]), reverse=True):
    for y in email_volume[x]:
        data.append([x, reformat_time(y), get_weekend_bool(y)])

data = pd.DataFrame(data, columns=['sender', 'time', 'weekend'])

# seaborn
sns.set_style('whitegrid')
f, ax = plt.subplots(figsize=(12, 8))
sns.swarmplot(x='time', y='sender', hue='weekend', data=data,
              palette=['#fdbb84', '#e34a33'], size=3)

ax.set_xlabel('Years in KAUST')
ax.set_ylabel('')
plt.legend(loc='center', bbox_to_anchor=(0.5, 1.02), ncol=2,
           markerscale=3, labels=['Weekend', 'Weekday'])
sns.plt.xlim(0, 3.7)
sns.despine(left=True, bottom=True, offset=10, trim=True)
#sns.plt.show()

# save figure
fig = plt.gcf()

# without bbox_inches, the saved figure has truncated axes.
output_filename = 'aranda_swarmplot.svg'
fig.savefig(output_filename, bbox_inches='tight')
