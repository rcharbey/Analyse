# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:26:30 2016

"""

import csv
import numpy as np
from os.path import expanduser

file_from = expanduser('~/Exports/egos_for_pca.csv')
file_out = expanduser('~/Analyse/Results/quintiles.csv')

def find_quintiles(tab):
    return np.percentile(tab, 50)

with open(file_from, 'r') as reader:
    csv_reader = csv.reader(reader, delimiter =';')

    indics = csv_reader.next()
    dico = {indic : [[],[]] for indic in indics}

    for line in csv_reader:
        for i in range(len(line)):
            this_indic = indics[i]
            data = float(line[i])
            if data < 0.83:
                dico[this_indic][0].append(data)
            elif data > 1.2:
                dico[this_indic][1].append(data)


dico_quintiles = {indic : [] for indic in dico}
for indic in dico:
    dico_quintiles[indic].append(find_quintiles(dico[indic][0]))
    dico_quintiles[indic].append(0.83)
    dico_quintiles[indic].append(1.2)
    dico_quintiles[indic].append(find_quintiles(dico[indic][1]))
    dico_quintiles[indic].append(float('inf'))

print dico_quintiles

with open(file_out, 'w') as writer:
    csv_writer = csv.writer(writer, delimiter = ';')
    with open(file_from, 'r') as reader:
        csv_reader = csv.reader(reader, delimiter =';')

        indics = csv_reader.next()
        csv_writer.writerow(indics)
        for line in csv_reader:
            temp = []
            for i in range(len(line)):
                this_indic = indics[i]
                for j in range(len(dico_quintiles[indic])):
                    if float(line[i]) < dico_quintiles[indic][j]:
                        temp.append(j)
                        break
            csv_writer.writerow(temp)


