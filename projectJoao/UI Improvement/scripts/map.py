from gmplot import gmplot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import datetime
import os
import glob


def make_map(name_folder):
    print ("Participant: " + name_folder[0:6])

    # Load files
    all_air_files = glob.glob(os.path.join(name_folder, "Airspeck/*.csv"))
    air_data = pd.concat((pd.read_csv(f) for f in all_air_files))
    all_gps_files = glob.glob(os.path.join(name_folder, "Phone GPS/*.csv"))
    gps_data = pd.concat((pd.read_csv(f) for f in all_gps_files))
    gmap = gmplot.GoogleMapPlotter(55.944581, -3.187566, 15, apikey='AIzaSyCN4k_RN5H9W097ev77QU6fhR1Y18egZxg')

    # Make time match
    try:
        list_media = os.listdir(os.path.join(name_folder, "Media"))
        list_media_time = map(lambda x:x.split('.')[0], list_media)
        list_media_timestamp = map(lambda x: int(time.mktime(datetime.datetime.strptime(x, "%Y%m%d_%H%M%S").timetuple())*1000), list_media_time)
    except:
        list_media = []
        list_media_timestamp = []
    # Map
    lats = list(air_data['gpsLatitude'])
    longs = list(air_data['gpsLongitude'])
    colors = list(air_data['pm2_5'])

    cmap = plt.cm.rainbow
    min_col = min(colors)
    max_col = max(colors)
    norm = matplotlib.colors.Normalize(vmin=min_col, vmax=max_col)

    m = np.zeros((1,20))
    for i in range(20):
        m[0,i] = (i*5)/100.0
    plt.imshow(m, cmap=cmap, aspect=2)
    plt.title("PM2.5")
    plt.yticks(np.arange(0))
    plt.xticks(np.arange(0,25,5), [min_col,(max_col-min_col)/4,(max_col-min_col)/2,(max_col-min_col)*3/4,max_col])
    plt.savefig( 'Graphs/legend_{}.png'.format(name_folder[0:6]))
    for lat,long, col in zip(lats, longs, colors):
        color = matplotlib.colors.to_hex(cmap(norm(col)))
        gmap.scatter([lat], [long], color, size=25, marker=False)

    # Media
    for name, timestamp in zip(list_media, list_media_timestamp):
        idx = (np.abs(gps_data['timestamp'].values - timestamp)).argmin()
        gmap.marker(gps_data['latitude'].values[idx], gps_data['longitude'].values[idx], 'black', title = name)

    # Draw
    gmap.draw( "Graphs/graph_{}.html".format(name_folder[0:6]))

    #Other info
    print ("Minimum PM2.5 value measured: {}".format(min_col))
    print ("Maximum PM2.5 value measured: {}".format(max_col))
    print ("Average PM1 exposure measured: {}".format(air_data[['pm1']].mean()[0]))
    print ("Average PM2.5 exposure measured: {}".format(air_data[['pm2_5']].mean()[0]))
    print ("Average PM10 exposure measured: {}".format(air_data[['pm10']].mean()[0]))
    print




folders = list(filter(lambda x: os.path.isdir(os.path.join('.', x)), os.listdir('.')))
if "Graphs" not in folders:
    os.mkdir("Graphs")
for folder in folders:
    if folder != "Graphs":
        make_map(folder)
