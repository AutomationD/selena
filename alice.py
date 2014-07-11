#!/usr/bin/env python3

import cherrypy
import config
import sys
import json
import os

class Alice(object):
    exposed = True

    def __init__(self) :
        self.modules = {}

        # load modules
        for mod_name in config.module_list:
            mod = __import__('modules.' + mod_name + '.' + mod_name, fromlist=[mod_name])

            # create a module instance
            try :
                mod_obj = getattr(mod, mod_name)()
                self.modules[mod_name] = mod_obj
                setattr(self, mod_name, mod_obj)

            except AttributeError as e :
                print ('Error while loading module \'' + mod_name + '\': ' + str(e))

    def GET(self, module, **kwarg) :
        if module == 'modules' :
            return json.dumps(config.module_list).encode('utf-8')
        else :
            cherrypy.response.status = 404
            return 'No module named \'' + module + '\''

    def POST(self, module, method, **kwarg):
        return ''

    def OPTIONS(self):
        cherrypy.response.headers['Access-Control-Allow-Credentials'] = True
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = cherrypy.request.headers['ACCESS-CONTROL-REQUEST-HEADERS']        


    def shutdown(self) :
        print('===== Exiting =====')
        for mod_name in modules :
            try :
                deinit_func = getattr(modules[mod_name], 'deinit')
                deinit_func()
            except AttributeError as e :
                print ('Error while deinitializing module \'' + mod_name + '\': ' + str(e))

        sys.exit()

if __name__ == '__main__':
    alice = Alice()

    cherrypy.engine.signal_handler.handlers["SIGINT"] = alice.shutdown
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
    conf = {
        'global' : {
            'server.socket_host': config.host,
            'server.socket_port': config.port
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : os.path.join(BASEDIR,'frontend'),
            'tools.staticdir.index' : 'weather.html'
        }
    }
    print('===== Starting Alice at \'' + config.host + ':' + str(config.port) + '\' =====')
    cherrypy.quickstart(alice, '/', conf)
