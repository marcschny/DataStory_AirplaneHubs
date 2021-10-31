#!/usr/bin/env python3

import csv

class Flight:
    def __init__(self, callsign, origin, destination, day, noFlights):
        self.callsign = callsign
        self.origin = origin
        self.destination = destination
        self.day = day
        self.noFlights = noFlights

class Airport:
    def __init__(self, ident, name, latitude, longitude):
        self.ident = ident
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

def readFlightData(file):
    flights=[]
    with open(r"data/raw/"+file, newline='') as csv_file:
        data = csv.DictReader(csv_file)
        
        for row in data:
            if(row["origin"] != "" and row["destination"] != ""):
                
                temp = row["callsign"];
                if(temp == ""):
                    temp = "UNDEF"
                flight = Flight(temp, row["origin"], row["destination"], row["day"], 1)
                flights.append(flight)
    return flights

def readAirports():
    airports = []
    with open(r'data/raw/airport-codes_csv.csv',newline='\n', encoding="ISO-8859-1") as csv_file:
        data = csv.DictReader(csv_file)

        for row in data:
            try:
                coords = row["coordinates"].split(",")
                airport = Airport(row["ident"], row["name"], coords[0], coords[1])
                airports.append(airport)
            except:
                pass
    return airports

def checkForDoubleFlights(flights):
    for i in range(len(flights)-1):
        j = i+1
        while j < len(flights):
            #if flight appears twice -> increase its noFlights and delete the second flight
            if flights[i].origin == flights[j].origin and flights[i].destination == flights[j].destination:
                flights[i].noFlights += 1
                flights.remove(flights[j])
            j += 1
    return flights

def save_flights(flights, fields, name):
    filename = "%s.csv" % name

    with open(filename, 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')

        writer.writerow(fields)
        
        for f in flights:
            writer.writerow([f.callsign, f.origin, f.destination, f.day, f.noFlights])

def save_airports(fields):
    with open('airports.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')

        writer.writerow(fields)

        for a in airports:
            writer.writerow([a.ident, a.name, a.latitude, a.longitude])
            
flights_sep = readFlightData("flightlist_09_2021_raw.csv")
flights_mai = readData("flightlist_05_2021_raw.csv")

flights_sep_no = checkForDoubleFlights(flights_sep)
flights_mai_no = checkForDoubleFlights(flights_mai)

airports = readAirports()

flight_fields = ["Callsign", "Origin", "Destination", "Day","noFlights"]
airport_fields = ["Ident", "Name", "Latitude", "Longitude"]

save_flights(flights_mai_no, flight_fields, "flights_05")
save_flights(flights_sep_no, flight_fields, "flights_09")
save_airports(airport_fields)
