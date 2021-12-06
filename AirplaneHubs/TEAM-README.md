# Data Stories HS 2021


## Team
- Marc Schnydrig (https://gitlab.fhnw.ch/marc.schnydrig)
- Koray Oezkaynak (https://gitlab.fhnw.ch/koray.oezkaynak)


## Ziel
Ziel ist es ausgehend eines bestimmten Tages alle gesammelten Flüge auf einer Karte zu visualisieren.
~~Der Nutzende kann dann ausgehend eines bestimmten Fluges die CO2-Emissionen dieses Fluges berechnen lassen.~~
[Update 30.10.2021]
Nach intensiver Recherche mussten wir feststellen, dass die Berechnung von CO2-Emissionen wegen 
mangelnder Daten, nur sehr unpräzise durchgeführt werden können. Dafür werden detailliertere Daten
zum Flugmodell wie das maximale Gewicht, das Leergewicht oder die Passagieranzahl benötigt.
Neu werden Analysen durchgeführt, um folgende Fragen zu beantworten:
- Welche Flughäfen weisen einen hohen Flugverkehr auf?
- Welche Flughäfen weisen die meisten Verbindungen auf?
- Welches sind die längsten Distanzen die zurückgelegt werden?
- Welche Flughäfen können als Verkehrsknotenpunkt identifiziert werden?
- Welche Unterschiede in den Flugbewegungen sind im Sommer zum Frühling zu sehen?


## Datenquellen
Wir verwenden folgende Datenquellen für die Data-Story - Download vom [26.10.2021]:
- Flugdaten - OpenSky Network API (https://opensky-network.org/)
- Flugplätze (https://datahub.io/core/airport-codes)
- Emissionsberechnung (https://www.klimaneutral-handeln.de/php/kompens-berechnen.php)


## Data Collection
Die Datensammlung kann mittels Script "fetch_data.py" ausgeführt werden. 
Um diese zu starten sind zwingend die Rohdaten wie folgt abzulegen: 
- data/raw/fluege_09_2021_raw.csv
- data/raw/fluege_05_2021_raw.csv
- data/raw/airports-codes_csv_raw.csv

ACHTUNG: Da wir alle Flüge auf doppeltes vorkommen prüfen, geht der Vorgang sehr lange. 
Wir suchen aktuell noch eine Methode wie wir dies beschleunigen/verbessern.
Infolgedessen sind Zeile 83 & 84 auskommentiert.
Nach Ausführung der Datensammlung befindet sich jeweils ein Flug-File sowie Airport-File unter "data". 


## Data Description: Raw
Wie bereits kurz in der Data Collection angedeutet, benutzen wir zwei unterschiedliche Datenquellen. 
In der folgenden Tabelle sind alle Attribute aus den Datenquellen aufgezeigt. 

[airports.csv](https://datahub.io/core/airport-codes "Quelle Flughäfen")

| Ident (String) | Type (String)    | Name (String)	        | Elevation Feet (Int)  | Continent (String)    | ISO-Country (String)  | ISO-Region (String)   | Municipality (String) | GPS-Code (String) | Iata-Code (String)    | Local-Code (String)   | Coordinates (String)      |
| ------------   |    ------------- | -------------         | ------------------    | ------------------    | --------------        | ----------            | ------------------    | ---------------   | ----------            | -------------------   | ----------                |
| 00AA           | small_airport    | Aero- B Ranch Airport	| 3435          	    | NA                    | US                    | US-KS                 | Leoti                 | 00AA              | -                     | 00AA                  | "-101.473911, 38.704022"  |

[fluege_jahr_monat.csv](https://zenodo.org/record/5557026#.YX02JhxCSM- "Quelle Flugbewegungen")

| Callsign (String)   | Number (String) | Aircraft_UID (String)                  | Typecode (String)        | Origin (String)   | Destination (Sting)   | Firstseen (String)        | Lastseen (String)          | Day (String)               | Latitude 1 (String)     | Longitude 1 (String)      | Altitude 1 (String)       | Latitude 2 (String)       | Longitude 2 (String)      | Altitude 2 (String)       |
| ----------------    | --------------  | ------------------                     | ---------------------    | ------------      | -------------         | ------------              | ---------------            | ---------                  | -----------             | ---------------------     | ------------------        | ----------------------    | ----------------------    | --------------------      | 
| CPA343			  | -   			| a6ffcb66-91a7-4cbf-9afb-fd2b9130fd9	 | A359     		        | YMML              | EGKK                  | 2018-12-31 04:51:50+00:00 | 2019-01-01 05:00:27+00:00  | 2019-01-01 00:00:00+00:00  | -37.68667602539062      | 144.84135404546208        | 304.8                     | 51.15701293945312         | -0.126342773437           | 83.82000000000002         |


## Data Description: Preprocessed
In der folgenden Tabelle beschreiben wir die benötigten Attribute aus den Datenquellen; Dabei ist jeweils die Attribute, dessen Typ sowie ein Beispiel enthalten (Alle Variablen sind 1-Dimensional):

#### airports.csv

| Ident (String) | Name (String)	        | Latitude (Double)         | Longitude (Double)       | Continent (String)      | Region (String)     | Municipality (String)      |
| ------------   | -------------            | ----------                | ----------               | ----------      | ----------      | ----------      |
| CPA343         | Aero- B Ranch Airport	| -101.473911               |  38.704022               | EU              | Südeuropa      | Grenchen       |

#### flights.csv

| Callsign (String)   | Origin (String)   | Destination (Sting)   | Day (String)               |
| ----------------    | ------------      | -------------         | ---------                  |
| 00AA  			  | YMML              | EGKK                  | 2019-01-01 00:00:00+00:00  | 

Da nicht immer alle Daten vorhanden sind, müssen Datensätze bei welcher "Origin" und "Destination" fehlen, aussortiert werden da diese essenziell zur Durchführung der Analysen sind.


## Descriptive Stats
Wer hat die Daten erhoben? </br>
Siehe [Datenquellen](#Datenquellen) </br>

Wie wurden die Daten erhoben? </br>
Die Datensätze wurden heruntergeladen (siehe ebenfalls [Datenquellen](#Datenquellen)) </br>

Wann wurden die Daten erhoben? </br>
Siehe [Datenquellen](#Datenquellen) </br>

Wie viele Datenpunkte (n) wurden erfasst? </br>
1'048'576 Flüge und 57'422 Flughäfen </br>

Wurden Attribute präprozessiert? Falls ja, wie? </br>
 Das Attribute "Coordinates" aus den Flughafen-Rohdaten wurde präprozessiert. Dabei wird der Tupel "Coordinates" 
bei jedem Flughafen gesplittet, und auf zwei neue Attribute "Latitude" und "Longtitude" aufgeteilt. </br>

Wurden die Daten gefiltert? Falls ja, wie? </br>
 Beim Einlesen der Flug-Rohdaten wird jeweils überprüft "Origin" und "Destination" des Fluges vorhanden sind.
Sind diese Felder leer, werden sie heraussortiert.</br>

Welche Merkmale, Variablen, Attribute wurden erfasst? </br>
 Siehe [Data Description: Preprocessed](#Data-Description:-Preprocessed)</br>

###  Qualitative Beschreibung der Variablen¶
#### Kategorische Variablen
##### FLights
Callsign, Origin & Destination sind nominale Variablen. Callsign besitzt selbst keine Ordnung und dient als Identifikationsnummer. <br>

Origin & Destination sind nominale Strings und lassen sich kategorisieren. Der sogenannte ICAO (International Civil Aviation Organization)  Nummer kann in zwei Substrings aufgeteilt werden. Erster Teil identifiziert Region/Kontinent und der zweite Buchstabe kennzeichnet das Land. <br>
IATA: ZRH; ICAO LSZH:
- L -> Südeuropa
- LS -> Schweiz
- ZH -> Zurich Airport

##### Airports
Der Ident bildet der ICAO String eines Flughafens und ist eindeutig. Er lässt sich wie vorhin beschrieben in Geographische Orte einordnen.<br>

Der Type beschreibt die Art des Flughafens welches erlaubt, unterschiedliche Flughafen bei Analysen zu Kennzeichnen. 

#### Quantitative Variablen
##### FLights
Die Spalte "day" ist als Variable auf der Intervallskala zu betrachten. Wir können Gleichheiten von Differenzen untersuchen, besitzen aber keinen natürlichen Nullpunkt. 

##### Airports
Latitude und Longitude bilden die Koordinaten des Flughafens. Diese sind in dezimaler Form und erlaubt uns sämltiche Kartenvisualisierungen mit Distanzen zu visualisieren. 

Angaben zu den Variablen, Merkmalen und Typen befinden sich unter [Data Description: Preprocessed](#Data-Description:-Preprocessed)

#### Zusammenhang verschiedener Variablen
Mittels zweier Dataframes "flights" & "airports" können wir die Anzahl FLüge pro Flughafen untersuchen. Dabei Untersuchen wir die Vorkomnisse in der Zeit sowie in geographische Abhängigkeiten.

## Milestones
- 10.10.21 - Thema und Datensatz ist festgelegt
- 31.10.21 - Rohdaten sind gesammelt und qualitativ beschrieben & dokumentiert. 
- 06.12.21 - Deskritive Statistiken (Jupyter Notebook)
- 19.12.21 - Daten sind explorativ visualisiert. Kernaussagen sind mit Visualisierungen illustriert.
- 16.01.22 - Abgabe