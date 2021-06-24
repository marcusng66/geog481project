import csv

all_new_rows = []

def write():
    with open('test.csv', mode='w', newline='') as test:
        writer = csv.writer(test)
        for row in all_new_rows:
            writer.writerow(row)
    print("Successfully Wrote Rows into CSV")

def calculate_moving_window():
    pass

def calculate_accum(raw_value_arrays):
    master_array = []
    for arrays in raw_value_arrays:
        if len(arrays) == 0:
            break
        weekly_accumulation = []
        count = 0
        weekly_accumulation.append(arrays[count])
        while(count + 1 < len(arrays)):
            accumulated_values = arrays[count + 1] - arrays[count]
            weekly_accumulation.append(round(accumulated_values, 5))
            count += 1
        master_array.append(weekly_accumulation)
    return master_array
        
def row_builder(misc, accumulations, ndvi):
    final_row = []
    valid_row = True
    for elem in misc:
        if elem == "-999":
            valid_row = False
        final_row.append(elem)
    for arrays in accumulations:
        for elem in arrays:
            final_row.append(elem)
    for elem in ndvi:
        final_row.append(elem)
    
    if valid_row:
        all_new_rows.append(final_row)

def calculate_accumulations(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        headers = next(reader)
        headers = headers[0].split(",")
        all_new_rows.append(headers)
        for row in reader:
            split_row = row[0].split(",")
            count = 0
            all_accumulated_values = []
            pcpn_values = []
            egdd_values = []
            heat_values = []
            frst_values = []
            avsi_values = []
            prcn_values = []
            ndvi_values = []
            misc_values = []
            for header in headers:
                if "SumPcpn" in header:
                    pcpn_values.append(float(split_row[count]))
                elif "SumEGDD_C" in header:
                    egdd_values.append(float(split_row[count]))
                elif "SumHeatD" in header:
                    heat_values.append(float(split_row[count]))
                elif "SumFrostD" in header:
                    frst_values.append(float(split_row[count]))
                elif "AvgSI" in header:
                    avsi_values.append(float(split_row[count]))
                elif "AvgPrcnAWHC" in header:
                    prcn_values.append(float(split_row[count]))
                elif "NDVI" in header:
                    ndvi_values.append(float(split_row[count]))
                else: 
                    misc_values.append(split_row[count])
                count += 1
            all_accumulated_values.extend((pcpn_values, egdd_values, heat_values, frst_values, avsi_values, prcn_values))
            all_accums = calculate_accum(all_accumulated_values)
            row_builder(misc_values, all_accums, ndvi_values)
        write()

file_path = "C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Book1.csv"
calculate_accumulations(file_path)


  
        
