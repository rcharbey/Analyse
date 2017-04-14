# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 18:55:50 2016

@author: raphael
"""

import csv
import json

typo_per_ego = {}

def fusion_egos_typo():
    with open('classes_final.csv', 'r') as classes_finales:
        csv_r = csv.reader(classes_finales, delimiter = ';')
        for line in csv_r:
            typo_per_ego[line[0]] = line[1]

    with open('Exports/egos.csv', 'r') as egos_file:
        csv_r = csv.reader(egos_file, delimiter = ';')
        with open('egos_typos.csv', 'w') as file_out:
            csv_w = csv.writer(file_out, delimiter = ';')
            first = csv_r.next()
            first.append('typo')
            csv_w.writerow(first)
            for line in csv_r:
                ego = line[0]
                if ego in typo_per_ego:
                    line.append(typo_per_ego[ego])
                    csv_w.writerow(line)

#fusion_egos_typo()

class st_gt_date_normalised(object):

    def __init__(self):
        self.date_per_gt_per_ego = {}
        self.percent_80_per_ego = {}
        self.gt_per_month = {}

    def _next_month(self, date):
        year = int(date[0:4])
        month = int(date[5:7])
        if month == 12:
            return '%s-01' % (year + 1)
        if date[5] == '1' or date[6] == '9':
            return '%s-%s' % (year, month + 1)
        return '%s-0%s' % (year, month + 1)

    def _prev_month(self, date):
        year = int(date[0:4])
        month = int(date[5:7])
        if month == 1:
            return '%s-12' % (year - 1)
        if date[5] == '1' and not date[6] == '1':
            return '%s-%s' % (year, month - 1)
        return '%s-0%s' % (year, month - 1)


    def _80_per_ego_full_months(self):
        with open('date_80_activity_unsuspected.csv', 'r') as file_in:
            csv_r = csv.reader(file_in, delimiter = ',')
            csv_r.next()
            for eid, debut, fin, a, b in csv_r:
                if debut == '_':
                    continue
                debut_full = self._prev_month(debut)
                fin_full = self._next_month(fin)
                if not fin_full > debut_full:
                    self.percent_80_per_ego[eid] = debut_full, debut_full
                else:
                    self.percent_80_per_ego[eid] = debut_full, fin_full

    def _gt_per_month(self):
        with open('statuses_ego_gt_date_likes_com.csv', 'r') as file_in:
            csv_r = csv.reader(file_in, delimiter = ';')
            for eid, gt, temp_date, nb_likes, nb_com in csv_r:
                date = temp_date[0:7]
                if not ( date >= self.percent_80_per_ego.get(eid, [3000])[0] and date <= self.percent_80_per_ego.get(eid, [0,0])[1]):
                    continue
                if not date in self.gt_per_month:
                    self.gt_per_month[date] = {gt : 1, 'egos' : set(eid)}
                    continue
                self.gt_per_month[date][gt] = self.gt_per_month[date].get(gt, 0) + 1
                if not 'egos' in self.gt_per_month[date]:
                    self.gt_per_month[date]['egos'] == set(eid)
                else:
                    self.gt_per_month[date]['egos'].add(eid)

    def _gt_per_ego_per_date(self):
        with open('statuses_ego_gt_date_likes_com.csv', 'r') as file_in:
            csv_r = csv.reader(file_in, delimiter = ';')
            for eid, gt, temp_date, nb_likes, nb_com in csv_r:
                if not eid in self.date_per_gt_per_ego:
                    self.date_per_gt_per_ego[ego] = {}
                short_date = temp_date[0:7]
                if not short_date in self.date_per_gt_per_ego[ego]:
                    self.date_per_gt_per_ego[ego][short_date] = {}
                if not gt in self.date_per_gt_per_ego[ego][short_date]:
                    self.date_per_gt_per_ego[ego][short_date][gt] = 1




tool = st_gt_date_normalised()
tool._80_per_ego_full_months()
tool._gt_per_month()
gt_per_month = tool.gt_per_month
with open('gt_per_month.csv', 'w') as file_out:
    csv_w = csv.writer(file_out, delimiter = ';')
    list_gt = set()
    for date in gt_per_month:
        for gt in gt_per_month[date]:
            list_gt.add(gt)
    list_gt = list(list_gt)
    list_gt.sort()
    temp = ['dates']
    temp.extend(list_gt)
    csv_w.writerow(temp)

    for date in gt_per_month:
        temp = [date]
        for gt in list_gt:
            if gt == 'egos':
                continue
            temp.append(float(gt_per_month[date].get(gt, 0)) / float(len(gt_per_month[date]['egos'])))
        csv_w.writerow(temp)












