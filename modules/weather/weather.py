# !/usr/bin/env python3

from .. import registry
from .. import modulebase

class weather(modulebase.ModuleBase):
    exposed = True

    def init(self) :
        pass

    def GET_temperature(self):
        return "Temp: 20 C"

    def GET_test(self) :
        return "Good!"
