code - 
	- Calibration.ipynb - notebook to calibrated between eight sensors during the colocation period (populates and uses data/20180601-20180615 folder)
	- constants.py - define constants such as grid size, static sensor location, and different collection dates datasets
	- data_download.py - pull and read AirSpeck data
	- grid_definition.py - define edge latitude and logitudes of test area
	- MAPE.ipynb - interpolate between six stationary sensors using five interpolation methods and calculate Mean Average Percentage Error of interpolation and CNN models
	- MapSensors.ipynb - plotting of stationary and mobile air pollution sensor data
	- model10.py - CNN tuned to 10 examples
	- model19.py - CNN tuned to 19 examples (includes L2 regularistion and dropout)
	- osm_reader.py - class to read OSM files '.geojson' files and plot polygons or lines using folium
	- Preprocess.ipynb - notebook to pull and format data for use in interpolations and CNN training (populates data/label and data/train files)
	- SpatialGeometry.ipynb -  reads OSM data and creates a grid of cells tagged by their primary land use or road type label

data - 
	20180601-20180615 - data used for sensor calibration
	label - 20x20 grid of labelled cells created from validation data collection walks
	osm - land use and road type information in csv format for 20x20 grid
	raw - raw data from stationary and mobile/personal sensors
	train - interpolations (linear, spline, ordinary kriging, universal kriging, gaussian RBF) of PM1, PM2.5 and PM10 data to be used as input to the CNN

images - examples of maps created using shapely and folium

OSM - 'lines' and 'multipolygons' layers of OpenStreetMap data of the test area in Edinburgh

results - predicted air pollution values and training and validation costs from CNNs trained on 6, 10, 13, 16 and 19 training examples
