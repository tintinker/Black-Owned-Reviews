import json
import sys
import math

DATA_FILE = 'data/geodata.json' #generated from census data using code in the geo_data_generation folder
MILES_TO_METERS = 1609

def get_geo(city_name):
    with open(DATA_FILE) as f:
        data = json.load(f)

    city_name = city_name.title() #san francisco -> San Francisco
    if city_name not in data:
        return {
            "success": False
        }
    
    return {
        "success": True,
        "lat": data[city_name]['lat'],
        "long": data[city_name]['long'],
        "radius": math.sqrt(data[city_name]['area'] / math.pi) * MILES_TO_METERS,
    }

if __name__ == '__main__':
    print(get_geo(sys.argv[1]))