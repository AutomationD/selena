# !/usr/bin/env python3

class ModuleBase(object) :
    exposed = True

    def GET(self, method='', **kwarg) :
        try :
            return getattr(self, 'GET_' + method)()
        except AttributeError as e :
            return str(e)

    def POST(self, method='', **kwarg) :
        try :
            return getattr(self, 'POST_' + method)()
        except AttributeError as e :
            return str(e)
