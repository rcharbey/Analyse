# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 12:21:43 2015

@author: raphael
"""

import utils
import csv

reader = utils.open_reader()
csv_reader = csv.reader(reader, delimiter = ';')

list_indics = csv_reader.next()
quintile_id = list_indics.index('quintile_comments')
gt_id = list_indics.index('guessed_type')

result = {}
try:
    i = 0
    for line in csv_reader:
        i += 1
        if i == 130000:
            break
        quintile = line[quintile_id]
        if quintile == '':
            continue
        if not quintile in result:
            result[quintile] = {}

        gt = line[gt_id]
        if not gt in result[quintile]:
            result[quintile][gt] = 1
        else:
            result[quintile][gt] += 1
finally:
    writer = open('../Exports/gt_per_quintile.csv', 'w')
    csv_writer = csv.writer(writer, delimiter = ';')
    temp = ['quintiles']
    list_gt = result['0'].keys()
    temp.extend(list_gt)
    csv_writer.writerow(temp)

    for int_quintile in range(5):
        quintile = '%s' % int_quintile
        gts = result[quintile]
        temp = [quintile]
        for gt in list_gt:
            temp.append(gts.get(gt, 0))
        csv_writer.writerow(temp)

    reader.close()
    writer.close()

