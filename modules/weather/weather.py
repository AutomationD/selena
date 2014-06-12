# !/usr/bin/env python3

from .. import registry

class weather:
    def init(self) :
        pass

    @registry.GET('weather')
    def temperature():
        return "Temp: 20 C"

    @registry.POST('weather')
    def test() :
        return "Good!"
