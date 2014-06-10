#!/usr/bin/env python3

import cherrypy
import config
import sys

modules = {}

def call_method(module, method, **kwarg):
    if module in modules:
        try:
            if method in dir(modules[module]):
                return getattr(modules[module], method)(**kwarg)
            else:
                return 'No method \'%s\' in module \'%s\'' % ( method, module )
        except Exception as e:
            return 'Error: ' + str(e)
    else:
        return 'No module named \'%s\'' % (module)

def load_modules():
    for mod_name in config.module_list:
        mod = __import__('modules.' + mod_name + '.' + mod_name, fromlist=[mod_name])
        modules[mod_name] = getattr(mod, mod_name)()


class Alice(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, module, method, **kwarg):
        return call_method(module, method, **kwarg)

if __name__ == '__main__':
    load_modules()

    cherrypy.engine.signal_handler.handlers["SIGINT"] = sys.exit
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.quickstart(Alice(), '/', conf)
