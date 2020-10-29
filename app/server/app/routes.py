from app import app
from flask import jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json

import pickle
import joblib as joblib
import pandas as pd
import numpy as np
import lightgbm as lb


import os
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD 
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from keras.callbacks import ModelCheckpoint, EarlyStopping
# from pylab import rcParams
import itertools
from statsmodels.tsa.stattools import adfuller
from keras.models import load_model


cors = CORS(app, resources={r"/*": {"origins": "*"}})

# LOAD DATA GLOBALLY
df = pd.read_csv('data/ocean-waves-clean.csv')


# ---------------------------------------------------------------------------------------------------------------------------------
# DATA PREPARATION 
# ---------------------------------------------------------------------------------------------------------------------------------

# LOAD
data = pd.read_csv('data/ocean-waves-clean.csv')

# PREPARE WAVES DATA SET

n_last = 12
n_rows = data.shape[0] - n_last

waves = data.head(n_rows)       # remove last n_rows to predict

future_vals = data.tail(n_last) # keep n_last rows as 'future' values

predictions_df = waves[['DateTime']].copy()

# ---------------------------------------------------------------------------------------------------------------------------------
# PEAK PERIOD MODEL
# ---------------------------------------------------------------------------------------------------------------------------------

# Load from file
peakperiod_fname = 'data/peakperiod.pkl'
with open(peakperiod_fname, 'rb') as file:
    peakperiod_model = pickle.load(file)

# Feature Engineering      --------------------------------------------------------

# Features for final prediction
peakperiod_df = waves[["CottMeanPeriod", "RottMeanPeriod", "CottRadiansRotated"]]

# ---------------------------------------------------------------------------------

# Make prediction
peakperiod_pred = peakperiod_model.predict(peakperiod_df)

# Update result_df
predictions_df['CottPeakPeriod'] =  peakperiod_pred

predictions_df['CottPeakPeriod'] = np.exp(predictions_df['CottPeakPeriod'])



# ---------------------------------------------------------------------------------------------------------------------------------
# DIRECTION MODEL
# ---------------------------------------------------------------------------------------------------------------------------------

# PREPARATION
def retrieve_direction(rotated_radian):
    deg = 180 * ((rotated_radian + np.pi) / np.pi) + 40
    if deg >= 360:
        deg -= 360
    return deg


# Load from file
direction_fname = 'data/direction.joblib'
direction_model = joblib.load(direction_fname)

# Feature Engineering      --------------------------------------------------------

# Features for final prediction
direction_df = waves[['RottRadiansRotated', 'RottHeight', 'Month']]

# ---------------------------------------------------------------------------------

# Make prediction
direction_pred = direction_model.predict(direction_df)

# Update result_df
predictions_df['CottDirection'] =  direction_pred
predictions_df['CottDirection'] = predictions_df['CottDirection'].apply(retrieve_direction)




# ---------------------------------------------------------------------------------------------------------------------------------
# WAVE HEIGHT MODEL
# ---------------------------------------------------------------------------------------------------------------------------------

# Load from file
height_fname = 'data/height.pkl'
with open(height_fname, 'rb') as file:
    height_model = pickle.load(file)

# Feature Engineering      --------------------------------------------------------

# extract the hour, day, and month
height_df = waves.copy()
time_series = pd.to_datetime(height_df['DateTime'])
height_df['month'] = time_series.dt.month
height_df['day'] = time_series.dt.day
height_df['hour'] = time_series.dt.hour

del height_df['DateTime']
del height_df['CottPeakPeriod']
del height_df['CottDirection']

order = ['month', 'day', 'hour', 'RottHeight', 'RottPeakPeriod', 'RottDirection', 'CottHeight']
height_df = height_df[order]

# use bin method to treat time feature as category variable
# After applying to the model, we found that the "bins of hour" almost has no effect on the model result,
# so we remove it to reduce dimension in case of overfitting. 

bins_of_month = [0, 4 ,7, 9, 13]
height_df['month'] = pd.cut(height_df['month'], bins_of_month, labels=[1, 2, 3, 4])

bins_of_day = [0, 10 ,20, 32]
height_df['day'] = pd.cut(height_df['day'], bins_of_day, labels=[1, 2, 3])

# bins_of_hour = [-1, 6 ,12, 18, 25]
# df['hour'] = pd.cut(df['hour'], bins_of_hour, labels=[1, 2, 3,4])
del height_df['hour']

# use OneHot Encoding to make all values of the categorical features are equally away from each other,
# and it help to avoid the overfitting caused by the gradient descent in high dimension. 
col_names = ['month','day']
for col in col_names:  
    OnehotEn = pd.get_dummies(height_df[col], prefix=col)
    height_df.drop([col], axis=1, inplace=True)
    height_df = pd.concat([height_df, OnehotEn], axis=1)


#normalize numerical feature to make the model faster to find the optimal solution during training
z_scaler = lambda x : (x - np.mean(x)) / np.std(x)
height_df_ = height_df[['RottHeight', 'RottPeakPeriod', 'RottDirection']].apply(z_scaler)

del height_df['RottHeight']
del height_df['RottPeakPeriod']
del height_df['RottDirection']

height_df = pd.concat([height_df,height_df_],axis=1)
label_y = height_df['CottHeight']
height_df.drop(['CottHeight'], axis=1, inplace=True)

# ---------------------------------------------------------------------------------

# Make prediction
height_pred = height_model.predict(height_df)

# Update result_df
predictions_df['CottHeight'] =  height_pred


# --------------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------------------
# ADD ROTTNEST BUOY DATA TO DF 
# ---------------------------------------------------------------------------------------------------------------------------------
rottdata = waves[["RottPeakPeriod", "RottDirection", "RottHeight"]]

predictions_df = predictions_df.join(rottdata)



# ---------------------------------------------------------------------------------------------------------------------------------
# TIME TO GET SIGNIFICANT SUMMARY STATS FROM DATA
# ---------------------------------------------------------------------------------------------------------------------------------

# ERROR, LOSS OF MODELS
confidence_height_model = 100
confidence_period_model = 100
confidence_forecast_model = 100

# FORECAST DATA.
max_forecast_height = 100 # dummyForecast["CottHeight"].max()

# DAY.
day_data = predictions_df.tail(49)

max_cottheight_day = day_data["CottHeight"].max()
max_cottperiod_day = day_data["CottPeakPeriod"].max()

# WEEK.
week_data = predictions_df.tail(295)

max_cottheight_week = day_data["CottHeight"].max()
max_cottperiod_week = day_data["CottPeakPeriod"].max()

# MONTH.
month_data = predictions_df.tail(1441)

max_cottheight_month = day_data["CottHeight"].max()
max_cottperiod_month = day_data["CottPeakPeriod"].max()

# CONSTRUCT RETURN OBJECT FOR BACKEND
stats = {
    'waveHeight': {
      'day': round(max_cottheight_day,2),
      'week': round(max_cottheight_week,2),
      'month': round(max_cottheight_month,2),
      'confidence': round(confidence_height_model,2)
    },
    'peakPeriod': {
      'day': round(max_cottperiod_day,2),
      'week': round(max_cottperiod_week,2),
      'month': round(max_cottperiod_month,2),
      'confidence': round(confidence_period_model,2)
    },
    'forecast': {
      'height': round(max_forecast_height,2),
      'period': 0,
      'confidence': {
        'waveHeight': round(confidence_forecast_model,2),
        'peakPeriod': 0,
        'direction': 0
      }
    },
    'direction': {
      'confidence': 0
    }
  }
# ---------------------------------------------------------------------------------------------------------------------------------
# 
# ---------------------------------------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------------------------------------
# HISTORY ROUTE
# ---------------------------------------------------------------------------------------------------------------------------------
preds = predictions_df.copy()
preds = preds[["DateTime", "CottHeight", "CottPeakPeriod", "CottDirection"]]
preds = preds.rename(columns={"CottHeight": "CottHeightPred", "CottPeakPeriod": "CottPeakPeriodPred", "CottDirection": "CottDirectionPred"})

history_data = pd.concat([preds, waves[["CottHeight", "CottPeakPeriod", "CottDirection"]]], axis=1).to_dict(orient='records')
# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------
# FORECASTING MODELLING
# ---------------------------------------------------------------------------------------------------
model_to_load = 'data/CottHeight_Uni_12_Step_HeightWeights.h5'
steps_future= 12

waves = data.copy()
# waves['DateTime'] = waves.index   # keep DateTime as a separate col for plotting

# ---------------------------------------------------------------------------------------------------
# 
# ---------------------------------------------------------------------------------------------------








# ---------------------------------------------------------------------------------------------------
# PREPARE.
# ---------------------------------------------------------------------------------------------------


# LOAD AND DISPLAY
waves_fcst = waves.copy()

waves_fcst = waves_fcst.set_index('DateTime')
waves_fcst['DateTime'] = waves_fcst.index


# ---------------------------------------------------------------------------------------------------
# 
# ---------------------------------------------------------------------------------------------------





# ---------------------------------------------------------------------------------------------------
# STATIC MODEL.
# ---------------------------------------------------------------------------------------------------


# LOAD
height_fname = 'data/height.pkl'
with open(height_fname, 'rb') as file:
    height_model = pickle.load(file)
    
    

# FEATURE ENGINEERING      --------------------------------------------------------

# extract the hour, day, and month
height_df = waves_fcst.copy()
time_series = pd.to_datetime(height_df['DateTime'])
height_df['month'] = time_series.dt.month
height_df['day'] = time_series.dt.day
height_df['hour'] = time_series.dt.hour

del height_df['DateTime']
del height_df['CottPeakPeriod']
del height_df['CottDirection']

order = ['month', 'day', 'hour', 'RottHeight', 'RottPeakPeriod', 'RottDirection', 'CottHeight']
height_df = height_df[order]

# use bin method to treat time feature as category variable
# After applying to the model, we found that the "bins of hour" almost has no effect on the model result,
# so we remove it to reduce dimension in case of overfitting. 

bins_of_month = [0, 4 ,7, 9, 13]
height_df['month'] = pd.cut(height_df['month'], bins_of_month, labels=[1, 2, 3, 4])

bins_of_day = [0, 10 ,20, 32]
height_df['day'] = pd.cut(height_df['day'], bins_of_day, labels=[1, 2, 3])

# bins_of_hour = [-1, 6 ,12, 18, 25]
# df['hour'] = pd.cut(df['hour'], bins_of_hour, labels=[1, 2, 3,4])
del height_df['hour']
# use OneHot Encoding to make all values of the categorical features are equally away from each other,
# and it help to avoid the overfitting caused by the gradient descent in high dimension. 
col_names = ['month','day']
for col in col_names:  
    OnehotEn = pd.get_dummies(height_df[col], prefix=col)
    height_df.drop([col], axis=1, inplace=True)
    height_df = pd.concat([height_df, OnehotEn], axis=1)


#normalize numerical feature to make the model faster to find the optimal solution during training
z_scaler = lambda x : (x - np.mean(x)) / np.std(x)
height_df_ = height_df[['RottHeight', 'RottPeakPeriod', 'RottDirection']].apply(z_scaler)

del height_df['RottHeight']
del height_df['RottPeakPeriod']
del height_df['RottDirection']

height_df = pd.concat([height_df,height_df_],axis=1)
label_y = height_df['CottHeight']
height_df.drop(['CottHeight'], axis=1, inplace=True)


# ---------------------------------------------------------------------------------

# MAKE PREDICTIONS
height_pred = height_model.predict(height_df)
height_pred.shape

# Update result_df
height_df['PredCottHeight'] =  height_pred
height_df['CottHeight']=label_y

Predicted_Cott_height = height_df


# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------
# COTT FORECAST UNIVARIATE MODEL.
# ---------------------------------------------------------------------------------------------------

# SELECT FEATURES INVOLVED IN TRAINING AND PREDICTIONS
cols = ["PredCottHeight"]

# ISOLATE TRAINING SET WITH ONLY cols THAT ARE REQUIRED
dataset_train = Predicted_Cott_height[cols]

# CONVERT TO ARRAY
training_set = dataset_train.to_numpy()


# CONSTRUCT X and y SETS
X = []    # each item is a window of size n_past
y = []    # corresponding y val that each window tries to predict

n_future = steps_future    # number of data points to predict in the future
n_past = 96     # number of past data points to use for predicting the future

# BUILD X AND y
for i in range(n_past, len(training_set) - n_future + 1):
  X.append( training_set[ i - n_past:i, 0:dataset_train.shape[1] ] )
  y.append( training_set[ i + n_future - 1:i + n_future, 0 ] )

X, y = np.array(X), np.array(y)

# BUILD LSTM MODEL
model_univar = Sequential()                                                                               # initialise LSTM neural network

model_univar.add(LSTM(units=64, return_sequences= True, input_shape=(n_past,dataset_train.shape[1])))     # 1st layer
model_univar.add(LSTM(units=30, return_sequences = False))                                                # 2nd layer
model_univar.add(Dropout(0.55))                                                                           # Dropout layer
model_univar.add(Dense(units=1, activation='linear'))                                                     # Output Layer

model_univar.compile(optimizer = Adam(learning_rate=0.0001), loss= 'mean_squared_error')                  # compile model


# LOAD DYNAMIC
model = model_univar.load_weights(model_to_load)


# PREDICTIONS MADE ON PAST VALUES
predictions_past = model_univar.predict(X[n_past:])


# CONSTRUCT A DF TO HOLD RESULTS
univar_pst_result_df = dataset_train[2 * n_past + n_future -1:].copy()                        # now reference the true set
univar_pst_result_df['DynPredCottHeight'] = predictions_past                                  # add prediction column to trueset
#univar_pst_result_df = univar_pst_result_df.rename(columns={"CottHeight": "ActlRottHeight"})


# FINAL Dataframe
_S2D_Final_df = waves_fcst.drop(waves_fcst.columns.difference(['CottHeight']),axis=1)
S2D_Final_df = _S2D_Final_df.join(univar_pst_result_df)
S2D_Final_df['DateTime'] = S2D_Final_df.index # add DateTime index back in


# ---------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------






# ---------------------------------------------------------------------------------------------------------------------------------
# FORECAST SIGNIFICANT WAVE HEIGHT MODEL
# ---------------------------------------------------------------------------------------------------------------------------------

# MAKE DUMMY FORECAST DATA ------------

# get last 18hrs (6hrs of real data + 12hr 'forecast') (38 rows)
last38 = data.tail(38)
# 6hrs == 12.5 data points
# use first 6hrs of last38 to represent 6hrs before forecast
# the next 12hrs will represent the DUMMY forecast
fake6hrBeforecast = S2D_Final_df.tail(steps_future + 12).head(12)
# dummyForecast = last38.tail(25)

# convert to dict
fake6hrBeforecast_data = fake6hrBeforecast.to_dict(orient='records')
# dummyForecast_data = dummyForecast.to_dict(orient='records')

dummyForecast_data = S2D_Final_df.tail(steps_future).to_dict(orient='records')

# convert to array [last 6hrs, next 12hrs]
arrayForecast = np.concatenate((fake6hrBeforecast_data, dummyForecast_data)).tolist() # concatenate 2 numpy arrays: row-wise

# --------------------------------------
# S2D_Final_df.tail(steps_future)
# print(dummyForecast.head())
# print(S2D_Final_df.tail(steps_future))
# --------------------------------------










# ROUTES
@app.route('/')
@app.route('/index')
def index():
  message = {}
  data = {}

  message['message'] = 'Hello Ocean Waves!'
  data['status'] = 200
  data['data'] = message

  return jsonify(data)


@app.route('/oceanwaves')
def oceanwaves():
  data = {}

  chart_data = predictions_df.to_dict(orient='records')

  data['data'] = { 'data': chart_data, 'summary': stats, 'forecast': arrayForecast }
  data['status'] = 200

  return jsonify(data)
#   data = {}

#   # DUMMY STATS DATA --------------------

#   # stats = {
#   #   'day': {
#   #     'maxWaveHeight': 1.16,
#   #     'maxWavePeriod': 27.1
#   #     },
#   #   'week': {
#   #     'maxWaveHeight': 0.98,
#   #     'maxWavePeriod': 19.0
#   #   },
#   #   'month': {
#   #     'maxWaveHeight': 1.1,
#   #     'maxWavePeriod': 23.23
#   #   },
#   #   'confidence': {
#   #       'waveHeight': 92.3,
#   #       'peakPeriod': 89.60,
#   #       'direction': 87.3
#   #   }
#   # }


#   stats = {
#     'waveHeight': {
#       'day': 1.16,
#       'week': 0.98,
#       'month': 1.1,
#       'confidence': 92.3
#     },
#     'peakPeriod': {
#       'day': 27.1,
#       'week': 19.0,
#       'month': 23.23,
#       'confidence': 89.60
#     },
#     'forecast': { 
#       'height': 1.05,
#       'period': 26.3,
#       'confidence': {
#         'waveHeight': 84.1,
#         'peakPeriod': 84.2,
#         'direction': 84.3
#       }
#     },
#     'direction': {
#       'confidence': 87.3
#     }
#   }

#   # -------------------------------------

#   # df = pd.read_csv('data/ocean-waves-clean.csv')

#   # -------------------------------------
  

#   # MAKE DUMMY FORECAST DATA ------------

#   # get last 18hrs (6hrs of real data + 12hr 'forecast') (38 rows)
#   last38 = df.tail(38)
#   # 6hrs == 12.5 data points
#   # use first 6hrs of last38 to represent 6hrs before forecast
#   # the next 12hrs will represent the DUMMY forecast
#   fake6hrBeforecast = last38.head(13)
#   dummyForecast = last38.tail(25)
  
#   # convert to dict
#   fake6hrBeforecast_data = fake6hrBeforecast.to_dict(orient='records')
#   dummyForecast_data = dummyForecast.to_dict(orient='records')

#   # convert to array [last 6hrs, next 12hrs]
#   arrayForecast = np.concatenate((fake6hrBeforecast_data, dummyForecast_data)).tolist() # concatenate 2 numpy arrays: row-wise

#   # --------------------------------------



#   # --------------------------------------

#   chart_data = df.to_dict(orient='records')



#   data['data'] = { 'data': chart_data, 'summary': stats, 'forecast': arrayForecast }
#   data['status'] = 200

#   return jsonify(data)


@app.route('/historywaves')
def historywaves():
  data = {}

  # DUMMY STATS DATA --------------------
  # history_stats = {

  #   'day': {
  #     'confidence': 92,
  #     'maxWaveHeight': 1.16,
  #     'maxWavePeriod': 27.1
  #     },
  #   'week': {
  #     'confidence': 92,
  #     'maxWaveHeight': 0.98,
  #     'maxWavePeriod': 19.0
  #   },
  #   'month': {
  #     'confidence': 92,
  #     'maxWaveHeight': 1.1,
  #     'maxWavePeriod': 23.23
  #   },
  #   'confidence': {
  #       'waveHeight': 92.3,
  #       'peakPeriod': 89.60,
  #       'direction': 87.3
  #   }

  # }


  history_stats = {
    'waveHeight': {
      'day': 1.16,
      'week': 0.98,
      'month': 1.1,
      'confidence': 92.3
    },
    'peakPeriod': {
      'day': 27.1,
      'week': 19.0,
      'month': 23.23,
      'confidence': 89.60
    },
    'forecast': { 
      'height': 1.05,
      'period': 26.3,
      'confidence': {
        'waveHeight': 84.1,
        'peakPeriod': 84.2,
        'direction': 84.3
      }
    },
    'direction': {
      'confidence': 87.3
    }
  }
  # -------------------------------------

  # df = pd.read_csv('data/ocean-waves-clean.csv')
  chart_data = df.to_dict(orient='records')


  # DUMMY HISTORY DATA  ---------------------


  # isolate cott data
  CottHeaders = ['CottHeight', 'CottPeakPeriod', 'CottDirection']
  CottData = df[CottHeaders]

  # add noise to Cott data
  mu, sigma = 0, 0.1 
  noise = np.random.normal(mu, sigma, CottData.shape)
  signal = CottData + noise

  signal.rename(columns={'CottHeight': 'CottHeightHistory', 'CottPeakPeriod': 'CottPeakPeriodHistory', 'CottDirection': 'CottDirectionHistory'}, inplace=True)
  df_horizontal_stack = pd.concat([df, signal], axis=1)

  # history_data = df_horizontal_stack.to_dict(orient='records')

  # print(df_horizontal_stack.tail())
  # ----------------------------------------

  # MAKE DUMMY FORECAST DATA ------------

  # get last 18hrs (6hrs of real data + 12hr 'forecast') (38 rows)
  last38 = df.tail(38)
  # 6hrs == 12.5 data points
  # use first 6hrs of last38 to represent 6hrs before forecast
  # the next 12hrs will represent the DUMMY forecast
  fake6hrBeforecast = last38.head(13)
  dummyForecast = last38.tail(25)

  # add noise to 'predicted'
  CottForecastData = dummyForecast[CottHeaders]
  noise = np.random.normal(mu, sigma, CottForecastData.shape)
  signal = CottForecastData + noise
  df_horizontal_stack = pd.concat([dummyForecast['DateTime'], signal], axis=1)
  dummyForecast_data = df_horizontal_stack.to_dict(orient='records')
  
  # convert to dict
  fake6hrBeforecast_data = fake6hrBeforecast.to_dict(orient='records')
  # dummyForecast_data = dummyForecast.to_dict(orient='records')

  # convert to array [last 6hrs, next 12hrs]
  arrayForecast = np.concatenate((fake6hrBeforecast_data, dummyForecast_data)).tolist() # concatenate 2 numpy arrays: row-wise

  # --------------------------------------

  # OUTCOME OF FORECASTED VALUES ---------
  forecast_outcome = last38.to_dict(orient='records')
  # --------------------------------------


  data['data'] = { 'history': history_data, 'summary_history': history_stats, 'forecast': arrayForecast, 'forecastOutcome': forecast_outcome }
  data['status'] = 200

  return jsonify(data)