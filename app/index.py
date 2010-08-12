import tornado.web

import lib.stations

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        stations = lib.stations.all_stations()
        self.render('index.html', stations=stations)
