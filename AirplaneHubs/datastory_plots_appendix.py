#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import descriptive_stats as ds
import datastory_plots as dsp
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go

def distribution_takeoff_landings(df_airports):
    df_takeoffs = df_airports.sort_values(['takeoffs'], ascending=False).head(50)
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

def traffic_map_typ(df_a, df_f):
    ''' 
    creates a scatter_mapbox of airports with most air traffic filtered by quantile divided by region
    quantiles of variables total & count_destinations & distance and,
    airports filtered by type
    '''
    q_a = dsp.get_quantiles_of_regions(df_a, 0.993)
    df_a_new = q_a.loc[(q_a['total'] > q_a['qt']) & (q_a['count_destinations'] > q_a['qc'])]
    
    q_f = df_f.quantile(0.993)
    df_flights = df_f[df_f['distance'] > q_f['distance']];
    
    traffic = df_a_new[df_a_new['ident'].isin(df_flights.destination)]
    
    traffic_by_type = traffic[traffic['type'] == 'large_airport']
    
    return dsp.get_map_of_airports(traffic_by_type, "total", "Verkehrknoten weltweit anhand Verbindungen")


def distance_of_small_airports(df_airports, df_flights):
    '''
    '''
    small_airports = df_airports[df_airports.type == "small_airport"]
    
    airportsDict = df_airports.set_index("ident").to_dict("index")

    # create list of ident
    small_airports_idents = small_airports["ident"].unique().tolist()
    # all flights with takeoff from small airports
    flights_from_small_airports = df_flights[(df_flights.origin.isin(small_airports_idents)) ]
    # sort by distance
    flights_from_small_airports = flights_from_small_airports.sort_values(by="distance", ascending=False)
    # assign airports group-count to flightDistances.counts
    flights_from_small_airports["counts"] = flights_from_small_airports.groupby("distance")["distance"].transform("count")

    # drop duplicates
    flights_from_small_airports.drop_duplicates(subset=["distance"], inplace=True)

    # add columns o_lat, o_long, d_lat, d_long
    flights_from_small_airports["o_lat"] = flights_from_small_airports.origin.apply(lambda a: airportsDict[a]["latitude"])
    flights_from_small_airports["o_long"] = flights_from_small_airports.origin.apply(lambda a: airportsDict[a]["longitude"])
    flights_from_small_airports["d_lat"] = flights_from_small_airports.destination.apply(lambda a: airportsDict[a]["latitude"])
    flights_from_small_airports["d_long"] = flights_from_small_airports.destination.apply(lambda a: airportsDict[a]["longitude"])
    # top 20 flight distances from small airports
    top_flights_from_small_airports = flights_from_small_airports.reset_index().head(20)
    # list of top 20 small airport origins
    top_flights_from_small_airports_list = top_flights_from_small_airports.origin.tolist()
    
    print("Längste Flüge kleiner Flughäfen: ")
    display(top_flights_from_small_airports[["origin", "destination", "day", "distance", "counts"]].head())

    print("Kleine Flughäfen mit längsten Distanzen: ")
    display(small_airports[["name", "municipality", "region", "total"]][small_airports.ident.isin(top_flights_from_small_airports_list)].head())
    
    fig = go.Figure()

    # add flight traces to map
    for index, row in top_flights_from_small_airports.iterrows():
        fig.add_trace(
            go.Scattergeo(
                locationmode = "country names",
                lon = [row["o_long"], row["d_long"]],
                lat = [row["o_lat"], row["d_lat"]],
                mode = "lines+markers",
                line = dict(width = 1, color = "#E6A64C"),
                opacity = 0.69,
                name = "",
                text = str(row["origin"])+" to "+str(row["destination"])+", "+str(round(row["distance"], 2))+"km, "+str(row["counts"])+" times",
                marker = {"size": 8}
            )
        )
    # visualization adjustments
    fig.update_traces(hoverinfo = "text",)
    fig.update_layout(
        title_text = "Länste Flugdistanzen kleiner Flughäfen (Top 20)",
        showlegend = False,
        width=900, height=540,
        margin=dict(l=10, r=10, t=50, b=40),
        geo = dict(
            scope = "world",
            #projection_type = "orthographic",
            showland = True,
            showocean = True,
            showcoastlines = False,
            showcountries = True,
            landcolor = "#F2F2F2",
            countrycolor = "#DDDDDD",
            oceancolor = "#FFFFFF",
            bgcolor = "#FFFFFF",
        ),
    )
    
    return fig

def difference_between_months(df_flights):
    '''
    return bar-chart with differents of flight connections
    '''
    df_flights["month"] = df_flights["day"].apply(lambda day: "May" if "-05-" in day else "September")
    
    df_flights["month_count"] =  df_flights.groupby("month")["month"].transform("count")
    
    h = sns.countplot(
        data=df_flights,
        x="month",
        palette=sns.color_palette(['orange', 'mediumseagreen'])
    )
    _ = h.set(xticklabels=["Mai", "September"])
    
    ylabels = ['{:,.2f}'.format(y) + 'K' for y in h.get_yticks()/1000]
    
    _ = h.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: '{:,.2f}'.format(y/1000) + 'K')) 
    
    return h