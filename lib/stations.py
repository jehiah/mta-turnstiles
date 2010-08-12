from google.appengine.api import memcache as mc

import models

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
    