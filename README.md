# Black-Owned-Reviews

This should be working now!!  

## Setting up dev environment
Note: `$` indicates a shell command. This assumes you're using a mac with virtualenv already installed  

1. Clone this repository to a location of your choice  
2. Initialize a virtual environment (we will call it `env`)  
`$ virtualenv env`  
3. Activate the virtual environment  
`$ source env/bin/activate`  
4. Install the requirements  
`(env) $ pip3 install -r requirements.txt`  
5. Add the secrets file  
`(env) $ touch secrets.py`
6. Add your api keys to the secrets file  
----
secrets.py  
PLACES\_API\_KEY = 'Abcdef1234g' (for the place search api)   
VIZ\_API\_KEY = 'Xyzcdef789g' (for the maps javascript api)   

----

You should be good to go!

## Visualize the geographic area for your target cities
*Important: make sure the virtual environment is activated (you should see (env) in the terminal)*  
If not: `$ source env/bin/activate`  
To see the covered geographic area for a city, run `viz.py` with the city name, and a webpage should pop up in your default browser with the area highlighted  
ex.  
`(env) $ python3 viz.py "St. Louis"`   
Generates:  
Example: ![Alt](/viz_example.png "Geo Example")

## Run the scraper
*Important: make sure the virtual environment is activated (you should see (env) in the terminal)*  
If not: `$ source env/bin/activate`  
1. Add a list of cities to a text file  
`(env) $ touch citylist.txt`   
----
citylist.txt  

San Antonio  
Chicago  
Atlanta  
Salt Lake City  

----
2. Run `start.py`  
Ex. `(env) $ python3 start.py --cache-file "data/citydata.json" citylist.txt`  
Ex. `(env) $ python3 start.py --no-cache-places citylist.txt`  
Full options:  
----
usage: start.py [-h] [--no-cache-places] [--cache-cities]
                [--cache-file CACHE_FILE] [--headless]
                [--max-places MAX_PLACES] [--log-level {INFO,DEBUG}]
                [--output-name OUTPUT_NAME]
                citylist

Google Maps Labels Data Collection  

positional arguments:  
  citylist              File containing list of cities (one per line) to
                        process

optional arguments:  
  -h, --help            show this help message and exit  
  --no-cache-places     If false (default), it will not update the data for a
                        given restaurant if it is already present in the cache  
  --cache-cities        If true, it will not update the list of restaurants in
                        a city if it is already present in the cache  
  --cache-file CACHE_FILE
                        Required if cache cities or cache places is true  
  --headless            Run selenium headless or not  
  --max-places MAX_PLACES
                        Maximum number of restaurants to process per city  
  --log-level {INFO,DEBUG}
                        Run debug for more detailed information  
  --output-name OUTPUT_NAME
                        Basename of output files (csv and json extensions
                        added)  

----
3. Output available in csv and json in root directory