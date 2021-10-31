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
- data/raw/fluege_jahr_monat.csv
- data/raw/airports.csv

Nach Ausführung der Datensammlung befindet sich ein data.csv-File unter "data". 


## Data Description . Raw
Wie bereits kurz in der Data Collection angedeutet, benutzen wir zwei unterschiedliche Datenquellen. 
In der folgenden Tabelle beschreiben wir die benötigten Attribute aus den Datenquellen. 

[airports.csv](https://datahub.io/core/airport-codes "Quelle Flughäfen")

| Ident - ICAO-Code (String) | Name (String)	| Latitude 	(Double) | Longitude (Double) |
| ------------       |    ---------------- | ------------------ | ------------------      |
| LSZH 		         | Zuerich Airport     | 47.458056 		    | 8.548056 	              | 

[fluege_jahr_monat.csv](https://zenodo.org/record/5557026#.YX02JhxCSM- "Quelle Flugbewegungen")

| Callsign (String)   | Origin (String)	| Destination (String)	| Day (UTC Day)					|
| ----------------    | --------------  | ------------------    | ----------------------------- |
| DLH439			  | KSEA			| LSZH					| 2021-08-01 00:00:00+00:00     |

Da nicht immer alle Daten vorhanden sind, müssen Datensätze bei welcher "Origin" und "Destination" fehlen, 
aussortiert werden da diese essenziell zur Durchführung der Analysen sind. 


## Milestones
- 10.10.21 - Thema und Datensatz ist festgelegt
- 31.10.21 - Rohdaten sind gesammelt und qualitativ beschrieben & dokumentiert. 
- 12.12.21 - Daten sind explorativ visualisiert. Kernaussagen sind mit Visualisierungen illustriert. 
- 16.01.22 - Abgabe