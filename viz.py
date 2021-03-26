from geo import get_geo
from secrets import VIZ_API_KEY
import argparse
import webbrowser
import tempfile

parser = argparse.ArgumentParser(description='Visualization for City Ranges')
parser.add_argument('city', help="name of city to visualize ex. 'San Antonio'")
args = parser.parse_args()

g, ok = get_geo(args.city)

if not ok:
    print(f"City {args.city} not found")
    exit(1)

html = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Circles</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
    <style type="text/css">
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }

      /* Optional: Makes the sample page fill the window. */
      html,
      body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
    <script>
      const citymap = {
        test: {
          center: { lat: '''+str(g["lat"])+''', lng: '''+str(g["long"])+''' },
          radius: '''+str(g["radius"])+''',
        },
      };

      function initMap() {
        // Create the map.
        const map = new google.maps.Map(document.getElementById("map"), {
          zoom: 10,
          center: { lat: '''+str(g["lat"])+''', lng: '''+str(g["long"])+''' },
        });

        // Construct the circle for each value in citymap.
        // Note: We scale the area of the circle based on the population.
        for (const city in citymap) {
          // Add the circle for this city to the map.
          const cityCircle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map,
            center: citymap[city].center,
            radius: citymap[city].radius,
          });
        }
      }
    </script>
  </head>
  <body>
    <div id="map"></div>

    <!-- Async script executes immediately and must be after any DOM elements used in callback. -->
    <script
      src="https://maps.googleapis.com/maps/api/js?key='''+VIZ_API_KEY+'''&callback=initMap&libraries=&v=weekly"
      async
    ></script>
  </body>
</html>
'''
_, path = tempfile.mkstemp(suffix='.html')
url = 'file://' + path
with open(path, 'w') as fp:
    fp.write(html)
webbrowser.open(url)