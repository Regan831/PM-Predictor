import csv
from constants import Constants
import pandas as pd
import numpy as np
import os
import tensorflow as tf
import time

def load_data(GRID_SIZE, collected_data_dates, PM_index):
    init_X = False  # define whether X is initialized
    init_Y = False  # define whether Y is initialized

    PMstrs = ['PM1', 'PM2.5', 'PM10']
 
    
    osm_dir = "/Users/zoepetard/Google Drive/Edinburgh/MscProj/FillingTheGaps/data/osm/"
    LU_file = osm_dir + "landuse_grid" + str(GRID_SIZE) + ".csv"
    road_file = osm_dir + "roadtype_grid" + str(GRID_SIZE) + ".csv"
    
    pd_df1=pd.read_csv(LU_file, sep=',',header=None, skiprows=1)
    landuse = pd_df1.values
    pd_df2=pd.read_csv(road_file, sep=',',header=None, skiprows=1)
    roadtype = pd_df2.values
    static_dir = "/Users/zoepetard/Google Drive/Edinburgh/MscProj/FillingTheGaps/data/train/"

    for date in collected_data_dates:
        PM_file = static_dir + str(date) + "/" + PMstrs[PM_index] + "/" + str(date) + "_grid" + str(GRID_SIZE) + "_ordinaryKriging.csv"
        pd_df=pd.read_csv(PM_file, sep=',',header=None)
        PM2pt5 = pd_df.values
        
        env_file = static_dir + str(date) + "/" + str(date) + "_grid" + str(GRID_SIZE) + ".csv"
        with open(env_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            medianTime = pd.to_datetime(next(reader)[0])
            averageTemp = next(reader)[0]
            averageHum = next(reader)[0]
            
        hum = np.zeros((GRID_SIZE, GRID_SIZE)) + float(averageHum)
        holder = np.ones((GRID_SIZE, GRID_SIZE)) #Placeholder if layers are to be excluded in the next line

        x = np.array([landuse, roadtype, PM2pt5, hum])

        x = np.transpose(x, (1, 2, 0))

        x = np.expand_dims(x,0)
        if not init_X:
            X = x
            init_X = True
        else:
            X = np.vstack([X,x])
         
        sids = ['XXM007', 'XXM008']
        label_dir = "/Users/zoepetard/Google Drive/Edinburgh/MscProj/FillingTheGaps/data/label/"+str(date)+"/"
        label_file = label_dir + sids[0] + "_" + str(date) + "_" + PMstrs[PM_index] + "_grid" + str(GRID_SIZE) + ".csv"
        labels_found = False
        
        if (os.path.isfile(label_file)):
            labels_found = True
        else:
            label_file = label_dir + sids[1] + "_" + str(date) + "_" + PMstrs[PM_index] + "_grid" + str(GRID_SIZE) + ".csv"
            if (os.path.isfile(label_file)):
                labels_found = True
        if(labels_found):
            pd_df=pd.read_csv(label_file, sep=',',header=None, skiprows=3)
            labels = pd_df.values
        else:
            print("no labels found")
          
        y = np.array(labels)

        y = np.expand_dims(y,0)
        if not init_Y:
            Y = y
            init_Y = True
        else:
            Y = np.vstack([Y,y])

    Y = np.expand_dims(Y,3)

    return X, Y

def go_forward(Xtf, kernel_size):

    # PARAMETERS
    W1 = tf.get_variable("W1",shape=[kernel_size,kernel_size,4,32],initializer=tf.contrib.layers.xavier_initializer(seed=0),dtype="float")
    W2 = tf.get_variable("W2",shape=[kernel_size,kernel_size,32,64],initializer=tf.contrib.layers.xavier_initializer(seed=0),dtype="float")
    W3 = tf.get_variable("W3",shape=[kernel_size,kernel_size,64,128],initializer=tf.contrib.layers.xavier_initializer(seed=0),dtype="float")
    W4 = tf.get_variable("W4",shape=[kernel_size,kernel_size,128,1],initializer=tf.contrib.layers.xavier_initializer(seed=0),dtype="float")

    # LAYER 1. pdding="SAME" ensures grid remains 20x20. Try without this?
    Z1 = tf.nn.conv2d(Xtf,W1,strides=[1,1,1,1],padding="SAME")
    A1 = tf.nn.relu(Z1)

    # LAYER 2
    Z2 = tf.nn.conv2d(A1,W2,strides=[1,1,1,1],padding="SAME")
    A2 = tf.nn.relu(Z2)

    # LAYER 3
    Z3 = tf.nn.conv2d(A2,W3,strides=[1,1,1,1],padding="SAME")
    A3 = tf.nn.relu(Z3)

    # LAYER 4
    Z4 = tf.nn.conv2d(A3,W4,strides=[1,1,1,1],padding="SAME")
    A4 = tf.nn.sigmoid(Z4)

    return A4

def split_data(X, Y, train_p, test_p, test=False):
    train_indx = int(X.shape[0]*train_p)
    #test_indx = int(X.shape[0]*test_p)

    x_train = X[:train_indx,:,:]
    y_train = Y[:train_indx,:,:]
    
    #if test:
    #    test_indx = int(data.shape[0]*test_p)
    #    test = data[train_indx:train_indx + test_indx,:,:]
    #    val = data[train_indx + test_indx:, :, :]
    #    test_y = masks[train_indx:train_indx + test_indx,:,:]
    #    val_y = masks[train_indx + test_indx:, :, :]
    #    return train, test, val, train_y, test_y, val_y
    #else:
    x_val = X[train_indx:,:,:]
    y_val = Y[train_indx:,:,:]
    return x_train, x_val, y_train, y_val

def compute_cost(A4, Y):
    diff_squared = tf.pow((A4 - Y), 2)
    zeros = tf.zeros_like(Y) 
    mask = tf.greater(Y, zeros) 
    masked = tf.boolean_mask(diff_squared, mask)
    cost = tf.reduce_sum(masked) 
    return cost

def train(X, Y, train_perc, kernel_size, GRID_SIZE, valid_date, PM_index, learning_rate):
    #Tensorflow placeholders
    PMstrs = ['PM1', 'PM2.5', 'PM10']
    PM_str = PMstrs[PM_index]

    tf.reset_default_graph()
    best_score = 0.
    best_iter = 0
    start_time = time.time()
    max_duration = 900
    max_iterations = 300
    X_train, X_valid, Y_train, Y_valid = split_data(X, Y, train_perc, (1 - train_perc), False)
    train_costs = [1] * max_iterations
    valid_costs = [1] * max_iterations
    
    with tf.Session() as sess:
        Xtf = tf.placeholder(name="Xtf",shape=[None,GRID_SIZE,GRID_SIZE,4],dtype="float")
        Ytf = tf.placeholder(name="Ytf",shape=[None,GRID_SIZE,GRID_SIZE,1],dtype="float")
        
        A4 = go_forward(Xtf, kernel_size)
        cost = compute_cost(A4,Ytf)
        optimizer = tf.train.RMSPropOptimizer(learning_rate=learning_rate).minimize(cost)
        init = tf.global_variables_initializer()
        sess.run(init)
        for i in range(max_iterations):
            X_tr, Y_tr = X_train, Y_train
            pred, train_costs[i] = sess.run([optimizer,cost],feed_dict={Xtf:X_tr,Ytf:Y_tr})
            valid_costs[i] = sess.run(cost,feed_dict={Xtf:X_valid,Ytf:Y_valid})

            print("\n************************")
            print("iter:",i)
            print("training cost:",train_costs[i])
            print("valid cost:",valid_costs[i])
            print("************************\n")

            if train_costs[i] < best_score and best_iter <= i-10:
                print("Converged")
                break
            # elif time.time() >= start_time + max_duration:
            #     print("timed out")
            #     break
            else:
                best_score = train_costs[i]
                best_iter = i
        
        prediction, iou_pred = sess.run([A4,cost],{Xtf:X_valid,Ytf:Y_valid})
        print("validation cost: ",iou_pred)
        print("prediction: ", prediction) #Useful to see if model converged

        directory = '../results/tune10examples/learning_rate/learning_rate_' +str(learning_rate) + '/kernel_size_' +str(kernel_size) + '/valid_date_'+str(valid_date)+'/'

        np.savetxt(directory + PM_str +"_train_cost.csv", train_costs)
        np.savetxt(directory + PM_str +"_valid_cost.csv", valid_costs)
        np.savetxt(directory + PM_str +"_Y_valid.csv", np.squeeze(Y_valid))
        np.savetxt(directory + PM_str +"_prediction.csv", np.squeeze(prediction))
    
def main():
    constants = Constants()
    GRID_SIZE = constants.getGridSize()
    collected_data_dates = constants.getTenDates()
    PMstrs = ['PM1', 'PM2.5', 'PM10']

    #Example values for performing a grid search over kernel size and learning rate
    kernel_sizes = [1]#[1, 2, 3]
    learning_rates = [0.0005]#[0.005, 0.001, 0.0005,  0.0001]

    for kernel_size in kernel_sizes:
        for learning_rate in learning_rates:
            PM_index = 1 #Train only on PM2.5
            PM_str = PMstrs[PM_index]
            for i in range(np.shape(collected_data_dates)[0]):
                valid_date = collected_data_dates[np.shape(collected_data_dates)[0] - 1]
                print("iteration i : ", i, "valid_date : ", valid_date)
                X, Y = load_data(GRID_SIZE, collected_data_dates, PM_index)
                directory = os.path.dirname('../results/tune10examples/learning_rate/learning_rate_' +str(learning_rate) + '/kernel_size_' +str(kernel_size) + '/valid_date_'+str(valid_date)+'/')

                if not os.path.exists(directory):
                    os.makedirs(directory)
        
                train(X, Y, 0.95, kernel_size, GRID_SIZE, valid_date, PM_index, learning_rate)
                collected_data_dates = np.roll(collected_data_dates, 1)
                valid_date = collected_data_dates[np.shape(collected_data_dates)[0] - 1]

main()