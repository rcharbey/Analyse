# -*- coding: utf-8 -*-

import csv
from os.path import expanduser
from utils import list_possible_values
import numpy as np

file_in = expanduser('~/Exports/egos_quelques_indics.csv')
base = 'rs_type'

base_values = list_possible_values(file_in, base)


with open(expanduser(file_in), 'r') as file_in:
    nb_egos = 0
    csv_r = csv.reader(file_in, delimiter = ';')
    indics = csv_r.next()

    compared_inds = [indic for indic in indics if not indic == base]
    dico = {pv : {compared_ind : [] for compared_ind in compared_inds} for pv in base_values}

    id_indics = {}
    for compared_ind in compared_inds:
        id_indics[compared_ind] = int(indics.index(compared_ind))
    id_base = int(indics.index(base))

    ok_lines = 0
    for line in csv_r:
        value_base = line[id_base]
        if value_base in ['', '_']:
            continue
        for indic in id_indics:
            id_indic = id_indics[indic]
            if line[id_indic] in ['nan', '_', '', 'undetermined']:
                continue
            value_indic = float(line[id_indic])
            dico[value_base][indic].append(float(line[id_indic]))
        ok_lines += 1
    print 'nombre de lignes ok : ' + str(ok_lines)


with open(expanduser('~/Analyse/Results/Base_vs_indics.csv'), 'w') as file_out:
    csv_wr = csv.writer(file_out, delimiter = ';')

    temp = ['indicateur']
    for ind in compared_inds:
        temp.append(str(ind)+'_moy')
#        temp.append(str(ind)+'_med')
    csv_wr.writerow(temp)

    for base_value in base_values:
        temp = [base_value]
        for compared_ind in compared_inds:
            temp.append(round(float(np.average(dico[base_value][compared_ind])),2))
#           temp.append(round(float(np.median(dico[base_value][compared_ind])),3))
        csv_wr.writerow(temp)