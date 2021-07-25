import csv
import os

# path = r"C:/Users/Gramm/Downloads/sprwhtoutput/Sprwht_output_david"
# path = r"C:/Users/Gramm/Downloads/Barleyoutput/Barley_output_david"
path = r"C:/Users/Gramm/Downloads/Canolaoutput/Canola_output_david"
compile_rows = [['Year,SumPcpn,SumEGDD_C,SumHeatD,SumFrostD,AvgSI,AvgPrcnAWHC,NDVI,Yield,Area']]
usable_models = [['File Name, RowCount']]
file_counter = 0
usable_files = 0

for filename in os.listdir(path):
    file_counter += 1
    with open(path + "/" + filename, newline = '') as csvfile: 
        csvreader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
        row_counter = 0
        for row in csvreader:
            row_counter+=1
            if (row[0].split(",")[0] != "Year"): 
                compile_rows.append(row)
        if (row_counter >= 375):
            usable_files += 1
            usable_models.append([filename + "," + str(row_counter)])
        print(filename + " - " + str(row_counter))

print(str(usable_files) + "/" + str(file_counter), usable_files/file_counter)

# with open(r"C:/Users/Gramm/Downloads/Barleyoutputs.csv", "w", newline='') as csvfile:
#     csvwriter = csv.writer(csvfile, delimiter = ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     csvwriter.writerows(compile_rows)

# with open(r"C:/Users/Gramm/Downloads/Barleyusable.csv", "w", newline='') as csvfile:
#     csvwriter = csv.writer(csvfile, delimiter = ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     csvwriter.writerows(usable_models)