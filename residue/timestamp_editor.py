import csv

with open('../CVS_data/output_csv_star_2500k/time_dimension.csv', 'r') as infile, open('time_dimension.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        row[-1] = row[-1].replace('T', ' ').replace('Z', '')  # Modify the timestamp
        writer.writerow(row)
