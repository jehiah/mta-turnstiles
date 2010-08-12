import os
import tornado.web
import tornado.wsgi
import wsgiref.handlers

# application imports
import app.index

class Application(tornado.wsgi.WSGIApplication):
    def __init__(self):
        app_settings = { 
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "debug" : True
        }
        handlers = [
            (r"^/$", app.index.IndexHandler),
            (r"^/station/([^\/]*?)/?$", app.index.StationHandler),
        ]
        tornado.wsgi.WSGIApplication.__init__(self, handlers, **app_settings)
        
if __name__ == "__main__":
    application = Application()
    wsgiref.handlers.CGIHandler().run(application)