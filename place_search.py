import requests
import sys
import json
import time
import logging
from secrets import PLACES_API_KEY
from labels import check_labels
from geo import get_geo

log = logging.getLogger(__name__)

def plus_replace(str):
    return str.replace(" ", "+")

def get_places(lat, lng, radius, data={}, cache_places=True, max_results=0, debug=False):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=restaurant&key={PLACES_API_KEY}'
    response = requests.get(url).json()
    results = response['results']

    while 'next_page_token' in response and (not max_results or len(results) < max_results): #continue if there are still tokens left
        next_url  = url + '&pagetoken=' + response['next_page_token']
        time.sleep(5)
        response = requests.get(next_url).json()
        results.extend(response['results']) 
    
    if max_results and len(results) > max_results:
        results = results[:max_results]
        
    log.info(f"Num Results: {len(results)}")
    
    for result in results:
        try:
            if result['name'] in data and cache_places:
                log.info(f"Using cache for {result['name']}")
                continue

            url = f'https://www.google.com/maps/search/{plus_replace(result["name"])}+near+{plus_replace(result["vicinity"])}/@{result["geometry"]["location"]["lat"]},{result["geometry"]["location"]["lng"]}'
            
            log.debug(f'Retrieving labels for {result["name"]} at url {url}')

            labels = check_labels(url, debug=debug)

            data[result["name"]] = {
                'name': result["name"],
                'rating': result['rating'],
                'num_ratings': result["user_ratings_total"],
                'place_id': result['place_id'], 
                'types': result['types'],
                'labels': labels,
            }

            log.debug(f'Collected: {data[result["name"]]}')

        except Exception as e:
            log.error(f'Error occured while processing {result["name"]}: {e}')
            continue

    return data

def run_city(city, cache_cities=False, cache_places=True, max_results=0, debug=True, cache_file='data/citydata.json'):
    city = city.lower()

    with open(cache_file) as f:
        data = json.load(f)

    if city in data and cache_cities:
        log.info(f"Using cache for city {city}")
        return
    
    data[city] = {}

    g, ok = get_geo(city)

    if not ok:
        log.info(f"City {city} not found")
        return
    
    log.info(f"Geographic search for {city} returned: {g}")
    city_data = get_places(g['lat'], g['long'], g['radius'], cache_places=cache_places, data=data[city], max_results=max_results, debug=debug)
    
    data[city] = city_data

    with open(cache_file, 'w+') as f:
        f.write(json.dumps(data))

    return data

if __name__ == '__main__':
    city_list = sys.argv[1:]
    for city in city_list:
        run_city(city)

    