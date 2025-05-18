from geopy.geocoders import Nominatim
#"Latitude": [19.355278, 17.016667, 19.4326],
#    "Longitude": [-97.1175, -97.808333, -99.1332],
initial_lat = 17.016667
initial_lon = -97.808333
geolocator = Nominatim(user_agent="CafeMX")
location = geolocator.reverse(str(initial_lat) +","+str(initial_lon))


# Display
print(location[0].split(','))