#!usr/bin/python

# Data Cleaning and Alignment of Time Series

# Script tasks:
#   - converting MATLAB date formats to standard Date Time format
#   - aligning the data on record dates
#   - exploration of time series consistency and further pruning
#   - time series rounding and alignment, and finally
#   - merging and outputing the Rottnest and Cottesloe data

# Environment/package dependencies
# - Python >= 3.6
# - `pandas`
# - `numpy`

# ___

import numpy as np
import pandas as pd
import datetime as dt
from os import path

INPATH = './Data'  # location of .json files
OUTPATH = './Data'  # location to save output csv files

cott, rott = (pd.read_json(path.join(INPATH, f'{buoy}-waves.json')) for buoy in ['cott','rott'])

# Convert MATLAB time format to standard DateTime
def matlab2datetime(matlab_datenum):
    day = dt.datetime.fromordinal(int(matlab_datenum))
    dayfrac = dt.timedelta(days=matlab_datenum%1) - dt.timedelta(days=366)
    return day + dayfrac

# Round to nearest min to remove floating point errors
cott['DateTime'] = cott['time'].apply(matlab2datetime).apply(lambda x: x.round('T'))
rott['DateTime'] = rott['time'].apply(matlab2datetime).apply(lambda x: x.round('T'))

data_dict = {'Dp': 'Direction', 'Tp': 'PeakPeriod', 'Tm': 'MeanPeriod', 'Hs': 'Height'}
col_order = ['DateTime','Height','PeakPeriod','MeanPeriod','Direction']
cott = cott.rename(columns=data_dict)[col_order]
rott = rott.rename(columns=data_dict)[col_order]

# Saving semi-cleaned CSV format data
cott.to_csv(path.join(OUTPATH, 'cott-waves.csv'), index=False)
rott.to_csv(path.join(OUTPATH, 'rott-waves.csv'), index=False)


# ___
# 2  Aligning dates

cott['Date'] = cott['DateTime'].dt.date
rott['Date'] = rott['DateTime'].dt.date

# Filtering out dates that do not exist in both datasets
filt = rott['Date'].isin(cott['Date'])
rott_all = rott.copy()
rott = rott[filt].copy()

filt = cott['Date'].isin(rott['Date'])
cott_all = cott.copy()
cott = cott[filt].copy()

# Filtering records from before Cottesloe buoy shutdown in 2010
threshold = pd.Timestamp('2015-12-01')
cott = cott[cott['DateTime'] > threshold]
rott = rott[rott['DateTime'] > threshold]

rott_filt1 = rott['DateTime'].diff().isin([pd.Timedelta(30, 'm'), pd.NaT])
rott = rott[rott_filt1]
cott_filt1 = cott['DateTime'].diff().isin([pd.Timedelta(30, 'm'), pd.NaT])
cott = cott[cott_filt1]

rott = rott.reset_index(drop=True)
cott = cott.reset_index(drop=True)

rott_filt2 = rott['DateTime'].diff().isin([pd.Timedelta(30, 'm'), pd.NaT])
rott_buoy_service = list(rott[~rott_filt2].index)

cott_filt2 = cott['DateTime'].diff().isin([pd.Timedelta(30, 'm'), pd.NaT])
cott_buoy_service = list(cott[~cott_filt2].index)


# ___
# Aligning time series
# Performing the time series '*rounding*' to complete the alignment of the Rottnest and Cottesloe data.

def round_to_30(tm):
    if tm.minute == 15:
        tm += pd.Timedelta('15min')  # making 15 -> 30 instead of 00
    else:
        tm = tm.round('30min')
    return tm

rott.drop(columns='Date', inplace=True)
cott.drop(columns='Date', inplace=True)

rott['DateTimeRounded'] = rott['DateTime'].apply(round_to_30)
cott['DateTimeRounded'] = cott['DateTime'].apply(round_to_30)

filt_rott_dts = rott['DateTimeRounded'].isin(cott['DateTimeRounded'])
filt_cott_dts = cott['DateTimeRounded'].isin(rott['DateTimeRounded'])

rott_filtered = rott[filt_rott_dts].reset_index(drop=True)
cott_filtered = cott[filt_cott_dts].reset_index(drop=True)

cott_filtered.rename(columns={'DateTimeRounded': 'DateTime', 'DateTime': 'DateTimeOrig'}, inplace=True)
rott_filtered.rename(columns={'DateTimeRounded': 'DateTime', 'DateTime': 'DateTimeOrig'}, inplace=True)

col_order = ['DateTime','Height','PeakPeriod','MeanPeriod','Direction','DateTimeOrig']
cott_out = cott_filtered.loc[:,col_order]
rott_out = rott_filtered.loc[:,col_order]

# Taking record of amount of time shift (in minutes)
rott_out['TimeShift'] = (rott_out['DateTime'] - rott_out['DateTimeOrig']) / np.timedelta64(1,'m')
cott_out['TimeShift'] = (cott_out['DateTime'] - cott_out['DateTimeOrig']) / np.timedelta64(1,'m')


# ___
# # 5  Merging the Cottesloe and Rottnest datasets

cott_to_merge = cott_out.rename(columns={col: f'Cott{col}' for col in cott_out})
rott_to_merge = rott_out.rename(columns={col: f'Rott{col}' for col in rott_out})

df = pd.merge(cott_to_merge, rott_to_merge, left_index=True, right_index=True)

df['TimeShiftTotal'] = abs(df['CottTimeShift'] - df['RottTimeShift'])
df = df.rename(columns={'CottDateTime': 'DateTime'}).drop(columns=['RottDateTime'])

dt_range = pd.date_range(min(df['DateTime']), max(df['DateTime']), freq='30min')
time_df = df.set_index('DateTime').reindex(index=dt_range)

# Save merged dataset

df.to_csv(path.join(OUTPATH, 'ocean-waves.csv'), index=False)
