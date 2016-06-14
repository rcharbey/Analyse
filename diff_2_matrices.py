# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 15:24:30 2016

"""

import csv
from os.path import expanduser

first_file = 'Results/Base_vs_indics_false_egos.csv'
second_file = 'Results/Base_vs_indics_all_egos.csv'

with open(first_file, 'r') as ff:
    csv_r1 = csv.reader(ff, delimiter = ';')
    indics = csv_r1.next()

    with open(second_file, 'r') as sf:
        csv_r2 = csv.reader(sf, delimiter = ';')
        csv_r2.next()

        with open(expanduser('~/Analyse/Results/diff_2_matrices.csv'), 'w') as result:
            csv_result = csv.writer(result, delimiter = ';')
            csv_result.writerow(indics)

            for l1 in csv_r1:
                temp = []
                l2 = csv_r2.next()

                for i in range(len(l1)):
                    if l1[i] == l2[i]:
                        temp.append(l1[i])
                    else:
                        num = float(l1[i]) - float(l2[i])
                        denom = float(l1[i]) + float(l2[i])
                        temp.append(round(100*num/denom,3))

                csv_result.writerow(temp)


