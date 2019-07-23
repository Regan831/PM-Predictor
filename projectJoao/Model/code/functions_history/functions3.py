# This version allows an offset para treinar, por exemplo treinar com a media da ultima hora em vez de a 15 min window.

from sklearn.linear_model import PassiveAggressiveRegressor
from pykrige.ok import OrdinaryKriging
import pandas as pd
from datetime import datetime
from datetime import timedelta
import numpy as np
import pykrige.kriging_tools as kt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import constants


#Transform to grid coordinates
def grid_lat_coord(lat):
    #TODO: substituir pelos constants
    if lat < 55.93814 or lat > 55.94686:
        return -1
    i = 0
    for lat_check in np.linspace(55.93814,55.94686,constants.gridSize+1)[1:]:
        if lat < lat_check:
            # devia ser 19 como no functions4.py
            return 20-i
        i+=1

def grid_long_coord(long):
    # TODO: substituir pelos constants
    if long < -3.19665 or long > -3.18123:
        return -1
    i = 0
    for long_check in np.linspace(-3.19665,-3.18123,constants.gridSize+1)[1:]:
        if long < long_check:
            return i
        i+=1

def load_static_sensors():
    static_sensor_data=[]
    for sensor in constants.sensors:
        list_ = []
        for date in constants.dates:
            filename = "data/raw/static/{}/{}.csv".format(date, sensor)
            df = pd.read_csv(filename,index_col=None)
            df['lat'] = constants.finalStaticCoords[sensor][0]
            df['long'] = constants.finalStaticCoords[sensor][1]
            list_.append(df)
        static_sensor_data.append(pd.concat(list_, axis = 0, ignore_index = False))
    all_static_data = pd.concat(static_sensor_data, axis = 0, ignore_index = False)
    # Select columns
    all_static_data = all_static_data[constants.columns_needed]
    return all_static_data

def load_static_sensors_calibrated():
    static_sensor_data=[]
    for sensor in constants.sensors:
        list_ = []
        for date in constants.dates:
            filename = "data/raw/static/{}/{}.csv".format(date, sensor)
            df = pd.read_csv(filename,index_col=None)
            df['lat'] = constants.finalStaticCoords[sensor][0]
            df['long'] = constants.finalStaticCoords[sensor][1]
            # Calibration
            df['PM1'] = df['PM1'].values / constants.factors[sensor][0]
            df['PM2.5'] = df['PM2.5'].values / constants.factors[sensor][0]
            df['PM10'] = df['PM10'].values / constants.factors[sensor][0]
            df['temperature'] = df['temperature'].values / constants.factors[sensor][0]
            df['humidity'] = df['humidity'].values / constants.factors[sensor][0]
            # -----------
            list_.append(df)
        static_sensor_data.append(pd.concat(list_, axis = 0, ignore_index = False))
    all_static_data = pd.concat(static_sensor_data, axis = 0, ignore_index = False)
    # Select columns
    all_static_data = all_static_data[constants.columns_needed]
    return all_static_data

def load_mobile_sensors():
    list_ = []
    for date in constants.dates:
        filename = "data/raw/personal/{}/XXM007_{}.csv".format(date, date.split("-")[0])
        df = pd.read_csv(filename,index_col=None)
        list_.append(df)
    mobile_sensor_data = (pd.concat(list_, axis = 0, ignore_index = False))
    mobile_sensor_data['lat'] = mobile_sensor_data['latitude']
    mobile_sensor_data['long'] = mobile_sensor_data['longitude']
    mobile_sensor_data = mobile_sensor_data[constants.columns_needed]
    return mobile_sensor_data

def transform_to_grid_coordinates(data):
    data['lat_grid'] = data['lat'].apply(grid_lat_coord)
    data['long_grid'] = data['long'].apply(grid_long_coord)
    data = data[data['lat_grid'] >= 0]
    data = data[data['long_grid'] >= 0]
    return data

def create_par(c=1, epsilon=0.1, loss='epsilon_insensitive'):
    par_grid = [[] for i in range(20)]
    for line in par_grid:
        for j in range(20):
            line.append(PassiveAggressiveRegressor(C=c, epsilon=epsilon, loss=loss, max_iter=100, random_state=0,tol=1e-3))
    return par_grid


def insert_into_par(par_grid, timeint, z):
    for i in range(20):
        for j in range(20):
            par_grid[i][j].partial_fit([[timeint]], [z[i][j]])



def train(all_static_data, mobile_sensor_data, start_time, end_time, par_grid, window, timeint_on_first_window=0, verbose=False, rolling_offset=0):
    timeint = timeint_on_first_window
    start_window = start_time
    end_window = (datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=window)).strftime("%Y-%m-%d %H:%M:%S")
    while end_window <= end_time:
        if verbose:
            print ("Inside while loop with timeint = {}".format(timeint))
            print ("start_window = {}".format(start_window))
            print ("end_window = {}".format(end_window))

        start_window_with_offset = (datetime.strptime(start_window, '%Y-%m-%d %H:%M:%S') - timedelta(minutes=rolling_offset)).strftime("%Y-%m-%d %H:%M:%S")
        to_insert = all_static_data[(all_static_data['Timestamp'] > start_window_with_offset) & (all_static_data['Timestamp'] < end_window)]
        if mobile_sensor_data is not None:
            to_insert = to_insert.append( mobile_sensor_data[(mobile_sensor_data['Timestamp'] > start_window_with_offset) & (mobile_sensor_data['Timestamp'] < end_window)])
        to_insert = to_insert.groupby(['lat_grid','long_grid']).mean()
        to_insert.reset_index(level=to_insert.index.names, inplace=True)
        z = [[0 for j in range(20)] for i in range(20)]


        # TODO: Tirei o Kriging
        #ok = OrdinaryKriging(to_insert['long_grid'], to_insert['lat_grid'], to_insert['PM2.5'], variogram_model='gaussian', verbose=False, enable_plotting=False)
        #gridx = np.arange(0.0, 20, 1)
        #gridy = np.arange(0.0, 20, 1)
        #z, ss = ok.execute('grid', gridx, gridy)

        for index, row in to_insert.iterrows():
            z[int(row['lat_grid'])][int(row['long_grid'])] = row['PM2.5']

        insert_into_par(par_grid, timeint, z)

        start_window = (datetime.strptime(start_window, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=window)).strftime("%Y-%m-%d %H:%M:%S")
        end_window = (datetime.strptime(end_window, '%Y-%m-%d %H:%M:%S') + timedelta(minutes=window)).strftime("%Y-%m-%d %H:%M:%S")
        timeint += 1
    if verbose:
        print ("Out of the while loop with timeint = {}".format(timeint))
        print ("start_window = {}".format(start_window))
        print ("end_window = {}".format(end_window))

    return timeint-1, par_grid

def test_square(par_grid, timeint, lat_grid, long_grid):
    return par_grid[lat_grid][long_grid].predict([[timeint]])[0]

def test_grid(par_grid, timeint):
    prediction_grid = [[0 for j in range(20)] for i in range(20)]
    for i in range(20):
        for j in range(20):
            prediction_grid[i][j] = par_grid[i][j].predict([[timeint]])[0]
    return prediction_grid

# Made for one time window only
def test_mobile(par_grid, timeint, mobile_sensor_data, start_time, end_time, offset_timeint):
    # TODO: Juntei a condição tem de ser um específico sensor
    to_test = mobile_sensor_data[(mobile_sensor_data['Timestamp'] > start_time) & (mobile_sensor_data['Timestamp'] < end_time) & (mobile_sensor_data['lat_grid'] == 4) & (mobile_sensor_data['long_grid'] == 6)]
    # to_test = mobile_sensor_data[(mobile_sensor_data['Timestamp'] > start_time) & (mobile_sensor_data['Timestamp'] < end_time)]
    to_test = to_test.groupby(['lat_grid','long_grid']).mean()
    to_test.reset_index(level=to_test.index.names, inplace=True)
    for index, row in to_test.iterrows():
        to_test.loc[index, 'pred_PM2.5'] = test_square(par_grid, timeint+offset_timeint, int(row['lat_grid']), int(row['long_grid']))
    return to_test
