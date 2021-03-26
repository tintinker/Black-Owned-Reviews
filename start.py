from place_search import run_city
import logging
import argparse
import json
import pandas as pd

log = logging.getLogger(__name__)
parser = argparse.ArgumentParser(description='Google Maps Labels Data Collection')

parser.add_argument('--no-cache-places', dest='cache_places', default=True, action='store_false', help="If false (default), it will not update the data for a given restaurant if it is already present in the cache")
parser.add_argument('--cache-cities', dest='cache_cities', default=False, action='store_true', help="If true, it will not update the list of restaurants in a city if it is already present in the cache")
parser.add_argument('--cache-file', dest='cache_file', default="", help="Required if cache cities or cache places is true")
parser.add_argument('--headless', dest='headless', default=False, action='store_true', help="Run selenium headless or not")
parser.add_argument('--max-places', dest='max_places', default=0, type=int, help="Maximum number of restaurants to process per city")
parser.add_argument('--log-level', dest='log_level', default="INFO", choices=["INFO","DEBUG"], help="Run debug for more detailed information")
parser.add_argument('--output-name', dest='output_name', default="output", help="Basename of output files (csv and json extensions added)")
parser.add_argument('citylist', help="File containing list of cities (one per line) to proces")
args = parser.parse_args()

if args.cache_places or args.cache_cities:
    if not args.cache_file:
        print("Error! Cache places/cities  is true but no cache file is specified (usually data/citydata.json)")
        exit(1)

logging.basicConfig(level=args.log_level)
debug = not args.headless

cache_file = args.cache_file
if not args.cache_file:
    cache_file = "data/citydata.json"
    with open(cache_file, 'w+') as f:
        f.write("{}")

with open(args.citylist) as f:
    for line in f:
        try:
            run_city(line.strip(), cache_places=args.cache_places, cache_cities=args.cache_cities, cache_file=cache_file, debug=debug, max_results=args.max_places)
        except Exception as e:
            log.error(f"Error running {line}: {e}")
            continue

with open(cache_file) as f:
    data = json.load(f)

with open(args.output_name + ".json", "w+") as f:
    f.write(json.dumps(data))

places_data = pd.DataFrame(columns=['city','name', 'place_id', 'avg_rating', 'num_ratings', 'labels_error', 'lgbtq','veteran','women','black', 'types'])
for city in data:
    for place_name in data[city]:
        place = data[city][place_name]
        arr = [
            city, 
            place["name"], 
            place["place_id"], 
            place["rating"], 
            place["num_ratings"], 
            place["labels"]["success"], 
            place["labels"]["lgbtq"] if 'lgbtq' in place["labels"] else False,  
            place["labels"]["veteran"] if 'veteran' in place["labels"] else False,  
            place["labels"]["women"] if 'women' in place["labels"] else False,  
            place["labels"]["black"] if 'black' in place["labels"] else False,  
            place["types"], 
        ]
        places_data.loc[len(places_data)] = arr
places_data.to_csv(args.output_name + ".csv")