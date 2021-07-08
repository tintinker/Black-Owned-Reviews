import psycopg2
from util import check_cache, get_db_connection, get_range, save_cache
from gmaps import get_info
import json
from os import path
import pandas as pd
import logging
from tqdm import tqdm

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
        self.db_connection = get_db_connection()
        self.cursor  = self.db_connection.cursor()

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

    def __del__(self):
        self.cursor.close()
        self.db_connection.close()

    def get_gmaps_info(self, row):
        """Generate url, and extract labels using cache or scraper
        """
        addr = self.extract_addr(row)
        name = self.extract_name(row)
        
        try:
            url = f'https://www.google.com/maps/search/{plus_replace(name)}+near+{plus_replace(addr)}'
            url_id = f'{name} near {addr}'[:50]
        except: #if problem with address or name, skip
            return
        
        log.debug(f"{name} | {addr} | {url}")

        if self.use_cache and check_cache(self.cursor, url_id):
            return
            
        get_info(self.cursor, url, url_id, debug=self.debug)

        if self.use_cache:
            save_cache(self.cursor, url_id)

        self.db_connection.commit()

    def process(self):
        """Run the script on the entire city directory file
        """
        tqdm.pandas()

        df = pd.read_csv(self.input_filename) 
        if self.filter:
            df = df[self.filter(df)]  
        
        range_start, range_end = get_range()
        if (range_start, range_end) != (-1,-1):
            log.debug(f"Using range {range_start} to {range_end}")
            df = df.iloc[range_start:range_end]

        df.progress_apply(self.get_gmaps_info, axis=1)


