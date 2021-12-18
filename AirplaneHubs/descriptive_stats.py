#!/usr/bin/env python3

from datetime import datetime
import pandas as pd
import numpy as np
import math
import seaborn as sns
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
    cnt = df.groupby('day').size().rename('Count')
    median = cnt.median()
    mittel = cnt.mean()
    
    length_mai = len(df.loc[df['day'] < '2021-06-01'])
    length_sep = len(df.loc[df['day'] > '2021-06-01'])
    
    text = "Total FLugverbindungen: "+str(length_mai+length_sep)+"\n"
    text += "Anzahl FLugverbindungen im Mai: "
    text += str(length_mai) + "\n"
    text += "Anzahl FLugverbindungen im Sep: "
    text += str(length_sep) + "\n\n"
    text += "Durchschnitt der Flugbewegungen\n"
    text += "Median:\t  " + str(median)+"\n"
    text += "Mittelwert:" + str(mittel)+"\n"
    
    return text

def show_flights_seperate(df_mai, df_sep):
    cnt_m = df_mai.groupby('day').size().rename('Count')
    cnt_s = df_sep.groupby('day').size().rename('Count')
    
    median_m = cnt_m.median()
    mittel_m = cnt_m.mean()
    median_s = cnt_s.median()
    mittel_s = cnt_s.mean()
    
    fig, ax = plt.subplots(ncols=2, figsize=(18,5))
    _ = ax[0].plot(cnt_m.keys(), cnt_m)
    _ = ax[0].set_xlabel('Datum')
    _ = ax[0].set_ylabel('Anzahl Flüge pro Tag')
    _ = ax[0].set_title('Flugbewegungen Mai')
    xin, xax = ax[0].get_xlim()
    _ = ax[0].hlines(y=median_m, xmin=xin, xmax=xax, linewidth=2, color='g', label="Median")
    _ = ax[0].hlines(y=mittel_m, xmin=xin, xmax=xax, linewidth=2, color='b', label="Mittelwert")
    _ = ax[0].legend()
    
    _ = ax[1].plot(cnt_s.keys(), cnt_s)
    _ = ax[1].set_xlabel('Datum')
    _ = ax[1].set_ylabel('Anzahl Flüge pro Tag')
    _ = ax[1].set_title('Flugbewegungen September')
    xin, xax = ax[1].get_xlim()
    _ = ax[1].hlines(y=median_s, xmin=xin, xmax=xax, linewidth=2, color='g', label="Median")
    _ = ax[1].hlines(y=mittel_s, xmin=xin, xmax=xax, linewidth=2, color='b', label="Mittelwert")
    _ = ax[1].legend()
    
    return fig

def show_distribution(df_a):   
    df = df_a.loc[df_a['total'] != 0].sort_values('total', ascending=False)
    df = df.head(50)
    g = sns.catplot(data=df, x='ident', y='total', kind='bar', height=5, aspect=3)    
    g.set_xticklabels(rotation=60) 
    return g

def show_distribution_region(df_a):   
    g = sns.catplot(data=df_a, x='region', y='total', kind='bar', height=5, aspect=2)    
    g.set_xticklabels(rotation=90) 
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
    