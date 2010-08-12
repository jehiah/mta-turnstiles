from google.appengine.api import memcache as mc

import models
import logging

def all_stations():
    mc_key = 'stations.all'
    v = mc.get(mc_key)
    if v is not None:
        return v
    o = []
    for x in models.Unit.all().order('station').fetch(1000):
        o.append(x.station)
    o = list(set(o))
    o.sort()
    mc.set(mc_key, o)
    return o
    
def get(station):
    rec = models.Unit.all().filter('station', station).fetch(1)
    return rec
    
def get_station_data(station):
    o = []
    for x in models.StationCount.all().filter('station', station).order('-record_date').fetch(1000):
        o.append(x)
    return o
    