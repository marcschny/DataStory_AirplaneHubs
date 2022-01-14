#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
from geopy.distance import geodesic

pd.options.mode.chained_assignment = None  # default='warn': ignore SettingWithCopyWarning


#class Flight:
#    def __init__(self, callsign, origin, destination, day):
#        self.callsign = callsign
#        self.origin = origin
#        self.destination = destination
#        self.day = day

#class Airport:
#    def __init__(self, ident, name, latitude, longitude):
#        self.ident = ident
#        self.name = name
#        self.latitude = latitude
#        self.longitude = longitude

#def readFlightData(file):
#    flights=[]
#    with open(r"data/raw/"+file, newline='') as csv_file:
#        data = csv.DictReader(csv_file)
        
#        for row in data:
#            if(row["origin"] != "" and row["destination"] != ""):
                
#                temp = row["callsign"];
#                if(temp == ""):
#                    temp = "UNDEF"
#                flight = Flight(temp, row["origin"], row["destination"], row["day"])
#                flights.append(flight)
#    return flights

#def readAirports():
#    airports = []
#    with open(r'data/raw/airport-codes_csv_raw.csv',newline='\n', encoding="ISO-8859-1") as csv_file:
#        data = csv.DictReader(csv_file)

#        for row in data:
#            try:
#                coords = row["coordinates"].split(",")
#                airport = Airport(row["ident"], row["name"], coords[0], coords[1])
#                airports.append(airport)
#            except:
#                pass
#    return airports

#def save_flights(flights, fields, name):
#    filename = "%s.csv" % name

#    with open(filename, 'w') as f:
#        writer = csv.writer(f, delimiter=',', lineterminator='\n')

#        writer.writerow(fields)
        
#        for f in flights:
#            writer.writerow([f.callsign, f.origin, f.destination, f.day])

#def save_airports(fields):
#    with open('data/raw/airports.csv', 'w') as f:
#        writer = csv.writer(f, delimiter=',', lineterminator='\n')

#        writer.writerow(fields)

#        for a in airports:
#            writer.writerow([a.ident, a.name, a.latitude, a.longitude])
            
#flights_sep = readFlightData("flightlist_09_2021_raw.csv")
#flights_mai = readFlightData("flightlist_05_2021_raw.csv")

#airports = readAirports()

#save_flights(flights_mai, flight_fields, "data/raw/flights_mai")
#save_flights(flights_sep, flight_fields, "data/raw/flights_sep")
#save_airports(airport_fields)

#######################################################
# New Version because we learned <3 Pandas <3
flights_path_mai = "data/raw/flightlist_05_2021_raw.csv"
flights_path_sep = "data/raw/flightlist_09_2021_raw.csv"
airports = "data/raw/airport-codes_csv_raw.csv"
regions = pd.DataFrame([['S', 'Südamerika'],
                        ['T', 'Zentralatlantik'],
                        ['L', 'Südeuropa'],
                        ['A', 'Südwest-Pazifik'],
                        ['B', 'Polarregion / Südeuropa'],
                        ['D', 'Westafrika'],
                        ['E', 'Nordeuropa'],
                        ['F', 'Südliches Afrika'],
                        ['N', 'Südpazifik'],
                        ['O', 'Naher Osten'],
                       ['U', 'Ehemalige Sowjetunion'],
                       ['G', 'Westafrikanische Küste'],
                       ['P', 'Nördlicher Pazifik'],
                       ['H', 'Ostafrika'],
                       ['V', 'Südasien'],
                       ['R', 'Ostasien'],
                       ['W', 'Südostasien'],
                       ['K', 'USA'],
                       ['M', 'Zentralamerika']], columns=['kennzeichen', 'region'])

def load_flights():
    '''Loading two flightlists.csv and merge to one structured DataFrame'''
    
    #Loading Flights
    data_mai = pd.read_csv(flights_path_mai, delimiter=',')
    data_sep = pd.read_csv(flights_path_sep, delimiter=',')
    
    df = pd.concat([data_mai, data_sep], ignore_index=True)
    df = df[(df['origin'].notnull()) & (df['destination'].notnull())].reset_index()
    df['callsign'].fillna('UNDEF', inplace=True)
    df['day'] = df['day'].str.split(' ').str[0]
    df['day'] = df['day'].apply(str_to_datetime)
    
    
    df = df.drop(['index','number','aircraft_uid', 'typecode','firstseen','lastseen','latitude_1','longitude_1','altitude_1','latitude_2','longitude_2','altitude_2'], axis=1)
    
    return df

def add_distance(df_f, airports):
    '''Adds distances to flights dataframe'''
    
    #create dictionary of airports
    airportsDict = airports.set_index("ident").to_dict("index")
    
    #only add flight where it's origin and destination are in airports
    airport_idents = airports['ident'].values
    flights = df_f.loc[(df_f.origin.isin(airport_idents)) & (df_f.destination.isin(airport_idents))]
    
    #origin coordinates as tuple
    flights["origin_latitudes"] = flights["origin"].apply(lambda x: airportsDict[x]["latitude"]).astype(float)
    flights["origin_longitudes"] = flights["origin"].apply(lambda x: airportsDict[x]["longitude"]).astype(float)
    flights["origin_coordinates"] = flights[["origin_latitudes","origin_longitudes"]].apply(tuple, axis=1)
    
    #destination coordinates as tuple
    flights["destination_latitudes"] = flights["destination"].apply(lambda x: airportsDict[x]["latitude"]).astype(float)
    flights["destination_longitudes"] = flights["destination"].apply(lambda x: airportsDict[x]["longitude"]).astype(float)
    flights["destination_coordinates"] = flights[["destination_latitudes","destination_longitudes"]].apply(tuple, axis=1)
    
    #coordinates tuple
    flights["coordinates"] = flights[["origin_coordinates", "destination_coordinates"]].apply(tuple, axis=1)
    
    #add distances using get_distance method
    flights["distance"] = flights["coordinates"].apply(get_distance)
    flights["distance"].astype(float)
    
    #drop columns
    flights = flights.drop(["origin_latitudes", "origin_longitudes", "origin_coordinates", "destination_latitudes", "destination_longitudes", "destination_coordinates", "coordinates"], axis=1)
    
    
    return flights



def get_distance(coordinates):
    '''Returns distance between two coordinates'''
    return geodesic(coordinates[0], coordinates[1]).km


def load_airports():
    '''Loading Airports.csv and structure DataFrame'''
    se_a = pd.read_csv(airports,   delimiter=',')
    
    df = pd.DataFrame(se_a)
    df['latitude'] = df['coordinates'].str.split(',').str[1]
    df['longitude'] = df['coordinates'].str.split(',').str[0]
    df['region'] = df['ident'].apply(extract_region_from_icao)
    df = df.drop(['elevation_ft', 'iso_country', 'iso_region', 'gps_code', 'iata_code', 'local_code', 'coordinates', 'continent'], axis=1)
    
    return df

def assignCountToFrame(x,d):
    counts = 0
    try:
        counts = d[x]["counts"]
    except:
        pass
    return counts

def countTakeoffsAndLandings(df_airports, df_flights):
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
    df_airports["takeoffs"] = df_airports['ident'].apply(lambda a: assignCountToFrame(a, takeoffs))
    df_airports["landings"] = df_airports['ident'].apply(lambda a: assignCountToFrame(a, landings))
    df_airports['total'] = df_airports['takeoffs'] + df_airports['landings']
    df_airports = df_airports[df_airports['total'] != 0]
    
    num_dest = df_flights.groupby(['origin', 'destination']).size().reset_index().groupby('origin').size().reset_index().rename(columns={'origin':'airport', 0:'counts'}).set_index('airport').to_dict("index")
    df_airports['count_destinations'] = df_airports['ident'].apply(lambda a: assignCountToFrame(a, num_dest))
    
    return df_airports

def str_to_datetime(date):
    '''Convert a str of "YYYY-MM-DD" strings to datetime objects.'''
    y, m, d = (int(x) for x in date.split("-"))
    date = datetime(y, m, d)
    return date


def extract_region_from_icao(x):
    re = x[0:1].upper()
    re = regions[regions['kennzeichen'] == re].values
    region = "unkown"
    
    if(len(re) == 1):
        region = re[0][1]
    
    return region

def save_file(df, file):
    df.to_csv(file, index=False)


#load flights and airports dataframes    
df_a = load_airports()
df_f = load_flights()

#add distances to flights 
df_flights  = add_distance(df_f, df_a)

#calculate takeoffs and landings
df_airports = countTakeoffsAndLandings(df_a, df_f)

#save dataframes as csv-file
save_file(df_airports, 'data/preprocessed/airports.csv')
save_file(df_flights, 'data/preprocessed/flights.csv')