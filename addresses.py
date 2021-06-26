import re

import geopy
from geopy.geocoders import Nominatim

rightmost_token_re = re.compile(r", [\w\s]+$")


class Geocoder:
    def __init__(self, user_agent: str):
        self.geolocator = Nominatim(user_agent=user_agent)

    def geocode(self, address: str) -> geopy.Location:
        # remove 'city, district, ' part as it cause geocoding failure
        normalized_address = re.sub(r"Москва, [\w]+, ", "", address,  count=1)

        while rightmost_token_re.search(normalized_address):
            location = self.geolocator.geocode(normalized_address)
            if location:
                return location

            prev_normalized_address = normalized_address
            # failed to geocode "улица Гончарова, 13к1" -- try again with "улица Гончарова"
            normalized_address = re.sub(rightmost_token_re, "", prev_normalized_address, count=1)
            print(f"Failed to geocode {prev_normalized_address}, will try with {normalized_address}")

        raise LookupError(f"Failed to geocode {address}")
