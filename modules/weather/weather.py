# !/usr/bin/env python3

import threading
import time
import urllib.request
import json

from .. import registry

weather_check_interval = 60 # check every minute
city = 'Kanata,ON'
cur_weather_url = ('http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric') % (city)


class weather:
    data = None
    encode = lambda x : json.dumps(x).encode('utf-8')

    def init(self) :
        weather.data = WeatherData()
        pass

    def deinit(self) :
        pass

    @registry.GET('weather')
    def temperature():
        data = {
            'temp' : weather.data.cur_temp()
        }
        return weather.encode(data)

    @registry.GET('weather')
    def current() :
        wd = weather.data
        data = {
            'temp' : wd.cur_temp(),
            'weather' : wd.cur_weather(),
            'humidity' : wd.cur_humidity()
        }
        return weather.encode(data)

    @registry.POST('weather')
    def test() :
        return "Good!"


class WeatherData :
    def __init__(self) :
        self.__cur_temp = -1
        self.__humidity = -1
        self.__cur_weather = {}

        self.__lock = threading.Lock()
        self.__start_checker()


    '''
    Public getters
    '''

    def cur_temp(self) :
        with self.__lock :
            return self.__cur_temp

    def cur_weather(self) :
        with self.__lock :
            return self.__cur_weather

    def cur_humidity(self) :
        with self.__lock :
            return self.__humidity


    '''
    Private setters
    '''

    def __set_cur_temp(self, temp) :
        with self.__lock :
            self.__cur_temp = temp

    def __set_cur_weather(self, weather_id, weather_descr) :
        with self.__lock :
            self.__cur_weather['id'] = weather_id
            self.__cur_weather['descr'] = weather_descr

    def __set_cur_humidity(self, hum) :
        with self.__lock :
            self.__humidity = hum


    '''
    Threading
    '''

    def __start_checker(self) :
        print('Starting weather checker...')
        self.__checker = threading.Thread(target=self.__check_weather)
        self.__checker.daemon = True
        self.__checker.start()

    def __check_weather(self) :
        while True :
            print('Checking weather...')
            response = urllib.request.urlopen( urllib.request.Request(url=cur_weather_url) )
            json_obj = json.loads(response.read().decode('utf-8'))
            print (str(json_obj))

            main = json_obj.get('main', {})
            temp = main.get('temp', -1)
            hum = main.get('humidity', -1)
            self.__set_cur_temp(temp)
            self.__set_cur_humidity(hum)

            weather = json_obj.get('weather', [])
            if len(weather) > 0 :
                wthr_id = weather[0].get('id', 0)
                wthr_descr = weather[0].get('main', '')
                self.__set_cur_weather(wthr_id, wthr_descr)

            time.sleep(weather_check_interval)

