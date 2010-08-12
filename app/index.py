import tornado.web
import logging
import urllib

import lib.stations

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        stations = lib.stations.all_stations()
        self.render('index.html', stations=stations)

class StationHandler(tornado.web.RequestHandler):
    def get(self, station):
        station = urllib.unquote_plus(station).replace('+', ' ')
        logging.info('station is %r' % station)
        station_record = lib.stations.get(station)
        if not station_record:
            raise tornado.web.HTTPError(404)
        
        data = lib.stations.get_station_data(station)
        self.render('station.html', station=station, data=data)
        