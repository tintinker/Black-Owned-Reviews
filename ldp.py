from labels import check_labels
import json
from os import path
from sys import argv, exit
from random import random
import pandas as pd
import logging

log = logging.getLogger(__name__)

CACHE_SAVE_FREQ = 1/5

def plus_replace(mystr):
    return mystr.replace(" ", "+")

class LDP: #License Directory Processer
    def __init__(self, filename, addr_func, name_func, filter_func = None, cache_filename=None, output_filename=None, debug=False, use_cache=True):
        self.input_filename = filename
        self.cache_filename = cache_filename
        self.output_filename = output_filename
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
        addr = self.extract_addr(row)
        name = self.extract_name(row)
        
        try:
            url = f'https://www.google.com/maps/search/{plus_replace(name)}+near+{plus_replace(addr)}'
        except:
            return pd.Series({'success': False, 'error_type': "missing_name_or_addr", 'lgbtq': None, 'veteran': None, 'women': None, 'black': None})
        
        log.debug(f"{name} | {addr} | {url}")

        if url in self.cache and self.use_cache:
            log.debug("Using Cache")
            labels = self.cache[url]
        else:
            labels = check_labels(url, debug=self.debug)
            self.cache[url] = labels
        
        if self.use_cache and random() < CACHE_SAVE_FREQ:
            log.debug("Saving Cache")
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


