#!/usr/bin/env python3

from .. import modulebase

class news (modulebase.ModuleBase) :

    def GET_latest(self) :
        return "London is the capital of Great Britain"
