import os 
coolstring = ""

for filename in os.listdir(r"C:/Users/Gramm/Downloads/sprwht/Sprwht_output_david"):
    coolstring += '"' + filename.split(".")[0] + '"' + ", "

csv_file = "CANOLA_1100"
csv_path = "/content/drive/MyDrive/GEOG481/david_input/{0}_output_david/{1}.csv".format(csv_file.split("_")[0].lower().capitalize(), csv_file)

print(csv_path)