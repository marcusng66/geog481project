import csv

all_new_rows = []

# Function to write all the built rows into a new csv file (will overwrite, does not accumulate)
def write(file_name, headers, curr_year_rows):
    with open(file_name, mode='w', newline='') as test:
        writer = csv.writer(test)
        writer.writerow(headers)
        for row in curr_year_rows:
            writer.writerow(row)
    print("Successfully Wrote Rows into CSV")

def getCropType(file_path):
    file_split = file_path.split("/")
    return file_split[len(file_split)-1].split("_")[0]

# Calculate moving window average? might not be needed? WIP WIP WIP WIP WIP
def calculate_moving_window(values):
    curr_index = 0
    moving_averages = []
    while (curr_index+2 != len(values)):
        average = ((values[curr_index] + values[curr_index + 1] + values[curr_index+2])/3)
        moving_averages.append(round(average, 5))
        curr_index += 1
    return moving_averages

# Function to calculate the amount of stuff per week (data is no longer accumulated)
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
        # master_array.append(calculate_moving_window(weekly_accumulation))
    return master_array
        
#Function to build rows for csv input
def row_builder(misc, accumulations, ndvi):
    final_row = []
    for elem in misc:
        final_row.append(elem)
    for arrays in accumulations:
        for elem in arrays:
            final_row.append(elem)
    for elem in ndvi:
        final_row.append(elem)
    all_new_rows.append(final_row)

# Function that breaks apart the rows into valid categories (Ie. precipication, heat, frost)
def calculate_accumulations(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        headers = next(reader)
        headers = headers[0].split(",")
        # headers = fix_headers(headers)
        row_number = 1
        # Breakdown each row and isolate each specific case
        for row in reader:
            split_row = row[0].split(",")
            count = 0
            all_accumulated_values = []
            pcpn_values = [] # all precipitation
            egdd_values = [] # all egdd?
            heat_values = [] # all heat values
            frst_values = [] # all frost values
            avsi_values = [] # all avsi values
            prcn_values = [] # all prcn values
            ndvi_values = [] # all ndvi values
            misc_values = [] # all misc values
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
            if "-1" not in misc_values:
                row_builder(misc_values, all_accums, ndvi_values)
                print("Row #", row_number, " Built")
                row_number += 1
        #Seperate all rows into their respective years
        curr_year = all_new_rows[0][0]
        crop_type = getCropType(file_path)
        file_name = "{0}_{1}.csv".format(crop_type, curr_year)
        curr_year_rows = []
        for rows in all_new_rows:
            if not rows[0] == curr_year:
                write(file_name, headers, curr_year_rows)
                curr_year = rows[0]
                file_name = "CANOLA_{0}.csv".format(curr_year)
                curr_year_rows = []
            curr_year_rows.append(rows)
        write(file_name, headers, curr_year_rows)

file_path = "C:/Users/Gramm/Desktop/School/spring2021/GEOG481/CANOLA_TEST.csv"
# file_path = "C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Data_to_Winston/CCYF_inputs/Oct/AVHRR-Accumulated/CANOLA_AVHRR-Accumulated_CCYF_Input_1987-2020_Oct_Canada_Imperial.csv"
calculate_accumulations(file_path)


  
        
