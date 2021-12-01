#!/usr/bin/env python3

from datetime import datetime
import csv
import pandas as pd

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

def load_flights():
    '''Loading two flightlists.csv and merge to one structured DataFrame'''
    
    #Loading Flights
    data_mai = pd.read_csv(flights_path_mai,   delimiter=',')
    data_sep = pd.read_csv(flights_path_sep,   delimiter=',')
    
    df = pd.concat([data_mai, data_sep], ignore_index=True)
    df = df[(df['origin'].notnull()) & (df['destination'].notnull())].reset_index()
    df['callsign'].fillna('UNDEF', inplace=True)
    df['day'] = df['day'].str.split(' ').str[0]
    df['day'] = df['day'].apply(str_to_datetime)
    
    df['callsign'] = df['callsign'].astype(str)
    df['origin'] = df['origin'].astype(str)
    df['destination'] = df['destination'].astype(str)
    
    df = df.drop(['index','number', 'aircraft_uid', 'typecode','firstseen','lastseen','latitude_1','longitude_1','altitude_1','latitude_2','longitude_2','altitude_2'], axis=1)
    
    return df

def load_airports():
    '''Loading Airports.csv and structure DataFrame'''
    se_a = pd.read_csv(airports,   delimiter=',')
    
    df = pd.DataFrame(se_a)
    df['latitude'] = df['coordinates'].str.split(',').str[0]
    df['longitude'] = df['coordinates'].str.split(',').str[1]
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    
    df['ident'] = df['ident'].astype(str)
    df['type'] = df['type'].astype(str)
    df['name'] = df['name'].astype(str)
    
    df = df.drop(['elevation_ft', 'continent', 'iso_country', 'iso_region', 'municipality', 'gps_code', 'iata_code', 'local_code', 'coordinates'], axis=1)
    
    return df

def str_to_datetime(date):
    '''Convert a str of "YYYY-MM-DD" strings to datetime objects.'''
    y, m, d = (int(x) for x in date.split("-"))
    date = datetime(y, m, d)
    return date