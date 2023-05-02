# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:50:59 2023

@author: MD
"""


import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


filepath = 'C:/MD/Dokumenty/python/data_analysis/air_weather/airly.csv'
pm10_limit = 45.0
pm25_limit = 15.0



def calculate_pm_mean(df_column):
    return df_column.mean()
    
def plot_air_pollution_hourly(df, pollutant, title, ylabel,limit, limit_label, pm_mean, mean_label):
    plt.figure(figsize=(15, 5))
    x = df.index
    y = df[pollutant]
    plt.bar(x, y)
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=20)
    plt.xticks(range(min(x.astype(int)), max(x.astype(int))+1))
    plt.yticks(range(0, 55, 5))
    plt.axhline(limit, color="red", linestyle="--", label=limit_label)
    plt.axhline(pm_mean, color="#12304a", linestyle="--", label=mean_label)
    plt.legend(loc='upper right')
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.show()
    
def plot_air_pollution_depending_on_weather(df, weather_factor, pollutant, title, 
        ylabel, xlabel, xticks_range, yticks_range, limit, limit_label):
    plt.figure(figsize=(15, 5))
    x = df[weather_factor]
    y = df[pollutant]
    plt.scatter(x, y)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.title(title, fontsize=20)
    plt.xticks(xticks_range)
    plt.yticks(yticks_range)
    plt.axhline(limit, color="red", linestyle="--", label=limit_label)
    plt.legend(loc='upper right')
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.show()
    
def create_data_series_for_boxplots(x, y, hum_range):
    data = pd.DataFrame((df_all[(df_all['Humidity'] >= x) & (df_all['Humidity'] < y)]).reset_index())
    data = data[data.columns[7]]
    data.rename(hum_range, inplace = True)
    return data    
    
    
    
    
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
    pm1_mean = calculate_pm_mean(df_all.PM1)
    pm25_mean = calculate_pm_mean(df_all.PM25)
    pm10_mean = calculate_pm_mean(df_all.PM10)
    
    # Create charts showing air pollution hourly
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
    plot_air_pollution_hourly(air_hourly, 'PM25', 'PM2.5 air pollution', 'PM2.5 [μg/m³]', 
                              pm25_limit, 'PM2.5 average daily limit', pm25_mean, 'PM2.5 mean value')
    plot_air_pollution_hourly(air_hourly, 'PM10', 'PM10 air pollution', 'PM10 [μg/m³]', 
                              pm10_limit, 'PM10 average daily limit', pm10_mean, 'PM10 mean value') 
    
    # Create charts showing air pollution depending on weather
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
    
    # Create correlation matrix
    df_corr = df_all[['PM1', 'PM25', 'PM10', 'Pressure', 'Humidity', 'Temperature', 'hour']]
    corr_matrix = df_corr.corr()
    sns.heatmap(corr_matrix, annot=True, cmap="crest")
    plt.show()
    
    # Create box plots showing PM10 concentration depending on humidity range
    humidity_25_30 = create_data_series_for_boxplots(25, 30, '25%-30%')
    humidity_30_35 = create_data_series_for_boxplots(30, 35, '30%-35%')
    humidity_35_40 = create_data_series_for_boxplots(35, 40, '35%-40%')  
    humidity_40_45 = create_data_series_for_boxplots(40, 45, '40%-45%')
    humidity_45_50 = create_data_series_for_boxplots(45, 50, '45%-50%')  
    humidity_50_55 = create_data_series_for_boxplots(50, 55, '50%-55%')
    humidity_55_60 = create_data_series_for_boxplots(55, 60, '55%-60%')  
    humidity_60_65 = create_data_series_for_boxplots(60, 65, '60%-65%')  
    humidity_65_70 = create_data_series_for_boxplots(65, 70, '65%-70%')   
    humidity_70_75 = create_data_series_for_boxplots(70, 75, '70%-75%')   
    humidity_75_80 = create_data_series_for_boxplots(75, 80, '75%-80%')
    humidity_80_85 = create_data_series_for_boxplots(80, 85, '80%-85%')
    humidity_85_90 = create_data_series_for_boxplots(85, 90, '85%-90%') 
    humidity_90_95 = create_data_series_for_boxplots(90, 95, '90%-95%')                         
    boxplots = pd.concat([humidity_25_30, humidity_30_35, humidity_35_40, humidity_40_45, humidity_45_50, 
                          humidity_50_55, humidity_55_60, humidity_60_65, humidity_65_70, humidity_70_75, 
                          humidity_75_80, humidity_80_85, humidity_85_90, humidity_90_95], axis=1)
    plt.figure(figsize=(15,5))
    plt.xlabel('Humidity ranges', fontsize=12)
    plt.ylabel('PM10[μg/m³]', fontsize=12)
    plt.title('PM10 in humidity ranges', fontsize=20)
    sns.boxplot(boxplots)
    plt.show()
    
    # Extract a date from 'fromDateTime' column into separate column
    df_all['date'] = df_all['fromDateTime'].apply(lambda x: pd.Series(x.date()))
    exceedings_daily = pd.pivot_table(df_all, index='date', values=['PM10'], aggfunc='mean')
    exceedings_daily['exceedings'] = ''
    exceeded = exceedings_daily['PM10'] > 45.0 
    exceedings_daily.loc[exceeded, 'exceedings'] = 'Exceeded'
    not_exceeded = exceedings_daily['PM10'] <= 45.0 
    exceedings_daily.loc[not_exceeded, 'exceedings'] = 'Not exceeded'
    plt.figure(figsize=(15, 5))
    sns.scatterplot(exceedings_daily, x='date', y='PM10', hue='exceedings')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('PM10 [μg/m³]', fontsize=12)
    plt.title('PM10 daily exceedings', fontsize=20)
    print(exceedings_daily.index[0])
    plt.xticks(exceedings_daily.index[0:18], rotation=45)
    plt.yticks(range(0, 35, 5))
    axes = plt.gca()
    axes.yaxis.grid()
    axes.set_axisbelow(True)
    plt.show()
    
    # Save concatenated data frame
    df_all.to_csv(filepath, index=False)