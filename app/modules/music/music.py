#!/usr/bin/env python3

from ... import modulebase

class music (modulebase.ModuleBase) :

    def GET_now_playing(self) :
        return "Metallica - Master of Puppets"
