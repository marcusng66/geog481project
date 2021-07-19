import os
import csv
from sklearn.metrics import mean_squared_error
from math import prod, sqrt

file_path = r"C:\Users\Gramm\Desktop\School\spring2021\GEOG481\Barley_predict_result_david\Barley_predict/"
time_steps = 19

def produce_predicted_yields(csv_reader):
    counter = 0
    sum_predictions = 0
    annual_predictions = []
    for rows in csv_reader:
        split_row = rows[0].split(",")
        if counter < time_steps:
            sum_predictions += float(split_row[-1])
            counter += 1
        else:
            annual_predictions.append(sum_predictions / time_steps) 
            sum_predictions = 0
            counter = 0
    return annual_predictions
    
def produce_actual_yields():
    pass

for files in os.listdir(file_path):
    predicted_results = []
    actual_results = []
    with open(file_path + files, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        next(reader)
        predicted_results = produce_predicted_yields(reader)
    break
