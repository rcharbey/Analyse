# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 15:00:08 2016

@author: raphael
"""

from datetime import datetime
from os.path import expanduser
import csv
import json
import gzip

list_egos = [
             '544484f1642f361d166744fe4f596942',
             '3e9ecd0915222023e606af19410cbf7d',
             '914dca4424355f8e8f59fbef8be3e077',
             '2f760bd430f2207e7f4ccf6077441efb',
             '03b0ee5109001789e5708d4714449261',
             '65c2a54e250ce370480b8bbab3efd234',
             '537f1e0c0760e15a53246c95cbd8e789',
             '03bebf48dbdbf2cb2828d385a16452d2',
             'fec1b592220516399d21c41344dd6c3d',
             '80f8ffe8d32904e66c9eaa5f1cca55fb',
             '34d92beeeaaf88edbadf4f169676605f',
             'fe230e062f8e21015ebed1b806f54efd',
             'd688850ad7269ce841cf50766c85dc62',
             '725a65a702314920ddb9fc3fbfc22b93',
             'e81ea822d74c8f82b1f01c438369440c',
             '92a654159280eb61128c7b50203eb5b9'
             ]

for ego in egos:
    dicto = {}
    with open(expanduser('~/STATUSES-CSV/%s.csv' % ego), 'r') as fichier_1:
        csv_reader = csv.reader(fichier_1, delimiter =';')
        csv_reader.next()
        for line in csv_reader:
            dicto[line[1]] = [line[1], line[2], line[3]]

    with open(expanduser('~/results/jsons_horodates/%s.csv' % ego), 'w') as sortie:
        csv_writer = csv.writer(sortie, delimiter = ';')
        with gzip.open(expanduser('~/data/all/%s/statuses.jsons.gz', 'r') as entree:

            for line_temp in entree:
                line = json.loads(line_temp)
                annee = str(datetime.fromtimestamp(int(line['created'])/1000)).split(' ')[0].split('-')[0]
                if line['id'] in dicto:
                    dicto[line['id']].append(line)
                    csv_writer.writerow(dicto[line['id']])
                else:
                    temp = []
                    temp.append(line['id'])
                    temp.append('')
                    temp.append(datetime.fromtimestamp(int(line['created'])/1000))
                    temp.append(line)
                    csv_writer.writerow(temp)