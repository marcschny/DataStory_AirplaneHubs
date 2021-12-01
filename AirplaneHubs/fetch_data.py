#!/usr/bin/env python3
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
flights_path_sep = "data/raw/flightlist_05_2021_raw.csv"
airports = "data/raw/airport-codes_csv_raw.csv"

flight_fields = ["Callsign", "Origin", "Destination", "Day"]
airport_fields = ["Ident", "Name", "Latitude", "Longitude"]

def load_flights():
    #Loading Flights
    data_mai = pd.read_csv(flights_path_mai,   delimiter=',')
    data_sep = pd.read_csv(flights_path_sep,   delimiter=',')
    
    df_f = pd.concat([data_mai, data_sep], ignore_index=True)
    df_f = df_f[(df_f['origin'].notnull()) & (df_f['destination'].notnull())].reset_index()
    df_f['callsign'].fillna('UNDEF', inplace=True)
    
    df_f = df_f.drop(['index','number', 'aircraft_uid', 'typecode','firstseen','lastseen','latitude_1','longitude_1','altitude_1','latitude_2','longitude_2','altitude_2'], axis=1)
    
    return df_f

def load_airports():
    #Loading Airports
    df_a = pd.read_csv(airports,   delimiter=',')
    df_a['latitude'] = df_a['coordinates'].str.split(',').str[0]
    df_a['longitude'] = df_a['coordinates'].str.split(',').str[1]
    
    df_a = df_a.drop(['type', 'elevation_ft', 'continent', 'iso_country', 'iso_region', 'municipality', 'gps_code', 'iata_code', 'local_code', 'coordinates'], axis=1)
    
    return df_a