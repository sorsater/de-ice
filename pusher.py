#!/usr/bin/env python
# coding: utf-8

import json
import datetime
import http.client
from urllib.parse import urlencode
import time
import os


class Pusher():
    def __init__(self, num_hours=8):
        self.num_hours = num_hours
        self.today = str(datetime.date.today())
        self.forecast_file_name = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'forecasts.json')
        self.credentials_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials.json')
        
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
        print('Reading credentials')
        credentials = json.load(open(self.credentials_file))
        self.API_TOKEN = credentials['API_TOKEN']
        self.USER_TOKEN = credentials['USER_TOKEN']
        
    def read_todays_forecasts(self):
        print('Reading forecast for today')
        forecasts = json.load(open(self.forecast_file_name))
        for timestamp, content in forecasts.items():
            timestamp_date = timestamp.split('T')[0]
            if self.today == timestamp_date:
                self.forecasts_today.append(content)

    def read_temperatures(self):
        print('Read temperatures')
        for forecast in self.forecasts_today:
            start_time = forecast['from'].split('T')[1]
            temp = int(forecast['temp'])
            self.temps_today.append([start_time, temp])
            
    def get_coldest_temp(self):
        print('Get coldest temp')
        self.temps_today.sort(reverse=True)

        recent_hours = self.temps_today[:self.num_hours]
        temps = [temp for timestamp, temp in recent_hours]

        self.coldest = min(temps)
        
    def create_msg(self):
        print('Create message')
        if self.coldest <= 0:
            # Snowman emoji, car emoji, degree sign
            self.msg = r'&#x2603 &#x1F697, {}&#186;'.format(self.coldest)
        else:
            # Blush emoji, car emoji, degree sign
            self.msg = r'&#x263A &#x1F697, {}&#186;'.format(self.coldest)
        
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


if __name__ == "__main__":
    print('Pushing')
    pusher = Pusher()
