#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
API Provider for VIPBOMBER-V2
"""

import json
import random
import time
import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings
disable_warnings(InsecureRequestWarning)

class APIProvider:
    api_providers = []
    api_version = "3.0.0"
    
    def __init__(self, cc, target, mode, delay=1):
        self.cc = cc
        self.target = target
        self.mode = mode
        self.delay = delay
        self.load_apis()
    
    def load_apis(self):
        """Load APIs from JSON file"""
        try:
            with open('apidata.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                if self.mode in data:
                    # Get country-specific and multi APIs
                    country_apis = data[self.mode].get(self.cc, [])
                    multi_apis = data[self.mode].get('multi', [])
                    providers = country_apis + multi_apis
                    # Set both instance and class-level providers so callers
                    # referencing APIProvider.api_providers (class attr) see them.
                    self.api_providers = providers
                    APIProvider.api_providers = providers
        except Exception as e:
            print(f"Error loading APIs: {e}")
            self.api_providers = []
            APIProvider.api_providers = []
    
    def hit(self):
        """Execute API call"""
        if not self.api_providers:
            return False
        
        # Select random API
        api = random.choice(self.api_providers)
        
        try:
            # Prepare data
            data = self.prepare_data(api)
            headers = api.get('headers', {})
            cookies = api.get('cookies', {})
            
            # Make request
            if api['method'].upper() == 'GET':
                response = requests.get(
                    api['url'],
                    params=data if 'params' in api else None,
                    headers=headers,
                    cookies=cookies,
                    verify=False,
                    timeout=30
                )
            elif api['method'].upper() == 'POST':
                if api.get('json'):
                    response = requests.post(
                        api['url'],
                        json=data,
                        headers=headers,
                        cookies=cookies,
                        verify=False,
                        timeout=30
                    )
                else:
                    response = requests.post(
                        api['url'],
                        data=data,
                        headers=headers,
                        cookies=cookies,
                        verify=False,
                        timeout=30
                    )
            else:
                return False
            
            # Check if successful
            if self.check_success(response, api.get('identifier')):
                return True
            else:
                return False
                
        except Exception as e:
            return False
        finally:
            time.sleep(self.delay)
    
    def prepare_data(self, api):
        """Prepare data with target information"""
        data = {}
        
        if 'data' in api:
            for key, value in api['data'].items():
                if isinstance(value, str):
                    data[key] = value.format(cc=self.cc, target=self.target)
                else:
                    data[key] = value
        elif 'json' in api:
            for key, value in api['json'].items():
                if isinstance(value, str):
                    data[key] = value.format(cc=self.cc, target=self.target)
                else:
                    data[key] = value
        elif 'params' in api:
            for key, value in api['params'].items():
                if isinstance(value, str):
                    data[key] = value.format(cc=self.cc, target=self.target)
                else:
                    data[key] = value
        
        return data
    
    def check_success(self, response, identifier):
        """Check if API call was successful"""
        if response.status_code == 200:
            if identifier:
                return identifier in response.text
            return True
        return False