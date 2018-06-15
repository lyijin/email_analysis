#!/usr/bin/env python3

"""
> parse_inbox.py <

Does what it says on the tin! Takes in what was copy-pasted from Outlook,
groups aliases of the same sender, and spits out a *.tsv with names and
UNIX times of the emails.

Also filters for emails that were sent after I joined KAUST (5/5/13).

The file can then be fed into downstream plotting scripts.
"""
import calendar
import csv
import datetime
import difflib
import re

KAUST_START_UNIX_TIME = 1367712000

def get_unix_time(time_string):
    """
    An example of how Outlook codes time is this: 'Wed 21/12/2016 15:39'.
    Function converts this string into UNIX time (int), ignoring time zone
    (i.e. makes local time zone == UTC).
    """
    return int(calendar.timegm(datetime.datetime.strptime(
            time_string, '%a %d/%m/%Y %H:%M').timetuple()))

# start by parsing emails into a dictionary
inbox = {}

tsv_reader = csv.reader(open('inbox.tsv'), delimiter='\t')
for row in tsv_reader:
    if not row: continue
    if len(row) < 3: continue
       
    # convert sender name to title case
    sender = row[0].title().replace('  ', ' ')
    
    # strangely, some people put TABS in their email subject titles...
    sent_time = re.search('(\w{3} \d{2}/\d{2}/\d{4} \d{2}:\d{2})', 
                          '\t'.join(row))
    if not sent_time: continue
    sent_time = get_unix_time(sent_time.group(1))
    
    if sent_time < KAUST_START_UNIX_TIME: continue         # 5th may 2013
    if '@' in sender: continue         # prevents spam to these addresses
    
    if sender not in inbox:
        inbox[sender] = []
    
    inbox[sender].append(sent_time)

# exclude senders that sent less than 10 emails: too much noise otherwise.
# causes lots of wrong name-clustering downstream too.
senders_counter = {x: len(y) for x, y in inbox.items() if len(y) > 10}

unique_senders = sorted(senders_counter, key=senders_counter.get, reverse=True)
get_best_alias = {}
excluded_senders = []
for s in unique_senders:
    freq = senders_counter[s]
    if s in excluded_senders: continue

    # cluster senders with similar names
    gcm = difflib.get_close_matches(s, unique_senders, n=10, cutoff=0.75)

    if len(gcm) > 1:
        # sort the list based on email frequency. aim to collapse all clustered
        # sender names to the one that the person uses most often
        gcm = sorted(gcm, key=lambda x: senders_counter[x], reverse=True)
        for g in gcm:
            get_best_alias[g] = gcm[0]

        excluded_senders += gcm[1:]
    else:
        get_best_alias[s] = s

# manually override someone's irritating first <--> last name flipping
if 'Chen Jit Ern' in get_best_alias:
    get_best_alias['Chen Jit Ern'] = 'Jit Ern Chen'
if 'J.E. Chen' in get_best_alias:
    get_best_alias['J.E. Chen'] = 'Jit Ern Chen'

# ... and someone else's shortened name
if 'Xinw' in get_best_alias:
    get_best_alias['Xinw'] = 'Wang Xin'

# ... and another person swapping her email name midway through her PhD
if 'Maha Czies. Olschowsky' in get_best_alias:
    get_best_alias['Maha Czies. Olschowsky'] = 'Maha J. Cziesielski'

# senders have now been collapsed and stored in dict get_best_alias
# next step: re-read the inbox file, and store info in a dict
collapsed_inbox = {}
for sender in inbox:
    if sender not in get_best_alias: continue
    
    if get_best_alias[sender] not in collapsed_inbox:
        collapsed_inbox[get_best_alias[sender]] = []

    collapsed_inbox[get_best_alias[sender]] += inbox[sender]

for c in sorted(collapsed_inbox, key=lambda x: -len(collapsed_inbox[x])):
    print (c, end='\t')
    print (*sorted(collapsed_inbox[c]), sep=', ')
