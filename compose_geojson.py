import os
import re
from typing import List

from geojson import Feature, Point, FeatureCollection, dump

from addresses import Geocoder
from browser_utils import make_driver
from fetch_favorites import fetch_favorites_from_cian, Favorite


def compose_geojson_from_favorites(favorites: List[Favorite]) -> FeatureCollection:
    geocoder = Geocoder(user_agent="cian-rent-map")
    for item in favorites:
        location = geocoder.geocode(address=item.address)
        if not location:
            print(f"Failed to geocode address for item: {item}")
            continue

        item.location = location.longitude, location.latitude

    feature_list = []
    for item in favorites:
        link_body = f"{item.main_title}\n{item.bargain_info}"
        description = f'<a target="_blank" rel="noopener noreferrer" href={item.url}>{link_body}</a>'
        short_address = item.address
        m = re.search(r"([\w\s]+, [\w\s]+)$", item.address)
        if m:
            short_address = m.group()

        feature = Feature(
            geometry=Point(item.location),
            properties={
                "description": description,
                "iconCaption": f"{short_address}",
                "marker-color": "#1e98ff"
            }
        )
        feature_list.append(feature)

    feature_collection = FeatureCollection(
        features=feature_list,
        metadata={
            "name": "rent 2021",
            "creator": "Yandex Map Constructor",
        }
    )

    return feature_collection


if __name__ == '__main__':
    with make_driver(headless=not bool(os.getenv('DISABLE_HEADLESS'))) as driver:
        favorites = fetch_favorites_from_cian(driver=driver)
        with open("map.geojson", "w") as f:
            feature_collection = compose_geojson_from_favorites(favorites=favorites)
            dump(feature_collection, f, indent=4)
