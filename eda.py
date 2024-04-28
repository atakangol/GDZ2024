# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 19:16:45 2024

@author: golat
"""

import pandas as pd
from math import sin, cos, sqrt, atan2, radians

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Radius of the Earth in kilometers
    R = 6371.0

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


train_data = pd.read_csv('train.csv')


weather = pd.read_csv('weather.csv')


holidays = pd.read_csv('holidays.csv')


holidays['date'] = holidays['Yıl'].astype(str)+'-'+ holidays['Ay'].astype(str)+'-'+ holidays['Gün'].astype(str)

train_data['is_holiday'] = None
train_data.loc[train_data['tarih'].isin(holidays['date']),'is_holiday'] = True

train_data['is_holiday'].fillna(False,inplace=True)

weather.columns = ['datetime', 'lat', 'lon', 't_2m:C', 'effective_cloud_cover:p',
       'global_rad:W', 'relative_humidity_2m:p', 'wind_dir_10m:d',
       'wind_speed_10m:ms', 'prob_precip_1h:p', 't_apparent:C', 'ilce']


weather['date'] = pd.to_datetime(weather['datetime']).dt.date




groupedweather = weather.groupby(['date','ilce']).agg('mean')
groupedweather = groupedweather.reset_index()

ilceler = [ilce.split('-') for ilce in train_data['ilce'].unique()]
merkez_manisa = 'yunusemre'
merkez_izmir = 'konak'



coordinates = weather[['lat', 'lon','ilce']].groupby('ilce').agg('first')



izmir_merkez_koord = coordinates.loc[coordinates.index =='izmir-konak'][['lat','lon']].values[0]
manisa_merkez_koord = coordinates.loc[coordinates.index =='manisa-yunusemre'][['lat','lon']].values[0]


train_data['distance_to_center'] = None
distance_to_center = {}
for index,row in coordinates.iterrows():
    lat1, lon1 =  row[['lat','lon']].tolist()
    
    if index.split('-')[0] == 'manisa':
        lat2, lon2 = manisa_merkez_koord.tolist()
        
    else:
        lat2, lon2 = izmir_merkez_koord.tolist()
        
        
    dist = haversine(lat1, lon1, lat2, lon2)
    distance_to_center[index] = dist

    
    train_data.loc[train_data['ilce'] == index,'distance_to_center'] = dist



[['t_2m:C', 'effective_cloud_cover:p',
       'global_rad:W', 'relative_humidity_2m:p', 'wind_dir_10m:d',
       'wind_speed_10m:ms', 'prob_precip_1h:p', 't_apparent:C']]



train_data.tarih.max(),train_data.tarih.min()
groupedweather.date.max(),groupedweather.date.min()


groupedweather['date'] = groupedweather['date'].astype(str)


    
    
train_data = train_data.merge(groupedweather,left_on = ['ilce','tarih'],right_on=['ilce','date'],how='left')   






