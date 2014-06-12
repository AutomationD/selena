#!/usr/bin/env python3

import cherrypy
import config
import sys
import modules.registry as registry

modules = {}

def call_method(module, method, rest_method, **kwarg):
    if module in modules:
        try:
            if method in dir(modules[module]):
                method_full_name = module + '.' + method
                func = registry.get_method(rest_method, method_full_name)

                if func :
                    return func(**kwarg)
                else :
                    cherrypy.response.status = 405
                    return 'Method \'%s\' in module \'%s\' doesn\'t support %s requests' % ( method, module, rest_method )
            else:
                cherrypy.response.status = 501
                return 'No method \'%s\' in module \'%s\'' % ( method, module )
        except Exception as e:
            cherrypy.response.status = 500
            return 'Error: ' + str(e)
    else:
        cherrypy.response.status = 404
        return 'No module named \'%s\'' % (module)

def load_modules():
    for mod_name in config.module_list:
        mod = __import__('modules.' + mod_name + '.' + mod_name, fromlist=[mod_name])

        # create a module instance
        try :
            modules[mod_name] = getattr(mod, mod_name)()

            # initialize the module
            try :
                init_func = getattr(modules[mod_name], 'init')
                init_func()
            except AttributeError as e :
                print ('Error while initializing module \'' + mod_name + '\': ' + str(e))

        except AttributeError as e :
            print ('Error while loading module \'' + mod_name + '\': ' + str(e))


class Alice(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, module, method, **kwarg):
        return call_method(module, method, 'GET', **kwarg)

    @cherrypy.tools.accept(media='text/plain')
    def POST(self, module, method, **kwarg):
        return call_method(module, method, 'POST', **kwarg)

    def OPTIONS(self):
        cherrypy.response.headers['Access-Control-Allow-Credentials'] = True
        cherrypy.response.headers['Access-Control-Allow-Origin'] = cherrypy.request.headers['ORIGIN']
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = cherrypy.request.headers['ACCESS-CONTROL-REQUEST-HEADERS']

if __name__ == '__main__':
    load_modules()

    cherrypy.engine.signal_handler.handlers["SIGINT"] = sys.exit
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
    cherrypy.quickstart(Alice(), '/', conf)
