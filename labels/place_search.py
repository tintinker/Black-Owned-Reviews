import requests
import sys
import json
from secrets import API_KEY
from labels import check_labels
from geo import get_geo

def plus_replace(str):
    return str.replace(" ", "+")

def get_places(lat, lng, radius, data={}, overwrite_labels=False, min_results=20, debug=False):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=restaurant&key={API_KEY}'
    response = requests.get(url)
    res = response.json() 
    results = res["results"]

    while(len(results) < min_results):
        page_token = res['next_page_token']
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={page_token}&key={API_KEY}'
        response = requests.get(url)
        
        if not response.ok:
            break
        
        res = response.json()
        results.extend(res["results"])
 

    if debug:
        print("Num Results:", len(results))
    
    for result in results:
        try:
            if result['name'] in data and not overwrite_labels:
                if debug:
                    print(f"Labels already found for {result['name']}")
                continue

            if debug:
                print(f"Getting labels for {result['name']}...")

            url = f'https://www.google.com/maps/search/{plus_replace(result["name"])}+near+{plus_replace(result["vicinity"])}/@{result["geometry"]["location"]["lat"]},{result["geometry"]["location"]["lng"]}'
            
            if debug:
                print(url)

            labels = check_labels(url, debug=debug)

            if debug:
                print("Place Name:", result["name"])
                print("rating: ", result["rating"])
                print("num ratings: ", result["user_ratings_total"])
                print(labels)

            data[result["name"]] = {
                'name': result["name"],
                'rating': result['rating'],
                'num_ratings': result["user_ratings_total"],
                'labels': labels
            }

        except Exception as e:
            print("Error: ", e)
            continue

    return data

def run_city(city, overwrite_cities=True, overwrite_labels=False, min_results=40, debug=True, data_file='citydata.json'):
    city = city.lower()

    with open(data_file) as f:
        data = json.load(f)

    if city in data and not overwrite_cities:
        print(data[city])
        return
    data[city] = {}

    g = get_geo(city)
    
    print(f"Geographic search for {city}: ", g)
    city_data = get_places(g['lat'], g['long'], g['radius'], overwrite_labels=overwrite_labels, data=data[city], min_results=min_results, debug=debug)
    
    data[city] = city_data

    with open(data_file, 'w') as f:
        f.write(json.dumps(data))

if __name__ == '__main__':
    city_list = sys.argv[1:]
    for city in city_list:
        run_city(city)

    