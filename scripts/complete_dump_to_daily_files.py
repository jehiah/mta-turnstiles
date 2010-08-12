"""
This takes a mta .txt data dump, and normalizes it to a single set of columns so it's a file that can be combined/sorted with other data sets
"""

import sys
import os
import csv
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import tornado.options

def load_stations(station_file):
    input_file = open(station_file, 'rb')
    reader = csv.reader(input_file)
    data = {}
    for row in reader:
        if not row or row[0] == 'unit':
            continue
        control_unit = row[0]
        station = row[-1]
        data[control_unit] = station
    input_file.close()
    return data

def run(input_filename, output_filename, stations_lookup):
    logging.info('reading %s' % input_filename)
    logging.info('outputing to %s' % output_filename)
    input_file = open(input_filename, 'rb')
    reader = csv.reader(input_file)
    
    # read the data getting only midnight entries
    data = {}
    for row in reader:
        if not row:
            continue
        time_str = row[4]
        if time_str != "00:00:00":
            continue
        key = ','.join(row[:3])
        values = [row[3], int(row[-2]), int(row[-1])]
        if key not in data:
            data[key] = []
        data[key].append(values)
    
    # now summarize each key to a daily total (ie: diff the previous day)
    daily_key_totals = {}
    for key, data_series in data.items():
        daily_key_totals[key] = []
        data_series.sort()
        for i in range(len(data_series)-1):
            date, entrances, exits = data_series[i]
            next_date, next_entrances, next_exits = data_series[i+1]
            delta_entrances = next_entrances - entrances
            delta_exits = next_exits - exits
            if key.startswith('A002,R051') :
                logging.info((key, date, entrances, exits, next_date, next_entrances, next_exits, delta_entrances, delta_entrances))
            if date == next_date:
                logging.warning((key, date, entrances, exits, next_date, next_entrances, next_exits))
            # assert date != next_date
            if next_entrances < entrances or next_exits < exits:
                logging.warning(('reset?',key, date, entrances, exits, next_date, next_entrances, next_exits))
                continue
            daily_key_totals[key].append((date, delta_entrances, delta_exits))

    # finally summarize all stuff to the station level
    station_totals = {}
    for key, data_series in daily_key_totals.items():
        control_area = key.split(',')[1]
        station = stations_lookup[control_area]
        if station not in station_totals:
            station_totals[station] = {}
            
        for date, entrances, exits in data_series:
            if date not in station_totals[station]:
                station_totals[station][date] = [entrances, exits]
            else:
                current_entrances, current_exits = station_totals[station][date]
                station_totals[station][date] = [current_entrances + entrances, current_exits + exits]
    
    # now go through all the dates
    all_dates = []
    for station, date_data in station_totals.items():
        all_dates += date_data.keys()
    all_dates = list(set(all_dates))
    all_dates.sort()
    
    output_file = open(output_filename, 'ab')
    writer = csv.writer(output_file)
    for date in all_dates:
        for station in station_totals:
            entrances, exits = station_totals[station].get(date, [0,0])
            writer.writerow([date, station, str(entrances), str(exits)])
    
    output_file.close()

if __name__ == "__main__":
    tornado.options.define('input_file', type=str, help="input csv file with complete data", default="../data/complete.csv")
    tornado.options.define('output_file', type=str, help="output file with daily data", default="../data/turnstile_daily.csv")
    tornado.options.define('stations_file', type=str, help="Remote-Booth-Stations.csv", default="../data/Remote-Booth-Station.csv")
    tornado.options.parse_command_line()

    input_file = tornado.options.options.input_file
    stations_file = tornado.options.options.stations_file
    assert os.path.exists(input_file)
    assert os.path.exists(stations_file)

    stations = load_stations(stations_file)
    logging.info('stations lookup %s' % stations)
    run(input_file, tornado.options.options.output_file, stations)
