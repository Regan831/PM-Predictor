##Adapted from Andrew Bates' code at https://github.com/specknet/airspeck-comparison/blob/master/6%20Airspeck%20S.ipynb
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
import time
import os


from bokeh.io import show, output_notebook, output_file, reset_output
from bokeh.plotting import figure
import  requests
import pandas as pd

class DataDownloader(object):
    
    def toTimestamp(self, date):
            date = datetime.strptime(date.split(".")[0], "%Y-%m-%d %H:%M:%S")
            return time.mktime(date.timetuple())

    def loadAirSpeckS(self, start_date, end_date, data_dir):
        uuids = ["B2BC10D2B9F14328", 'FD368D7D6B815C1B', '229B8913D6A5B970', 'DA1F257AD20C85A7',
            '9C4F842B28FC5971', '3AB8A58A952B89B6', 'AE93FD8053BFDDFD', '3BC10C97D2490E7B',
            '660CB9BC2A97231A', 'F753DAAE895C0DEB']

        
        with requests.Session() as s:
            s.headers.update({'referer': 'https://dashboard.specknet.uk'})
            p = s.post('https://dashboard.specknet.uk/login', data=payload)
                # print the html returned or something more intelligent to see if it's a successful login page.
#             print(p.text)

        ## An authorised request.
        for u in uuids:
            url = 'https://dashboard.specknet.uk/downloadStaticAirspeck/' + u + '/' + str(start_date) + '/' + str(end_date)
            r = s.get(url)
            open(data_dir + "/" + str(u) + '.csv', 'wb').write(r.content)
            
    def readAirSpeckSCSV(self, start_date, end_date, data_dir):
        uuids = ["B2BC10D2B9F14328", 'FD368D7D6B815C1B', '229B8913D6A5B970', 'DA1F257AD20C85A7',
            '9C4F842B28FC5971', '3AB8A58A952B89B6', 'AE93FD8053BFDDFD', '3BC10C97D2490E7B',
            '660CB9BC2A97231A', 'F753DAAE895C0DEB']
        
        factors = [[1.0 ,        1.96136704053 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.89133597535 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        1.83537667641 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.54733398945 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.04216376741 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.42453772033 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.37690917896 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.76145339021 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        2.35869648906 ,       1.0 , 1.0    ,     1.0            ],
                  [1.0 ,        1.53821777337 ,       1.0 , 1.0    ,     1.0            ]]
        
        sdata = []
        for i in range(len(uuids)):
            if (os.path.isfile(data_dir + uuids[i]+".csv")):
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
        sids = ['XXE101', 'XXE102', 'XXE103', 'XXE104']
        factors = [[1, 1.78779367671, 1, 1, 1],
                 [1, 1.13096151596, 1, 1, 1  ],
                 [1, 1.79901752348, 1, 1, 1  ],
                 [1, 1.27183615641, 1, 1, 1  ]]
        
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
        
        
        