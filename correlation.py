from string import letters
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from os.path import expanduser
import csv
import argparse

parser = argparse.ArgumentParser(description="main")
parser.add_argument('file', help="csv file to read")
args = parser.parse_args()

def get_data():
    result = []
    max_size = 0
    with open(expanduser(args.file), 'r') as info:
        csv_reader = csv.reader(info, delimiter = ';')
        headers = [x.decode('utf8') for x in csv_reader.next()]
        i = 0
        for line in csv_reader:
            if not line:
                continue
            try:
                result.append([round(float(x),4) for x in line])
                i += 1
            except:
                continue
    return result, headers

rought_data, headers = get_data()
data = np.array(rought_data)
d = pd.DataFrame(data, columns=headers)

# Compute the correlation matrix
corr = d.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots()

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, cmap=cmap, linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

plt.show()