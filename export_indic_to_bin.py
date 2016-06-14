import argparse
import csv
from utils import list_posible_values

parser = argparse.ArgumentParser()
parser.add_argument('file')
parser.add_argument('indicator')

args = vars(parser.parse_args())

indic_values = list_posible_values(args['file'], args['indicator'])

new_indics = []
for indic in indics:
    if indic == args['indicator']:
        new_indics.extend(indic_values)
    else:
        new_indics.append(indic)

print new_indics

with open(args['file'], 'r') as from_file:
    csv_reader = csv.reader(from_file, delimiter = ';')
    csv_reader.next()

    with open('%s_bin.csv' % args['file'].split('.csv')[0], 'w') as to_file:
        csv_writer = csv.writer(to_file, delimiter = ';')
        csv_writer.writerow(new_indics)

        for line in csv_reader:
            temp = []
            for i in range(len(line)):
                if i == to_bin_id:
                    for possible_value in indic_values:
                        if line[i] == possible_value:
                            temp.append(1)
                        else:
                            temp.append(0)
                else:
                    temp.append(line[i])

            csv_writer.writerow(temp)