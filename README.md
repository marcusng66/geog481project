GEOG481 Machine Learning Project

This is the Repo for GEOG 481 Group 12, Oh Crop!

CNN_GilMarcus contains the various scripts and the specific jupyter notebook that we used to create, train and predict the CNN models.
    
     1. DetermineUsableModels.py is a script specifically used for the CNN group to determine the CARUIDs that will work with the CNN implementation
     
     2. ModularBackup1.py is a backup for when transporting the original model into a modular one that allowed easier creation, training and predicting
     
     3. ModularV1.py is the original script that was used to compile everything before being put into a Jupyter Notebook
     
     4. Modular_CNN.ipynb is the actual notebook that we used to create, train and predict for the CNN implemtation.
     
     5. WideDataProcess.py is a prototype script for training the models using data in a wider format as opposed to a longer format. WAS NOT USED ASIDE FROM INITIAL TESTING
     
LSTM_DavidHubert contains the various scripts and the specific jupyter notebook that we used to create, train and predict the LSTM models.
     1. AAFC_Mape_Calculator.ipynb is a script used to calculate the MAPE from the ICCYF's own forecast
     2. Data_preprocess_long_format.ipynb is the script that shapes the data into a longer format (weekly) for the models. THIS WAS USED FOR DATA PROCESSING
     3. Evaluate_annual_yld.ipynb is the script used to find all the model statistics that we contemplated using (R_squared, MAPE, MEI, RMSE) Also used by CNN group
     4. LSTM_long_final.ipynb is the actual notebook that was used to create, train and predict for the LSTM implementation.
     
The raw data, processed data and performance data will be sent through a google drive.

Yeonhak Choo, Hubert Yoo, Gil Paolo Adiao, Marcus Cy Ng
