import csv
import os

# Set path to the three specific path where the outputs were stored
# path = r"C:/Users/Gramm/Desktop/school/geog481/sprwhtoutput/Sprwht_output_david"
# path = r"C:/Users/Gramm/Desktop/school/geog481/Barleyoutput/Barley_output_david"
path = r"C:/Users/Gramm/Desktop/school/geog481/Canola_output_david"

# Set the header rows for the original csv file
compile_rows = [['Year,SumPcpn,SumEGDD_C,SumHeatD,SumFrostD,AvgSI,AvgPrcnAWHC,NDVI,Yield,Area']]
# Set the header rows for the new csv file
usable_models = [['File Name, RowCount']]
# Set counters
file_counter = 0
usable_files = 0

# Iterate through all available CSV files in the directory
for filename in os.listdir(path):
    file_counter += 1

    with open(path + "/" + filename, newline = '') as csvfile: 
        csvreader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
        row_counter = 0
        # Iterate through all rows to count them
        for row in csvreader: 
            row_counter+=1
        # Check if the row_counter is greater or equal to the lower limit
        if (row_counter >= 375):
            usable_files += 1
            usable_models.append([filename + "," + str(row_counter)])
        print(filename + " - " + str(row_counter))

# Output the percentage of files that passed the check
print(str(usable_files) + "/" + str(file_counter), usable_files/file_counter)

# Write to usable model file
with open(r"C:/Users/Gramm/Downloads/Barleyusable.csv", "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter = ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerows(usable_models)