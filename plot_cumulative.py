# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 14:06:18 2016

@author: raphael
"""

www = 'fb_active_days_with_apps'

import numpy as np
import matplotlib.pyplot as plt
import csv
import utils

fichier = open('../Exports/export_pa.csv', 'r')
csv_reader = csv.reader(fichier, delimiter =';')
list_indics = next(csv_reader)

www_index = list_indics.index(www)
data = []
for line in csv_reader:
    data.append(float(line[www_index]))

# evaluate the histogram
values, base = np.histogram(data, bins=40)
#evaluate the cumulative
cumulative = np.cumsum(values)
# plot the cumulative function
plt.plot(cumulative, base[:-1], c='blue')

plt.show()