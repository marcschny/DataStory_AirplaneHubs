#!/usr/bin/env python3

#import statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import descriptive_stats as ds
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.ticker as ticker

def load_data():
    ''' 
    returns pre-processed data files for airports and flights 
    '''
    df_airports = pd.read_csv("data/preprocessed/airports.csv")
    df_flights = pd.read_csv("data/preprocessed/flights.csv")
    return df_airports, df_flights


def flight_connections(df):
    ''' groups takeoffs, landings and total per region
    and returns grouped bar plot for flight traffic per region
    '''
    o = df.groupby(['region'], as_index=False)[['takeoffs', 'landings', 'total']].sum()
    g = o.plot(x='region', y=['takeoffs','landings'], kind='barh', width=.8, figsize=(12,7)).set(title='Flugverkehr nach Region', xlabel="Anzahl Flugverbindungen", ylabel="Regionen")
    
    return g

def traffic_map_total_destinations(df, quantile):
    ''' 
    creates a scatter_mapbox of airports with most air traffic filtered by quantile divided by region
    quantiles of variables total & count_destinations
    '''
    df_a = get_quantiles_of_regions(df, quantile)
    most_traffic = df_a.loc[(df_a['total'] > df_a['qt']) & (df_a['count_destinations'] > df_a['qc'])]
    
    return get_map_of_airports(most_traffic, "total", "Weltweiter Flugverkehr nach Anzahl Flugverbindungen")

def traffic_map_total_destinations_distance(df_a, df_f, quantile):
    ''' 
    creates a scatter_mapbox of airports with most air traffic filtered by quantile divided by region
    quantiles of variables total & count_destinations & distance
    '''
    q_a = get_quantiles_of_regions(df_a, quantile)
    df_a_new = q_a.loc[(q_a['total'] > q_a['qt']) & (q_a['count_destinations'] > q_a['qc'])]
    
    q_f = df_f.quantile(quantile)
    df_flights = df_f[df_f['distance'] > q_f['distance']];
    
    most_traffic = df_a_new[df_a_new['ident'].isin(df_flights.destination)]
    
    return get_map_of_airports(most_traffic, "total", "Verkehrknoten weltweit anhand Verbindungen")

def get_map_of_airports(df, col, title):
    '''
    create a map with circles which size depends of col value
    '''
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                      color=col, size=col,
                      color_continuous_scale='magma',
                      size_max=24, zoom=1.2, hover_name='name', 
                      hover_data = ['municipality'], 
                      title = title,
                      width=900, height=540)
    fig.update_layout(mapbox_style="open-street-map", margin=dict(l=10, r=10, t=50, b=40))
    return fig

def get_quantiles_of_regions(df_a, quantile):
    '''
    returns a new dataframe with new columns containing the calculated quantile per region.
    '''
    regions = df_a[df_a['total'] != 0].groupby(['region', 'ident'])[['total','takeoffs','landings','count_destinations']].sum().reset_index()
    q = regions.groupby('region')[['total','count_destinations','takeoffs','landings']].quantile(quantile)
    labels = {'total':'qt', 'count_destinations':'qc', 'takeoffs':'qd', 'landings':'ql'}
    q = q.rename(columns=labels)
    regions = df_a.set_index('region')
    df_a_new = regions.join(q).reset_index()
    
    return df_a_new

def show_stats(df_flights):
    ''' 
    computes statistics (mean, abbreviation, ...) for both months (may and september)
    and returns these statistics together with a bar plot
    '''
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
    #_ = ax[0].set_xticklabels(xlabels_m)
    _ = ax[0].legend()

    flights_s.plot(kind="bar", width=.8, rot=85, title="Flugverbindungen Monat Sep.", xlabel="Tag", ylabel="Anzahl Verbindungen", ax=ax[1])
    xmin, xmax = ax[0].get_xlim()
    _ = ax[1].hlines(mittel_s, xmin, xmax, 'red', linestyle='-', label='Mittelwert')
    _ = ax[1].hlines(mittel_s-std_s, xmin, xmax, 'lightgreen', linestyle='--', label='Standardabweichung')
    _ = ax[1].hlines(mittel_s+std_s, xmin, xmax, 'lightgreen', linestyle='--')
    _ = ax[1].legend()
    
    _ = plt.subplots_adjust(hspace = 1.8)
    
    return fig, mittel_m, mittel_s, std_m, std_s


def map_longest_flight_distances(df_airports, df_flights):
    ''' 
    processes new dataframe to compute the longest flight distances
    and returns the top 50 longest flights as a ScatterGeo figure
    '''
    
    # create dictionary of airports
    airportsDict = df_airports.set_index("ident").to_dict("index")

    # only flights with distances > 1.0
    flightDistances = df_flights[df_flights.distance > 1.0]
    # sort flights by distance descending
    flightDistances = flightDistances.sort_values(by=["distance"], ascending=False)
    # assign airports group-count to flightDistances.counts
    flightDistances["counts"] = flightDistances.groupby("distance")["distance"].transform("count")
    # drop duplicates from flightDistances
    flightDistances.drop_duplicates(subset=["distance"], inplace=True)

    # add columns o_lat, o_long, d_lat, d_long
    flightDistances["o_lat"] = flightDistances.origin.apply(lambda a: airportsDict[a]["latitude"])
    flightDistances["o_long"] = flightDistances.origin.apply(lambda a: airportsDict[a]["longitude"])
    flightDistances["d_lat"] = flightDistances.destination.apply(lambda a: airportsDict[a]["latitude"])
    flightDistances["d_long"] = flightDistances.destination.apply(lambda a: airportsDict[a]["longitude"])

    # first 50 flight distances
    topFlightDistances = flightDistances.reset_index().head(50)

    # create figure
    fig = go.Figure()

    # add flight traces to map
    flight_paths = []
    for index, row in topFlightDistances.iterrows():
        fig.add_trace(
            go.Scattergeo(
                locationmode = "country names",
                lon = [row["o_long"], row["d_long"]],
                lat = [row["o_lat"], row["d_lat"]],
                mode = "lines+markers",
                line = dict(width = 0.7+(row["counts"]*0.02), color = "#5b2c6f"),
                opacity = 0.75,
                name = "",
                marker = {'size': 4},
                hovertemplate =
                "<b>"+str(airportsDict[row["origin"]]["municipality"])+" to "+str(airportsDict[row["destination"]]["municipality"])+"</b><br>" +
                str(round(row["distance"], 2))+"km<br>"+
                str(row["counts"])+" times<br>" 
            )
        )

    # visualization adjustments
    fig.update_traces(
        hoverinfo = "text",
    )    

    fig.update_layout(
        title_text = "Distanz von Flugverbindungen",
        showlegend = False,
        width=900, height=540,
        margin=dict(l=10, r=10, t=50, b=40),
        hoverlabel=dict(
            bgcolor="#5b2c6f",
            font_size=15,
            font_family="Calibri"
        ),
        geo = dict(
            scope = "world",
            #projection_type = "orthographic",
            showland = True,
            showocean = True,
            showcoastlines = False,
            showcountries = True,
            landcolor = "#F2EFE9",
            countrycolor = "#DDDDDD",
            oceancolor = "#AAD3DF",
            bgcolor = "#FFFFFF",
        ),
    )
    
    return fig
