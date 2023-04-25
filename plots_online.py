# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 09:59:14 2023

@author: MD
"""

import pandas as pd
import plotly.graph_objects as go
import chart_studio.plotly as py
import plotly.express as px


filepath = 'C:/MD/Dokumenty/python/data_analysis/air_weather/airly.csv'
pm25_limit = 15.0
pm10_limit = 45.0



def create_air_pollution_hourly_bar_chart(df, y):
    return px.bar(df, x=x, y=y, template='plotly_dark')
    
def create_layout_for_air_pollution_hourly(y_title, title):
    return {'xaxis': {'linecolor': '#fff', 'title': {'text': 'Hour', 'font': {'size': 17}}, 
                      'tickmode': 'array', 'tickvals': xticks, 'mirror': True}, 
            'yaxis': {'linecolor': '#fff', 'gridcolor': ' #cbcbcb ', 'title': {'text': y_title, 'font': {'size': 17}}, 
                        'tickmode': 'array', 'tickvals': yticks, 'range': yrange, 'showgrid': True, 'mirror': True}, 
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
    
    # PM1
    fig = create_air_pollution_hourly_bar_chart(air_hourly, air_hourly['PM1'])
    layout = create_layout_for_air_pollution_hourly('PM1 [μg/m³]', 'PM1 air pollution')
    fig['layout'].update(layout)
    plot_air_pollution_hourly('air_pollution_hourly_pm1')
    
    # PM2.5
    fig = create_air_pollution_hourly_bar_chart(air_hourly, air_hourly['PM25'])
    layout = create_layout_for_air_pollution_hourly('PM2.5 [μg/m³]', 'PM2.5 air pollution')
    fig['layout'].update(layout)
    fig.add_hline(y=pm25_limit, line_color="red")
    plot_air_pollution_hourly('air_pollution_hourly_pm25')
    
    # PM10
    fig = create_air_pollution_hourly_bar_chart(air_hourly, air_hourly['PM10'])
    layout = create_layout_for_air_pollution_hourly('PM10 [μg/m³]', 'PM10 air pollution')
    fig['layout'].update(layout)
    fig.add_hline(y=pm10_limit, line_color="red")
    plot_air_pollution_hourly('air_pollution_hourly_pm10')