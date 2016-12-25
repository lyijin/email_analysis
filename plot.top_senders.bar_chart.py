#!/usr/bin/env python3

"""
> plot.top_senders.bar_chart.py <

Based on the parsed inbox file, plot a bar chart that also highlights email
volume from lab members.
"""
import csv

import matplotlib.pyplot as plt
import seaborn as sns

LAB_MEMBERS = ['Manuel Aranda', 'Yong Li', 'Jit Ern Chen', 'Noura Zahran',
               'Guoxin Cui', 'Maha Czies. Olschowsky', 
               'Marcela Herrera Sarrias', 'Wang Xin']
NOT_INDIVIDUALS = ['Announcements', 'Whs Order', 'It Helpdesk',
                   'Coral-List-Request@Coral.Aoml.Noaa.Gov']

email_volume = {}

tsv_reader = csv.reader(open('inbox.parsed.tsv'), delimiter='\t')
# read the top 18 lines, ignore rest
for x in range(18):
    row = next(tsv_reader)
    if row[0] in NOT_INDIVIDUALS: continue

    email_volume[row[0]] = len(row[1].split(', '))

# input lists for seaborn
senders = []
volumes = []
colours = []
for e in sorted(email_volume, key=email_volume.get, reverse=True):
    senders.append(e)
    volumes.append(email_volume[e])
    colours.append('#e34a33' if e in LAB_MEMBERS else '#fee8c8')

# seaborn
sns.set_style('whitegrid')
f, ax = plt.subplots(figsize=(10, 5))
ax = sns.barplot(x=volumes, y=senders, palette=colours)

# add in text at bar tips, with thousand separator
for n, rects in enumerate(ax.patches):
    ax.text(rects.get_width() + 10, rects.get_y() + 0.5,
            '{0:,g}'.format(volumes[n]),
            color='#000000' if senders[n] in LAB_MEMBERS else '#666666',
            verticalalignment='center')

# change colour of y-ticks, depending on whether lab member or not
for n, label in enumerate(ax.get_yticklabels()):
    label.set_color('#000000' if senders[n] in LAB_MEMBERS else '#666666')

# remove x-axis values
ax.set_xticks([])

# remove borders around bars
plt.setp(ax.patches, linewidth=0)

sns.plt.xlim(0, 1480)
sns.despine(left=True, bottom=True, offset=10, trim=True)
# sns.plt.show()

# save figure
fig = plt.gcf()

# without bbox_inches, the saved figure has truncated axes.
output_filename = 'top_senders.svg'
fig.savefig(output_filename, bbox_inches='tight')
