import numpy as np

corners = np.array([[55.94686, -3.19665], #NW
                [55.94686, -3.18123], #NE
                [55.93814, -3.18123], #SE
                [55.93814, -3.19665]]) #SW

UPPER_BOUND = 55.94686
LOWER_BOUND = 55.93814
LEFT_BOUND = -3.19665
RIGHT_BOUND = -3.18123

STATIC_COORDS = { "E5FD8C55EAA37555" : [55.9454333, -3.1913917], # Lauriston
                      "02E5F77764B873DA" : [55.9397722,-3.1915444],   # Melville
                      "200A7CED9D597407" : [55.9430028,-3.1921472],   # Library
                      "AA0E63CF5118F98F" : [55.940953, -3.186092],    # Tennis court
                      "B61241EF668DBC2C" : [55.945302, -3.188279],    # Bristo Square
                      "E786F1568F65C296" : [55.943014, -3.185994]}    # Buccleuch Place

STATIC_COORDS_GRID = { "E5FD8C55EAA37555" : [3, 6],   # Lauriston
                     "02E5F77764B873DA" : [16, 6],  # Melville
                     "200A7CED9D597407" : [8, 5],   # Library
                     "AA0E63CF5118F98F" : [13, 13], # Tennis court
                     "B61241EF668DBC2C" : [3, 10],  # Bristo Square
                     "E786F1568F65C296" : [8, 13]}  # Buccleuch Place

SENSOR_IDS =  np.array(['02E5F77764B873DA', '200A7CED9D597407', 'E5FD8C55EAA37555','AA0E63CF5118F98F', 'B61241EF668DBC2C', 'E786F1568F65C296'])

MOBILE_SENSORS = np.array(['XXM007' ,'XXM008'])

#PM1, PM2.5, PM10, Temperature, Humidity
CALIBRATION_FACTORS = {"02E5F77764B873DA" : [1.0 ,        1.0 ,       1.0 , 1.    ,     1.            ],
           "200A7CED9D597407" : [2.0100042 , 1.54961648 ,1.5126218 , 1.00494929, 1.00478554],
           "E5FD8C55EAA37555" :[1.59078671, 1.21618292, 1.19189916, 1.01233884, 0.9918236],
           "AA0E63CF5118F98F" : [2.93987177 ,2.3760729 , 2.31180713, 0.98098509, 1.03301718],
           "B61241EF668DBC2C" : [2.75341775 ,2.34367823, 2.21772871, 0.98226178, 1.01829024],
           "E786F1568F65C296" : [8.11136564, 7.08428589, 7.04657879, 0.96830023, 1.03546691],
           "XXM007" : [5.05004303, 4.86456945, 4.72626118, 1.16005363, 0.74392267],
           "XXM008" : [5.09431241, 4.90857996, 4.6303786, 1.18617219, 0.7362692  ]}

SELECT_DATES = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180724, 20180726, 20180730, 20180801, 20180802, 20180806, 20180807, 20180808, 20180809] 

START_TIME = '2018-06-29 00:00:00'
END_TIME = '2019-08-09 23:59:59'
# 2019 dataset

# corners = np.array([[55.9478, -3.2075], #NW
#                 [55.9478, -3.1808], #NE
#                 [55.9357, -3.1808], #SE
#                 [55.9357, -3.2075]]) #SW

# UPPER_BOUND = 55.9478
# LOWER_BOUND = 55.9357
# LEFT_BOUND = -3.2075
# RIGHT_BOUND = -3.1808

# STATIC_COORDS = { "B2BC10D2B9F14328" : [55.9452,-3.1916], # Lauriston
#                       "FD368D7D6B815C1B" : [55.9425,-3.1918],   # Melville
#                       "229B8913D6A5B970" : [55.9400,-3.1915],   # Library
#                       "DA1F257AD20C85A7" : [55.9409,-3.1860],    # Tennis court
#                       "9C4F842B28FC5971" : [55.9455,-3.1821],    # Pleasance
#                       "3AB8A58A952B89B6" : [55.9445,-3.1878],   # George Square
#                       "AE93FD8053BFDDFD" : [55.9471,-3.1908],   # Museum
#                       "3BC10C97D2490E7B" : [55.9405,-3.1826],    # Summerhall
#                       "660CB9BC2A97231A" : [55.9431,-3.2012]}    # Lothian
# #                       "F753DAAE895C0DEB" : [55.9422,-3.1965]}    # Coronation

# STATIC_COORDS_GRID = { "B2BC10D2B9F14328" : [4, 11], # Lauriston 
#                       "FD368D7D6B815C1B" : [8, 11],   # Melville
#                       "229B8913D6A5B970" : [12, 11],   # Library
#                       "DA1F257AD20C85A7" : [11, 16],    # Tennis court
#                       "9C4F842B28FC5971" : [3, 19],    # Pleasance
#                       "3AB8A58A952B89B6" : [5, 14],   # George Square
#                       "AE93FD8053BFDDFD" : [1, 12],   # Museum
#                       "3BC10C97D2490E7B" : [12, 18],    # Summerhall
#                       "660CB9BC2A97231A" : [7,4]    # Lothian
# #                       "F753DAAE895C0DEB" : [9,8]}    # Coronation
#                      }

# CALIBRATION_FACTORS = {"B2BC10D2B9F14328": [1.0 ,        1.96136704053 ,       1.0 , 1.0    ,     1.0            ],
#                       "FD368D7D6B815C1B" : [1.0 ,        2.89133597535 ,       1.0 , 1.0    ,     1.0            ],
#                       "229B8913D6A5B970" : [1.0 ,        1.83537667641 ,       1.0 , 1.0    ,     1.0            ],
#                       "DA1F257AD20C85A7" : [1.0 ,        2.54733398945 ,       1.0 , 1.0    ,     1.0            ],
#                       "9C4F842B28FC5971" :  [1.0 ,        2.04216376741 ,       1.0 , 1.0    ,     1.0            ],
#                       "3AB8A58A952B89B6" : [1.0 ,        2.42453772033 ,       1.0 , 1.0    ,     1.0            ],
#                       "AE93FD8053BFDDFD" : [1.0 ,        2.37690917896 ,       1.0 , 1.0    ,     1.0            ],
#                       "3BC10C97D2490E7B" : [1.0 ,        2.76145339021 ,       1.0 , 1.0    ,     1.0            ],
#                       "660CB9BC2A97231A" : [1.0 ,        2.35869648906 ,       1.0 , 1.0    ,     1.0            ],
# #                       "F753DAAE895C0DEB" : [1.0 ,        1.53821777337 ,       1.0 , 1.0    ,     1.0            ],
#                       "XXE101" : [1, 1.78779367671, 1, 1, 1],
#                       'XXE102' : [1, 1.13096151596, 1, 1, 1  ],
#                       "XXE103" : [1, 1.79901752348, 1, 1, 1  ],
#                       "XXE104" : [1, 1.27183615641, 1, 1, 1  ]
#                       }

# SENSOR_IDS =  np.array(["B2BC10D2B9F14328", 'FD368D7D6B815C1B', '229B8913D6A5B970', 'DA1F257AD20C85A7',
#             '9C4F842B28FC5971', '3AB8A58A952B89B6', 'AE93FD8053BFDDFD', '3BC10C97D2490E7B',
#             '660CB9BC2A97231A'])

# MOBILE_SENSORS = np.array(['XXE101', 'XXE102', 'XXE103', 'XXE104'])

# SELECT_DATES = [20190628, 20190629, 20190701, 20190702, 20190703, 20190704, 20190705, 20190706, 20190707, 20190708, 20190709, 20190710, 20190711, 20190712, 20190713, 20190714, 20190715, 20190716, 20190717, 20190718, 20190719, 20190720, 20190721, 20190722, 20190723, 20190724, 20190725, 20190726, 20190727, 20190728] 

# START_TIME = '2019-06-28 00:00:00'
# END_TIME = '2019-07-28 23:59:59'

##################################

GRID_SIZE = 20

WINDOW = 15

FEATURES = ['prev_pm_2.5','lat_grid', 'long_grid', 'humidity', 'PM2.5', 'hour', 'next_pm_2.5']

TRAINING_FEATURES = ['prev_pm_2.5', 'humidity', 'hour', 'PM2.5']

LSTM_TRAINING_FEATURES = ['humidity', 'hour', 'PM2.5']

UPDATED_FEATURES = ['temperature', 'hour', 'commercial', 'residential', 'green', 'primary', 'tertiary', 'unclassified', 'residential/service', 'pedestrian/cycle/noroad']

CONTINUOUS_TRAINING_FEATURES = ['PM2.5', 'temperature', 'lat_grid', 'long_grid', 'commercial', 'residential', 'green', 'primary', 'tertiary', 'unclassified', 'residential/service', 'pedestrian/cycle/noroad']

CONTINUOUS_TRAINING_FEATURES_W_PREV = [ 'PM2.5', 'hour', 'temperature', 'humidity', 'lat_grid', 'long_grid', 'commercial', 'residential', 'green', 'primary', 'tertiary', 'unclassified', 'residential/service', 'pedestrian/cycle/noroad', 'prev_pm_2.5']

COLUMNS = ['Timestamp','PM1', 'PM2.5', 'PM10', 'temperature', 'humidity', 'lat', 'long']

UPDATED_COLUMNS = ['PM1', 'PM2.5', 'PM10', 'temperature', 'humidity', 'lat', 'long', 'lat_grid', 'long_grid', 'hour', 'minute', 'timestep', 'timestepContinuous']


STATIC_COORDS_GRID_20 = { "E5FD8C55EAA37555" : [3, 6],   # Lauriston
                     "02E5F77764B873DA" : [16, 6],  # Melville
                     "200A7CED9D597407" : [8, 5],   # Library
                     "AA0E63CF5118F98F" : [13, 13], # Tennis court
                     "B61241EF668DBC2C" : [3, 10],  # Bristo Square
                     "E786F1568F65C296" : [8, 13]}  # Buccleuch Place


STATIC_COORDS_GRID_50 = { "E5FD8C55EAA37555" : [8, 17],   # Lauriston
                     "02E5F77764B873DA" : [8, 27],  # Melville
                     "200A7CED9D597407" : [22, 14],   # Library
                     "AA0E63CF5118F98F" : [22, 34], # Tennis court
                     "B61241EF668DBC2C" : [33, 34],  # Bristo Square
                     "E786F1568F65C296" : [40, 16]}  # Buccleuch Place
         


#22 days of data collection
allCollectedDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180724, 20180725, 20180726, 20180730, 20180731, 20180801, 20180802, 20180803, 20180806, 20180807, 20180808, 20180809] 

#Dates than all ML tuning experiments were run on
experimentCollectedDates = [20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180726]

recentCollectedDates = [20180807, 20180808, 20180809]
doubleCollectionDates = [20180704, 20180706, 20180802, 20180803] #(but 20180803 is bad)

sixDates = [20180703, 20180706, 20180716, 20180724, 20180726, 20180801]
thirteenDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180726, 20180801, 20180807]
sixteenDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180724, 20180726, 20180801, 20180806, 20180807, 20180808]
