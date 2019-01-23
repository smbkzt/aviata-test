from concurrent.futures.thread import ThreadPoolExecutor

import celery

from directions.models import MinPrice
from utils.constants import AVAILABLE_DIRECTIONS
from utils.requests_lib import get_months_keys, make_search


@celery.task()
def update_flight_prices():
    MinPrice.flush()
    print("Initializing script is started")
    for direction in AVAILABLE_DIRECTIONS:
        print('Started initializing direction:', direction)
        _, keys = get_months_keys(direction)
        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(make_search, keys)
    print("The script is finished")
