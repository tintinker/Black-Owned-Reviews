from place_search import run_city

CITY_LIST_FILE = 'citylist.txt'

with open(CITY_LIST_FILE) as f:
    for line in f:
        try:
            run_city(line.strip(), data_file='data/citydata.json')
        except Exception as e:
            print(f"Error running {line}: ", e)
            continue