# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:21:30 2015

@author: raphael
"""

import csv
import numpy as np
import utils

def open_reader(origin):
    aggregation_statuses = open('../Exports/statuses_%s.csv' % origin, 'r')
    return aggregation_statuses

def constraints_ok(line, non_friends_com, one_com):
    if not line:
        return False
    if line == ['\n']:
        return False
    if non_friends_com and int(line[utils.LIST_INDICS.index('non_friend_commenters')]) != 0:
        return False
    if one_com and int(line[utils.LIST_INDICS.index('nb_comments')]) < 1:
        return False
    return True

origin = 'all'
to = '_all'
id_gt = utils.LIST_INDICS.index('guessed_type')
id_density = utils.LIST_INDICS.index('induced_density')

indic_to_id = dict((indic, 0) for indic in utils.list_indics_to_consider)
info_per_gt = {}

#CONSTRAINTS
non_friends_com = False
one_com = True
if one_com:
    to += '_1_com'
if non_friends_com:
    to += '_non_friends'

with open('../Exports/statuses_%s.csv' % origin, 'r') as data_in:
    list_indics = data_in.readline().split(';')
    for indic in utils.list_indics_to_consider:
        indic_to_id[indic] = list_indics.index(indic)

    for line in data_in:
        data = line.split(';')
        if not constraints_ok(data, non_friends_com, one_com):
            continue

        to_continue = False
        gt = data[id_gt]
        if not gt in info_per_gt:
            info_per_gt[gt] = dict((indic, []) for indic in utils.LIST_INDICS)
            info_per_gt[gt]['nb'] = 0
        info = info_per_gt[gt]
        info['nb'] += 1
        for indic in utils.list_indics_to_consider:
            id_indic = indic_to_id[indic]
            indic_value = data[id_indic]
            if indic_value != '_' and indic_value != '':
                info[indic].append(indic_value)


aggregation_statuses = open_reader(origin)
csv_reader = csv.reader(aggregation_statuses, delimiter = ';')


print_aver = open('Results/%s_indics_per_gt%s_aver.csv' % (origin, to), 'w')
print_med = open('Results/%s_indics_per_gt%s_med.csv' % (origin, to), 'w')

csv_writer_aver = csv.writer(print_aver, delimiter = ';')
csv_writer_med = csv.writer(print_med, delimiter = ';')

temp = ['guessed_type', 'nb_of_statuses']
temp.extend([indic for indic in utils.list_indics_to_consider])

csv_writer_aver.writerow(temp)
csv_writer_med.writerow(temp)

for gt in info_per_gt:
    temp_aver = [gt + ' aver', info_per_gt[gt]['nb']]
    temp_med = [gt + ' med', info_per_gt[gt]['nb']]
    for indic in utils.list_indics_to_consider:
        if indic == 'nb':
            continue
        temp_list = [float(x) for x in info_per_gt[gt][indic] if not 'bug' in x]
        if temp_list:
            med_tab = np.median(temp_list)
        else:
            temp_aver.append('bug')
            temp_med.append('bug')
            continue
        sum_indic = sum(temp_list)
        average = sum_indic / float(len(temp_list)) if len(temp_list) != 0 else 0

        temp_aver.append(round(average, 5))
        temp_med.append(round(med_tab, 5))

    csv_writer_aver.writerow(temp_aver)
    csv_writer_med.writerow(temp_med)

print_aver.close()
print_med.close()
aggregation_statuses.close()