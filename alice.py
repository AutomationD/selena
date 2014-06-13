#!/usr/bin/env python3

import cherrypy
import config
import sys
import json
import modules.registry as registry

modules = {}

def load_modules():
    for mod_name in config.module_list:
        mod = __import__('modules.' + mod_name + '.' + mod_name, fromlist=[mod_name])

        # create a module instance
        try :
            modules[mod_name] = getattr(mod, mod_name)()

        except AttributeError as e :
            print ('Error while loading module \'' + mod_name + '\': ' + str(e))


class Alice(object):
    exposed = True

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
        cherrypy.response.headers['Access-Control-Allow-Origin'] = cherrypy.request.headers['ORIGIN']
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
    load_modules()
    alice = Alice()
    for mod_name in config.module_list :
        setattr(alice, mod_name, modules[mod_name])

    cherrypy.engine.signal_handler.handlers["SIGINT"] = alice.shutdown
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
        }
    }
    print('===== Starting Alice at \'' + config.host + ':' + str(config.port) + '\' =====')
    cherrypy.quickstart(alice, '/', conf)
