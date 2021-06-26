from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="cian-rent-map")
location = geolocator.geocode("Москва, САО, р-н Войковский, Старопетровский проезд, 12к4")
