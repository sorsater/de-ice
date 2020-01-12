#!/usr/bin/env python
# coding: utf-8

import urllib.request
import xml.etree.ElementTree as ET
import xmltodict
import os
import json
import time
import datetime

class Forecaster():
    def __init__(self, location_url):
        self.url = location_url + "/forecast_hour_by_hour.xml"
        self.data = ''
        self.forecasts = {}
        
        self.location = ''
        self.forecast_file_name = 'forecasts.json'
        
        self.parse_page()
        self.read_location()
        self.read_current_forecast()
        self.merge_with_previous_forecast()
        self.save_forecast()
        
    def parse_page(self):
        print('Parse page')
        try:
            xml_content = urllib.request.urlopen(self.url).read()
            self.data = xmltodict.parse(xml_content)
        except:
            print('ERROR: Parsing failed')
            
    def read_location(self):
        print('Read location')
        self.location = self.data['weatherdata']['location']['name']
    
    def read_current_forecast(self):
        print('Read current forecasts')
        forecast = self.data['weatherdata']['forecast']['tabular']['time']

        for entry in forecast:
            # Read out relevant content from the entry dict
            start = entry['@from']
            end = entry['@to']
            temp = entry['temperature']['@value']
    
            dict_entry = {
                'from': start,
                'to': end,
                'temp': temp,        
            }
    
            self.forecasts[start] = dict_entry
        
    def merge_with_previous_forecast(self):
        print('Merge with previous forecasts')
        if os.path.exists(self.forecast_file_name):
            previous_forecasts = json.load(open(self.forecast_file_name))
    
            for timestamp, content in previous_forecasts.items():
                # Newer data is better data
                if timestamp in self.forecasts:
                    continue
                self.forecasts[timestamp] = content
    
    def save_forecast(self):
        print('Save forecas')
        # Save forecasts to file
        json.dump(self.forecasts, open(self.forecast_file_name, 'w'), indent=True, sort_keys=True)


def __main__():
    print('Running forecast')
    forecast = Forecaster('https://www.yr.no/place/Sweden/J%C3%B6nk%C3%B6ping/Eksj%C3%B6')
