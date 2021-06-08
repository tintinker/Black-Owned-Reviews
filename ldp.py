from util import flatten_gmaps_response
from gmaps import get_info
import json
from os import path
import pandas as pd
import logging

log = logging.getLogger(__name__)

def plus_replace(mystr):
    """Convert strings to URL friendly format

    Args:
        mystr (str): ex. "burger king"

    Returns:
        str]: ex. "burger+king"
    """
    return mystr.replace(" ", "+")

class LDP:
    """
    License Directory Processer
    Wrapper Class for processing a city's license directory
    """

    def __init__(self, filename, addr_func, name_func, filter_func = None, cache_filename=None, output_filename=None, debug=False, use_cache=True):
        """Create new LDP

        Args:
            filename (str): location of .csv license directory file for the city
            addr_func (function): function describing how to combine columns into an address for a given row
            name_func (function): function indicating which column has the commonly known (google  maps) name of a business
            filter_func (function, optional): function describing how to filter rows using pandas.loc style. Defaults to None.
            cache_filename (string, optional): If specified, overrride default to use and store cache in a specific file. Defaults to None.
            output_filename (string, optional): If specified, override default output filename. Defaults to None.
            debug (bool, optional): If False, run headless. Defaults to False.
            use_cache (bool, optional): [description]. Defaults to True.
        """
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
        except: #if file doesn't exist or is ilformated, use empty
            self.cache = {}

    def get_gmaps_info(self, row):
        """Generate url, and extract labels using cache or scraper
        """
        addr = self.extract_addr(row)
        name = self.extract_name(row)
        
        try:
            url = f'https://www.google.com/maps/search/{plus_replace(name)}+near+{plus_replace(addr)}'
        except: #if problem with address or name, skip
            return pd.Series({'success': False, 'error_type': "missing_name_or_addr", 'lgbtq': None, 'veteran': None, 'women': None, 'black': None})
        
        log.debug(f"{name} | {addr} | {url}")

        if url in self.cache and self.use_cache:
            log.debug(f"Using Cache for {name}")
            gmaps_info = self.cache[url]
        else:
            gmaps_info = get_info(url, debug=self.debug)
            self.cache[url] = gmaps_info
        
        if self.use_cache:
            log.debug(f"Saving Cache to {self.cache_filename}")
            with open(self.cache_filename, 'w+') as f:
                json.dump(self.cache, f)

        return pd.Series(flatten_gmaps_response(gmaps_info))

    def process(self):
        """Run the script on the entire city directory file
        """
        df = pd.read_csv(self.input_filename) 
        if self.filter:
            df = df[self.filter(df)]  

        df = df.merge(df.apply(lambda row: self.get_gmaps_info(row), axis=1), left_index=True, right_index=True)
        df.to_csv(self.output_filename)
        return df


