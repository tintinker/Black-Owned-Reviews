const citymap = {
    chicago: {
      center: { lat: 41.878, lng: -87.629 },
      area: 234.173,
    },
    newyork: {
      center: { lat: 40.714, lng: -74.005 },
      area: 468.197,
    },
    losangeles: {
      center: { lat: 34.052, lng: -118.243 },
      area: 502.728,
    },
}

function initMap() {
    // Create the map.
    const map = new google.maps.Map(
      document.getElementById("map"),
      {
        zoom: 4,
        center: { lat: 37.09, lng: -95.712 },
      }
    );
  
    // Construct the circle for each value in citymap.
    // Note: We scale the area of the circle based on the population.
    for (const city in citymap) {
      // Add the circle for this city to the map.
      const cityCircle = new google.maps.Circle({
        strokeColor: "#FF0000",
        strokeOpacity: 0.5,
        strokeWeight: 2,
        fillColor: "#FF0000",
        fillOpacity: 0.2,
        map,
        center: citymap[city].center,
        radius: Math.sqrt(citymap[city].area / 3.14) * 1609,
      });
    }
  }