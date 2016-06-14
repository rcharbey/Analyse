# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 18:21:28 2016

@author: raphael
"""
import csv
from os.path import expanduser

nb_to_place = {50:0, 150:1, 300:2, 1000:3, 5000:4}

result = [
[{},{},{},{},{}],
[{},{},{},{},{}],
[{},{},{},{},{}],
[{},{},{},{},{}],
[{},{},{},{},{}],
[{},{},{},{},{}]
]

indics_we_want = ['gini_comments_per_commenter',
                'friends_per_month',
                'commenters_per_month',
                'likers_per_month',
                'avg_surprise_comments',
                'avg_surprise_likes',
                'avg_nb_clusters_comments',
                'avg_nb_clusters_likes',
                'avg_norm_distance',
                'avg_norm_distance_ego_included',
                'avg_norm_path_dependency',
                'avg_norm_start_dependency',
                'avg_norm_prev_dependency',
                'avg_induced_prop_non_isolated_commenters',
                'avg_induced_density',
                'avg_induced_betweenness',
                'avg_induced_nb_com_louvain',
                'avg_burstiness_30',
                'avg_burstiness_50',
                'avg_simple_burstiness',
                'avg_lifetime',
                'avg_separating_time',
                'avg_plurality',
                'diff_commenters_likers',
                'prop_commenters_likers',
                'commenters_non_likers',
                'prop_commenters_non_likers',
                'likers_non_commenters',
                'prop_likers_non_commenters',
                'diff_on_sum_likers_commenters',
                'nb_clusters_best_commenters_10',
                'nb_clusters_best_commenters_25',
                'nb_clusters_best_commenters_40',
                'ego_age',
                'rs_density',
                'rs_nb_links',
                'rs_modularity',
                'rs_diameter',
                'rs_size_max_cc',
                'rs_louvain_2',
                'rs_louvain_2_max_cc',
                'rs_louvain_5',
                'rs_louvain_5_max_cc',
                'rs_clustering_coeff',
                'rs_betweenness',
                'rs_nb_isolated_vertices',
                'rs_sub_com_modularity',
                'rs_sub_com_diameter',
                'rs_sub_com_density',
                'rs_sub_com_betweenness',
                'fb_friends_count',
                'fb_male_friends_count',
                'fb_female_friends_count',
                'fb_publications_count',
                'fb_unique_apps_count',
                'fb_likes_count',
                'duplications',
                'norm_duplications',
                'fb_active_days_with_apps',
                'fb_active_days_without_apps',
                'fb_active_periods',
                'fb_max_friends_year',
                'pubs_1like',
                'pubs_1comment',
                'alters_comment_1_st',
                'alters_comment_5_st',
                'alters_comment_20_st',
                'alters_comment_100_st'
]


with open(expanduser('~/Exports/egos.csv'), 'r') as file_in:
    csv_r = csv.reader(file_in, delimiter = ',')
    indics = csv_r.next()
    indexes = []
    for elem in indics_we_want:
        indexes.append(indics.index(elem))

    id_nb_friends = indics.index('fb_friends_count')
    id_class_typo = indics.index('class_typo')

    for line in csv_r:

        if line[id_class_typo] == 'banned' or line[id_class_typo] == '':
            continue
        class_typo = int(line[id_class_typo])
        dico_typo = result[class_typo]

        nb_friends = int(line[id_nb_friends])
        for nb in [50, 150, 300, 1000, 5000]:
            if nb_friends < nb:
                place = nb_to_place[nb]
                break
        dico_to_put = dico_typo[place]

        for index in indexes:
            indic = indics[index]
            if not indic in dico_to_put:
                dico_to_put[indic] = []
            if line[index] == '_' or line[index] == '' or line[index] == 'nan' or line[index] == 'undetermined':
                continue
            dico_to_put[indic].append(float(line[index]))


with open(expanduser('~/Analyse/Results/stats_egos_per_class_per_size.csv'), 'w') as file_out:
    csv_wr = csv.writer(file_out, delimiter = ';')

    temp = ['classe', 'taille max']
    temp.extend(indics_we_want)
    temp.append('nb_egos')
    csv_wr.writerow(temp)

    for classe in range(6):
        for size_max in nb_to_place:
            temp = [classe,size_max]
            dico_a_lire = result[classe][nb_to_place[size_max]]
            for indicateur in indics_we_want:
                if not indicateur in dico_a_lire:
                    temp.append('_')
                    continue
                list_valeurs = dico_a_lire[indicateur]
                if not list_valeurs:
                    temp.append('_')
                    continue
                temp.append(round(sum(list_valeurs) / float(len(list_valeurs)),5))
            temp.append(len(list_valeurs))
            csv_wr.writerow(temp)





