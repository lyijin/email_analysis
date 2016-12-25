#!/usr/bin/env python3

"""
> plot.time_of_day.heatmap.py <

Based on the parsed inbox file, plot a heatmap to contrast when people send
their emails.
"""
import collections
import csv

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

LAB_MEMBERS = ['Manuel Aranda', 'Yong Li', 'Jit Ern Chen', 'Noura Zahran',
               'Guoxin Cui', 'Maha Czies. Olschowsky', 
               'Marcela Herrera Sarrias', 'Wang Xin']

def get_hour_of_day(unix_time):
    """
    Converts UNIX time to the hour of the day!
    """
    time_of_day = int(unix_time) % (24 * 60 * 60)
    hour_of_day = int(time_of_day / 3600)
    return hour_of_day

email_volume = {}
tsv_reader = csv.reader(open('inbox.parsed.tsv'), delimiter='\t')
# read the top 18 lines, ignore non-lab members
for x in range(18):
    row = next(tsv_reader)
    if row[0] not in LAB_MEMBERS: continue

    email_volume[row[0]] = [get_hour_of_day(x) for x in row[1].split(', ')]

# create pandas table for seaborn plot
data = []
senders = []
for x in sorted(email_volume, key=lambda x: len(email_volume[x]), reverse=True):
    senders.append(x)
    abs_freq = collections.Counter(email_volume[x])
    rel_freq = [abs_freq[y] / sum(abs_freq.values()) for y in range(24)]
    
    data.append(rel_freq)

data = pd.DataFrame(data, index=senders, columns=range(24))

# seaborn
sns.set_style('whitegrid')
f, ax = plt.subplots(figsize=(15, 4))
sns.heatmap(data, square=True, cmap='OrRd', vmax=0.125, linewidths=.5)

ax.set_xlabel('Hour of day')
plt.yticks(rotation=0)
#sns.plt.show()

# save figure
fig = plt.gcf()

# without bbox_inches, the saved figure has truncated axes.
output_filename = 'aranda_heatmap.svg'
fig.savefig(output_filename, bbox_inches='tight')
