from concurrent.futures.thread import ThreadPoolExecutor

import celery

from utills.constants import AVAILABLE_DIRECTIONS
from utills.requests_lib import get_months_keys, get_and_set_min_price


@celery.task()
def initialize_data():
    for direction in AVAILABLE_DIRECTIONS:
        _, keys = get_months_keys(direction)
        with ThreadPoolExecutor(max_workers=50) as pool:
            pool.map(get_and_set_min_price, keys)


@celery.task()
def update_flight_prices():
    pass
