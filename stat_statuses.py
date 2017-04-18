import csv
import numpy as np
import utils
import os
from os.path import splitext

ATTRS_STATUSES = [
              'ego_id', 'guessed_type', 'date',
              'friend_likes', 'friend_comments'
              'status_id',
              'from',
              'nb_comments',
              'nb_commenters', 'autocomments', 'friend_commenters', 'friend_comments', 'non_friend_commenters', 'non_friend_comments',
              'nb_likes',
              'autolike', 'friend_likes', 'non_friend_likes',
              'rarity_comments', 'norm_rarity_comments', 'rarity_likes', 'norm_rarity_likes',
              'nb_rare_comments', 'norm_rare_comments', 'nb_rare_commenters', 'nb_rare_likes', 'norm_rare_likes',
              'surprise_comments', 'surprise_likes',
              'nb_clusters_comments', 'nb_clusters_likes',
              'distance', 'norm_distance', 'distance_ego_included', 'norm_distance_ego_included',
              'path_dependency', 'norm_path_dependency', 'start_dependency', 'norm_start_dependency', 'prev_dependency', 'norm_prev_dependency',
              'induced_prop_non_isolated_commenters', 'induced_density', 'induced_betweenness', 'induced_nb_com_louvain',
              'burstiness_30', 'norm_burstiness_30', 'burstiness_50', 'norm_burstiness_50', 'simple_burstiness',
              'lifetime', 'separating_time',
              'quintile_comments', 'quintile_likes',
              'quintile_by_gt_comments', 'quintile_by_gt_likes',
              'plurality',
              'link', 'link_domain',
              'message', 'text_comments',
              ]

LIST_INDICS_OK = ['nb_comments', 'nb_commenters', 'autocomments', 'friend_commenters',
              'friend_comments', 'non_friend_commenters', 'non_friend_comments', 'nb_likes', 'autolike', 'friend_likes',
              'non_friend_likes', 'rarity_comments', 'norm_rarity_comments', 'rarity_likes', 'norm_rarity_likes',
              'nb_rare_comments', 'norm_rare_comments', 'nb_rare_commenters', 'nb_rare_likes', 'norm_rare_likes',
              'surprise_comments', 'surprise_likes', 'distance', 'norm_distance', 'distance_ego_included',
              'norm_distance_ego_included', 'path_dependency', 'norm_path_dependency', 'start_dependency',
              'norm_start_dependency', 'prev_dependency', 'norm_prev_dependency', 'burstiness_50', 'norm_burstiness_50',
              'simple_burstiness', 'lifetime', 'quintile_comments', 'quintile_likes', 'plurality'
]

def constraints_ok(line):
    if not line:
        return False
    if line == ['\n']:
        return False
    if non_friends_com and line[ATTRS_STATUSES.index('non_friend_commenters')] != '' and int(line[ATTRS_STATUSES.index('non_friend_commenters')]) != 0:
        return False
    if one_com and line[ATTRS_STATUSES.index('nb_comments')] != '' and int(line[ATTRS_STATUSES.index('nb_comments')]) < 1:
        return False
    return True

origin = 'all'
to = '_all'

info_per_gt = {}

#CONSTRAINTS
non_friends_com = False
one_com = False
if one_com:
    to += '_1_com'
if non_friends_com:
    to += '_non_friends'

list_file_ego = [file_ego for file_ego in os.listdir('../results/Statuses_indicators') if splitext(file_ego)[1] == '.csv']

for file_ego in list_file_ego:
    with open('../results/Statuses_indicators/%s' % file_ego, 'r') as data_in:

        indic_to_id = {}
        list_indics = data_in.readline().split(';')
        for indic in LIST_INDICS_OK :
            indic_to_id[indic] = ATTRS_STATUSES.index(indic)

        for line in data_in:
            data = line.split(';')
            if not constraints_ok(data):
                continue

            gt = data[1]

            if not gt in info_per_gt:
                info_per_gt[gt] = dict((indic, []) for indic in LIST_INDICS_OK)
                info_per_gt[gt]['nb'] = 0

            info = info_per_gt[gt]
            info['nb'] += 1
            for indic in LIST_INDICS_OK:
                id_indic = indic_to_id[indic]
                indic_value = data[id_indic]
                if indic_value != '_' and indic_value != '' and indic_value != 'bug':
                    info[indic].append(round(float(indic_value), 2))

csv_writer_aver = csv.writer(open('Results/%s_indics_per_gt%s_aver.csv' % (origin, to), 'w'), delimiter = ';')
csv_writer_med = csv.writer(open('Results/%s_indics_per_gt%s_med.csv' % (origin, to), 'w'), delimiter = ';')

temp = ['guessed_type', 'nb_of_statuses']
temp.extend([indic for indic in LIST_INDICS_OK])

csv_writer_aver.writerow(temp)
csv_writer_med.writerow(temp)

for gt in info_per_gt:
    temp_aver = [gt + ' aver', info_per_gt[gt]['nb']]
    temp_med = [gt + ' med', info_per_gt[gt]['nb']]
    for indic in LIST_INDICS_OK:
        if indic == 'nb':
            continue
        temp_list = info_per_gt[gt][indic]
        if temp_list:
            med_tab = np.median(temp_list)
        else:
            temp_aver.append('bug')
            temp_med.append('bug')
            continue
        sum_indic = sum([x for x in temp_list if not x == 'bug'])
        average = sum_indic / float(len(temp_list)) if len(temp_list) != 0 else 0

        temp_aver.append(round(average, 2))
        temp_med.append(round(med_tab, 2))

    csv_writer_aver.writerow(temp_aver)
    csv_writer_med.writerow(temp_med)