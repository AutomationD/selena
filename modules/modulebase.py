# !/usr/bin/env python3

class ModuleBase(object) :
    exposed = True

    def GET(self, method='', **kwarg) :
        try :
            return getattr(self, method)()
        except AttributeError as e :
            return str(e)
