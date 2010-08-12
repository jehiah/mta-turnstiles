from google.appengine.ext import db

# class Count(db.Model):
#     unit = db.StringProperty()
#     control_area = db.StringProperty()
#     record_type = db.IntegerProperty()
#     record_date = db.DateProperty()
#     record_hr = db.IntegerProperty()
#     entries_count = db.IntegerProperty()
#     entries_diff = db.IntegerProperty(default=0)
#     exits_count = db.IntegerProperty()
#     exits_diff = db.IntegerProperty(default=0)

class StationCount(db.Model):
   station = db.StringProperty()
   record_date = db.DateProperty()
   entrances = db.IntegerProperty()
   exits = db.IntegerProperty()

class Unit(db.Model):
    station = db.StringProperty()
    unit = db.StringProperty()
    control_area = db.StringProperty()

