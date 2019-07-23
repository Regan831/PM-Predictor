##Adapted from Andrew Bates' code at https://github.com/specknet/airspeck-comparison/blob/master/6%20Airspeck%20S.ipynb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import time


from bokeh.io import show, output_notebook, output_file, reset_output
from bokeh.plotting import figure
import  requests
import pandas as pd

class DataDownloader(object):
    
    def toTimestamp(self, date):
            date = datetime.strptime(date.split(".")[0], "%Y-%m-%d %H:%M:%S")
            return time.mktime(date.timetuple())

    def loadAirSpeckS(self, start_date, end_date, data_dir):
        uuids = ["02E5F77764B873DA",
        "200A7CED9D597407",
        "E5FD8C55EAA37555",
        "AA0E63CF5118F98F",
        "B61241EF668DBC2C",
        "E786F1568F65C296" ]

        payload = {
            'username': 'jupyter',
            'password': 'd84hr75yG4fE',
            'form.submitted':'Login'
        }
        
        with requests.Session() as s:
            s.headers.update({'referer': 'https://dashboard.specknet.uk'})
            p = s.post('https://dashboard.specknet.uk/login', data=payload)
                # print the html returned or something more intelligent to see if it's a successful login page.
            print(p.text)

        ## An authorised request.
        for u in uuids:
            url = 'https://dashboard.specknet.uk/downloadStaticAirspeck/' + u + '/' + str(start_date) + '/' + str(end_date)
            r = s.get(url)
            open(data_dir + "/" + str(u) + '.csv', 'wb').write(r.content)
            
    def readAirSpeckSCSV(self, start_date, end_date, data_dir):
        uuids = ["02E5F77764B873DA",
        "200A7CED9D597407",
        "E5FD8C55EAA37555",
        "AA0E63CF5118F98F",
        "B61241EF668DBC2C",
        "E786F1568F65C296" ]
        
        factors = [[1.0 ,        1.0 ,       1.0 , 1.0    ,     1.0            ],
             [2.0100042 , 1.54961648 ,1.5126218 , 1.00494929, 1.00478554],
             [1.59078671, 1.21618292, 1.19189916, 1.01233884, 0.9918236],
             [2.93987177 ,2.3760729 , 2.31180713, 0.98098509, 1.03301718],
             [2.75341775 ,2.34367823, 2.21772871, 0.98226178, 1.01829024],
             [8.11136564, 7.08428589, 7.04657879, 0.96830023, 1.03546691]]
        
        sdata = []
        for i in range(len(uuids)):
            sdata.append(pd.read_csv(data_dir + uuids[i]+".csv"))
            absoluteTime = []
            for j in range(len(sdata[i])):
                absoluteTime.append(self.toTimestamp(sdata[i]["Timestamp"].values[j]))
            sdata[i]["absoluteTime"] = absoluteTime
            sdata[i]["PM1"] = sdata[i]["PM1"].values / factors[i][0]
            sdata[i]["PM2.5"] = sdata[i]["PM2.5"].values / factors[i][1]
            sdata[i]["PM10"] = sdata[i]["PM10"].values / factors[i][2]
            sdata[i]["temperature"] = sdata[i]["temperature"].values / factors[i][3]
            sdata[i]["humidity"] = sdata[i]["humidity"].values / factors[i][4]
        return sdata
            
    def loadAirSpeckP(self, start_date, end_date, sids, data_dir):
        payload = {
            'username': 'jupyter',
            'password': 'd84hr75yG4fE',
            'form.submitted':'Login'
        }
        
        with requests.Session() as s:
            s.headers.update({'referer': 'https://dashboard.specknet.uk'})
            p = s.post('https://dashboard.specknet.uk/login', data=payload)
            # print the html returned or something more intelligent to see if it's a successful login page.
            print(p.text)

        ## An authorised request.
        for sid in sids:
            url = 'https://dashboard.specknet.uk/downloadPersonalAirspeck/' + sid + '/' + str(start_date) + '/' + str(end_date)
            print(url)
            r = s.get(url)
            open(data_dir + "/" + str(sid) + '_' + str(start_date) + '.csv', 'wb').write(r.content)
                
    def readAirSpeckPCSV(self, start_date, end_date, data_dir):
        sids = ['XXM007', 'XXM008']
        factors = [[5.05004303, 4.86456945, 4.72626118, 1.16005363, 0.74392267],
             [5.09431241, 4.90857996, 4.6303786, 1.18617219, 0.7362692  ]]
        
        pdata = []
        for i in range(len(sids)):
            pdata_by_day = []
            pdata_by_day.append(pd.read_csv(data_dir + "/" + str(sids[i]) + '_' + str(start_date) + '.csv'))
        
            pdata_by_sid = pd.concat(pdata_by_day)
            pdata.append(pdata_by_sid)
            absoluteTime = []
            for k in range(len(pdata[i])):
                absoluteTime.append(self.toTimestamp(pdata[i]["Timestamp"].values[k]))
            pdata[i]["absoluteTime"] = absoluteTime
            pdata[i]["PM1"] = pdata[i]["PM1"].values / factors[i][0]
            pdata[i]["PM2.5"] = pdata[i]["PM2.5"].values / factors[i][1]
            pdata[i]["PM10"] = pdata[i]["PM10"].values / factors[i][2]
            pdata[i]["temperature"] = pdata[i]["temperature"].values / factors[i][3]
            pdata[i]["humidity"] = pdata[i]["humidity"].values / factors[i][4]
        return pdata
        
        
        