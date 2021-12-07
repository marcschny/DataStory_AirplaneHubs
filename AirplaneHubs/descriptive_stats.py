#!/usr/bin/env python3

from datetime import datetime
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def get_varianz(df):
    cnt = df.groupby('day').size().rename('Count')
    
    mittel = cnt.mean()
    varianz = np.sum(((cnt - mittel)**2)) / len(cnt)
    standard = math.sqrt(varianz)
    max_f = cnt.max()
    min_f = cnt.min()
    
    text = "\nMittelwert: " + str(mittel) + "\n"
    text += "Varianz: " + str(varianz) + "\n"
    text += "Standardabweichung: " + str(standard)+"\n"
    text += "Max:"+str(max_f)+" Min:"+str(min_f)
    return text

def unkown_flight_to_airport(df_f, df_a):
    airports = df_a['ident'].values
    flights = df_f[['origin', 'destination']].isin(airports)
    both = flights.loc[(flights['destination'] == True) & (flights['origin'] == True)]
    text = "Alle Flugverbindungen:\t"+str(len(flights)) +"\n"
    text+= "Klare Standorte:\t"+str(len(both))+"\n"
    text+="Es fehlen uns:\t\t"+str((len(flights)-len(both))) + " Standorte"
    return text

def get_unkown_flights(df_f, df_a):
    airports = df_a['ident'].values
    flights = df_f[['origin', 'destination']].isin(airports)
    
    index = flights.index
    ohne_standort = flights['origin'] == False
    ohne = index[ohne_standort]
    ohne_standort = df_f.loc[ohne]
    ohne_standort = ohne_standort.rename(columns={'Unnamed: 0':'index'})
    return ohne_standort

def bar_category(df):
    #df = df[(df['region'] != 'unkown') & (df['continent'].notnull())]
    ax = df['type'].value_counts().plot(kind='bar')
    _ = ax.set_title('Bar-Chart Airport Typen')
    _ = ax.set_ylabel('Anzahl Flughafen')
    return ax

def bar_region(df):
    #df = df[(df['region'] != 'unkown') & (df['continent'].notnull())]
    
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

def show_flights_seperate(df_mai, df_sep):
    cnt_m = df_mai.groupby('day').size().rename('Count')
    cnt_s = df_sep.groupby('day').size().rename('Count')
    
    median_m = cnt_m.median()
    mittel_m = cnt_m.mean()
    median_s = cnt_s.median()
    mittel_s = cnt_s.mean()
    
    fig, ax = plt.subplots(ncols=2, figsize=(18,5))
    _ = ax[0].scatter(cnt_m.keys(), cnt_m, alpha=0.6)
    _ = ax[0].set_xlabel('Datum')
    _ = ax[0].set_ylabel('Anzahl Flüge pro Tag')
    _ = ax[0].set_title('Flugbewegungen Mai')
    xin, xax = ax[0].get_xlim()
    _ = ax[0].hlines(y=median_m, xmin=xin, xmax=xax, linewidth=2, color='r', label="Median")
    _ = ax[0].hlines(y=mittel_m, xmin=xin, xmax=xax, linewidth=2, color='b', label="Mittelwert")
    _ = ax[0].legend()
    
    _ = ax[1].scatter(cnt_s.keys(), cnt_s, alpha=0.6)
    _ = ax[1].set_xlabel('Datum')
    _ = ax[1].set_ylabel('Anzahl Flüge pro Tag')
    _ = ax[1].set_title('Flugbewegungen September')
    xin, xax = ax[1].get_xlim()
    _ = ax[1].hlines(y=median_s, xmin=xin, xmax=xax, linewidth=2, color='r', label="Median")
    _ = ax[1].hlines(y=mittel_s, xmin=xin, xmax=xax, linewidth=2, color='b', label="Mittelwert")
    _ = ax[1].legend()
    
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
    