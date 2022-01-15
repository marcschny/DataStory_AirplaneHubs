#!/usr/bin/env python3

from datetime import datetime
import pandas as pd
import numpy as np
import math
import seaborn as sns
import matplotlib.pyplot as plt

def get_stats(df, col):
    cnt = df.groupby(col).size().rename('Count')
    
    mittel  = round(cnt.mean(),2)
    varianz = round(cnt.var(),2)
    std     = round(cnt.std(),2)
    max_f   = round(cnt.max(),2)
    min_f   = round(cnt.min(),2)
    
    text = "\nMittelwert: " + str(mittel) + "\n"
    text += "Varianz:\t" + str(varianz) + "\n"
    text += "Standardabweichung: " + str(std)+"\n"
    text += "Max:"+str(max_f)+"\nMin:"+str(min_f)
    return text    

def stats_destinations(df):
    var    = round(df['count_destinations'].var(),2)
    std    = round(df['count_destinations'].std(),2)
    mittel = round(df['count_destinations'].mean(),2)
    median = round(df['count_destinations'].median(),2)
    
    count = len(df);
    
    text = "Anzahl Flughafen:"+str(count)+"\n"
    text += "Mittelwert: "+str(mittel)+"\n"
    text += "Median:\t"+str(median)+"\n"
    text += "Varianz:\t"+str(var)+"\n"
    text += "Standardabweichung: "+str(std)
    return text

def bar_category_region(df):
    fig, axes = plt.subplots(ncols=2, figsize=(20,7))
    df['type'].value_counts().plot(kind='bar', ax=axes[0])
    _ = axes[0].set_title('Bar-Chart Airport Typen')
    _ = axes[0].set_ylabel('Anzahl Flughafen')
    
    df['region'].value_counts().plot(kind='bar', ax=axes[1])
    _ = axes[1].set_title("Flughäfen pro Land")
    _ = axes[1].set_ylabel("Anzahl Flughäfen")
    return fig

def airport_infos(df):
    text = "Anzahl Flughafen total:\t"+ str(len(df)) + "\n"
    text += "Flughäfen für Flugzeuge:"+str(len(df[df['type'] == 'small_airport'])+len(df[df['type'] == 'medium_airport'])+len(df[df['type'] == 'large_airport']))+"\n\n"
    
    text += "Anzahl grosser Flughäfen: "+str(len(df[df['type'] == 'large_airport'])) + "\n"
    text += "Anzahl kleiner & mittlerer Flughäfen:   "+str(len(df[df['type'] == 'small_airport'])+len(df[df['type'] == 'medium_airport']))+ "\n"
    text += "\nAnzahl Flughäfen ohne Region/Continent: " + str(len(df[(df['region'] != 'unkown') | (df['continent'].notnull())]))
    
    select = df.loc[df['region'] == 'unkown']
    mittel = select['total'].mean()
    text += "\nDurchschnitt der Takeoffs/Landings ohne Region/Continent: "+str(mittel)+"\n"
    
    return text
    
def flight_infos(df):    
    df_mai = df.loc[df['day'] < '2021-06-01']
    df_sep = df.loc[df['day'] > '2021-06-01']
    
    cnt     = df.groupby('day').size().rename('Count')
    cnt_mai = df_mai.groupby('day').size().rename('Count')
    cnt_sep = df_sep.groupby('day').size().rename('Count')
    
    std = round(cnt.std(),2)
    std_mai = round(cnt_mai.std(),2)
    std_sep = round(cnt_sep.std(),2)
    median = round(cnt.median(),2)
    mittel = round(cnt.mean(),2)
    
    median_mai = cnt_mai.median()
    mittel_mai = round(cnt_mai.mean(),2)
    
    median_sep = cnt_sep.median()
    mittel_sep = round(cnt_sep.mean(),2)
    
    length_mai = len(df.loc[df['day'] < '2021-06-01'])
    length_sep = len(df.loc[df['day'] > '2021-06-01'])
    
    text = "Total FLugverbindungen: "+str(len(df))+"\n"
    text += "Median:\t\t\t" + str(median)+"\n"
    text += "Mittelwert:\t\t" + str(mittel)+"\n"
    text += "Standardabweichung:\t" + str(std)+"\n\n"
    
    text += "FLugverbindungen im Mai: "
    text += str(length_mai) + "\n"
    text += "Mittelwert:\t\t" +str(mittel_mai) + "\n"
    text += "Median:\t\t\t"+str(median_mai) + "\n"
    text += "Standardabweichung:\t" + str(std_mai)+"\n\n"
                                          
    text += "FLugverbindungen im Sep: "
    text += str(length_sep) + "\n"
    text += "Mittelwert:\t\t" +str(mittel_sep) + "\n"
    text += "Median:\t\t\t"+str(median_sep) + "\n"
    text += "Standardabweichung:\t" + str(std_sep)
    
    return text

def show_distribution(df_airports):   
    df_takeoffs = df_airports.sort_values(['takeoffs'], ascending=False).head(60)
    fig, ax = plt.subplots(figsize=(15,5))
    _ = ax.bar(df_takeoffs['ident'], df_takeoffs['takeoffs'], width=0.6, label="Takeoff's")
    _ = ax.bar(df_takeoffs['ident'], df_takeoffs['landings'], width=0.6, bottom=df_takeoffs['takeoffs'], label="Landings")
    _ = ax.set_title("Anzahl Flugverkehr")
    _ = ax.set_xlabel("Flughäfen")
    _ = ax.set_ylabel("Anzahl Flüge (ein- und ausgehend)")
    _ = ax.set_xticks(df_takeoffs['ident'])
    _ = ax.set_xticklabels(df_takeoffs['ident'],rotation=70)
    _ = ax.legend()
    return fig

def show_distribution_region(df_airports):   
    o = df_airports.groupby(['region'], as_index=False)[['takeoffs', 'landings', 'total']].sum()
    g = o.plot(x='region', y=['takeoffs','landings'], kind='barh', width=.95, figsize=(10,8),fontsize=13).set(
    title='Flugverkehr nach Region', xlabel="Anzahl Flugverbindungen", ylabel="Regionen")
    return g

def show_cum_flights(df, title):
    cnt = df.groupby('day').size().rename('Count')
    hist = np.histogram(cnt)
    pv = np.cumsum(cnt)

    fig, ax = plt.subplots(figsize=(20,5))
    _ = ax.step(cnt.keys(), pv, where='pre', drawstyle='steps', label='Kumulative Verteilung')
    _ = ax.set_title(title)
    _ = ax.set_ylabel("Kumulative Verteilung")
    _ = ax.set_xlabel("Datum")
    
    return ax

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

def show_stats_destinations(df_airports):
    o = df_airports.groupby(['region'], as_index=False)[['count_destinations']].sum()
    g = o.plot(x='region', y='count_destinations', kind='barh', width=.95, figsize=(10,8),fontsize=13).set(
    title='Anzahl unterschiedlicher Destinationen nach Region', xlabel="Anzahl Destinationen", ylabel="Regionen")
    return g

def load_airports():
    df = pd.read_csv("data/preprocessed/airports.csv")
    
    df['landings'] = df['landings'].astype(int)
    df['takeoffs'] = df['takeoffs'].astype(int)
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    df['type'] = df['type'].astype('category')
    df['region'] = df['region'].astype('category')
    
    return df

def load_flights():
    df = pd.read_csv("data/preprocessed/flights.csv")
    df['day'] = pd.to_datetime(df['day'])
    return df
    