# !/usr/bin/env python3

import threading
import time
import urllib.request
import json

from ... import modulebase

currency_check_interval = 5 * 60 # check every 5 minutes
currency_list = [
    { 'from' : 'USD', 'to' : 'RUB' },
    { 'from' : 'CAD', 'to' : 'RUB' }
]

cur_rate_url = ('http://rate-exchange.appspot.com/currency')

class currency(modulebase.ModuleBase):
    data = None
    encode = lambda x : json.dumps(x).encode('utf-8')

    def __init__(self) :
        currency.data = CurrencyData()

    def deinit(self) :
        pass

    def GET_rates(self):
        data = currency.data.get_rates()
        return currency.encode(data)


class CurrencyData :
    def __init__(self) :
        self.__rates = []

        self.__lock = threading.Lock()
        self.__start_checker()


    '''
    Public getters
    '''

    def get_rates(self) :
        with self.__lock :
            return self.__rates


    '''
    Private setters
    '''

    def __set_rates(self, rates) :
        with self.__lock :
            self.__rates = rates


    '''
    Threading
    '''

    def __start_checker(self) :
        print('Starting currency checker...')
        self.__checker = threading.Thread(target=self.__check_rates)
        self.__checker.daemon = True
        self.__checker.start()

    def __check_rates(self) :
        while True :
            print('Checking weather...')

            currency_rates = []
            for pair in currency_list :
                url = "%s?from=%s&to=%s" % ( cur_rate_url, pair['from'], pair['to'] )
                response = urllib.request.urlopen( urllib.request.Request(url=url) )
                json_obj = json.loads(response.read().decode('utf-8'))
                print (str(json_obj))

                currency_rates.append(json_obj)

            self.__set_rates(currency_rates)

            time.sleep(currency_check_interval)

