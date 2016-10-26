################################################################################
# Data converter/analyzer for Global City Ave Temp dataset                     #
#                                                                              #
# Authors                                                                      #
#  Yicheng Wang                                                                #
#                                                                              #
# Description                                                                  #
#  The file from Berkeley Labs and Kaggle is a csv file that monitors the      #
#  monthly temperature of major cities around the world. We want the average   #
#  yearly temperature and put them in the format of a list with each element   #
#  being in the format required by WebGL Globe:                                #
#  ['year', [lat, long, temp, lat, long, temp, ...]                            #
#                                                                              #
################################################################################


import csv
import json

temps = {}
result = []

with open("GlobalLandTemperaturesByMajorCity.csv", "rb") as original_dat:
    reader = csv.DictReader(original_dat)

    yearly_temp = []
    year = 0
    long = 0
    lat = 0

    max_temp = 0
    min_temp = 999

    for row in reader:
        if row['dt'][0:4] < "1950": # otherwise overloads js rip
            continue
        if row['dt'][0:4] != year: # new year
            if (len(yearly_temp) != 0):
                average_temp = sum(yearly_temp) / float(len(yearly_temp))

                if (max_temp < average_temp):
                    max_temp = average_temp

                if (min_temp > average_temp):
                    min_temp = average_temp

                if year in temps.keys():
                    temps[year] += [lat, long, average_temp]
                else:
                    temps[year] = [lat, long, average_temp]

            yearly_temp = []
            year = row['dt'][0:4]

            long = float(row['Longitude'][:-1])
            if row['Longitude'][-1] == 'W':
                long *= -1

            lat = float(row['Latitude'][:-1])
            if row['Latitude'][-1] == 'S':
                lat *= -1
        else:
            if (row['AverageTemperature'] != ''):
                yearly_temp.append(float(row['AverageTemperature']))

    for year in sorted(temps):
        scaled_temps = []
        #print temps[year]
        for i in range(2, len(temps[year]), 3):
            #print temps[year][i]
            scaled_temps += [temps[year][i - 2], temps[year][i - 1]]
            scaled_temps.append((temps[year][i] - min_temp) / (max_temp - min_temp))
            #print scaled_temps[-3:]

        result.append([year, scaled_temps])

with open("CityTempJSON.json", 'wb') as outfile:
    json.dump(result, outfile)
