##Class to read OSM files '.geojson' files and plot polygons or lines using folium
import folium
import json
from shapely.geometry import Point, MultiPolygon, Polygon, mapping
import shapely
import numpy as np
from grid_definition import GridDefinition

class OSMReader(object):
    
    colors = []
    
    def init(self):
        self.colors = ["red", "orange", "yellow", "green", "blue", "purple", "#778899"]
        
    def assignColor(self, pm, maxPM, minPM):
        rangePM = maxPM - minPM
        if pm > 99999:
            return "#000000"
        elif pm < (0.1 * rangePM + minPM):
            color = "#1b7837"
        elif pm < (0.2 * rangePM + minPM):
            color ="#5aae61"
        elif pm < (0.3 * rangePM + minPM):
            color ="#a6dba0"
        elif pm < (0.4 * rangePM + minPM):
            color ="#d9f0d3"
        elif pm < (0.5 * rangePM + minPM):
             color ="#f7f7f7"
        elif pm < (0.6 * rangePM + minPM):
            color = "#e7d4e8"
        elif pm < (0.7 * rangePM + minPM):
            color = "#c2a5cf"
        elif pm < (0.8 * rangePM + minPM):
            color = "#9970ab"
        else:
            color ="#762a83"
        return color

    def addRoadType(self, mapObj, roadGeo, num):
        if(len(roadGeo) > 0):
            folium.GeoJson(roadGeo, 
                  style_function=lambda x: {
                        'color' : self.colors[num],
                        'weight' : 4.0
            }
                  ).add_to(mapObj)
    
    def addLandUse(self, mapObj, landUse, num):
        colors = ["red", "orange", "yellow", "green", "blue", "purple", "#778899"]
        folium.GeoJson(landUse, 
              style_function=lambda x: {
                    'color' : "red",
                    'fillColor' : colors[num],
                    'fillOpacity': 0.0
        }
              ).add_to(mapObj)
        
    def addCellPM(self, mapObj, cell, PM, maxPM, minPM):
        #colors = ["red", "orange", "yellow", "green", "blue", "purple"]
        color = self.assignColor(PM, maxPM, minPM)
        folium.GeoJson(cell, 
              style_function=lambda x: {
                    'color' : 'red',
                    'fillColor' : 'red',
                    'fillOpacity': 0.0
        }
              ).add_to(mapObj)
        
    def getRoadGeoClasses(self):
        with open('../OSM/test-area-lines.geojson') as f:
            lines = json.load(f)
    
        roads1 = []
        roads2 = []
        roads3 = []
        roads4 = []
        roads5 = []    
        roads6 = []

        for feature in lines["features"]:
            if "highway" in feature["properties"]:
                if (feature["properties"]["highway"] == "primary" ):
                    roads1.append(feature)
                if feature["properties"]["highway"] == "secondary" :
                    roads2.append(feature)
                if feature["properties"]["highway"] == "tertiary" or feature["properties"]["highway"] == "tertiary_link" : 
                    roads3.append(feature)
                if (feature["properties"]["highway"] == "unclassified" ):
                    roads4.append(feature)
                if feature["properties"]["highway"] == "residential" or feature["properties"]["highway"] == "service" : 
                    roads5.append(feature) 
                if (feature["properties"]["highway"] == "footway" 
                    or feature["properties"]["highway"] == "cycleway"
                    or feature["properties"]["highway"] == "pedestrian"
                    or feature["properties"]["highway"] == "path"
                    or feature["properties"]["highway"] == "steps"): 
                    roads6.append(feature) 

        roads1geo = {
            'type': 'FeatureCollection',
            'features': roads1
        }

        roads2geo = {'type': 'FeatureCollection', 'features': roads2}
        roads3geo = {'type': 'FeatureCollection', 'features': roads3}
        roads4geo = {'type': 'FeatureCollection', 'features': roads4}
        roads5geo = {'type': 'FeatureCollection', 'features': roads5}
        roads6geo = {'type': 'FeatureCollection', 'features': roads6}
    
        roadGeos = [roads1geo, roads2geo, roads3geo, roads4geo, roads5geo, roads6geo]
    
        return roadGeos
    
    def getLandGeoClasses(self):
        with open('../OSM/test-area-multipolygons.geojson') as f:
            shapes = json.load(f)
    
        areas1 = [] #industrial
        areas2 = [] #commercial
        areas3 = [] #residential
        areas4 = [] #parks
        areas5 = []    
        areas6 = []

        for feature in shapes["features"]:
            if "landuse" in feature["properties"]:
                if feature["properties"]["landuse"] == "grass" :
                    areas4.append(feature)
                if feature["properties"]["landuse"] == "commercial" :
                    areas2.append(feature)
            if "leisure" in feature["properties"]:
                if (feature["properties"]["leisure"] == "park" 
                    or feature["properties"]["leisure"] == "garden"):
                    areas4.append(feature)
            if "amenity" in feature["properties"]:
                if feature["properties"]["amenity"] == "grave_yard":
                    areas4.append(feature)
                if feature["properties"]["amenity"] == "school":
                    areas2.append(feature)
            if "building" in feature["properties"]:
                if (feature["properties"]["building"] == "house" 
                    or feature["properties"]["building"] == "apartments"
                    or feature["properties"]["building"] == "residential"
                    or feature["properties"]["building"] == "detached"):
                    areas3.append(feature)
                if (feature["properties"]["building"] == "yes" 
                    or feature["properties"]["building"] == "university"
                    or feature["properties"]["building"] == "church"
                    or feature["properties"]["building"] == "office"
                    or feature["properties"]["building"] == "museum"
                    or feature["properties"]["building"] == "school"):
                    areas2.append(feature)
            
        areas1geo = {
            'type': 'FeatureCollection',
            'features': areas1
        }

        areas2geo = {'type': 'FeatureCollection', 'features': areas2}
        areas3geo = {'type': 'FeatureCollection', 'features': areas3}
        areas4geo = {'type': 'FeatureCollection', 'features': areas4}
        areas5geo = {'type': 'FeatureCollection', 'features': areas5}

        areaGeos = [areas1geo, areas2geo, areas3geo, areas4geo, areas5geo]
        return areaGeos
                    
    def getCellsWithMajorLU(self):
        areaGeos = self.getLandGeoClasses()
        cells = self.getGeoCells()
                    
        for cell_num, cell in enumerate(cells):
            cell_multi = cell[0]["geometry"]
            cell_shape = shapely.geometry.asShape(cell_multi)
            major_LU = 0
            major_LU_index = 0
        
            for LU_level, areaGeo in enumerate(areaGeos):
                features = areaGeo["features"]
                area = 0
                for feat in range(len(features)):
                    landuse_multi = areaGeo["features"][feat]["geometry"] 
                    landuse_shape = shapely.geometry.asShape(landuse_multi)
                    intersection = cell_shape.intersection(landuse_shape)
                    area += intersection.area
                if (area > major_LU):
                    major_LU = area
                    major_LU_index = LU_level
            if (major_LU_index == 0): #if there are no landuses in the cell, make it the middle land use category
                major_LU_index = 2
            cells[cell_num][0]["properties"]["major_LU"] = major_LU_index
        return cells
                    
    def getGeoCells(self):
        grid_definition = GridDefinition()
        grid_definition.init()   
        gridSize = grid_definition.getGridSize()
        topLat = grid_definition.getTopLat()
        bottomLat = grid_definition.getBottomLat()
        leftLon = grid_definition.getLeftLon()
        rightLon = grid_definition.getRightLon()
                    
        height = topLat - bottomLat
        width = rightLon - leftLon

        heightInterval = height / gridSize
        widthInterval = width / gridSize
                    
        cells = []
        for r in range(gridSize):
            top = topLat - r * heightInterval
            bottom = topLat - (r+1) * heightInterval
            for c in range(gridSize):
                cellTuple = []
                left = leftLon + c * widthInterval
                right = leftLon + (c + 1) * widthInterval
                cellTuple.append(tuple([left, top]))
                cellTuple.append(tuple([right, top]))
                cellTuple.append(tuple([right, bottom]))
                cellTuple.append(tuple([left, bottom]))
                cellTuple.append(tuple([left, top]))
                polygon = Polygon(cellTuple)
                m = MultiPolygon([polygon])
                feature = [{'type': 'Feature', 'properties': {'type': 'multipolygon'}, 'geometry': mapping(m)}]
                multi =  {'type': 'FeatureCollection', 'features': feature}
                cells.append(feature)
        return cells
        
                    