# !/usr/bin/env python3

from .. import registry
from .. import modulebase

class weather(modulebase.ModuleBase):
    exposed = True

    def init(self) :
        pass

    #@registry.GET('weather')
    def temperature(self):
        return "Temp: 20 C"

    @registry.POST('weather')
    def test() :
        return "Good!"

    '''def GET(self, method='', **kwarg) :
        try :
            return getattr(self, method)()
        except AttributeError as e :
            return str(e)
    '''
