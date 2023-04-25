# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:50:59 2023

@author: MD
"""


import requests
import pandas as pd
import matplotlib.pyplot as plt


filepath = 'C:/MD/Dokumenty/python/data_analysis/air_weather/airly.csv'
pm10_limit = 45.0
pm25_limit = 15.0



def plot_air_pollution_hourly(df, pollutant, title, ylabel,limit, axhline_label):
    plt.figure(figsize=(15, 5))
    x = df.index
    y = df[pollutant]
    plt.bar(x, y)
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=20)
    plt.xticks(range(min(x.astype(int)), max(x.astype(int))+1))
    plt.yticks(range(0, 55, 5))
    plt.axhline(limit, color="red", linestyle="--")
    plt.legend([axhline_label], loc='upper right')
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.show()
    
def plot_air_pollution_depending_on_weather(df, weather_factor, pollutant, title, 
        ylabel, xlabel, xticks_range, yticks_range, limit, axhline_label):
    plt.figure(figsize=(15, 5))
    x = df[weather_factor]
    y = df[pollutant]
    plt.scatter(x, y)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=20)
    plt.xticks(xticks_range)
    plt.yticks(yticks_range)
    plt.axhline(limit, color="red", linestyle="--", label=axhline_label)
    plt.legend(loc='upper right')
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.show()
    
    
    
    
if __name__ == "__main__":
    
    
    # Read file with previously scraped data
    df_old = pd.read_csv(filepath)
    
    # Change type of columns with dates and times to datetime
    df_old['fromDateTime'] = pd.to_datetime(df_old['fromDateTime'])
    df_old['tillDateTime'] = pd.to_datetime(df_old['tillDateTime'])
    
    # Connect to the airly webpage with apikey and get data from 'history' column as pandas data frame
    headers = {'Accept': 'application/json', 'apikey': 'zEXRtEFMLErdJG1db0wMohy1qYxWYon2'}
    response = requests.get("https://airapi.airly.eu/v2/measurements/nearest?lat=50.096411&lng=19.718471&maxDistanceKM=5", headers=headers)
    response = response.json()
    df_new = pd.DataFrame(response['history'])
    
    # Split 'values' column into separate columns with one value per each and drop 'values' column
    df_new[['PM1', 'PM25', 'PM10', 'Pressure', 'Humidity', 'Temperature']] = df_new['values'].apply(lambda x: pd.Series(str(e) for e in x))
    df_new.drop(columns='values', inplace=True)
    
    # Unpack 'indexes' and 'standards' columns containing lists
    df_new[['indexes']] = df_new['indexes'].apply(lambda x: pd.Series(str(e) for e in x))
    df_new[['standards']] = df_new['standards'].apply(lambda x: pd.Series(' '.join(str(e) for e in x)))
    
    #  Extract numeric values of parameters from every parameter column and change its type to float
    df_new['PM1'] = df_new['PM1'].apply(lambda x: pd.Series(str(x)[25:-1]))
    df_new['PM1'] = df_new['PM1'].astype(float)
    df_new['PM25'] = df_new['PM25'].apply(lambda x: pd.Series(str(x)[26:-1]))
    df_new['PM25'] = df_new['PM25'].astype(float)
    df_new['PM10'] = df_new['PM10'].apply(lambda x: pd.Series(str(x)[26:-1]))
    df_new['PM10'] = df_new['PM10'].astype(float)
    df_new['Pressure'] = df_new['Pressure'].apply(lambda x: pd.Series(str(x)[30:-1]))
    df_new['Pressure'] = df_new['Pressure'].astype(float)
    df_new['Humidity'] = df_new['Humidity'].apply(lambda x: pd.Series(str(x)[30:-1]))
    df_new['Humidity'] = df_new['Humidity'].astype(float)
    df_new['Temperature'] = df_new['Temperature'].apply(lambda x: pd.Series(str(x)[33:-1]))
    df_new['Temperature'] = df_new['Temperature'].astype(float)
    
    # Change type of columns with dates and times to datetime
    df_new['fromDateTime'] = pd.to_datetime(df_new['fromDateTime'])
    df_new['tillDateTime'] = pd.to_datetime(df_new['tillDateTime'])
    
    # Extract an hour from 'fromDateTime' column into separate column
    df_new['hour'] = df_new['fromDateTime'].apply(lambda x: pd.Series(x.hour))
    
    # Concatenate old and new data frames, drop duplicates and missing values
    df_all = pd.concat([df_old, df_new])
    df_all = df_all.drop_duplicates(subset=['fromDateTime'], ignore_index=True)
    df_all.dropna(inplace=True)
    
    # Calculate mean values of PMs
    pm1_mean = df_all.PM1.mean()
    pm25_mean = df_all.PM25.mean()
    pm10_mean = df_all.PM10.mean()
    
    # Plot charts showing air pollution hourly
    air_hourly = pd.pivot_table(df_all, index='hour', values=['PM1', 'PM10', 'PM25'], aggfunc='mean')
    plt.figure(figsize=(15, 5))
    x = air_hourly.index
    y = air_hourly['PM1']
    plt.bar(x, y)
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel('PM1 [μg/m³]', fontsize=12)
    plt.title('PM1 air pollution', fontsize=20)
    plt.xticks(range(min(x.astype(int)), max(x.astype(int))+1))
    plt.yticks(range(0, 55, 5))
    plt.axhline(pm1_mean, color="#12304a", linestyle="--", label='PM1 mean value')
    plt.legend(loc='upper right')
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.show()
    plot_air_pollution_hourly(air_hourly, 'PM25', 'PM2.5 air pollution', 'PM2.5 [μg/m³]', pm25_limit, 'PM2.5 average daily limit')
    plot_air_pollution_hourly(air_hourly, 'PM10', 'PM10 air pollution', 'PM10 [μg/m³]', pm10_limit, 'PM10 average daily limit') 
    
    # Plot charts showing air pollution depending on weather
    plot_air_pollution_depending_on_weather(df_all, 'Temperature', 'PM25', 'Dependence of PM2.5 on temperature', 
        'PM2.5 [μg/m³]', 'Temperature [ºC]', range(0, 21), range(0, 55, 5), pm25_limit, 'PM2.5 average daily limit')
    plot_air_pollution_depending_on_weather(df_all, 'Temperature', 'PM10', 'Dependence of PM10 on temperature', 
        'PM10 [μg/m³]', 'Temperature [ºC]', range(0, 21), range(0, 55, 5), pm10_limit, 'PM10 average daily limit')
    plot_air_pollution_depending_on_weather(df_all, 'Pressure', 'PM25', 'Dependence of PM2.5 on pressure', 
        'PM2.5 [μg/m³]', 'Pressure [hPa]', range(1000, 1030, 5), range(0, 55, 5), pm25_limit, 'PM2.5 average daily limit')
    plot_air_pollution_depending_on_weather(df_all, 'Pressure', 'PM10', 'Dependence of PM10 on pressure', 
        'PM10 [μg/m³]', 'Pressure [hPa]', range(1000, 1030, 5), range(0, 55, 5), pm10_limit, 'PM10 average daily limit')
    plot_air_pollution_depending_on_weather(df_all, 'Humidity', 'PM25', 'Dependence of PM2.5 on humidity', 
        'PM2.5 [μg/m³]', 'Humidity [%]', range(30, 100, 5), range(0, 55, 5), pm25_limit, 'PM2.5 average daily limit')
    plot_air_pollution_depending_on_weather(df_all, 'Humidity', 'PM10', 'Dependence of PM10 on humidity', 
        'PM10 [μg/m³]', 'Humidity [%]', range(30, 100, 5), range(0, 55, 5), pm10_limit, 'PM10 average daily limit')
      
    # Save concatenated data frame
    df_all.to_csv(filepath, index=False)