# !/usr/bin/env python3

import threading
import time
import urllib.request
import json

from ... import modulebase

weather_check_interval = 60 # check every minute
city = 'Kanata,ON'
cur_weather_url = ('http://api.openweathermap.org/data/2.5/weather?q=%s&units=metric') % (city)
forecast_url    = ('http://api.openweathermap.org/data/2.5/forecast?q=%s&units=metric') % (city)

class weather(modulebase.ModuleBase):
    data = None
    encode = lambda x : json.dumps(x).encode('utf-8')

    def __init__(self) :
        weather.data = WeatherData()

    def deinit(self) :
        pass

    def GET_temperature(self):
        data = {
            'temp' : weather.data.cur_temp()
        }
        return weather.encode(data)

    def GET_current(self) :
        wd = weather.data
        data = {
            'city' : city,
            'temp' : wd.cur_temp(),
            'weather' : wd.cur_weather(),
            'humidity' : wd.cur_humidity(),
            'clouds' : wd.cur_clouds()
        }
        return weather.encode(data)

    def GET_forecast(self) :
        data = weather.data.forecast()
        return weather.encode(data)

    def POST_test(self) :
        return "Good!"


class WeatherData :
    def __init__(self) :
        self.__cur_temp = -1
        self.__humidity = -1
        self.__clouds = -1
        self.__cur_weather = {}
        self.__forecast = []

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

    def cur_clouds(self) :
        with self.__lock :
            return self.__clouds

    def forecast(self) :
        with self.__lock :
            return self.__forecast

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

    def __set_cur_clouds(self, clouds) :
        with self.__lock :
            self.__clouds = clouds

    def __set_forecast(self, forecast) :
        with self.__lock :
            self.__forecast = forecast


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

            clouds = json_obj.get('clouds', {}).get('all', -1)
            self.__set_cur_clouds(clouds)

            # get forecast
            response = urllib.request.urlopen( urllib.request.Request(url=forecast_url) )
            json_obj = json.loads(response.read().decode('utf-8'))

            # extract data
            data_list = json_obj.get('list', [])
            fc_data = []

            for list_item in data_list[:8] :
                fc_item = {}
                fc_item['timestamp'] = list_item.get('dt', 0)

                fc_main = list_item.get('main', {})
                fc_item['temp'] = fc_main.get('temp', -1)
                fc_item['humidity'] = fc_main.get('humidity', -1)

                fc_weather = list_item.get('weather', [])
                fc_item['weather'] = {
                    'id' : fc_weather[0].get('id', 0),
                    'descr' : fc_weather[0].get('main', '')
                } if len(fc_weather) > 0 else { 'id' : 0, 'descr': '' }

                fc_data.append(fc_item)

            self.__set_forecast(fc_data)

            time.sleep(weather_check_interval)

