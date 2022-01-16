#!/usr/bin/env python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go

import descriptive_stats as ds
import datastory_plots as dsp

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
    
    traffic = df_a_new[df_a_new['ident'].isin(df_flights.origin)]
    
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
    returns bar-chart with differences between flight connections
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

def difference_months_map(df_a, df_f):
    ''' 
    creates a scatter_mapbox of airports with most air traffic filtered by quantile divided by region
    quantiles of variables total & count_destinations & distance and,
    airports filtered by type
    '''
    df_f_mai = df_f[df_f['day'] < '2021-06-01']
    df_f_sep = df_f[df_f['day'] > '2021-06-01']
    
    df_a_mai = countTakeoffsAndLandings(df_a, df_f_mai, "mai")
    df_a_sep = countTakeoffsAndLandings(df_a, df_f_sep, "sep")
    
    q_a_mai = get_quantiles_of_regions(df_a_mai, 0.993, "mai")
    q_a_sep = get_quantiles_of_regions(df_a_sep, 0.993, "sep")
    
    df_a_mai_new = q_a_mai.loc[(q_a_mai['total_mai'] > q_a_mai['qt']) & (q_a_mai['count_destinations_mai'] > q_a_mai['qc'])]
    df_a_sep_new = q_a_sep.loc[(q_a_sep['total_sep'] > q_a_sep['qt']) & (q_a_sep['count_destinations_sep'] > q_a_sep['qc'])]
    
    q_f_mai = df_f_mai.quantile(0.993)
    q_f_sep = df_f_sep.quantile(0.993)
    
    df_flights_mai = df_f_mai.loc[df_f_mai['distance'] > q_f_mai['distance']];
    df_flights_sep = df_f_sep.loc[df_f_sep['distance'] > q_f_sep['distance']];
    
    traffic_mai = df_a_mai_new.loc[df_a_mai_new['ident'].isin(df_flights_mai.origin)]
    traffic_sep = df_a_sep_new.loc[df_a_sep_new['ident'].isin(df_flights_sep.origin)]
    
    return dsp.get_map_of_airports(traffic_mai, "total", "Verkehrknoten Mai"), dsp.get_map_of_airports(traffic_sep, "total", "Verkehrknoten September")

##Import from fetch_data.py & datastory_plots.py
def countTakeoffsAndLandings(df_airports, df_flights, month):
    '''Return new df with all airports and their value_counts'''
    
    takeoff = pd.DataFrame(columns=["airport", "counts"])
    takeoff['airport'] = df_flights['origin']
    takeoff["counts"] = takeoff.groupby("airport")["airport"].transform("count")
    
    landing = pd.DataFrame(columns=["airport", "counts"])
    landing['airport'] = df_flights['destination']
    landing["counts"] = landing.groupby("airport")["airport"].transform("count")
    
    takeoff.drop_duplicates(inplace=True)
    landing.drop_duplicates(inplace=True)
    takeoffs = takeoff.set_index("airport").to_dict("index")
    landings  = landing.set_index("airport").to_dict("index")
    df_airports["takeoffs_"+month] = df_airports['ident'].apply(lambda a: assignCountToFrame(a, takeoffs))
    df_airports["landings_"+month] = df_airports['ident'].apply(lambda a: assignCountToFrame(a, landings))
    df_airports['total_'+month] = df_airports['takeoffs_'+month] + df_airports["landings_"+month]
    df_airports = df_airports.loc[df_airports['total_'+month] != 0]
    
    num_dest = df_flights.groupby(['origin', 'destination']).size().reset_index().groupby('origin').size().reset_index().rename(columns={'origin':'airport', 0:'counts'}).set_index('airport').to_dict("index")
    df_airports['count_destinations_'+month] = df_airports['ident'].apply(lambda a: assignCountToFrame(a, num_dest))
    
    return df_airports

def assignCountToFrame(x,d):
    '''check if value is valid, otherwise return 0'''
    counts = 0
    try:
        counts = d[x]["counts"]
    except:
        pass
    return counts

def get_quantiles_of_regions(df_a, quantile, month):
    '''
    returns a new dataframe with new columns containing the calculated quantile per region.
    '''
    regions = df_a[df_a['total_'+month] != 0].groupby(['region', 'ident'])[['total_'+month,'count_destinations_'+month,'takeoffs_'+month,'landings_'+month]].sum().reset_index()
    q = regions.groupby('region')[['total_'+month,'count_destinations_'+month,'takeoffs_'+month,'landings_'+month]].quantile(quantile)
    labels = {'total_'+month:'qt', 'count_destinations_'+month:'qc', 'takeoffs_'+month:'qd', 'landings_'+month:'ql'}
    q = q.rename(columns=labels)
    regions = df_a.set_index('region')
    df_a_new = regions.join(q).reset_index()
    
    return df_a_new