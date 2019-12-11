# PM-Predictor

## Introduction
Included are a collection of notebooks, models, and helpers used in writing my Master's Dissertation at University of Edinburgh. The purpose of the dissertation was to explore methods to predict Particulate Matter (PM) across time and space. The main direction of the paper examined online learning methods vs. pretrained learning methods, ensemble models, and deep learning vs. classical approaches. 

Two types of sensors were used in collecting data: one mobile and one stationary. The stationary sensors were setup for the entirity of summers 2018 and 2019, and up to 4 mobile sensors were used both summers. The mobile sensors required someone to walk around while carrying a sensor in order to collect data.

First the area used for exploration was split into a 20x20 grid roughly 50 x 50 meters in size. Within this grid  Two methods were used in setting up the prediction models. One where there is a neural network (NN) setup for each cell with a stationary sensor and a Passive-Agressive Regressor (PAR) on all other cells. The second method uses one single NN for all cells. This second method requires a way to interpolate predictions across the entire grid. Tests were conducted to see if statistical methods such as Ordinary Krieging were as powerful as a Convulutional Neural Network (CNN).

The second method with a CNN had the most predictive power.

This work could be enhanced with more features being extracted for use. Only land use, road type, humidity, temperature, time, and PM values were collected.

**Abstract from dissertation**

As air pollution levels rise in urban areas and in developing countries, methods for predicting pollution levels in both the spatial and temporal aspect are necessary. Air pollution is a leading cause of cardiovascular diseases, strokes, cancer and asthma. Proposed is a new model to predict spatio-temporal air pollution, specifically Particulate Matter (PM) levels. Included are a state-of-the-art Convolutional Neural Network (CNN) to spatially interpolate PM values, and a novel method of building a model that predicts temporally using a single Artificial Neural Network (ANN) which uses land usage, and road type as input features. A combination of the two are used to predict spatio-temporally. Both mobile data and stationary data are used in training of the model. The model uses online learning to improve adaptability as well as ensembles to improve generalization. Experiments on different grid size, online update rules, larger datasets, and mobile data are included.

This work shows that ANNs can effectively be used to predict PM values temporally, spatially, and spatio-temporally. The proposed model ensemble was the only model that was able to perform better than the baseline in temporal predictions with an MAE of 0.124 on the 2018 dataset. The spatial CNN introduced in this work improved upon previous best MAPE spatial interpolation by 3 percentage points and the previous best CNN model by 17 percentage points with an MAPE of 39.10\%. The spatio-temporal predictions on the 2018 datasets also had positive results. For the 2018-A dataset, the proposed model predicted better than the previous best with an MAE of 1.50. On the 2018-B dataset, the proposed model's MAE was 1.16 which was also better than the previous best MAE of 1.21.

A new dataset was also collected for central Edinburgh that used ten stationary sensors and up to four concurrent mobile sensors. The proposed model set a baseline MAPE of 17.20\% for temporal predictions and 56.89\% for spatio-temporal predictions. 


## Files
**temporal_pred** - Notebook which uses method one (multiple NNs) to make strictly temporal predictions.
**continuous-Pred-Grid-CNN** - Notebook using method two (one NN for entire grid) to make temporal predictions then uses a CNN to fill in empty cells.
**continuous-Pred-Grid-OK** - Notebook using method two (one NN for entire grid) to make temporal predictions then uses a Ordinary Krieging to fill in empty cells.
