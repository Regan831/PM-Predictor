import numpy as np

class Constants(object):
    corners = np.array([[55.94686, -3.19665], #NW
                    [55.94686, -3.18123], #NE
                    [55.93814, -3.18123], #SE
                    [55.93814, -3.19665]]) #SW
    
    gridSize = 20
    
    finalStaticCoords = np.array([[55.9454333, -3.1913917], #E5FD8C55EAA37555 Lauriston  
                            [55.9397722,-3.1915444], #02E5F77764B873DA Melville
                            [55.9430028,-3.1921472], #200A7CED9D597407 Library 
                            [55.940953, -3.186092], #AA0E63CF5118F98F Tennis court
                            [55.945302, -3.188279], #B61241EF668DBC2C  Bristo Square
                            [55.943014, -3.185994]]) #E786F1568F65C296 Buccleuch Place
    
    #22 days of data collection
    allCollectedDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180724, 20180725, 20180726, 20180730, 20180731, 20180801, 20180802, 20180803, 20180806, 20180807, 20180808, 20180809] 
    
    #On 20180725, 20180731 and 20180803, there were issues with the collection
    selectCollectedDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180724, 20180726, 20180730, 20180801, 20180802, 20180806, 20180807, 20180808, 20180809] 
#     selectCollectedDates = [20180629] 
    
    #Dates than all ML tuning experiments were run on
    experimentCollectedDates = [20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180726]
    
    recentCollectedDates = [20180807, 20180808, 20180809]
    doubleCollectionDates = [20180704, 20180706, 20180802, 20180803] #(but 20180803 is bad)
        
    sixDates = [20180703, 20180706, 20180716, 20180724, 20180726, 20180801]
    thirteenDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180726, 20180801, 20180807]
    sixteenDates = [20180629, 20180703, 20180704, 20180705, 20180706, 20180709, 20180710, 20180716, 20180719, 20180723, 20180724, 20180726, 20180801, 20180806, 20180807, 20180808]
    
    def getGridSize(self):
        return self.gridSize
    
    def getCorners(self):
        return self.corners
    
    def getStaticCoords(self):
        return self.finalStaticCoords
    
    def getAllCollectedDates(self):
        return self.allCollectedDates
    
    def getRecentCollectedDates(self):
        return self.recentCollectedDates
    
    def getDoubleCollectedDates(self):
        return self.doubleCollectionDates
    
    def getSelectCollectedDates(self):
        return self.selectCollectedDates
    
    def getExperimentCollectedDates(self):
        return self.experimentCollectedDates
    
    def getSixDates(self):
        return self.sixDates
    
    def getTenDates(self):
        return self.experimentCollectedDates
    
    def getThirteenDates(self):
        return self.thirteenDates
    
    def getSixteenDates(self):
        return self.sixteenDates
    
    def getNineteenDates(self):
        return self.selectCollectedDates
