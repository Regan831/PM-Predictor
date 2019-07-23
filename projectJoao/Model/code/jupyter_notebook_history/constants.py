import numpy as np

dates = ["20180703-20180704",
         "20180704-20180705",
         "20180705-20180706",
         "20180706-20180707"]

dates2 = ["20180723-20180724",
         "20180724-20180725",
         "20180725-20180726",
         "20180726-20180727"]

sensors = ["02E5F77764B873DA",
           "200A7CED9D597407",
           "E5FD8C55EAA37555",
           "AA0E63CF5118F98F",
           "B61241EF668DBC2C",
           "E786F1568F65C296"]

finalStaticCoords = { "E5FD8C55EAA37555" : [55.9454333, -3.1913917],  # Lauriston
                      "02E5F77764B873DA" : [55.9397722,-3.1915444],   # Melville
                      "200A7CED9D597407" : [55.9430028,-3.1921472],   # Library
                      "AA0E63CF5118F98F" : [55.940953, -3.186092],    # Tennis court
                      "B61241EF668DBC2C" : [55.945302, -3.188279],    # Bristo Square
                      "E786F1568F65C296" : [55.943014, -3.185994]}    # Buccleuch Place

gridStaticCoords = { "E5FD8C55EAA37555" : [3, 6],   # Lauriston
                     "02E5F77764B873DA" : [16, 6],  # Melville
                     "200A7CED9D597407" : [8, 5],   # Library
                     "AA0E63CF5118F98F" : [13, 13], # Tennis court
                     "B61241EF668DBC2C" : [3, 10],  # Bristo Square
                     "E786F1568F65C296" : [8, 13]}  # Buccleuch Place

sensorNames = { "E5FD8C55EAA37555" : "Lauriston",   # Lauriston
                     "02E5F77764B873DA" : "Melville",  # Melville
                     "200A7CED9D597407" : "Library",   # Library
                     "AA0E63CF5118F98F" : "Tennis Court", # Tennis court
                     "B61241EF668DBC2C" : "Bristo Square",  # Bristo Square
                     "E786F1568F65C296" : "Buccleuch Place"}  # Buccleuch Place

columns_needed = ['Timestamp','PM1', 'PM2.5', 'PM10', 'temperature', 'humidity', 'lat', 'long']

corners = np.array([[55.94686, -3.19665], #NW
                    [55.94686, -3.18123], #NE
                    [55.93814, -3.18123], #SE
                    [55.93814, -3.19665]]) #SW

gridSize = 20

# PM1, PM2.5, PM10, Temperature, Humidity
factors = {"02E5F77764B873DA" : [1.0 ,        1.0 ,       1.0 , 1.    ,     1.            ],
           "200A7CED9D597407" : [2.0100042 , 1.54961648 ,1.5126218 , 1.00494929, 1.00478554],
           "E5FD8C55EAA37555" :[1.59078671, 1.21618292, 1.19189916, 1.01233884, 0.9918236],
           "AA0E63CF5118F98F" : [2.93987177 ,2.3760729 , 2.31180713, 0.98098509, 1.03301718],
           "B61241EF668DBC2C" : [2.75341775 ,2.34367823, 2.21772871, 0.98226178, 1.01829024],
           "E786F1568F65C296" : [8.11136564, 7.08428589, 7.04657879, 0.96830023, 1.03546691],
           "XXM007" : [5.05004303, 4.86456945, 4.72626118, 1.16005363, 0.74392267],
           "XXM008" : [5.09431241, 4.90857996, 4.6303786, 1.18617219, 0.7362692  ]}
