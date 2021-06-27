import os
import pathlib

import geojson

from browser_utils import make_driver
from compose_geojson import compose_geojson_from_favorites
from fetch_favorites import authorize_at_cian, fetch_favorites_from_cian
from import_map import authorize_at_ya, cleanup_rent_maps, import_geojson_to_ya


if __name__ == '__main__':
    cian_username, cian_password = os.environ["CIAN_USERNAME"], os.environ["CIAN_PASSWORD"]
    ya_username, ya_password = os.environ["YA_USERNAME"], os.environ["YA_PASSWORD"]

    with make_driver(headless=not bool(os.getenv('DISABLE_HEADLESS'))) as driver:
        authorize_at_cian(username=cian_username, password=cian_password, driver=driver)
        favorites = fetch_favorites_from_cian(driver=driver)
        with open("map.geojson", "w") as f:
            feature_collection = compose_geojson_from_favorites(favorites=favorites)
            geojson.dump(feature_collection, f, indent=4)

        authorize_at_ya(username=ya_username, password=ya_password, driver=driver)
        map_js_code_str = import_geojson_to_ya(file_path=str(pathlib.Path("./map.geojson").resolve()), driver=driver)
        with open("map.html", "w") as f:
            f.write(map_js_code_str)

        cleanup_rent_maps(driver=driver, except_first_n=1)
