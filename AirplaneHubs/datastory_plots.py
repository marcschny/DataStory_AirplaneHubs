#!/usr/bin/env python3

#import statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import descriptive_stats as ds
import plotly.express as px
import seaborn as sns

def load_data():
    df_airports = pd.read_csv("data/preprocessed/airports.csv")
    df_flights = pd.read_csv("data/preprocessed/flights.csv")
    return df_airports, df_flights

def flight_connections(df):
    o = df.groupby(['region'], as_index=False)[['takeoffs', 'landings', 'total']].sum()
    g = o.plot(x='region', y=['takeoffs','landings'], kind='barh', width=.8, figsize=(12,7)).set(title='Flugverkehr nach Region', xlabel="Anzahl Flugverbindungen", ylabel="Regionen")
    
    return g

def traffic_map_total_destinations(df, quantile):
    regions = df[df['total'] != 0].groupby(['region', 'ident'])[['total','takeoffs','landings','count_destinations']].sum().reset_index()
    q = regions.groupby('region')[['total','count_destinations','takeoffs','landings']].quantile(quantile)
    labels = {'total':'qt', 'count_destinations':'qc', 'takeoffs':'qd', 'landings':'ql'}
    q = q.rename(columns=labels)
    regions = df.set_index('region')
    df_new = regions.join(q).reset_index()

    #5 biggest airports of each region
    most_traffic = df_new.loc[(df_new['total'] > df_new['qt']) & (df_new['count_destinations'] > df_new['qc'])]
    fig = px.scatter_mapbox(most_traffic, lat="latitude", lon="longitude",
                      color="total", size="total",
                      color_continuous_scale='magma',
                      size_max=24, zoom=1.2, hover_name='municipality', 
                      hover_data = ['name'], 
                      title = 'Flughäfen mit dem meisten Flugverkehr',
                      width=900, height=540)
    fig.update_layout(mapbox_style="open-street-map", margin=dict(l=10, r=10, t=50, b=40))
    return fig

def show_stats(df_flights):
    df_flights["day"] = df_flights["day"].astype("datetime64")

    df_mai = df_flights.loc[df_flights['day'] < '2021-06-01']
    flights_m = df_mai.groupby([df_mai["day"]]).size()
    df_sep = df_flights.loc[df_flights['day'] > '2021-06-01']
    flights_s = df_sep.groupby([df_sep["day"]]).size()

    mittel_m = flights_m.mean()
    std_m    = flights_m.std()
    mittel_s = flights_s.mean()
    std_s    = flights_s.std()

    fig, ax = plt.subplots(ncols=2, figsize=(18,5))
    flights_m.plot(kind="bar", width=.8, rot=85, title="Flugverbindungen Monat Mai", xlabel="Tag", ylabel="Anzahl Verbindungen", ax=ax[0])
    xmin, xmax = ax[0].get_xlim()
    _ = ax[0].hlines(mittel_m, xmin, xmax, 'red', linestyle='-', label='Mittelwert')
    _ = ax[0].hlines(mittel_m-std_m, xmin, xmax, 'lightgreen', linestyle='--', label='Standardabweichung')
    _ = ax[0].hlines(mittel_m+std_m, xmin, xmax, 'lightgreen', linestyle='--')
    _ = ax[0].legend()

    flights_s.plot(kind="bar", width=.8, rot=85, title="Flugverbindungen Monat Sep.", xlabel="Tag", ylabel="Anzahl Verbindungen", ax=ax[1])
    xmin, xmax = ax[0].get_xlim()
    _ = ax[1].hlines(mittel_s, xmin, xmax, 'red', linestyle='-', label='Mittelwert')
    _ = ax[1].hlines(mittel_s-std_s, xmin, xmax, 'lightgreen', linestyle='--', label='Standardabweichung')
    _ = ax[1].hlines(mittel_s+std_s, xmin, xmax, 'lightgreen', linestyle='--')
    _ = ax[1].legend()
    
    return fig, mittel_m, mittel_s, std_m, std_s

