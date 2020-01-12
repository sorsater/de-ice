#!/usr/bin/env python
# coding: utf-8

import json
import datetime
import http
from urllib.parse import urlencode
import time


class Pusher():
    def __init__(self, num_hours=8):
        self.num_hours = num_hours
        self.today = str(datetime.date.today())
        self.forecast_file_name = 'forecasts.json'
        self.credentials_file = 'credentials.json'
        
        self.API_TOKEN = None
        self.USER_TOKEN = None
        
        self.forecasts_today = []
        self.temps_today = []
        
        self.coldest = None
        self.msg = ''
        
        self.read_todays_forecasts()
        self.read_temperatures()
        self.get_coldest_temp()
        self.create_msg()
        
        self.read_credentials()
        self.push()
        
    def read_credentials(self):
        credentials = json.load(open(self.credentials_file))
        self.API_TOKEN = credentials['API_TOKEN']
        self.USER_TOKEN = credentials['USER_TOKEN']
        
    def read_todays_forecasts(self):
        forecasts = json.load(open(self.forecast_file_name))
        for timestamp, content in forecasts.items():
            timestamp_date = timestamp.split('T')[0]
            if today == timestamp_date:
                self.forecasts_today.append(content)

    def read_temperatures(self):
        for forecast in self.forecasts_today:
            start_time = forecast['from'].split('T')[1]
            temp = int(forecast['temp'])
            self.temps_today.append([start_time, temp])
            
    def get_coldest_temp(self):
        self.temps_today.sort(reverse=True)

        recent_hours = self.temps_today[:self.num_hours]
        temps = [temp for timestamp, temp in recent_hours]

        self.coldest = min(temps)
        
    def create_msg(self):
        
        if coldest < 0:
            self.msg = r'You need to de-ice your car &#x1F643'
        else:
            self.msg = r'No need to worry, drive safely &#x263A'
            
        #self.msg = r'You need to de-ice your car &#x2705 &#x1F604 &#x263A &#x1F643'
            
        
    def push(self):
        print('Trying to push!')
        try:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                urlencode({
                    "token": self.API_TOKEN,
                    "user": self.USER_TOKEN,
                    "message":  self.msg,
                    "html": 1,
                }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()
        except Exception as e:
            print('Failed!', e)
        else:
            print('Success!')


def __main__():
    pusher = Pusher()