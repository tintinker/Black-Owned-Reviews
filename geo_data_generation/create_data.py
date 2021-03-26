with open('cities.json') as f:
  data = json.load(f)

with open('abbrevs.json') as f:
    abbrevs = json.load(f)

lat_long_info = {}
for d in data:
    lat_long_info[d['city']] = {'lat': d['latitude'], 'long': d['longitude'], 'state': abbrevs[d['state'].lower()].upper()}

with open('latlong.json') as f:
    l = json.load(f)

with open('census.txt') as f:
    with open('census-small.txt', 'w') as g: 
        for line in f:
            data = line.split('\t')
            city = data[3]
            if 'city' in city and city[:-5] in l:
                d = l[city[:-5]]
                if d['state'] == data[0]:
                    g.write(line)
                    l[city[:-5]]['area'] = float(data[8]) + float(data[9])

with open('citydata.json', 'w') as f:
    f.write(json.dumps(l))
