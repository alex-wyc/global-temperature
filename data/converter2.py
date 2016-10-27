import csv
import json

temps = []

with open("GlobalTemperatures.csv", 'rb') as original_dat:
    reader = csv.DictReader(original_dat)

    yearly_temp = []
    year = 0

    max_temp = []
    min_temp = []

    for row in reader:
        if row['dt'][0:4] < "1950": # just continue
            continue

        if row['dt'][0:4] != year: # new year
            if (len(yearly_temp) != 0):
                average_temp = sum(yearly_temp) / float(len(yearly_temp))
                
                maxv = "No Data"
                minv = "No Data"

                if len(max_temp):
                    maxv = max(max_temp)

                if len(min_temp):
                    minv = min(min_temp)

                temps.append([average_temp, maxv, minv])

            yearly_temp = []
            year = row['dt'][0:4]
            max_temp = []
            min_temp = []

        else:
            if (row['LandAverageTemperature'] != ''):
                yearly_temp.append(float(row['LandAverageTemperature']))
            if (row['LandMaxTemperature'] != ''):
                max_temp.append(float(row['LandMaxTemperature']))
            if (row['LandMinTemperature'] != ''):
                min_temp.append(float(row['LandMinTemperature']))

with open("WorldTempJSON.json", 'wb') as outfile:
    json.dump(temps, outfile)
