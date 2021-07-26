import csv

#IMPORTANT
#-----------------------------------------

# FILE NAME MUST BEGIN WITH THE {CROPTYPE} FOLLOWED BY THE {ACCUMULATED OR BASELINE} THEN ANYTHING AFTER WITH A CSV EXTENSION
# EXAMPLE - CANOLA_AccumulatedTest.csv
# CURRENTLY NEED TO CHANGE {filtertype} WITHIN THE FILE, WILL FIND ANOTHER WAY IF NEEDED
# FILE_PATH IS ALSO CHANGED IN FILE, CAN MAKE INPUT IF NEEDED

# WAS NOT USED ---- WE TESTED USING WIDE DATA BUT IT DIDNT WORK 

#-----------------------------------------


all_new_rows = [] #Stores all the new rows that are going to be written to csv
valid_labels = ["SumPcpn", "SumEGDD_C", "SumHeatD", "SumFrostD", "AvgSI", "AvgPrcnAWHC", "NDVI"] #Used to create proper headers
filtertype = "year" #Either "year or caruid"

# Function to write all the built rows into a new csv file (will overwrite, does not accumulate)
def write(file_name, headers, current_rows):
    with open(file_name, mode='w', newline='') as test:
        writer = csv.writer(test)
        writer.writerow(headers)
        for row in current_rows:
            writer.writerow(row)
    print("Successfully Wrote Rows into {0}".format(file_name))

#Function to get crop type out of the file name
def getCropType(file_path):
    file_split = file_path.split("/")
    return file_split[len(file_split)-1].split("_")[0]

#Determine if breaking csvs by year or caruid
def determine_filter(filtertype, crop_type, file_type, new_headers):
    if filtertype == "year":
        curr_year = all_new_rows[0][0]
        file_name = "{0}_{1}_{2}.csv".format(crop_type, curr_year, file_type)
        curr_year_rows = []
        for rows in all_new_rows:
            if not rows[0] == curr_year:
                write(file_name, new_headers, curr_year_rows)
                curr_year = rows[0]
                file_name = "{0}_{1}_{2}.csv".format(crop_type, curr_year, file_type)
                curr_year_rows = []
            curr_year_rows.append(rows)
        write(file_name, new_headers, curr_year_rows)
    if filtertype == "caruid":
        valid_caruids = []
        for rows in all_new_rows:
            if rows[1] not in valid_caruids:
                valid_caruids.append(rows[1])
        for caruid in valid_caruids:
            curr_id_rows = []
            for rows in all_new_rows:
                if int(rows[1]) == int(caruid):
                    curr_id_rows.append(rows)
            file_name = "{0}_{1}_{2}.csv".format(crop_type, caruid, file_type)
            write(file_name, new_headers, curr_id_rows)

#Function to create proper headers with the desired ranges
def fix_headers(headers):
    new_headers = []
    new_headers.extend(headers[0:4])
    for labels in valid_labels:
        for i in range(18, 37):
            new_headers.append("{0}{1}_{2}".format(labels, i, i+2))
    new_headers.append("NDVI_MAX")
    return new_headers

# Calculate moving window average? might not be needed? WIP WIP WIP WIP WIP
def calculate_moving_window(values):
    moving_averages = []
    for i in range(0, 19):
        average = ((values[i] + values[i + 1] + values[i+2])/3)
        moving_averages.append(round(average, 5))
    return moving_averages

# Function to calculate the amount of stuff per week (data is no longer accumulated)
def calculate_accum(raw_value_arrays):
    master_array = []
    for arrays in raw_value_arrays:
        if len(arrays) == 0:
            continue
        weekly_values = []
        count = 0
        weekly_values.append(arrays[count])
        while(count + 1 < len(arrays)):
            accumulated_values = arrays[count + 1] - arrays[count]
            weekly_values.append(round(accumulated_values, 5))
            count += 1
        master_array.append(calculate_moving_window(weekly_values))
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
def process_data(file_path, filtertype):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        headers = next(reader)
        headers = headers[0].split(",")
        crop_type = getCropType(file_path) # Get the crop type from the file
        new_headers = fix_headers(headers) # New Headers
        filetype = ""
        row_number = 1
        # Breakdown each row and isolate each specific case
        for row in reader:
            split_row = row[0].split(",")
            count = 0
            organized_values = [] #Raw values
            moving_averages = [] # Processed values
            pcpn_values = [] # all precipitation
            egdd_values = [] # all egdd?
            heat_values = [] # all heat values
            frst_values = [] # all frost values
            avsi_values = [] # all avsi values
            prcn_values = [] # all prcn values
            ndvi_values = [] # all ndvi values
            misc_values = [] # all misc values
            if "Accumulated".lower() in file_path.lower():
                filetype = "Accumulated"
                for header in headers:
                    if "SumPcpn" in header:
                        check_head = header.split("_")[1]
                        if int(check_head) > 17:
                            pcpn_values.append(float(split_row[count]))
                    elif "SumEGDD_C" in header:
                        check_head = header.split("_")[2]
                        if int(check_head) > 17:
                            egdd_values.append(float(split_row[count]))
                    elif "SumHeatD" in header:
                        check_head = header.split("_")[1]
                        if int(check_head) > 17:
                            heat_values.append(float(split_row[count]))
                    elif "SumFrostD" in header:
                        check_head = header.split("_")[1]
                        if int(check_head) > 17:
                            frst_values.append(float(split_row[count]))
                    elif "AvgSI" in header:
                        check_head = header.split("_")[1]
                        if int(check_head) > 17:
                            avsi_values.append(float(split_row[count]))
                    elif "AvgPrcnAWHC" in header:
                        check_head = header.split("_")[1]
                        if int(check_head) > 17:
                            prcn_values.append(float(split_row[count]))
                    elif "NDVI" in header:
                        ndvi_values.append(float(split_row[count]))
                    else: 
                        misc_values.append(split_row[count])
                    count += 1
                organized_values.extend([pcpn_values, egdd_values, heat_values, frst_values])
                moving_averages = calculate_accum(organized_values)
                moving_averages.extend((calculate_moving_window(avsi_values), calculate_moving_window(prcn_values)))
            elif "Weekly".lower() in file_path.lower():
                filetype = "Baseline"
                for header in headers:
                    if "SumPcpn" in header:
                        check_head = header.split("SumPcpn")[1]
                        if int(check_head) > 17:
                            pcpn_values.append(float(split_row[count]))
                    elif "SumEGDD_C" in header:
                        check_head = header.split("SumEGDD_C")[1]
                        if int(check_head) > 17:
                            egdd_values.append(float(split_row[count]))
                    elif "SumHeatD" in header:
                        check_head = header.split("SumHeatD")[1]
                        if int(check_head) > 17:
                            heat_values.append(float(split_row[count]))
                    elif "SumFrostD" in header:
                        check_head = header.split("SumFrostD")[1]
                        if int(check_head) > 17:
                            frst_values.append(float(split_row[count]))
                    elif "AvgSI" in header:
                        check_head = header.split("AvgSI")[1]
                        if int(check_head) > 17:
                            avsi_values.append(float(split_row[count]))
                    elif "AvgPrcnAWHC" in header:
                        check_head = header.split("AvgPrcnAWHC")[1]
                        if int(check_head) > 17:
                            prcn_values.append(float(split_row[count]))
                    elif "NDVI" in header:
                        ndvi_values.append(float(split_row[count]))
                    else: 
                        misc_values.append(split_row[count])
                    count += 1
                organized_values.extend([pcpn_values, egdd_values, heat_values, frst_values, avsi_values, prcn_values])
                for arrays in organized_values:
                    moving_averages.append(calculate_moving_window(arrays))
            if "-999.0" not in misc_values:
                row_builder(misc_values, moving_averages, ndvi_values)
                print("Row #", row_number, " Built")
                row_number += 1
        determine_filter(filtertype, crop_type, filetype, new_headers)

# file_path = "C:/Users/Gramm/Desktop/School/spring2021/GEOG481/Barley_BaselineTest.csv"
file_path = "C:/Users/Gramm/Desktop/School/spring2021/GEOG481/CANOLA_AVHRR-Accumulated_CCYF_Input_1987-2020_Oct_Canada_Imperial.csv"
process_data(file_path, filtertype)

  
        
