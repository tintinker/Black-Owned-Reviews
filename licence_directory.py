from labels import check_labels
import pandas as pd
from os import path
from sys import argv, exit
import json
from random import random

CACHE_SAVE_FREQ = 1/5

def plus_replace(str):
    return str.replace(" ", "+")

class LDP: #License Directory Processer
    def __init__(self, filename, addr_func, name_func, latlng_func = None, filter_func = None, cache_filename=None, output_filename=None, debug=False, use_cache=True):
        self.input_filename = filename
        self.cache_filename = cache_filename
        self.output_filename = output_filename
        self.extract_latlng = latlng_func
        self.filter = filter_func
        self.extract_addr = addr_func
        self.extract_name = name_func
        self.debug = debug
        self.use_cache = use_cache
        
        if not self.cache_filename:
            self.cache_filename = path.splitext(self.input_filename)[0] + "cache.json"
        if not self.output_filename:
            self.output_filename = path.splitext(self.input_filename)[0] + "output.csv"
        
        try:
            with open(self.cache_filename) as f:
                self.cache = json.load(f)
        except:
            self.cache = {}

    def get_labels(self, row):
        lat, lng =  None, None
        if self.extract_latlng:
            lat, lng = self.extract_latlng(row)
        addr = self.extract_addr(row)
        name = self.extract_name(row)
        
        url = f'https://www.google.com/maps/search/{plus_replace(name)}+near+{plus_replace(addr)}'
        if lat and lng:
            url += '/@{lat},{lng}'
        
        print(name, addr, url)

        if url in self.cache and self.use_cache:
            print("Using Cache")
            labels = self.cache[url]
        else:
            labels = check_labels(url, debug=self.debug)
            self.cache[url] = labels
        
        if self.use_cache and random() < CACHE_SAVE_FREQ:
            print("Saving Cache")
            with open(self.cache_filename, 'w+') as f:
                json.dump(self.cache, f)

        return pd.Series({'success': labels['success'], 'error_type': labels['error_type'], 'lgbtq': labels['lgbtq'], 'veteran': labels['veteran'], 'women': labels['women'], 'black': labels['black']})

    def process(self, output_filename=None):
        df = pd.read_csv(self.input_filename) 
        if self.filter:
            df = df[self.filter(df)]  

        df = df.merge(df.apply(lambda row: self.get_labels(row), axis=1), left_index=True, right_index=True)
        df.to_csv(self.output_filename)
        return df

    '''
    -------------------------------Seattle Example Methods----------------------------------
    '''
    
    @staticmethod
    def Seattle_Addr(row):
        return row["Street Address"] + ", " + row["City"] + " " + row["State"] + " " + row["Zip"]
    
    @staticmethod
    def Seattle_Name(row):
        return row["Trade Name"]
    
    @staticmethod
    def Seattle_Filter(df):
        return  (df["NAICS Description"] == "Full-Service Restaurants") | (df["NAICS Description"] == "Limited-Service Restaurants")
    
    '''
    -------------------------------Chicago Example Methods----------------------------------
    '''

    @staticmethod
    def Chicago_Addr(row):
        return row["ADDRESS"] + ", " + row["CITY"] + " " + row["STATE"] + " " + row["ZIP CODE"]
    
    @staticmethod
    def Chicago_Name(row):
        return row["DOING BUSINESS AS NAME"]

    @staticmethod
    def Chicago_LatLng(row):
        return row['LATITUDE'] + "," + row['LONGITUDE']

    @staticmethod
    def Chicago_Filter(df):
        return  df["LICENSE DESCRIPTION"] == "Retail Food Establishment"
    
    '''
    -------------------------------Add More Here----------------------------------
    '''


if __name__ == '__main__':
    if len(argv) <= 1:
        print("Usage: start.py [city_license_directory.csv] ([output_file_name.csv])")
        exit(1)

    if len(argv) <= 2:
        l = LDP(argv[1], LDP.Seattle_Addr, LDP.Seattle_Name, filter_func=LDP.Seattle_Filter)
    else:
        l = LDP(argv[1], LDP.Seattle_Addr, LDP.Seattle_Name, filter_func=LDP.Seattle_Filter, output_filename=argv[2])
    
    l.process()