# -*- coding: utf-8 -*-

import csv

def list_possible_values(file_name, indicator):
#    read the indic name in the header
#    then give all its posible values

    with open(file_name, 'r') as from_file:
        csv_reader = csv.reader(from_file, delimiter = ';')

        indics = csv_reader.next()
        to_bin_id = indics.index(indicator)
        indic_values = set()

        for line in csv_reader:
            if line[to_bin_id] in ['_', '']:
                continue
            indic_values.add(line[to_bin_id])

    return indic_values