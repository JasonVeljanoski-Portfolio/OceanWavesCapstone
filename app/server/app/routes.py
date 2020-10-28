from app import app
from flask import jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
@app.route('/index')
def index():
  message = {}
  data = {}

  message['message'] = 'Hello World from Flask!'
  data['status'] = 200
  data['data'] = message

  return jsonify(data)


@app.route('/oceanwaves')
def oceanwaves():
  data = {}

  # DUMMY STATS DATA --------------------

  # stats = {
  #   'day': {
  #     'maxWaveHeight': 1.16,
  #     'maxWavePeriod': 27.1
  #     },
  #   'week': {
  #     'maxWaveHeight': 0.98,
  #     'maxWavePeriod': 19.0
  #   },
  #   'month': {
  #     'maxWaveHeight': 1.1,
  #     'maxWavePeriod': 23.23
  #   },
  #   'confidence': {
  #       'waveHeight': 92.3,
  #       'peakPeriod': 89.60,
  #       'direction': 87.3
  #   }
  # }


  stats = {
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

  df = pd.read_csv('data/ocean-waves.csv')

  # -------------------------------------
  

  # MAKE DUMMY FORECAST DATA ------------

  # get last 18hrs (6hrs of real data + 12hr 'forecast') (38 rows)
  last38 = df.tail(38)
  # 6hrs == 12.5 data points
  # use first 6hrs of last38 to represent 6hrs before forecast
  # the next 12hrs will represent the DUMMY forecast
  fake6hrBeforecast = last38.head(13)
  dummyForecast = last38.tail(25)
  
  # convert to dict
  fake6hrBeforecast_data = fake6hrBeforecast.to_dict(orient='records')
  dummyForecast_data = dummyForecast.to_dict(orient='records')

  # convert to array [last 6hrs, next 12hrs]
  arrayForecast = np.concatenate((fake6hrBeforecast_data, dummyForecast_data)).tolist() # concatenate 2 numpy arrays: row-wise

  # --------------------------------------



  # --------------------------------------

  chart_data = df.to_dict(orient='records')



  data['data'] = { 'data': chart_data, 'summary': stats, 'forecast': arrayForecast }
  data['status'] = 200

  return jsonify(data)


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

  df = pd.read_csv('data/ocean-waves.csv')
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

  history_data = df_horizontal_stack.to_dict(orient='records')


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