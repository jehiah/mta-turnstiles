from google.appengine.ext import db
from google.appengine.tools import bulkloader
import datetime

class Count(db.Model):
    unit = db.StringProperty()
    control_area = db.StringProperty()
    record_type = db.IntegerProperty()
    record_date = db.DateProperty()
    record_hr = db.IntegerProperty()
    entries_count = db.IntegerProperty()
    entries_diff = db.IntegerProperty(default=0)
    exits_count = db.IntegerProperty()
    exits_diff = db.IntegerProperty(default=0)

class CountLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Count',
                                   [('unit', lambda x: x.decode('utf-8')),
                                    ('control_area', lambda x: x.decode('utf-8')),
                                    ('record_date',
                                     lambda x: datetime.datetime.strptime(x, '%Y/%m/%d').date()),
                                    ('record_hr', int),
                                    ('entries_count', int),
                                    ('entries_diff', int),
                                    ('exits_count', int),
                                    ('exits_diff', int)
                                   ])


class StationCount(db.Model):
   station = db.StringProperty()
   record_date = db.DateProperty()
   entrances = db.IntegerProperty()
   exits = db.IntegerProperty()

class StationCountLoader(bulkloader.Loader):
   def __init__(self):
       bulkloader.Loader.__init__(self, 'StationCount',
                                  [('record_date',
                                    lambda x: datetime.datetime.strptime(x, '%m-%d-%y').date()),
                                   ('station', lambda x: x.decode('utf-8')),
                                   ('entrances', int),
                                   ('exits', int),
                                  ])


class Unit(db.Model):
    station = db.StringProperty()
    unit = db.StringProperty()
    control_area = db.StringProperty()

class UnitLoader(bulkloader.Loader):
    def __init__(self):
        bulkloader.Loader.__init__(self, 'Unit',
                                   [('unit', lambda x: x.decode('utf-8')),
                                    ('control_area', lambda x: x.decode('utf-8')),
                                    ('station', lambda x: x.decode('utf-8')),
                                    ])

loaders = [CountLoader, UnitLoader, StationCountLoader]
