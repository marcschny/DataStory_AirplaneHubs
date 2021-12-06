#!/usr/bin/env python3

from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def bar_category(df):
    df = df[(df['region'] != 'unkown') & (df['continent'].notnull())]
    ax = df['type'].value_counts().plot(kind='bar')
    _ = ax.set_title('Bar-Chart Airport Typen')
    _ = ax.set_ylabel('Anzahl Flughafen')
    return ax

def bar_region(df):
    df = df[(df['region'] != 'unkown') & (df['continent'].notnull())]
    
    ax = df['region'].value_counts().plot(kind='bar')
    _ = ax.set_title("Flughäfen pro Land")
    _ = ax.set_ylabel("Anzahl Flughäfen")
    return ax

def airport_infos(df):
    text = "Anzahl Flughafen total:\t"+ str(len(df)) + "\n"
    text += "Flughäfen für Flugzeuge:"+str(len(df[df['type'] == 'small_airport'])+len(df[df['type'] == 'medium_airport'])+len(df[df['type'] == 'large_airport']))+"\n\n"
    
    text += "Anzahl grosser Flughäfen: "+str(len(df[df['type'] == 'large_airport'])) + "\n"
    text += "Anzahl kleiner & mittlerer Flughäfen: "+str(len(df[df['type'] == 'small_airport'])+len(df[df['type'] == 'medium_airport']))+ "\n"
    text += "Anzahl Flughäfen ohne Region/Continent" + str(len(df[(df['region'] != 'unkown') | (df['continent'].notnull())]))
    
    return text
    
def flight_infos(df):    
    cnt = df.groupby('day').size().rename('Count')
    median = cnt.median()
    mittel = cnt.mean()
    
    length_mai = len(df[df['day'] < '2021-06-01'])
    length_sep = len(df[df['day'] > '2021-06-01'])
    
    text = "Anzahl FLugverbindungen im Mai: "
    text += str(length_mai) + "\n"
    text += "Anzahl FLugverbindungen im Sep: "
    text += str(length_sep) + "\n"
    text += "Total Takeoffs/Landings: " + str(len(df['day'])) + "\n"
    
    text += "Median:\t  " + str(median)+"\n"
    text += "Mittelwert:" + str(mittel)+"\n"
    
    return text

def show_flights(df):
    cnt = df.groupby('day').size().rename('Count')
    
    median = cnt.median()
    mittel = cnt.mean()
    
    fig, ax = plt.subplots(figsize=(10,5))
    _ = ax.scatter(cnt.keys(), cnt, alpha=0.6)
    _ = ax.set_xlabel('Datum')
    _ = ax.set_ylabel('Anzahl Flüge pro Tag')
    _ = ax.set_title('Flugbewegungen')
    xin, xax = ax.get_xlim()
    _ = ax.hlines(y=median, xmin=xin, xmax=xax, linewidth=2, color='r', label="Median")
    _ = ax.hlines(y=mittel, xmin=xin, xmax=xax, linewidth=2, color='b', label="Mittelwert")
    _ = ax.legend()
    
    return fig

def show_cum_flights(df):
    
    cnt = df.groupby('day').size().rename('Count')
    hist = np.histogram(cnt)
    pv = np.cumsum(cnt)

    fig, ax = plt.subplots(figsize=(13,8))
    _ = ax.step(cnt.keys(), pv, where='pre', drawstyle='steps', label='Kumulative Verteilung')
    _ = ax.set_title("Verteilung Flugbewegungen")
    _ = ax.legend()
    
    return fig

def load_airports():
    df = pd.read_csv("data/preprocessed/airports.csv")
    
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    df['ident'] = df['ident'].astype(str)
    df['type'] = df['type'].astype('category')
    df['name'] = df['name'].astype(str)
    df['region'] = df['region'].astype('category')
    
    return df

def load_flights():
    df = pd.read_csv("data/preprocessed/flights.csv")
    
    df['callsign'] = df['callsign'].astype(str)
    df['origin'] = df['origin'].astype(str)
    df['destination'] = df['destination'].astype(str)
    df['day'] = pd.to_datetime(df['day'])
    
    return df
    