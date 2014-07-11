# !/usr/bin/env python3

import cherrypy

class ModuleBase(object) :
    exposed = True

    def GET(self, method='', **kwarg) :
        try :
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
            return getattr(self, 'GET_' + method)()
        except AttributeError as e :
            cherrypy.response.status = 501
            return 'Error: method \'' + method + '\' not found or not allowed for GET requests'

    def POST(self, method='', **kwarg) :
        try :
            cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
            return getattr(self, 'POST_' + method)()
        except AttributeError as e :
            cherrypy.response.status = 501
            return 'Error: method \'' + method + '\' not found or not allowed for POST requests'
