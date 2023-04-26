# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 09:59:14 2023

@author: MD
"""

import pandas as pd
import chart_studio.plotly as py
import plotly.express as px
from air_weather_brzoskwinia import calculate_pm_mean, pm10_limit, pm25_limit


filepath = 'C:/MD/Dokumenty/python/data_analysis/air_weather/airly.csv'



def create_air_pollution_hourly_bar_chart(df, y):
    return px.bar(df, x=x, y=y, template='plotly_dark')
    
def create_layout_for_air_pollution_hourly(y_title, title):
    return {'xaxis': {'title': {'text': 'Hour', 'font': {'size': 17}}, 
                      'tickmode': 'array', 'tickvals': xticks}, 
            'yaxis': {'title': {'text': y_title, 'font': {'size': 17}}, 
                        'tickmode': 'array', 'tickvals': yticks, 'range': yrange, 'showgrid': False}, 
            'title': {'text': title, 'x': 0.5, 'xanchor': 'center', 'font': {'size': 30}}, 
            'plot_bgcolor': '#000000', 'paper_bgcolor': 'black'}

def plot_air_pollution_hourly(filename):
    return py.plot(fig, filename=filename, auto_open=True)




if __name__ == "__main__":
    
    
    df = pd.read_csv(filepath)
    air_hourly = pd.pivot_table(df, index='hour', values=['PM1', 'PM10', 'PM25'], aggfunc='mean')
    x = air_hourly.index
    xticks = list(range(min(x.astype(int)), max(x.astype(int))+1))
    yticks = list(range(0, 55, 5))
    yrange = [0, 55]
    pm1_mean = calculate_pm_mean(df.PM1)
    pm25_mean = calculate_pm_mean(df.PM25)
    pm10_mean = calculate_pm_mean(df.PM10)
    
    # PM1
    fig = create_air_pollution_hourly_bar_chart(air_hourly, air_hourly['PM1'])
    layout = create_layout_for_air_pollution_hourly('PM1 [μg/m³]', 'PM1 air pollution')
    fig['layout'].update(layout)
    fig.add_hline(y=pm1_mean, line_color="#d792f5", line_width=5, annotation_text="PM1 mean", 
                  annotation_font_size=15, annotation_font_color="#d792f5")
    plot_air_pollution_hourly('air_pollution_hourly_pm1')
    
    # PM2.5
    fig = create_air_pollution_hourly_bar_chart(air_hourly, air_hourly['PM25'])
    layout = create_layout_for_air_pollution_hourly('PM2.5 [μg/m³]', 'PM2.5 air pollution')
    fig['layout'].update(layout)
    fig.add_hline(y=pm25_limit, line_color="#a35994", line_width=5, 
                  annotation_text="PM2.5 average daily limit ", annotation_font_size=15, 
                  annotation_position="left top", annotation_font_color="#a35994")
    fig.add_hline(y=pm25_mean, line_color="#d792f5", line_width=5, 
                  annotation_text="PM2.5 mean", annotation_font_size=15, annotation_font_color="#d792f5")
    plot_air_pollution_hourly('air_pollution_hourly_pm25')
    
    # PM10
    fig = create_air_pollution_hourly_bar_chart(air_hourly, air_hourly['PM10'])
    layout = create_layout_for_air_pollution_hourly('PM10 [μg/m³]', 'PM10 air pollution')
    fig['layout'].update(layout)
    fig.add_hline(y=pm10_limit, line_color="#a35994", line_width=5, 
                  annotation_text="PM10 average daily limit ", annotation_font_size=15, annotation_font_color="#a35994")
    fig.add_hline(y=pm10_mean, line_color="#d792f5", line_width=5, 
                  annotation_text="PM10 mean", annotation_font_size=15, annotation_font_color="#d792f5")
    plot_air_pollution_hourly('air_pollution_hourly_pm10')